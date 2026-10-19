"""ROBOAGENTIC Supplier Identity Resolution"""
Product: ROBOPARTS \ ROBOAGENTIC 
Author: Aaron Bailot

Classifies candidate suppliers using available textual evidence.

This module provides preliminary, rule-based assessments. It does not
perform legal identity verification, independently verify websites, or
establish supplier legitimacy.
"""

from dataclasses import asdict, dataclass, field
from urllib.parse import urlsplit
import ipaddress
import re
from typing import Any

MANUFACTURER_TERMS = (
    "manufacturer",
    "manufacturing",
    "factory",
    "production facility",
    "machining",
    "cnc machining",
    "assembly",
    "original equipment manufacturer",
    "oem",
)

DISTRIBUTOR_TERMS = (
    "distributor",
    "distribution",
    "reseller",
    "authorized dealer",
    "wholesale supplier",
)

DIRECTORY_TERMS = (
    "company directory",
    "business directory",
    "supplier directory",
    "marketplace",
    "vendor listings",
)

ROBOTICS_TERMS = (
    "robotics",
    "robot",
    "humanoid",
    "actuator",
    "servo motor",
    "robotic hand",
    "gripper",
    "wiring harness",
    "motion control",
    "robotics components",
    "cnc machining",
    "lidar",
    "force sensor",
)

# Terms that can indicate a negative statement about a business role.
NEGATION_TERMS = (
    "not",
    "never",
    "no",
    "doesn't",
    "does not",
    "isn't",
    "is not",
    "cannot",
    "can't",
)

MAX_TEXT_LENGTH = 20_000

@dataclass
class IdentityAssessment:
    """Structured preliminary assessment of a candidate supplier."""

    company_name: str
    website: str
    classification: str
    robotics_relevance: int
    completeness_score: int
    review_required: bool
    reasons: list[str] = field(default_factory=list)
    matched_manufacturer_terms: list[str] = field(default_factory=list)
    matched_distributor_terms: list[str] = field(default_factory=list)
    matched_directory_terms: list[str] = field(default_factory=list)
    matched_robotics_terms: list[str] = field(default_factory=list)
    normalized_domain: str = ""
    source_domain: str = ""

def _clean_text(value: Any, field_name: str) -> str:
    """Validate and normalize a text input."""
    if value is None:
        return ""

    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string or None.")

    return value.strip()[:MAX_TEXT_LENGTH]

def normalize_domain(url: str) -> str:
    """
    Return a normalized hostname from an absolute HTTP(S) URL.

    Returns an empty string when the URL is invalid or unsupported.
    This function parses URLs; it does not verify domain ownership.
    """
    if not isinstance(url, str) or not url.strip():
        return ""

    try:
        parsed = urlsplit(url.strip())

        if parsed.scheme.casefold() not in ("http", "https"):
            return ""

        if not parsed.hostname:
            return ""

        # Reject embedded credentials.
        if parsed.username is not None or parsed.password is not None:
            return ""

        # Reject malformed ports.
        if parsed.port is not None and not 1 <= parsed.port <= 65535:
            return ""

        hostname = parsed.hostname.rstrip(".").casefold()

        # Reject whitespace and malformed hostname labels.
        if not hostname or any(char.isspace() for char in hostname):
            return ""

        # Normalize internationalized domain names when possible.
        try:
            hostname = hostname.encode("idna").decode("ascii")
        except UnicodeError:
            return ""

        # Accept IP addresses, but reject malformed IP-like strings
        # through the normal hostname validation below.
        try:
            ipaddress.ip_address(hostname)
            return hostname
        except ValueError:
            pass

        if len(hostname) > 253:
            return ""

        labels = hostname.split(".")

        if any(
            not label
            or len(label) > 63
            or not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", label)
            for label in labels
        ):
            return ""

        return hostname

    except (ValueError, AttributeError, UnicodeError):
        return ""

def _find_terms(text: str, terms: tuple[str, ...]) -> list[str]:
    """
    Find distinct terms using case-insensitive word-boundary matching.

    Multiword terms are matched with flexible whitespace.
    """
    matches = []

    for term in terms:
        pattern = r"(?<!\w)" + re.escape(term).replace(r"\ ", r"\s+") + r"(?!\w)"

        if re.search(pattern, text, flags=re.IGNORECASE):
            matches.append(term)

    return matches

def _has_local_negation(text: str, term: str) -> bool:
    """
    Check for a simple negation immediately before a matching term.

    This is a conservative heuristic, not full natural-language
    understanding. Complex statements still require human review.
    """
    pattern = (
        r"\b("
        + "|".join(re.escape(word) for word in NEGATION_TERMS)
        + r")\b(?:\W+\w+){0,3}\W+"
        + re.escape(term).replace(r"\ ", r"\s+")
        + r"\b"
    )

    return bool(re.search(pattern, text, flags=re.IGNORECASE))

def _find_positive_terms(
    text: str,
    terms: tuple[str, ...],
) -> list[str]:
    """Exclude terms that appear to be locally negated."""
    matches = _find_terms(text, terms)

    return [
        term
        for term in matches
        if not _has_local_negation(text, term)
    ]

def assess_identity(
    company_name: str,
    website: str,
    title: str = "",
    description: str = "",
    source_url: str = "",
) -> IdentityAssessment:
    """
    Produce a preliminary supplier assessment from supplied text.

    The source URL may belong to a search engine, marketplace, directory,
    or third-party publisher. A source-domain mismatch is recorded as
    provenance information and does not automatically disqualify a supplier.

    Scores:
        robotics_relevance: 0-100 heuristic based on distinct matched terms.
        completeness_score: 0-100 based on five populated input fields.

    Neither score is a probability or a measure of verified identity.
    """
    company_name = _clean_text(company_name, "company_name")
    website = _clean_text(website, "website")
    title = _clean_text(title, "title")
    description = _clean_text(description, "description")
    source_url = _clean_text(source_url, "source_url")

    reasons: list[str] = []

    domain = normalize_domain(website)
    source_domain = normalize_domain(source_url)

    if not company_name:
        reasons.append("Company name is missing.")

    if not domain:
        reasons.append("A valid absolute HTTP(S) supplier website is missing.")

    if not source_url:
        reasons.append("Source URL is missing.")
    elif not source_domain:
        reasons.append("Source URL is not a valid absolute HTTP(S) URL.")

    if domain and source_domain and domain != source_domain:
        reasons.append(
            "Source and supplier website domains differ; "
            "the source may be a third-party publisher or directory."
        )

    combined = " ".join((company_name, title, description)).casefold()

    manufacturer_hits = _find_positive_terms(
        combined, MANUFACTURER_TERMS
    )
    distributor_hits = _find_positive_terms(
        combined, DISTRIBUTOR_TERMS
    )
    directory_hits = _find_terms(
        combined, DIRECTORY_TERMS
    )
    robotics_hits = _find_positive_terms(
        combined, ROBOTICS_TERMS
    )

    # Completeness is intentionally separate from evidence quality.
    populated_fields = sum(
        bool(value)
        for value in (
            company_name,
            website,
            title,
            description,
            source_url,
        )
    )
    completeness_score = populated_fields * 20

    # A capped heuristic, not a probability or verification score.
    robotics_relevance = min(100, len(set(robotics_hits)) * 20)

    # Classify the business role independently from directory references.
    roles = []

    if manufacturer_hits:
        roles.append("manufacturer")

    if distributor_hits:
        roles.append("distributor")

    if roles == ["manufacturer", "distributor"]:
        classification = "manufacturer_and_distributor_possible"
        reasons.append(
            "Manufacturing and distribution terms appear in the supplied text."
        )
    elif "manufacturer" in roles:
        classification = "possible_manufacturer"
        reasons.append(
            "Manufacturing-related terms appear in the supplied text."
        )
    elif "distributor" in roles:
        classification = "possible_distributor"
        reasons.append(
            "Distribution-related terms appear in the supplied text."
        )
    else:
        classification = "unclassified"
        reasons.append(
            "Insufficient positive textual evidence to classify the business role."
        )

    if directory_hits:
        reasons.append(
            "Directory or marketplace terminology appears in the supplied text; "
            "verify whether the candidate is a supplier or merely a listing."
        )

    if robotics_hits:
        reasons.append(
            "Robotics-related terms were found; product relevance has not "
            "been independently verified."
        )
    else:
        reasons.append(
            "No recognized positive robotics or component terms were found."
        )

    reasons.append(
        "Classification is based on supplied text and does not establish "
        "legal identity, domain ownership, manufacturing capability, "
        "or commercial legitimacy."
    )

    # Human review remains mandatory for this preliminary version.
    review_required = True

    return IdentityAssessment(
        company_name=company_name,
        website=website,
        classification=classification,
        robotics_relevance=robotics_relevance,
        completeness_score=completeness_score,
        review_required=review_required,
        reasons=reasons,
        matched_manufacturer_terms=manufacturer_hits,
        matched_distributor_terms=distributor_hits,
        matched_directory_terms=directory_hits,
        matched_robotics_terms=robotics_hits,
        normalized_domain=domain,
        source_domain=source_domain,
    )

def assessment_to_dict(
    assessment: IdentityAssessment,
) -> dict[str, Any]:
    """Convert an assessment into a JSON-serializable dictionary."""
    if not isinstance(assessment, IdentityAssessment):
        raise TypeError("assessment must be an IdentityAssessment.")

    return asdict(assessment)
```

## Step 3 — Test that the file works

After committing the file, you can test it locally or in a Python environment.

Create a separate file called `test_identity.py`:

python
```

import json
import unittest

from identity import (
    assess_identity,
    assessment_to_dict,
    normalize_domain,
)

class TestIdentity(unittest.TestCase):

    def test_normalize_domain(self):
        self.assertEqual(
            normalize_domain("https://Example.com/about"),
            "example.com",
        )
        self.assertEqual(normalize_domain("example.com"), "")
        self.assertEqual(normalize_domain("javascript:alert(1)"), "")
        self.assertEqual(
            normalize_domain("https://user:pass@example.com"),
            "",
        )

    def test_manufacturer_classification(self):
        result = assess_identity(
            company_name="Acme Robotics",
            website="https://acme.example",
            title="Robotics manufacturer",
            description="We produce robotic grippers.",
            source_url="https://acme.example/about",
        )

        self.assertEqual(result.classification, "possible_manufacturer")
        self.assertGreater(result.robotics_relevance, 0)
        self.assertEqual(result.completeness_score, 100)
        self.assertTrue(result.review_required)

    def test_third_party_source(self):
        result = assess_identity(
            company_name="Acme",
            website="https://acme.example",
            title="Industrial supplier",
            description="Manufacturing components.",
            source_url="https://directory.example/listing/acme",
        )

        self.assertEqual(result.classification, "possible_manufacturer")
        self.assertNotEqual(result.normalized_domain, result.source_domain)

    def test_missing_information(self):
        result = assess_identity(
            company_name="",
            website="",
        )

        self.assertEqual(result.completeness_score, 0)
        self.assertTrue(result.review_required)
        self.assertTrue(result.reasons)

    def test_json_serialization(self):
        result = assess_identity(
            company_name="Acme",
            website="https://acme.example",
            title="Robotics manufacturer",
            description="Manufactures actuators.",
            source_url="https://acme.example",
        )

        serialized = json.dumps(assessment_to_dict(result))
        self.assertIn("possible_manufacturer", serialized)

if __name__ == "__main__":
    unittest.main()
```

Run the tests with:

bash
```
python -m unittest -v test_identity.py
```
My recommendation: Upload `identity.py` first, run the tests, and then connect it to your ROBOPARTS supplier discovery pipeline. Treat its results as preliminary classifications rather than verified supplier identities.
