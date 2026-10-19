"""Shared data models for ROBOAGENTIC / ROBOPARTS.ai.

Version: 0.1.0

These models define application data structures. They do not provide
database persistence, identity verification, or access control.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
import uuid


def new_id() -> str:
    """Generate a persistent-format UUID identifier."""
    return str(uuid.uuid4())


def utc_now() -> str:
    """Return the current UTC timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Product:
    """A product definition, distinct from a physical instance."""

    manufacturer: str
    mpn: str
    namespace: str
    revision: str = "1"
    specifications: dict[str, Any] = field(default_factory=dict)
    capabilities: list[str] = field(default_factory=list)
    source: str = ""
    verification_status: str = "unverified"
    id: str = field(default_factory=new_id)


@dataclass
class ComponentInstance:
    """A specific physical component or serialized unit."""

    product_id: str
    serial_number: str
    physical_identifier_type: str = "unknown"
    verification_status: str = "unverified"
    id: str = field(default_factory=new_id)


@dataclass
class Organization:
    """A company or other organization."""

    name: str
    organization_type: str = "unknown"
    verification_status: str = "unverified"
    website: str = ""
    id: str = field(default_factory=new_id)


@dataclass
class Robot:
    """A robot product or tracked robot system."""

    name: str
    manufacturer: str = ""
    model: str = ""
    id: str = field(default_factory=new_id)


@dataclass
class BOMPosition:
    """A component installation relationship within a robot."""

    robot_id: str
    component_instance_id: str
    position: str
    configuration_revision: str = "1"
    installed_at: str = field(default_factory=utc_now)
    removed_at: str | None = None
    id: str = field(default_factory=new_id)


@dataclass
class LifecycleEvent:
    """An event affecting a physical component during its lifecycle."""

    component_instance_id: str
    event_type: str
    actor: str
    payload: dict[str, Any] = field(default_factory=dict)
    evidence_references: list[str] = field(default_factory=list)
    occurred_at: str = field(default_factory=utc_now)
    id: str = field(default_factory=new_id)


@dataclass
class CompatibilityAssessment:
    """An evidence-based assessment of product compatibility."""

    source_product_id: str
    target_robot_id: str
    status: str = "undetermined"
    checked_requirements: list[str] = field(default_factory=list)
    missing_evidence: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    assessed_at: str = field(default_factory=utc_now)
    id: str = field(default_factory=new_id)


@dataclass
class PerformanceObservation:
    """A measured performance value with units and source provenance."""

    component_instance_id: str
    metric: str
    value: float
    unit: str
    source: str = ""
    observed_at: str = field(default_factory=utc_now)
    id: str = field(default_factory=new_id)


@dataclass
class OntologyRelationship:
    """A typed relationship between two identified entities."""

    source_id: str
    relationship_type: str
    target_id: str
    source_type: str
    target_type: str
    provenance: str = ""
    id: str = field(default_factory=new_id)
