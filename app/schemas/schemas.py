from pydantic import BaseModel
from typing import Optional, Any, List

class ActionRequest(BaseModel):
    action_type: str  # onboard, salary_change, attendance_correction, leave
    actor: Optional[str] = None
    # Generic payload to include action-specific fields
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    start_date: Optional[str] = None
    employee_id: Optional[str] = None
    old_salary: Optional[float] = None
    new_salary: Optional[float] = None
    hours: Optional[float] = None
    days: Optional[int] = None
    manager_email: Optional[str] = None
    employee_email: Optional[str] = None
    external_recipient: Optional[bool] = False

class ActionResponse(BaseModel):
    request_id: str
    status: str
    risk_score: Optional[int] = None
    approvers: Optional[List[str]] = None
    results: Optional[Any] = None

class ApprovalDecision(BaseModel):
    approver_id: str
    decision: str  # approved | denied
    notes: Optional[str] = None

class ApprovalOut(BaseModel):
    id: int
    request_id: str
    action_type: str
    actor: Optional[str]
    payload: dict
    approvers: list
    status: str
    created_at: str
