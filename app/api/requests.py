from fastapi import APIRouter, Depends, HTTPException
from app.schemas.schemas import ActionRequest, ActionResponse
from app.approval.service import submit_action_request, get_pending_approvals
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=ActionResponse)
def create_request(payload: ActionRequest, db=Depends(get_db)):
    """
    Submit an HR-related action (onboard, salary_change, attendance_correction, leave).
    The agent will compute risk and either execute or create an approval request.
    """
    req = submit_action_request(db, payload)
    return req
