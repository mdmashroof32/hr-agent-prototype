import os
import requests
from typing import List, Dict

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def plan_for_action(action_type: str, payload: Dict) -> List[Dict]:
    """
    Produce a list of steps for the given action.
    If OPENAI_API_KEY is set, this can call an LLM; otherwise use a deterministic plan.
    Each step is a dict: {"name": "...", "adapter": "hris|attendance|email", "action": "...", "params": {...}}
    """
    # Fallback deterministic planner
    if not OPENAI_API_KEY:
        if action_type == "onboard":
            return [
                {"name": "create_employee", "adapter": "hris", "action": "create_employee", "params": payload},
                {"name": "create_accounts", "adapter": "hris", "action": "provision_accounts", "params": payload},
                {"name": "send_welcome_email", "adapter": "email", "action": "send_email", "params": {"to": payload.get("email"), "subject": "Welcome", "body": "Welcome!"}},
            ]
        if action_type == "salary_change":
            return [
                {"name": "update_salary", "adapter": "hris", "action": "update_salary", "params": payload},
                {"name": "notify_employee", "adapter": "email", "action": "send_email", "params": {"to": payload.get("employee_email"), "subject": "Salary updated", "body": "Your salary has been updated."}},
            ]
        if action_type == "attendance_correction":
            return [
                {"name": "apply_attendance_correction", "adapter": "attendance", "action": "apply_correction", "params": payload},
                {"name": "notify_manager", "adapter": "email", "action": "send_email", "params": {"to": payload.get("manager_email"), "subject": "Attendance corrected", "body": "An attendance correction was applied."}},
            ]
        if action_type == "leave":
            return [
                {"name": "create_leave_request", "adapter": "hris", "action": "create_leave", "params": payload},
                {"name": "notify_manager", "adapter": "email", "action": "send_email", "params": {"to": payload.get("manager_email"), "subject": "Leave request", "body": "New leave request pending approval."}},
            ]
        # default
        return [
            {"name": "noop", "adapter": "email", "action": "send_email", "params": {"to": payload.get("employee_email"), "subject": "No-op", "body": "No plan defined."}} 
        ]
    else:
        # Minimal OpenAI call example (not robust) — left as an exercise to extend.
        # This stub intentionally avoids complex prompt engineering in the prototype.
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        prompt = f"Produce JSON array of steps for action {action_type} with payload {payload}"
        resp = requests.post("https://api.openai.com/v1/chat/completions",
                             headers=headers,
                             json={"model": "gpt-4o-mini", "messages": [{"role":"user", "content": prompt}], "max_tokens": 400})
        try:
            data = resp.json()
            text = data["choices"][0]["message"]["content"]
            # Expect the LLM to return JSON; parse safely
            import json
            return json.loads(text)
        except Exception:
            # fallback
            return plan_for_action(action_type, payload)
