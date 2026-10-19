# Upload 03 — ROBOAGENTIC Application Entry Point

**Target source path:** `src/roboagentic/main.py`

**Version:** 0.1.0

## Purpose

Provide an initial command-line interface, SQLite persistence,
database initialization, company registration, and basic reporting.

## Source code

Save the following code as `src/roboagentic/main.py`.

```python
"""ROBOAGENTIC application entry point."""

import argparse
import json
import os
import sqlite3
import uuid
from pathlib import Path
from urllib.parse import urlsplit


def database_path() -> Path:
    """Resolve the configured SQLite database path."""
    url = os.getenv("DATABASE_URL", "sqlite:///./data/roboagentic.db")

    if not url.startswith("sqlite:///"):
        raise RuntimeError(
            "This initial implementation supports SQLite only. "
            "PostgreSQL support will be added in a later step."
        )

    path = Path(url.removeprefix("sqlite:///"))

    if not path.is_absolute():
        path = Path.cwd() / path

    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def connect() -> sqlite3.Connection:
    """Open a database connection with foreign keys enabled."""
    db = sqlite3.connect(database_path())
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db


def initialize_database() -> None:
    """Create the initial company and RFQ tables."""
    with connect() as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS companies (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                website TEXT NOT NULL DEFAULT '',
                country TEXT NOT NULL DEFAULT 'Unknown',
                company_type TEXT NOT NULL DEFAULT 'Unknown',
                description TEXT NOT NULL DEFAULT '',
                capabilities TEXT NOT NULL DEFAULT '[]',
                source_url TEXT NOT NULL DEFAULT '',
                source_verified INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT
                    (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
            );

            CREATE TABLE IF NOT EXISTS rfqs (
                id TEXT PRIMARY KEY,
                component TEXT NOT NULL,
                quantity REAL NOT NULL CHECK(quantity > 0),
                unit TEXT NOT NULL,
                specifications TEXT NOT NULL DEFAULT '{}',
                status TEXT NOT NULL DEFAULT 'draft',
                created_at TEXT NOT NULL DEFAULT
                    (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
            );
            """
        )


def classify_company(text: str) -> list[str]:
    """Return preliminary component categories from text signals."""
    value = text.casefold()
    rules = {
        "actuation": ("actuator", "servo motor", "joint motor"),
        "mechanical": ("cnc machining", "structural frame", "machining"),
        "manipulation": ("robotic hand", "gripper", "end effector"),
        "wiring": ("wiring harness", "electrical connector"),
        "sensing": ("lidar", "force sensor", "tactile sensor"),
        "electronics": ("motor controller", "embedded controller", "pcb"),
    }

    return [
        category
        for category, terms in rules.items()
        if any(term in value for term in terms)
    ]


def calculate_fit_score(
    categories: list[str],
    source_verified: bool = False,
    contact_verified: bool = False,
    capabilities_documented: bool = False,
) -> int:
    """Calculate a preliminary, explainable score from 0 to 100."""
    score = min(len(set(categories)), 5) * 12
    score += 20 if source_verified else 0
    score += 10 if contact_verified else 0
    score += 10 if capabilities_documented else 0
    return min(score, 100)


def qualification_label(score: int) -> str:
    """Describe a preliminary score without claiming qualification."""
    if not 0 <= score <= 100:
        raise ValueError("Score must be between 0 and 100.")

    if score < 25:
        return "low_priority_or_insufficient_evidence"
    if score < 60:
        return "candidate_requires_review"
    return "higher_priority_requires_verification"


def add_company(
    name: str,
    website: str = "",
    country: str = "Unknown",
    company_type: str = "Unknown",
    description: str = "",
    capabilities: list[str] | None = None,
    source_url: str = "",
    source_verified: bool = False,
) -> str:
    """Store a supplier candidate and preserve its source evidence."""
    name = name.strip()
    if not name:
        raise ValueError("Company name is required.")

    for value in (website, source_url):
        if value:
            parsed = urlsplit(value)
            if (
                parsed.scheme not in {"http", "https"}
                or not parsed.hostname
                or parsed.username
                or parsed.password
            ):
                raise ValueError("Website and source must be valid HTTP(S) URLs.")

    company_id = str(uuid.uuid4())
    categories = capabilities or classify_company(description)

    with connect() as db:
        db.execute(
            """
            INSERT INTO companies (
                id, name, website, country, company_type,
                description, capabilities, source_url, source_verified
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                company_id,
                name,
                website,
                country,
                company_type,
                description,
                json.dumps(categories, ensure_ascii=False),
                source_url,
                int(source_verified),
            ),
        )

    return company_id


def create_rfq(
    component: str,
    quantity: float,
    unit: str,
    specifications: dict | None = None,
) -> str:
    """Create a draft RFQ without contacting suppliers."""
    component = component.strip()
    unit = unit.strip()

    if not component or not unit:
        raise ValueError("Component and unit are required.")
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")

    rfq_id = str(uuid.uuid4())

    with connect() as db:
        db.execute(
            """
            INSERT INTO rfqs (
                id, component, quantity, unit, specifications, status
            )
            VALUES (?, ?, ?, ?, ?, 'draft')
            """,
            (
                rfq_id,
                component,
                quantity,
                unit,
                json.dumps(specifications or {}, ensure_ascii=False),
            ),
        )

    return rfq_id


def generate_report() -> Path:
    """Write a basic operational report to the reports directory."""
    initialize_database()
    output = Path("reports/operational_report.txt")
    output.parent.mkdir(parents=True, exist_ok=True)

    with connect() as db:
        company_count = db.execute(
            "SELECT COUNT(*) FROM companies"
        ).fetchone()[0]

        rfq_count = db.execute(
            "SELECT COUNT(*) FROM rfqs"
        ).fetchone()[0]

        draft_count = db.execute(
            "SELECT COUNT(*) FROM rfqs WHERE status = 'draft'"
        ).fetchone()[0]

    output.write_text(
        "ROBOAGENTIC Operational Report\n"
        f"Company records: {company_count}\n"
        f"RFQ records: {rfq_count}\n"
        f"Draft RFQs: {draft_count}\n"
        "Company records are not necessarily verified suppliers.\n",
        encoding="utf-8",
    )

    return output


def main() -> None:
    """Run the ROBOAGENTIC command-line interface."""
    parser = argparse.ArgumentParser(
        description="ROBOAGENTIC robotics sourcing platform"
    )
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("init", help="Initialize the local database")
    commands.add_parser("list", help="List stored company candidates")
    commands.add_parser("report", help="Generate an operational report")

    rfq_parser = commands.add_parser("rfq", help="Create a draft RFQ")
    rfq_parser.add_argument("--component", required=True)
    rfq_parser.add_argument("--quantity", required=True, type=float)
    rfq_parser.add_argument("--unit", required=True)
    rfq_parser.add_argument("--specifications", default="{}")

    args = parser.parse_args()

    if args.command == "init":
        initialize_database()
        print("Database initialized.")

    elif args.command == "list":
        initialize_database()
        with connect() as db:
            rows = db.execute(
                "SELECT id, name, country, company_type FROM companies "
                "ORDER BY name"
            ).fetchall()

        if not rows:
            print("No company candidates are stored.")
        for row in rows:
            print(
                f"{row['name']} | {row['country']} | "
                f"{row['company_type']} | {row['id']}"
            )

    elif args.command == "report":
        print(f"Report written to {generate_report()}")

    elif args.command == "rfq":
        try:
            specifications = json.loads(args.specifications)
        except json.JSONDecodeError as exc:
            parser.error(f"Invalid specifications JSON: {exc}")

        if not isinstance(specifications, dict):
            parser.error("Specifications must be a JSON object.")

        initialize_database()
        rfq_id = create_rfq(
            args.component,
            args.quantity,
            args.unit,
            specifications,
        )
        print(f"Draft RFQ created: {rfq_id}")


if __name__ == "__main__":
    main()
```

## Initial limitations

- SQLite is the only supported database backend at this stage.
- Company candidates are not independently verified.
- RFQs are saved as drafts and are not sent externally.
- Supplier deduplication, authentication, authorization, and migrations remain future implementation tasks.
- This file does not yet integrate the shared dataclasses in `models.py`.
