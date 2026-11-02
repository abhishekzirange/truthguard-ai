import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_PATH = os.path.join(BASE_DIR, "..", "tests", "data", "benchmark_100_claims.json")

# Ground truth human-reviewed reference dataset: 100 claims across 6 categories
CLAIMS_100 = [
    # 1 - 25: Software & Framework Versions
    {"id": "claim-001", "claim_text": "Python 3.11 is the latest stable Python release.", "category": "software_version", "ground_truth_verdict": "OUTDATED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-002", "claim_text": "Python 3.13 is a current stable Python release.", "category": "software_version", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "HIGH"},
    {"id": "claim-003", "claim_text": "FastAPI 0.100.0 is the latest version of FastAPI.", "category": "software_version", "ground_truth_verdict": "OUTDATED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-004", "claim_text": "FastAPI 0.115 is a recent release of FastAPI.", "category": "software_version", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "HIGH"},
    {"id": "claim-005", "claim_text": "React 16 is the newest major release of React.", "category": "software_version", "ground_truth_verdict": "OUTDATED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-006", "claim_text": "React 19 was introduced with action hooks and compiler support.", "category": "software_version", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "HIGH"},
    {"id": "claim-007", "claim_text": "Node.js 12 is currently receiving active LTS updates.", "category": "software_version", "ground_truth_verdict": "OUTDATED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-008", "claim_text": "Node.js 22 is an Active LTS release of Node.js.", "category": "software_version", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "HIGH"},
    {"id": "claim-009", "claim_text": "Pydantic V1 is the primary recommended version for new FastAPI apps.", "category": "software_version", "ground_truth_verdict": "OUTDATED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-010", "claim_text": "Vue 2 is the active primary release of Vue.js.", "category": "software_version", "ground_truth_verdict": "OUTDATED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-011", "claim_text": "TypeScript 3.5 is the latest version of TypeScript.", "category": "software_version", "ground_truth_verdict": "OUTDATED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-012", "claim_text": "Ubuntu 18.04 LTS is currently in standard public support.", "category": "software_version", "ground_truth_verdict": "OUTDATED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-013", "claim_text": "PostgreSQL 11 is currently actively supported by the PostgreSQL Global Development Group.", "category": "software_version", "ground_truth_verdict": "OUTDATED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-014", "claim_text": "PostgreSQL 16 and 17 are supported releases of PostgreSQL.", "category": "software_version", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "HIGH"},
    {"id": "claim-015", "claim_text": "Kubernetes 1.15 is the latest Kubernetes release.", "category": "software_version", "ground_truth_verdict": "OUTDATED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-016", "claim_text": "Rust 1.40 is the latest stable release of the Rust compiler.", "category": "software_version", "ground_truth_verdict": "OUTDATED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-017", "claim_text": "Go 1.12 is the latest release of the Go programming language.", "category": "software_version", "ground_truth_verdict": "OUTDATED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-018", "claim_text": "Linux 2.4 kernel is the newest production release of the Linux kernel.", "category": "software_version", "ground_truth_verdict": "OUTDATED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-019", "claim_text": "OpenSSL 1.0.2 is the recommended release for TLS termination.", "category": "software_version", "ground_truth_verdict": "OUTDATED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-020", "claim_text": "Docker Engine 1.13 is the modern version of Docker.", "category": "software_version", "ground_truth_verdict": "OUTDATED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-021", "claim_text": "PHP 5.6 is the active supported release of PHP.", "category": "software_version", "ground_truth_verdict": "OUTDATED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-022", "claim_text": "Tailwind CSS v2 is the latest version of Tailwind.", "category": "software_version", "ground_truth_verdict": "OUTDATED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-023", "claim_text": "AngularJS 1.5 is the current version supported by Google.", "category": "software_version", "ground_truth_verdict": "OUTDATED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-024", "claim_text": "Next.js 9 is the latest version of Next.js.", "category": "software_version", "ground_truth_verdict": "OUTDATED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-025", "claim_text": "FastAPI is written in PHP.", "category": "software_version", "ground_truth_verdict": "CONTRADICTED", "temporal_sensitivity": "LOW"},

    # 26 - 45: Product Pricing
    {"id": "claim-026", "claim_text": "GPT-4o costs $30.00 per 1M input tokens.", "category": "pricing", "ground_truth_verdict": "CONTRADICTED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-027", "claim_text": "OpenAI GPT-4o input tokens cost $2.50 per 1 million tokens.", "category": "pricing", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "HIGH"},
    {"id": "claim-028", "claim_text": "GitHub Copilot for Individual developers costs $10 per month.", "category": "pricing", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "HIGH"},
    {"id": "claim-029", "claim_text": "AWS Lambda includes 1 million free requests per month in the AWS Free Tier.", "category": "pricing", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "MEDIUM"},
    {"id": "claim-030", "claim_text": "OpenAI GPT-3 DaVinci model costs $0.06 per 1,000 tokens.", "category": "pricing", "ground_truth_verdict": "OUTDATED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-031", "claim_text": "Google Cloud Storage standard tier costs $50 per gigabyte per month.", "category": "pricing", "ground_truth_verdict": "CONTRADICTED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-032", "claim_text": "Claude 3.5 Sonnet input pricing is $3.00 per million tokens.", "category": "pricing", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "HIGH"},
    {"id": "claim-033", "claim_text": "Stripe standard US processing fee is 2.9% plus 30 cents per transaction.", "category": "pricing", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "MEDIUM"},
    {"id": "claim-034", "claim_text": "Twitter Blue subscription was always free for verified public figures.", "category": "pricing", "ground_truth_verdict": "OUTDATED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-035", "claim_text": "Docker Desktop requires a commercial subscription for enterprises with over 250 employees.", "category": "pricing", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "MEDIUM"},
    {"id": "claim-036", "claim_text": "Vercel Hobby plan is $20 per month.", "category": "pricing", "ground_truth_verdict": "CONTRADICTED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-037", "claim_text": "ChatGPT Plus costs $20 per month.", "category": "pricing", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "HIGH"},
    {"id": "claim-038", "claim_text": "OpenAI Whisper API costs $0.006 per minute of audio transcribed.", "category": "pricing", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "HIGH"},
    {"id": "claim-039", "claim_text": "Cloudflare Zero Trust free tier supports up to 50 users.", "category": "pricing", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "MEDIUM"},
    {"id": "claim-040", "claim_text": "Amazon S3 Glacier Flexible Retrieval retrieval rate is $1,000 per GB.", "category": "pricing", "ground_truth_verdict": "CONTRADICTED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-041", "claim_text": "PostgreSQL database license costs $5,000 per CPU core.", "category": "pricing", "ground_truth_verdict": "CONTRADICTED", "temporal_sensitivity": "LOW"},
    {"id": "claim-042", "claim_text": "Redis open-source license transitioned away from BSD in 2024.", "category": "pricing", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "HIGH"},
    {"id": "claim-043", "claim_text": "Elasticsearch transitioned back to including AGPL open source options in 2024.", "category": "pricing", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "HIGH"},
    {"id": "claim-044", "claim_text": "AWS S3 storage costs zero dollars under all non-free usage.", "category": "pricing", "ground_truth_verdict": "CONTRADICTED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-045", "claim_text": "Databricks community edition is a paid-only product with no free access tier.", "category": "pricing", "ground_truth_verdict": "CONTRADICTED", "temporal_sensitivity": "MEDIUM"},

    # 46 - 65: Regulations & Compliance
    {"id": "claim-046", "claim_text": "The European Union AI Act entered into force in 2024.", "category": "regulation", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "MEDIUM"},
    {"id": "claim-047", "claim_text": "GDPR became enforceable in the European Union in May 2018.", "category": "regulation", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "LOW"},
    {"id": "claim-048", "claim_text": "California Consumer Privacy Act (CCPA) was repealed and no longer exists.", "category": "regulation", "ground_truth_verdict": "CONTRADICTED", "temporal_sensitivity": "MEDIUM"},
    {"id": "claim-049", "claim_text": "US SEC requires public companies to report material cybersecurity incidents within four business days.", "category": "regulation", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "MEDIUM"},
    {"id": "claim-050", "claim_text": "EU Safe Harbor agreement is the current active legal framework for US-EU data transfers.", "category": "regulation", "ground_truth_verdict": "OUTDATED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-051", "claim_text": "The EU-US Data Privacy Framework was adopted by the European Commission in 2023.", "category": "regulation", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "MEDIUM"},
    {"id": "claim-052", "claim_text": "HIPAA protects consumer health information in the United States.", "category": "regulation", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "LOW"},
    {"id": "claim-053", "claim_text": "SOX compliance only applies to private LLCs with fewer than 10 employees.", "category": "regulation", "ground_truth_verdict": "CONTRADICTED", "temporal_sensitivity": "LOW"},
    {"id": "claim-054", "claim_text": "PCI-DSS v4.0 replaced v3.2.1 as the active payment card standard in 2024.", "category": "regulation", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "HIGH"},
    {"id": "claim-055", "claim_text": "Export controls on advanced AI chips to certain countries were instituted by the US in 2022 and updated in 2023.", "category": "regulation", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "MEDIUM"},
    {"id": "claim-056", "claim_text": "The UK is currently a formal member state of the European Union.", "category": "regulation", "ground_truth_verdict": "OUTDATED", "temporal_sensitivity": "LOW"},
    {"id": "claim-057", "claim_text": "Copyright law in the United States grants 1,000 years of protection to software algorithms.", "category": "regulation", "ground_truth_verdict": "CONTRADICTED", "temporal_sensitivity": "LOW"},
    {"id": "claim-058", "claim_text": "EU Digital Markets Act (DMA) designated major tech platforms as gatekeepers in 2023.", "category": "regulation", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "MEDIUM"},
    {"id": "claim-059", "claim_text": "Net neutrality regulations have been subject to ongoing FCC rule revisions across administrations.", "category": "regulation", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "MEDIUM"},
    {"id": "claim-060", "claim_text": "FCC announced the complete shutdown of the global internet in 2024.", "category": "regulation", "ground_truth_verdict": "CONTRADICTED", "temporal_sensitivity": "LOW"},
    {"id": "claim-061", "claim_text": "Corporate income tax was abolished worldwide by the United Nations in 2020.", "category": "regulation", "ground_truth_verdict": "CONTRADICTED", "temporal_sensitivity": "LOW"},
    {"id": "claim-062", "claim_text": "OECD Pillar Two establishes a 15% global minimum corporate tax rate.", "category": "regulation", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "MEDIUM"},
    {"id": "claim-063", "claim_text": "US SEC approved spot Bitcoin ETFs in January 2024.", "category": "regulation", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "MEDIUM"},
    {"id": "claim-064", "claim_text": "US SEC approved spot Ethereum ETFs in 2024.", "category": "regulation", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "MEDIUM"},
    {"id": "claim-065", "claim_text": "FDA requires clinical trials before new medical pharmaceuticals are distributed in the US.", "category": "regulation", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "LOW"},

    # 66 - 80: Company Info & Leadership
    {"id": "claim-066", "claim_text": "Twitter is currently run by CEO Parag Agrawal.", "category": "company_info", "ground_truth_verdict": "OUTDATED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-067", "claim_text": "Satya Nadella is the CEO of Microsoft.", "category": "company_info", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "MEDIUM"},
    {"id": "claim-068", "claim_text": "Sundar Pichai is the CEO of Alphabet and Google.", "category": "company_info", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "MEDIUM"},
    {"id": "claim-069", "claim_text": "Steve Jobs is the current living CEO of Apple.", "category": "company_info", "ground_truth_verdict": "OUTDATED", "temporal_sensitivity": "LOW"},
    {"id": "claim-070", "claim_text": "Tim Cook is the CEO of Apple.", "category": "company_info", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "MEDIUM"},
    {"id": "claim-071", "claim_text": "Sam Altman is the CEO of OpenAI.", "category": "company_info", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "HIGH"},
    {"id": "claim-072", "claim_text": "Amazon was founded in 1994 by Jeff Bezos.", "category": "company_info", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "LOW"},
    {"id": "claim-073", "claim_text": "Andy Jassy is the CEO of Amazon.", "category": "company_info", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "MEDIUM"},
    {"id": "claim-074", "claim_text": "Microsoft completed its acquisition of Activision Blizzard.", "category": "company_info", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "MEDIUM"},
    {"id": "claim-075", "claim_text": "A stealth startup named QuantumWave Inc will acquire Intel next month.", "category": "company_info", "ground_truth_verdict": "UNVERIFIED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-076", "claim_text": "Broadcom completed its acquisition of VMware.", "category": "company_info", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "MEDIUM"},
    {"id": "claim-077", "claim_text": "Adobe completed its acquisition of Figma after regulatory approval.", "category": "company_info", "ground_truth_verdict": "CONTRADICTED", "temporal_sensitivity": "HIGH"},
    {"id": "claim-078", "claim_text": "Adobe and Figma terminated their planned merger agreement in December 2023.", "category": "company_info", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "MEDIUM"},
    {"id": "claim-079", "claim_text": "Tesla headquarters relocated from California to Austin, Texas.", "category": "company_info", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "MEDIUM"},
    {"id": "claim-080", "claim_text": "Meta was formerly known as Facebook Inc before its corporate rebranding in 2021.", "category": "company_info", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "LOW"},

    # 81 - 100: Technical Docs & General Facts
    {"id": "claim-081", "claim_text": "PostgreSQL supports the JSONB binary JSON storage data type.", "category": "technical_docs", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "LOW"},
    {"id": "claim-082", "claim_text": "PostgreSQL uses write-ahead logging (WAL) for durability.", "category": "technical_docs", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "LOW"},
    {"id": "claim-083", "claim_text": "Kubernetes 1.20 deprecated dockershim.", "category": "technical_docs", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "LOW"},
    {"id": "claim-084", "claim_text": "SQLite databases store data in multiple client-server daemon processes.", "category": "technical_docs", "ground_truth_verdict": "CONTRADICTED", "temporal_sensitivity": "LOW"},
    {"id": "claim-085", "claim_text": "Git is a distributed version control system.", "category": "general_technical", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "LOW"},
    {"id": "claim-086", "claim_text": "HTTP/2 introduces binary framing and multiplexed streams over a single TCP connection.", "category": "technical_docs", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "LOW"},
    {"id": "claim-087", "claim_text": "HTTP/3 uses QUIC protocol over UDP instead of TCP.", "category": "technical_docs", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "LOW"},
    {"id": "claim-088", "claim_text": "DNS resolves domain names to IP addresses.", "category": "general_technical", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "LOW"},
    {"id": "claim-089", "claim_text": "Python was originally created by Guido van Rossum and first released in 1991.", "category": "general_fact", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "LOW"},
    {"id": "claim-090", "claim_text": "Python was created by OpenAI in 2023.", "category": "general_fact", "ground_truth_verdict": "CONTRADICTED", "temporal_sensitivity": "LOW"},
    {"id": "claim-091", "claim_text": "B-Tree indexes are supported by PostgreSQL for equality and range queries.", "category": "technical_docs", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "LOW"},
    {"id": "claim-092", "claim_text": "Redis operates primarily as an in-memory data store.", "category": "technical_docs", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "LOW"},
    {"id": "claim-093", "claim_text": "IPv4 addresses are 32 bits in length.", "category": "general_technical", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "LOW"},
    {"id": "claim-094", "claim_text": "IPv6 addresses are 128 bits in length.", "category": "general_technical", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "LOW"},
    {"id": "claim-095", "claim_text": "TLS 1.3 removes support for obsolete cryptographic algorithms like MD5 and RC4.", "category": "technical_docs", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "LOW"},
    {"id": "claim-096", "claim_text": "Docker containers share the host operating system kernel.", "category": "general_technical", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "LOW"},
    {"id": "claim-097", "claim_text": "Virtual machines run a full guest operating system on hypervisor virtualization.", "category": "general_technical", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "LOW"},
    {"id": "claim-098", "claim_text": "REST APIs universally require SOAP envelope wrappers.", "category": "technical_docs", "ground_truth_verdict": "CONTRADICTED", "temporal_sensitivity": "LOW"},
    {"id": "claim-099", "claim_text": "JSON supports strings, numbers, booleans, arrays, objects, and null.", "category": "general_technical", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "LOW"},
    {"id": "claim-100", "claim_text": "SQL standard was originally developed at IBM in the 1970s.", "category": "general_fact", "ground_truth_verdict": "CURRENT", "temporal_sensitivity": "LOW"},
]

def main():
    os.makedirs(os.path.dirname(TARGET_PATH), exist_ok=True)
    with open(TARGET_PATH, "w", encoding="utf-8") as f:
        json.dump(CLAIMS_100, f, indent=2)
    print(f"Successfully generated 100-claim benchmark dataset at {TARGET_PATH}")

if __name__ == "__main__":
    main()
