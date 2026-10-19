Upload 04 — ROBOAGENTIC Dependencies and Installation

Product: ROBOPARTS.ai
Project: ROBOAGENTIC
Version: 0.1.0
Status: Installation plan — not yet tested

1. Required environment
Python 3.12 or newer within the supported project configuration.
Git and a local clone of the repository.
A Python virtual environment.
Internet access for installing packages.
No external API keys are required for the initial local database stage.
2. Planned dependency groups
Core application
pydantic — data validation.
httpx — HTTP requests for future discovery integrations.
beautifulsoup4 — future HTML parsing.
SQLAlchemy — planned database abstraction.
python-dotenv — optional local environment configuration.
Development and testing
pytest — automated tests.
pytest-asyncio — asynchronous test support.
ruff — Python linting.
Future API service
fastapi — HTTP API framework.
uvicorn[standard] — ASGI server.
Future PostgreSQL support
psycopg[binary] — PostgreSQL driver.

These dependencies must be declared in the actual pyproject.toml before they can be installed reliably as project dependencies.

3. Installation sequence

Run commands from the repository root.

Create a virtual environment:

python -m venv .venv


Activate on Windows:

.venv\Scripts\activate


Activate on macOS or Linux:

source .venv/bin/activate


Upgrade the installer:

python -m pip install --upgrade pip


Install the project and development dependencies after the actual project configuration is verified:

python -m pip install -e ".[dev]"

4. Initial verification

Check the Python version:

python --version


Check the package installer:

python -m pip --version


Check installed dependencies:

python -m pip check


After the source files have been created at their actual target paths, initialize the database:

roboagentic init


Generate an initial report:

roboagentic report


Run automated tests once the test suite exists:

pytest


Run lint checks once the source tree exists:

ruff check src tests

5. Installation safeguards
Never commit .env files containing secrets.
Do not place API keys or SMTP credentials in source code.
Keep development dependencies separate from production-only dependencies where practical.
Do not deploy a background worker before its database, configuration, and error handling have been tested.
Record installation failures and resolve them before advancing.
6. Acceptance criteria

This stage is complete only after:

The real pyproject.toml has been reviewed and reconciled with the planned dependencies.
The application source exists at its declared package path.
The package installs successfully in a clean virtual environment.
python -m pip check passes.
The initial database commands work.
Automated tests pass once implemented.

Important: Creating this planning document does not install dependencies or prove that the application works.
