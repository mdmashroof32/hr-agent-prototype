import os
from typing import Dict

# Thresholds from env or defaults
SALARY_SINGLE_THRESHOLD = float(os.getenv("SALARY_SINGLE_APPROVER_THRESHOLD", 5000))
SALARY_SINGLE_PERCENT = float(os.getenv("SALARY_SINGLE_APPROVER_PERCENT", 10))
SALARY_TWO_THRESHOLD = float(os.getenv("SALARY_TWO_APPROVER_THRESHOLD", 20000))
SALARY_TWO_PERCENT = float(os.getenv("SALARY_TWO_APPROVER_PERCENT", 30))
ATTENDANCE_AUTO_HOURS = float(os.getenv("ATTENDANCE_AUTO_CORRECTION_MAX_HOURS", 2))

def compute_risk(action_type: str, payload: Dict) -> int:
    score = 0
    if action_type == "salary_change":
        old = float(payload.get("old_salary", 0))
        new = float(payload.get("new_salary", 0))
        delta = new - old
        pct = (delta / old * 100) if old > 0 else 100.0
        if delta > 0:
            score += 50
        if delta >= SALARY_SINGLE_THRESHOLD:
            score += 30
        if pct >= SALARY_SINGLE_PERCENT:
            score += 20
        if delta >= SALARY_TWO_THRESHOLD or pct >= SALARY_TWO_PERCENT:
            score += 40
    if action_type == "onboard":
        score += 10
    if action_type == "attendance_correction":
        hours = float(payload.get("hours", 0))
        if hours > ATTENDANCE_AUTO_HOURS:
            score += 40
        else:
            score += 5
    if action_type == "leave":
        days = float(payload.get("days", 0))
        if days > 14:
            score += 30
    # If external recipients or PII exposure, bump risk (not exhaustive)
    if payload.get("external_recipient"):
        score += 25
    return int(score)

AUTO_THRESHOLD = 30

def requires_approval(action_type: str, payload: Dict) -> bool:
    score = compute_risk(action_type, payload)
    return score >= AUTO_THRESHOLD

def required_approvers(action_type: str, payload: Dict) -> list:
    """
    Return list of approver roles required. Simple mapping for prototype.
    """
    approvers = ["hr_manager"]
    if action_type == "salary_change":
        old = float(payload.get("old_salary", 0))
        new = float(payload.get("new_salary", 0))
        delta = new - old
        pct = (delta / old * 100) if old > 0 else 100.0
        if delta >= SALARY_TWO_THRESHOLD or pct >= SALARY_TWO_PERCENT:
            approvers = ["hr_manager", "finance_manager"]
    return approvers
