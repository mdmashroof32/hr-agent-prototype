from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import requests as requests_router
from app.api import approvals as approvals_router
from app.db.session import engine, Base

# Create DB tables (simple approach for prototype)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Semi-Autonomous HR Agent Prototype")

app.include_router(requests_router.router, prefix="/requests", tags=["requests"])
app.include_router(approvals_router.router, prefix="/approvals", tags=["approvals"])

# Simple static serving for a tiny approval UI if needed
app.mount("/static", StaticFiles(directory="app/static"), name="static")
