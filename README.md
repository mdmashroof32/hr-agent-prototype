# Semi-Autonomous HR Agent (Prototype)

This project is a minimal semi-autonomous HR agent prototype implemented in Python with FastAPI. It demonstrates core components for:
- submitting HR action requests (onboarding, salary change, attendance correction, leave),
- risk scoring and approval workflows,
- mock adapters for HRIS, attendance, email, and Slack,
- a simple approval UI (API + HTML),
- persistence via SQLAlchemy.

You can save the files from this package into a directory, run the app locally (or with Docker), and exercise the workflows with the provided sample requests.

Features
- Submit actions via REST API (`/requests`) — the agent will compute a risk score and either auto-execute or create an approval request.
- Approvers can list pending approvals (`/approvals`) and make decisions (`/approvals/{id}/decision`).
- Mock adapters simulate external systems (HRIS, Attendance, Email).
- Planner is an LLM-backed stub: if `OPENAI_API_KEY` is set, it will call OpenAI for planning; otherwise it uses a deterministic plan generator.
- Configurable thresholds via environment variables.

Defaults (change as needed)
- Language: Python 3.11
- Framework: FastAPI
- DB: Postgres (docker-compose) or local SQLite by default
- LLM backend: OpenAI if `OPENAI_API_KEY` is provided; otherwise fallback stub
- Notifications: Slack stub (prints or uses webhook if `SLACK_WEBHOOK_URL` set)

Quickstart (local, without Docker)
1. Create a Python virtualenv and activate it
   python -m venv .venv
   source .venv/bin/activate

2. Install dependencies
   pip install -r requirements.txt

3. Copy `.env.example` to `.env` and adjust values as needed.

4. Run the app
   uvicorn app.main:app --reload

5. Submit a sample request (see scripts/sample_requests.sh) or visit:
   - POST /requests
   - GET /approvals
   - POST /approvals/{id}/decision

Quickstart (Docker Compose)
1. Ensure Docker and Docker Compose are installed.
2. Copy `.env.example` to `.env`.
3. Run:
   docker-compose up --build

Project layout
- app/
  - main.py — FastAPI application and router registration
  - api/requests.py — endpoint to submit actions
  - api/approvals.py — endpoints to list and decide approvals
  - core/
    - planner.py — plan generator (LLM stub + fallback)
    - policy.py — risk scoring and auto-approval logic
    - executor.py — executes approved actions via adapters
  - adapters/ — mock external integrations
  - db/ — SQLAlchemy setup and models
  - approval/ — approval service helpers
  - schemas/ — Pydantic request/response models
- scripts/ — helper scripts and curl examples
- tests/ — minimal unit tests
- Dockerfile, docker-compose.yml — containerization

Important notes
- This project is a prototype and uses mock adapters by default. Before connecting to real HRIS or payroll systems:
  - Implement secure adapter modules with least-privilege credentials.
  - Add manual human approval gates for high-risk actions (salary changes, terminations).
  - Enable audit logging and retention per your compliance requirements.
  - Use Vault (or similar) to manage secrets rather than plain `.env` files.

What you can do next
- Replace mock adapters (app/adapters/*.py) with real API clients (Workday, BambooHR, G Suite, Okta, SendGrid).
- Harden security: Vault, OAuth2 SSO, role-based access control for approvers.
- Add tests and CI, and integrate a real Slack/Email provider for notifications.
- Swap planner to a private LLM if required for data governance.

License
MIT
