from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.approval.service import list_approvals, decide_approval
from app.db.session import get_db
from app.schemas.schemas import ApprovalDecision, ApprovalOut

router = APIRouter()

@router.get("/", response_model=List[ApprovalOut])
def get_pending(db=Depends(get_db)):
    return list_approvals(db)

@router.post("/{request_id}/decision", response_model=ApprovalOut)
def post_decision(request_id: int, decision: ApprovalDecision, db=Depends(get_db)):
    out = decide_approval(db, request_id, decision)
    if not out:
        raise HTTPException(status_code=404, detail="Approval request not found")
    return out
