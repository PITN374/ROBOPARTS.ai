"""Tests for ROBOAGENTIC supplier identity resolution."""

import json

from roboagentic.discovery.identity import (
    assess_identity,
    assessment_to_dict,
    normalize_domain,
)


def test_normalize_domain():
    assert (
        normalize_domain("https://Example.com/products")
        == "example.com"
    )


def test_normalize_domain_with_trailing_dot():
    assert normalize_domain("https://example.com./") == "example.com"


def test_invalid_url():
    assert normalize_domain("not-a-url") == ""
    assert normalize_domain("javascript:alert(1)") == ""


def test_url_with_credentials_is_rejected():
    assert normalize_domain("https://user:pass@example.com") == ""


def test_possible_manufacturer():
    result = assess_identity(
        company_name="Example Robotics",
        website="https://example.com",
        title="Robotics actuator manufacturer",
        description="Manufacturing servo motors for humanoid robots",
        source_url="https://example.com/products",
    )

    assert result.classification == "possible_manufacturer"
    assert result.robotics_relevance > 0
    assert result.review_required is True
    assert result.completeness_score == 100
    assert "manufacturer" in result.matched_manufacturer_terms


def test_possible_distributor():
    result = assess_identity(
        company_name="Example Components",
        website="https://example.com",
        title="Authorized distributor",
        description="Wholesale supplier of servo motors",
        source_url="https://example.com/about",
    )

    assert result.classification == "possible_distributor"
    assert result.review_required is True
    assert result.matched_distributor_terms


def test_manufacturer_and_distributor():
    result = assess_identity(
        company_name="Example Robotics",
        website="https://example.com",
        title="Robotics manufacturer and distributor",
        description="We manufacture and distribute actuators.",
        source_url="https://example.com/about",
    )

    assert (
        result.classification
        == "manufacturer_and_distributor_possible"
    )
    assert result.matched_manufacturer_terms
    assert result.matched_distributor_terms


def test_directory_evidence_is_recorded():
    result = assess_identity(
        company_name="Example Directory",
        website="https://example.com",
        title="Robotics supplier directory",
        description="Directory of robotics component vendors",
        source_url="https://example.com/listings",
    )

    # Directory evidence is recorded separately from business role.
    assert result.classification == "unclassified"
    assert result.matched_directory_terms
    assert any("directory" in reason.lower() for reason in result.reasons)


def test_third_party_source_does_not_disqualify_supplier():
    result = assess_identity(
        company_name="Example Robotics",
        website="https://example.com",
        title="Robotics manufacturer",
        description="Manufacturer of robotic grippers",
        source_url="https://directory.example/listings/example",
    )

    assert result.classification == "possible_manufacturer"
    assert result.normalized_domain == "example.com"
    assert result.source_domain == "directory.example"
    assert any("domains differ" in reason for reason in result.reasons)


def test_missing_evidence_requires_review():
    result = assess_identity(
        company_name="",
        website="",
        source_url="",
    )

    assert result.review_required is True
    assert result.completeness_score == 0
    assert result.classification == "unclassified"
    assert result.reasons


def test_unclassified_company():
    result = assess_identity(
        company_name="Example Holdings",
        website="https://example.com",
        title="Welcome to our company",
        description="Learn more about our business.",
        source_url="https://example.com/about",
    )

    assert result.classification == "unclassified"
    assert result.robotics_relevance == 0


def test_assessment_to_dict_is_json_serializable():
    result = assess_identity(
        company_name="Example Robotics",
        website="https://example.com",
        title="Robotics manufacturer",
        description="We manufacture actuators.",
        source_url="https://example.com/about",
    )

    data = assessment_to_dict(result)
    serialized = json.dumps(data)

    assert isinstance(data, dict)
    assert "classification" in data
    assert "completeness_score" in data
    assert "evidence_score" not in data
    assert "possible_manufacturer" in serialized
