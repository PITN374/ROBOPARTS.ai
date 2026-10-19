# ROBOAGENTIC / ROBOPARTS.ai
## Implementation Manifest

Version: 0.1.0
Status: Initial implementation planning

### 1. Project Objective
Build ROBOAGENTIC, the robotics intelligence and sourcing platform for ROBOPARTS.ai, with supplier discovery, component identity, procurement workflows, lifecycle traceability, and operational reporting.

### 2. Implementation Rules
- Preserve existing functionality when integrating new files.
- Maintain one authoritative version of each project file.
- Record every file's destination and dependencies before implementation.
- Treat supplier search results as candidates until supporting evidence has been reviewed.
- Keep product identity separate from physical component instance identity.
- Do not infer verification, compatibility, or manufacturing capability from missing evidence.
- Never commit API keys, passwords, tokens, or private credentials.
- Test each implementation stage before proceeding to dependent stages.
- Document unresolved dependencies and request additional source material when necessary.

### 3. Implementation Sequence
1. Repository structure, configuration, and implementation manifest.
2. Python package configuration and shared data models.
3. Database schema, persistence, and migrations.
4. Supplier discovery and evidence capture.
5. Manufacturer verification and identity resolution.
6. Component registry, robots, BOM relationships, and lifecycle traceability.
7. Compatibility assessment and performance observations.
8. API schemas, endpoints, and application integration.
9. RFQ preparation, reporting, and background worker.
10. Automated tests and continuous integration.
11. Security, monitoring, backup, and recovery.
12. Deployment, operational documentation, and launch-readiness review.

### 4. Supplied Material Inventory
- Python data model specification, version 0.1.0.
- Python package configuration and dependency declarations.
- FastAPI and Uvicorn dependency requirements.
- FastAPI application draft using SQLite and pitn.db.
- Brave Search manufacturer discovery module.
- Discovery package initializer and environment configuration template.
- Autonomous worker, email reporting module, and Render deployment configuration.
- Manufacturer evidence review and identity assessment modules.
- README, .gitignore, tests, GitHub Actions workflow, and development roadmap drafts.

### 5. Initial File Inventory
- README.md — repository overview and operating instructions.
- .gitignore — protect secrets and exclude generated files.
- pyproject.toml — Python packaging, dependencies, CLI, and development tools.
- requirements.txt — application runtime dependencies where needed.
- .env.example — documented configuration placeholders without credentials.
- src/roboagentic/__init__.py — package initializer.
- src/roboagentic/models.py — shared Python data models; confirm final module name before implementation.
- Database schema and migration files — to be designed against the existing application.
- Discovery modules — search.py, verify.py, identity.py.
- Job modules — worker.py and reporting.py.
- app/main.py — API entry point; integrate with the authoritative database design.
- tests/ — unit and integration tests.
- .github/workflows/tests.yml — automated test workflow.
- render.yaml — deployment configuration, after runtime and database requirements are confirmed.
- docs/ROADMAP.md — staged development and launch requirements.

### 6. Integration Risks to Resolve
- Confirm the existing repository tree and current contents of main.py before merging.
- Reconcile the existing application database with the proposed pitn.db SQLite API.
- Confirm whether shared data models will live in models.py or another established module.
- Ensure all declared CLI commands have corresponding implementations.
- Verify that worker imports and reporting configuration match the final package structure.
- Add database migrations, authentication, authorization, validation, and operational safeguards before production use.
- Test idempotency and duplicate handling before enabling recurring discovery.

### 7. Definition of Done for Each File
- Exact repository destination recorded.
- Dependencies and interfaces identified.
- Complete file content prepared in the requested transfer format.
- Syntax and integration assumptions reviewed.
- Tests identified or added where appropriate.
- Status updated: planned, supplied, prepared, uploaded, integrated, or tested.

### 8. Launch Gate
Uploading files does not itself constitute a working or production-ready deployment. Launch requires successful tests, verified configuration, secure credentials, persistent storage, access controls, monitoring, backup and recovery procedures, and documented operational review.

### 9. Change Log
- Version 0.1.0: initial implementation inventory and staged delivery plan.
