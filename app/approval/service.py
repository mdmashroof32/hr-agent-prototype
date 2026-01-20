import uuid
from typing import Dict, List
from sqlalchemy.orm import Session
from app.core import planner, policy, executor
from app.db import models
from app.adapters import slack_notifier, emailer

def submit_action_request(db: Session, payload: Dict):
    """
    Create an action request, compute risk, auto-execute or create approval request.
    """
    req_id = str(uuid.uuid4())
    action_type = payload.action_type
    p = payload.dict()
    # compute risk
    risk = policy.compute_risk(action_type, p)
    # store action record
    ar = models.ActionRecord(
        request_id=req_id,
        action_type=action_type,
        actor=p.get("actor"),
        payload=p,
        status="pending",
        risk_score=risk
    )
    db.add(ar)
    db.commit()
    db.refresh(ar)

    # create plan
    plan = planner.plan_for_action(action_type, p)

    if policy.requires_approval(action_type, p):
        approvers = policy.required_approvers(action_type, p)
        apr = models.ApprovalRequest(
            action_record_id=ar.id,
            status="pending",
            approvers=approvers,
            decisions=[]
        )
        db.add(apr)
        db.commit()
        db.refresh(apr)
        # notify via Slack/email in prototype
        slack_notifier.notify(f"Approval required: {action_type} request {req_id} (risk {risk}) Approvers: {approvers}")
        emailer.send_email({"to": "approver@example.com", "subject": "Approval required", "body": f"Request {req_id} needs approval."})
        return {
            "request_id": req_id,
            "status": "approval_required",
            "risk_score": risk,
            "approvers": approvers
        }
    else:
        # Execute directly
        results = executor.execute_plan(plan)
        ar.status = "executed"
        db.add(ar)
        db.commit()
        return {"request_id": req_id, "status": "executed", "risk_score": risk, "results": results}


def list_approvals(db: Session):
    rows = db.query(models.ApprovalRequest).filter(models.ApprovalRequest.status == "pending").all()
    out = []
    for r in rows:
        ar = db.query(models.ActionRecord).filter(models.ActionRecord.id == r.action_record_id).first()
        out.append({
            "id": r.id,
            "request_id": ar.request_id,
            "action_type": ar.action_type,
            "actor": ar.actor,
            "payload": ar.payload,
            "approvers": r.approvers,
            "status": r.status,
            "created_at": r.created_at.isoformat()
        })
    return out

def decide_approval(db: Session, request_id: int, decision_payload: Dict):
    r = db.query(models.ApprovalRequest).filter(models.ApprovalRequest.id == request_id).first()
    if not r:
        return None
    # Append decision
    decisions = r.decisions or []
    decisions.append({"approver_id": decision_payload.approver_id, "decision": decision_payload.decision, "notes": decision_payload.notes})
    r.decisions = decisions
    # If any deny -> mark denied
    if decision_payload.decision == "denied":
        r.status = "denied"
        db.add(r)
        db.commit()
        # Update action record
        ar = db.query(models.ActionRecord).filter(models.ActionRecord.id == r.action_record_id).first()
        ar.status = "denied"
        db.add(ar)
        db.commit()
        slack_notifier.notify(f"Approval {r.id} denied by {decision_payload.approver_id}")
        return {
            "id": r.id,
            "status": r.status,
            "decisions": r.decisions
        }
    # If approved, check if we have required number of approvals (simple: all approvers must approve; prototype assumes one)
    # For prototype, treat single approval as enough unless approvers list length >1
    approvers_required = r.approvers or []
    # Count unique approvers who approved
    approved_set = set([d["approver_id"] for d in decisions if d["decision"] == "approved"])
    if len(approvers_required) == 0 or len(approved_set) >= len(approvers_required):
        r.status = "approved"
        db.add(r)
        db.commit()
        # Execute the action
        ar = db.query(models.ActionRecord).filter(models.ActionRecord.id == r.action_record_id).first()
        plan = planner.plan_for_action(ar.action_type, ar.payload)
        results = executor.execute_plan(plan)
        ar.status = "executed"
        db.add(ar)
        db.commit()
        slack_notifier.notify(f"Approval {r.id} approved and executed")
        return {
            "id": r.id,
            "status": r.status,
            "decisions": r.decisions,
            "execution_results": results
        }
    else:
        db.add(r)
        db.commit()
        return {
            "id": r.id,
            "status": r.status,
            "decisions": r.decisions
        }
