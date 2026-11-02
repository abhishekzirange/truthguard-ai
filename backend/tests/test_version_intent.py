import pytest
from app.engines.deterministic_engine import DeterministicEngine, VersionIntent


class TestSemanticVersionIntentDetection:
    """Comprehensive test suite for Fix 1: Semantic Version Intent Detection."""

    # 1. Explicit Latest Assertions
    def test_explicit_latest_keyword(self):
        intent = DeterministicEngine.detect_version_intent("Python 3.11 is the latest stable release.")
        assert intent == VersionIntent.LATEST_ASSERTION

    def test_explicit_newest_keyword(self):
        intent = DeterministicEngine.detect_version_intent("FastAPI 0.100 is the newest version.")
        assert intent == VersionIntent.LATEST_ASSERTION

    def test_explicit_current_keyword(self):
        intent = DeterministicEngine.detect_version_intent("React 18 is currently the active release.")
        assert intent == VersionIntent.LATEST_ASSERTION

    def test_explicit_most_recent_keyword(self):
        intent = DeterministicEngine.detect_version_intent("Node.js 18 is the most recent release.")
        assert intent == VersionIntent.LATEST_ASSERTION

    def test_explicit_up_to_date_keyword(self):
        intent = DeterministicEngine.detect_version_intent("PostgreSQL 14 is the up to date version.")
        assert intent == VersionIntent.LATEST_ASSERTION

    # 2. Historical Milestones & Deprecations
    def test_historical_deprecation_statement(self):
        intent = DeterministicEngine.detect_version_intent("Kubernetes 1.20 deprecated dockershim.")
        assert intent == VersionIntent.HISTORICAL_MILESTONE

    def test_historical_introduced_in(self):
        intent = DeterministicEngine.detect_version_intent("Hooks were introduced in React 16.8.")
        assert intent == VersionIntent.HISTORICAL_MILESTONE

    def test_historical_was_released(self):
        intent = DeterministicEngine.detect_version_intent("Python 3.8 was released in 2019.")
        assert intent == VersionIntent.HISTORICAL_MILESTONE

    def test_historical_retired_in(self):
        intent = DeterministicEngine.detect_version_intent("Go 1.12 was retired in 2019.")
        assert intent == VersionIntent.HISTORICAL_MILESTONE

    def test_historical_removed_in(self):
        intent = DeterministicEngine.detect_version_intent("Dockershim was removed in Kubernetes 1.24.")
        assert intent == VersionIntent.HISTORICAL_MILESTONE

    # 3. Compatibility & Support Assertions
    def test_compatibility_supports(self):
        intent = DeterministicEngine.detect_version_intent("FastAPI supports Python 3.11 and 3.12.")
        assert intent == VersionIntent.COMPATIBILITY_ASSERTION

    def test_compatibility_compatible_with(self):
        intent = DeterministicEngine.detect_version_intent("React 19 is compatible with TypeScript 5.6.")
        assert intent == VersionIntent.COMPATIBILITY_ASSERTION

    def test_compatibility_requires(self):
        intent = DeterministicEngine.detect_version_intent("This library requires Python 3.10.")
        assert intent == VersionIntent.COMPATIBILITY_ASSERTION

    def test_compatibility_works_with(self):
        intent = DeterministicEngine.detect_version_intent("The plugin works with Vite 5.0.")
        assert intent == VersionIntent.COMPATIBILITY_ASSERTION

    # 4. Ambiguous Mentions
    def test_ambiguous_version_mention(self):
        intent = DeterministicEngine.detect_version_intent("We looked at version 2.4.0 in our discussion.")
        assert intent == VersionIntent.AMBIGUOUS

    def test_empty_string_intent(self):
        intent = DeterministicEngine.detect_version_intent("")
        assert intent == VersionIntent.AMBIGUOUS

    # 5. Semantic Version Comparison Integration with Intent
    def test_compare_versions_superseded_when_asserting_latest(self):
        evidence = ["Python 3.13 is the newest release. Python 3.12 is stable."]
        result = DeterministicEngine.compare_software_versions(
            claimed_version_str="3.11",
            retrieved_texts=evidence,
            claim_text="Python 3.11 is the latest stable Python release."
        )
        assert result is not None
        assert result["verdict"] == "OUTDATED"
        assert result["is_outdated"] is True
        assert result["latest_version"] == "3.13"
        assert result["intent"] == "LATEST_ASSERTION"

    def test_compare_versions_historical_milestone_preserved(self):
        evidence = ["Kubernetes 1.20 deprecated dockershim, which was removed in 1.24. Latest is 1.31."]
        result = DeterministicEngine.compare_software_versions(
            claimed_version_str="1.20",
            retrieved_texts=evidence,
            claim_text="Kubernetes 1.20 deprecated dockershim."
        )
        assert result is not None
        assert result["verdict"] == "CURRENT"
        assert result["is_outdated"] is False
        assert result["intent"] == "HISTORICAL_MILESTONE"

    def test_compare_versions_current_same_minor_release_line(self):
        evidence = ["Official release: Python 3.13.2 bugfix update available."]
        result = DeterministicEngine.compare_software_versions(
            claimed_version_str="3.13",
            retrieved_texts=evidence,
            claim_text="Python 3.13 is a current stable release."
        )
        assert result is not None
        assert result["verdict"] == "CURRENT"
        assert result["is_outdated"] is False

    def test_compare_versions_ambiguous_returns_unverified(self):
        evidence = ["We analyzed version 1.5.0 in the lab."]
        result = DeterministicEngine.compare_software_versions(
            claimed_version_str="1.5.0",
            retrieved_texts=evidence,
            claim_text="The report referenced 1.5.0."
        )
        assert result is not None
        assert result["verdict"] == "UNVERIFIED"
        assert result["intent"] == "AMBIGUOUS"

    def test_compare_versions_invalid_version_string(self):
        result = DeterministicEngine.compare_software_versions(
            claimed_version_str="not_a_version",
            retrieved_texts=["Version 1.0 released"],
            claim_text="not_a_version is the latest"
        )
        assert result is None

