import os
import sys
import json
import time
import asyncio
from collections import defaultdict

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database.session import SessionLocal
from app.services.verification_service import VerificationService
from app.schemas.verification import VerificationRequest
from app.database.init_db import init_database

CLASSES = ["CURRENT", "OUTDATED", "CONTRADICTED", "UNVERIFIED", "TIME_SENSITIVE"]


async def run_audit():
    init_database()
    benchmark_file = os.path.join(os.path.dirname(__file__), "..", "tests", "data", "benchmark_100_claims.json")
    with open(benchmark_file, "r", encoding="utf-8") as f:
        claims = json.load(f)

    db = SessionLocal()
    service = VerificationService(db)

    confusion_matrix = {actual: {pred: 0 for pred in CLASSES} for actual in CLASSES}
    mismatches = []
    category_results = defaultdict(lambda: {"total": 0, "correct": 0})
    latencies = []

    print(f"Auditing {len(claims)} benchmark claims...\n")

    for idx, item in enumerate(claims):
        claim_id = item["id"]
        claim_text = item["claim_text"]
        gt_verdict = item["ground_truth_verdict"]
        category = item["category"]

        req = VerificationRequest(
            answer_text=claim_text,
            domain=category,
            verification_depth="standard",
            freshness_policy="standard"
        )

        t0 = time.time()
        run = await service.execute_verification(req)
        lat = (time.time() - t0) * 1000
        latencies.append(lat)

        pred_verdict = run.claims[0].status if run.claims else "UNVERIFIED"

        confusion_matrix[gt_verdict][pred_verdict] += 1
        category_results[category]["total"] += 1

        is_match = (pred_verdict == gt_verdict)
        if is_match:
            category_results[category]["correct"] += 1
        else:
            mismatches.append({
                "id": claim_id,
                "text": claim_text,
                "category": category,
                "ground_truth": gt_verdict,
                "predicted": pred_verdict,
                "reasoning": run.claims[0].assessment.reasoning if run.claims and run.claims[0].assessment else ""
            })

    db.close()

    total = len(claims)
    correct = sum(confusion_matrix[c][c] for c in CLASSES)
    accuracy = correct / total

    print("=== CONFUSION MATRIX (Row=Actual, Col=Predicted) ===")
    header = f"{'Actual \\ Pred':<15}" + "".join(f"{c:>15}" for c in CLASSES)
    print(header)
    for actual in CLASSES:
        row_str = f"{actual:<15}" + "".join(f"{confusion_matrix[actual][pred]:>15}" for pred in CLASSES)
        print(row_str)

    print("\n=== PER-CLASS METRICS ===")
    class_metrics = {}
    for c in CLASSES:
        tp = confusion_matrix[c][c]
        fn = sum(confusion_matrix[c][p] for p in CLASSES if p != c)
        fp = sum(confusion_matrix[a][c] for a in CLASSES if a != c)
        tn = total - tp - fn - fp

        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0
        actual_total = sum(confusion_matrix[c].values())

        class_metrics[c] = {
            "tp": tp, "fn": fn, "fp": fp, "tn": tn,
            "precision": prec, "recall": rec, "f1": f1,
            "support": actual_total
        }
        print(f"{c:<15} Support: {actual_total:<3} Precision: {prec*100:6.2f}% Recall: {rec*100:6.2f}% F1: {f1:5.3f}")

    # Outdated specific metrics
    outdated = class_metrics["OUTDATED"]
    outdated_recall = outdated["recall"]
    outdated_precision = outdated["precision"]
    outdated_f1 = outdated["f1"]
    
    # FPR on OUTDATED (FP / (FP + TN) where negative = all non-outdated)
    outdated_fpr = outdated["fp"] / (outdated["fp"] + outdated["tn"]) if (outdated["fp"] + outdated["tn"]) > 0 else 0.0

    # Macro F1
    active_classes = [c for c in CLASSES if class_metrics[c]["support"] > 0]
    macro_f1 = sum(class_metrics[c]["f1"] for c in active_classes) / len(active_classes)

    print(f"\n=== OVERALL SUMMARY ===")
    print(f"Total Evaluated:              {total}")
    print(f"Overall Multi-Class Accuracy: {accuracy*100:.2f}% ({correct}/{total})")
    print(f"Macro F1:                     {macro_f1:.3f}")
    print(f"OUTDATED Recall:              {outdated_recall*100:.2f}% ({outdated['tp']}/{outdated['support']})")
    print(f"OUTDATED Precision:           {outdated_precision*100:.2f}%")
    print(f"OUTDATED F1:                  {outdated_f1:.3f}")
    print(f"OUTDATED False Positive Rate: {outdated_fpr*100:.2f}%")
    print(f"Average Pipeline Latency:     {sum(latencies)/len(latencies):.2f} ms")
    print(f"Min Latency:                  {min(latencies):.2f} ms")
    print(f"Max Latency:                  {max(latencies):.2f} ms")

    print(f"\n=== CATEGORY PERFORMANCE ===")
    for cat, res in category_results.items():
        pct = (res["correct"] / res["total"]) * 100 if res["total"] > 0 else 0
        print(f"{cat:<20} {res['correct']}/{res['total']} ({pct:.1f}%)")

    print(f"\n=== MISCLASSIFIED CLAIMS ({len(mismatches)} total) ===")
    for m in mismatches:
        print(f"[{m['id']}] Category: {m['category']}")
        print(f"  Claim:     \"{m['text']}\"")
        print(f"  Expected:  {m['ground_truth']} | Got: {m['predicted']}")
        print(f"  Reasoning: {m['reasoning']}\n")

    # Output JSON for reporting
    audit_data = {
        "confusion_matrix": confusion_matrix,
        "class_metrics": class_metrics,
        "overall_accuracy": accuracy,
        "macro_f1": macro_f1,
        "outdated_recall": outdated_recall,
        "outdated_precision": outdated_precision,
        "outdated_f1": outdated_f1,
        "outdated_fpr": outdated_fpr,
        "avg_latency_ms": sum(latencies)/len(latencies),
        "category_results": dict(category_results),
        "mismatches": mismatches
    }
    with open("backend/tests/data/audit_recalculated_results.json", "w") as f:
        json.dump(audit_data, f, indent=2)

if __name__ == "__main__":
    asyncio.run(run_audit())

