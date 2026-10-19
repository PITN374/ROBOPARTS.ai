Upload 05 — ROBOAGENTIC Project Configuration

Project: ROBOAGENTIC
Product: ROBOPARTS.ai
Version: 0.1.0
Status: Proposed configuration — implementation and installation not yet verified

1. Purpose

Define the Python build system, package metadata, dependency groups, source layout, test configuration, linting settings, and command-line entry point.

2. Required target file

The actual configuration must eventually be saved as:

pyproject.toml

Important: This Markdown document is the implementation specification. Python packaging tools require the actual configuration to be saved as pyproject.toml, not as a Markdown file.

3. Complete proposed pyproject.toml

Copy the following contents into the actual pyproject.toml file when we reach the configuration implementation stage.

[build-system]
requires = ["setuptools>=69.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "roboagentic"
version = "0.1.0"
description = "Robotics supplier intelligence, manufacturer discovery, RFQ preparation, and reporting for ROBOPARTS.ai"
requires-python = ">=3.12"
license = "MIT"
authors = [
    { name = "ROBOPARTS.ai" }
]
keywords = [
    "robotics",
    "humanoid-robots",
    "supplier-discovery",
    "procurement",
    "RFQ",
    "automation",
    "multilingual",
    "multi-agent"
]
dependencies = [
    "pydantic>=2.8,<3.0",
    "httpx>=0.27,<1.0",
    "beautifulsoup4>=4.12,<5.0",
    "SQLAlchemy>=2.0,<3.0",
    "python-dotenv>=1.0,<2.0",
    "fastapi>=0.115,<1.0",
    "uvicorn[standard]>=0.30,<1.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0,<9.0",
    "pytest-asyncio>=0.23,<2.0",
    "ruff>=0.6,<1.0"
]
postgres = [
    "psycopg[binary]>=3.2,<4.0"
]

[project.scripts]
roboagentic = "roboagentic.main:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
asyncio_mode = "auto"

[tool.ruff]
line-length = 88
target-version = "py312"

4. Expected repository structure
ROBOPARTS.ai/
├── pyproject.toml
├── README.md
├── .gitignore
├── src/
│   └── roboagentic/
│       ├── __init__.py
│       └── main.py
├── tests/
└── docs/


This is the target structure, not a claim that these files already exist or have been tested.

5. Dependency responsibilities
setuptools and wheel: package building.
pydantic: data validation.
httpx: HTTP requests for future discovery integrations.
beautifulsoup4: HTML parsing.
SQLAlchemy: planned database abstraction.
python-dotenv: local environment configuration.
fastapi and uvicorn: future API service.
pytest and pytest-asyncio: automated testing.
ruff: code quality checks.
psycopg: optional PostgreSQL connectivity.

The current proposed SQLite implementation uses Python's built-in sqlite3 module. Installing SQLAlchemy does not automatically migrate that implementation to SQLAlchemy.

6. Important implementation dependencies

Before installing the project:

Create the actual pyproject.toml.
Create the Python package at src/roboagentic/.
Create the actual main.py source file.
Create README.md if the final configuration declares it as package metadata.
Create the initial test suite.
Install the project in a clean virtual environment.
Verify the command-line entry point and run the tests.
7. Acceptance criteria

This configuration is accepted only after the actual TOML file parses successfully, package installation succeeds, declared dependencies resolve, and the command-line entry point works.

No production readiness or successful installation is implied by creating this document.
