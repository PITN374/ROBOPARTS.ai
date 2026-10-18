""" ROBOAGENTIC Global Robotics Intelligence and Sourcing Agent Product: ROBOPARTS.ai
Author: Aaron Bailot PITN powerinthenumbers.ai aka ROBOPARTS.ai and ROBOAGENTIC.ai 
Initial executable implementation.

Capabilities:

Local company and supplier database
Robotics component taxonomy
Company classification
Evidence-backed company records
Supplier relevance scoring
RFQ draft generation
Developer text reports
Command-line interface

Live search, external databases, AI services, and email delivery require separately configured provider integrations.

Email sending is disabled by default. """

from future import annotations

import argparse import json import logging import os import re from datetime import datetime, timezone from pathlib import Path from typing import Any

from dotenv import load_dotenv from sqlalchemy import ( Boolean, DateTime, Float, ForeignKey, Integer, String, Text, create_engine, select, ) from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

load_dotenv()

APP_NAME = "ROBOAGENTIC" PRODUCT_NAME = "ROBOPARTS.ai"

DATA_DIR = Path("data") REPORT_DIR = Path("reports")

DATA_DIR.mkdir(exist_ok=True) REPORT_DIR.mkdir(exist_ok=True)

DATABASE_URL = os.getenv( "DATABASE_URL", "sqlite:///./data/roboagentic.db", )

OUTREACH_ENABLED = ( os.getenv("OUTREACH_ENABLED", "false").strip().lower() == "true" )

OUTREACH_DRY_RUN = ( os.getenv("OUTREACH_DRY_RUN", "true").strip().lower() == "true" )

logging.basicConfig( level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(asctime)s %(levelname)s %(name)s: %(message)s", )

logger = logging.getLogger(APP_NAME)

def utc_now() -> datetime: """Return a timezone-aware UTC timestamp.""" return datetime.now(timezone.utc)

class Base(DeclarativeBase): """Base class for database models."""

class Company(Base): """A robotics manufacturer, supplier, or integrator."""

__tablename__ = "companies"

id: Mapped[int] = mapped_column(Integer, primary_key=True)

name: Mapped[str] = mapped_column(String(250), nullable=False, index=True)

website: Mapped[str] = mapped_column(String(1000), default="")

country: Mapped[str] = mapped_column(String(100), default="Unknown")

company_type: Mapped[str] = mapped_column(
    String(100),
    default="Unclassified",
)

component_categories: Mapped[str] = mapped_column(
    Text,
    default="[]",
)

manufacturing_capabilities: Mapped[str] = mapped_column(
    Text,
    default="[]",
)

source_url: Mapped[str] = mapped_column(String(2000), default="")

source_verified: Mapped[bool] = mapped_column(Boolean, default=False)

contact_email: Mapped[str] = mapped_column(String(320), default="")

contact_source_url: Mapped[str] = mapped_column(
    String(2000),
    default="",
)

contact_verified: Mapped[bool] = mapped_column(
    Boolean,
    default=False,
)

fit_score: Mapped[float] = mapped_column(Float, default=0.0)

qualification_status: Mapped[str] = mapped_column(
    String(50),
    default="unreviewed",
)

created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=utc_now,
)

updated_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=utc_now,
    onupdate=utc_now,
)


class RFQ(Base): """A request for quotation prepared for supplier review."""

__tablename__ = "rfqs"

id: Mapped[int] = mapped_column(Integer, primary_key=True)

component_name: Mapped[str] = mapped_column(
    String(250),
    nullable=False,
)

quantity: Mapped[int] = mapped_column(Integer, nullable=False)

unit: Mapped[str] = mapped_column(String(50), default="units")

specifications: Mapped[str] = mapped_column(Text, default="{}")

status: Mapped[str] = mapped_column(
    String(50),
    default="draft",
)

created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=utc_now,
)


class AuditEvent(Base): """An operational event for traceability."""

__tablename__ = "audit_events"

id: Mapped[int] = mapped_column(Integer, primary_key=True)

event_type: Mapped[str] = mapped_column(String(100), nullable=False)

details: Mapped[str] = mapped_column(Text, default="{}")

created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=utc_now,
)


engine = create_engine(DATABASE_URL) SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

COMPONENT_TAXONOMY: dict[str, list[str]] = { "actuation": [ "joint actuator", "servo motor", "bldc motor", "linear actuator", "motor controller", ], "mechanical": [ "aluminum structural parts", "cnc machining", "gearbox", "harmonic drive", "bearing", "structural frame", ], "manipulation": [ "robotic hand", "robotic hands", "gripper", "end effector", "robot finger", ], "electronics": [ "wiring harness", "connector", "printed circuit board", "embedded controller", "power distribution", ], "sensing": [ "lidar", "camera", "force sensor", "tactile sensor", "encoder", "imu", ], "computing": [ "edge computer", "ai accelerator", "robotics software", "motion planning", "robot control", ], }

def record_event( session: Any, event_type: str, details: dict[str, Any], ) -> None: """Store a structured audit event.""" session.add( AuditEvent( event_type=event_type, details=json.dumps(details, ensure_ascii=False), ) )

def classify_company( description: str, capabilities: list[str] | None = None, ) -> list[str]: """Identify component categories using configurable keyword rules.""" text = " ".join( [description, *(capabilities or [])] ).casefold()

matches: list[str] = []

for category, keywords in COMPONENT_TAXONOMY.items():
    if any(keyword.casefold() in text for keyword in keywords):
        matches.append(category)

return matches


def calculate_fit_score( categories: list[str], source_verified: bool, contact_verified: bool, capabilities_documented: bool, ) -> float: """ Calculate a preliminary relevance and evidence score.

This is a heuristic, not a validated commercial prediction.
A high score never independently authorizes outreach.
"""
category_points = min(len(set(categories)) * 10, 30)

evidence_points = 15 if source_verified else 0

contact_points = 10 if contact_verified else 0

capability_points = 20 if capabilities_documented else 0

industry_points = 15 if categories else 0

score = (
    category_points
    + evidence_points
    + contact_points
    + capability_points
    + industry_points
)

return float(min(score, 100))


def qualification_label(score: float) -> str: """Convert a preliminary score to a review priority.""" if score >= 80: return "high_priority_review"

if score >= 60:
    return "relevant_candidate"

if score >= 40:
    return "needs_research"

return "low_priority_or_insufficient_evidence"


def add_company( name: str, website: str, country: str, company_type: str, description: str, capabilities: list[str] | None = None, source_url: str = "", source_verified: bool = False, contact_email: str = "", contact_source_url: str = "", contact_verified: bool = False, ) -> int: """Create or update a company using its normalized website or name.""" if not name.strip(): raise ValueError("Company name cannot be empty.")

if website and not re.match(r"^https?://", website, re.IGNORECASE):
    raise ValueError("Website must begin with http:// or https://.")

if source_verified and not source_url:
    raise ValueError("A verified source requires a source URL.")

if contact_verified and (
    not contact_email or not contact_source_url
):
    raise ValueError(
        "A verified contact requires an email and source URL."
    )

if contact_email and not re.fullmatch(
    r"[^@\s]+@[^@\s]+\.[^@\s]+",
    contact_email,
):
    raise ValueError("Contact email has invalid syntax.")

capabilities = capabilities or []

categories = classify_company(description, capabilities)

score = calculate_fit_score(
    categories=categories,
    source_verified=source_verified,
    contact_verified=contact_verified,
    capabilities_documented=bool(capabilities),
)

normalized_website = website.strip().rstrip("/").casefold()

with SessionLocal() as session:
    existing = None

    if normalized_website:
        existing = session.scalar(
            select(Company).where(
                Company.website == normalized_website
            )
        )

    if existing is None:
        existing = session.scalar(
            select(Company).where(
                Company.name == name.strip()
            )
        )

    if existing is None:
        company = Company(
            name=name.strip(),
            website=normalized_website,
            country=country.strip() or "Unknown",
            company_type=company_type.strip() or "Unclassified",
            component_categories=json.dumps(categories),
            manufacturing_capabilities=json.dumps(capabilities),
            source_url=source_url,
            source_verified=source_verified,
            contact_email=contact_email,
            contact_source_url=contact_source_url,
            contact_verified=contact_verified,
            fit_score=score,
            qualification_status=qualification_label(score),
        )
        session.add(company)
        record_event(
            session,
            "company_created",
            {"name": name.strip(), "categories": categories},
        )
    else:
        company = existing
        company.name = name.strip()
        company.website = normalized_website or company.website
        company.country = country.strip() or company.country
        company.company_type = company_type.strip() or company.company_type
        company.component_categories = json.dumps(categories)
        company.manufacturing_capabilities = json.dumps(capabilities)

        if source_url:
            company.source_url = source_url
            company.source_verified = source_verified

        if contact_email:
            company.contact_email = contact_email
            company.contact_source_url = contact_source_url
            company.contact_verified = contact_verified

        company.fit_score = score
        company.qualification_status = qualification_label(score)

        record_event(
            session,
            "company_updated",
            {"name": name.strip(), "categories": categories},
        )

    session.commit()
    session.refresh(company)

    return company.id


def list_companies() -> list[dict[str, Any]]: """Return stored companies ordered by fit score.""" with SessionLocal() as session: companies = session.scalars( select(Company).order_by(Company.fit_score.desc()) ).all()

    return [
        {
            "id": company.id,
            "name": company.name,
            "website": company.website,
            "country": company.country,
            "categories": json.loads(company.component_categories),
            "fit_score": company.fit_score,
            "qualification_status": company.qualification_status,
            "source_verified": company.source_verified,
            "contact_verified": company.contact_verified,
        }
        for company in companies
    ]


def create_rfq( component_name: str, quantity: int, unit: str, specifications: dict[str, Any], ) -> int: """Create an RFQ draft; do not transmit it to a supplier.""" if not component_name.strip(): raise ValueError("Component name cannot be empty.")

if quantity <= 0:
    raise ValueError("Quantity must be greater than zero.")

with SessionLocal() as session:
    rfq = RFQ(
        component_name=component_name.strip(),
        quantity=quantity,
        unit=unit.strip() or "units",
        specifications=json.dumps(
            specifications,
            ensure_ascii=False,
        ),
        status="draft",
    )

    session.add(rfq)

    record_event(
        session,
        "rfq_draft_created",
        {
            "component_name": component_name,
            "quantity": quantity,
        },
    )

    session.commit()
    session.refresh(rfq)

    return rfq.id


def generate_report() -> Path: """Generate a text report of current application records.""" companies = list_companies()

with SessionLocal() as session:
    rfqs = session.scalars(
        select(RFQ).order_by(RFQ.id.desc())
    ).all()

report_path = REPORT_DIR / (
    f"roboagentic_report_{utc_now().strftime('%Y%m%dT%H%M%SZ')}.txt"
)

lines = [
    "ROBOAGENTIC OPERATIONAL REPORT",
    f"Product: {PRODUCT_NAME}",
    f"Generated UTC: {utc_now().isoformat()}",
    "",
    f"Company records: {len(companies)}",
    f"RFQ drafts: {len(rfqs)}",
    "",
    "COMPANY RECORDS",
    "=" * 72,
]

for company in companies:
    lines.extend(
        [
            f"ID: {company['id']}",
            f"Name: {company['name']}",
            f"Website: {company['website'] or 'Not available'}",
            f"Country: {company['country']}",
            f"Categories: {', '.join(company['categories']) or 'Unclassified'}",
            f"Fit score: {company['fit_score']}",
            f"Priority: {company['qualification_status']}",
            f"Source verified: {company['source_verified']}",
            f"Contact verified: {company['contact_verified']}",
            "-" * 72,
        ]
    )

lines.extend(["", "RFQ DRAFTS", "=" * 72])

for rfq in rfqs:
    lines.extend(
        [
            f"RFQ ID: {rfq.id}",
            f"Component: {rfq.component_name}",
            f"Quantity: {rfq.quantity} {rfq.unit}",
            f"Specifications: {rfq.specifications}",
            f"Status: {rfq.status}",
            "-" * 72,
        ]
    )

lines.extend(
    [
        "",
        "OUTREACH STATUS",
        f"Outreach enabled: {OUTREACH_ENABLED}",
        f"Dry-run mode: {OUTREACH_DRY_RUN}",
        "No email delivery is implemented in this initial release.",
        "",
        "Coverage note:",
        "These figures describe local database records only.",
        "They do not represent total worldwide robotics coverage.",
    ]
)

report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

logger.info("Report created: %s", report_path)

return report_path


def seed_demo_data() -> None: """Insert clearly labeled synthetic examples for testing.""" examples = [ { "name": "DEMO Actuator Manufacturer", "website": "https://example.com/demo-actuators", "country": "Demo Country", "company_type": "Synthetic test record", "description": "Joint actuators and servo motors for humanoid robots", "capabilities": ["Actuator assembly", "Servo motor integration"], }, { "name": "DEMO Robotics Machining Supplier", "website": "https://example.com/demo-machining", "country": "Demo Country", "company_type": "Synthetic test record", "description": "CNC machining aluminum structural parts and frames", "capabilities": ["CNC machining", "Aluminum machining"], }, { "name": "DEMO Robotic Hand Manufacturer", "website": "https://example.com/demo-hands", "country": "Demo Country", "company_type": "Synthetic test record", "description": "Robotic hands, grippers, and end effectors", "capabilities": ["Robotic hand assembly", "Gripper manufacturing"], }, { "name": "DEMO Wiring Harness Supplier", "website": "https://example.com/demo-harnesses", "country": "Demo Country", "company_type": "Synthetic test record", "description": "Wiring harnesses and electrical connectors", "capabilities": ["Harness assembly", "Connector integration"], }, ]

for example in examples:
    add_company(**example)

logger.info("Synthetic demonstration records loaded.")


def initialize_database() -> None: """Create database tables.""" Base.metadata.create_all(engine) logger.info("Database initialized.")

def main() -> None: """Command-line entry point.""" parser = argparse.ArgumentParser( prog="roboagentic", description=( "ROBOAGENTIC robotics supplier intelligence " "and RFQ preparation" ), )

subparsers = parser.add_subparsers(dest="command")

subparsers.add_parser(
    "init",
    help="Initialize the local database",
)

subparsers.add_parser(
    "demo",
    help="Load synthetic demonstration company records",
)

subparsers.add_parser(
    "list",
    help="List stored companies",
)

subparsers.add_parser(
    "report",
    help="Generate an operational text report",
)

rfq_parser = subparsers.add_parser(
    "rfq",
    help="Create an RFQ draft",
)

rfq_parser.add_argument("--component", required=True)
rfq_parser.add_argument("--quantity", required=True, type=int)
rfq_parser.add_argument("--unit", default="units")
rfq_parser.add_argument(
    "--specifications",
    default="{}",
    help="Specifications as a JSON object",
)

args = parser.parse_args()

initialize_database()

if args.command == "init":
    print("ROBOAGENTIC database initialized.")

elif args.command == "demo":
    seed_demo_data()
    print("Synthetic demonstration records loaded.")

elif args.command == "list":
    print(
        json.dumps(
            list_companies(),
            indent=2,
            ensure_ascii=False,
        )
    )

elif args.command == "report":
    print(f"Report saved to: {generate_report()}")

elif args.command == "rfq":
    try:
        specifications = json.loads(args.specifications)

        if not isinstance(specifications, dict):
            raise ValueError("Specifications must be a JSON object.")

        rfq_id = create_rfq(
            component_name=args.component,
            quantity=args.quantity,
            unit=args.unit,
            specifications=specifications,
        )

        print(f"RFQ draft created successfully. ID: {rfq_id}")

    except (json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))

else:
    parser.print_help()


if name == "main": main()
