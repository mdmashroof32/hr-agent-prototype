from typing import Dict
from app.adapters import mock_hris, mock_attendance, emailer
from app.adapters import slack_notifier

ADAPTERS = {
    "hris": mock_hris,
    "attendance": mock_attendance,
    "email": emailer
}

def execute_plan(steps):
    results = []
    for step in steps:
        adapter_name = step.get("adapter")
        action = step.get("action")
        params = step.get("params", {})
        adapter = ADAPTERS.get(adapter_name)
        if not adapter:
            results.append({"step": step.get("name"), "status": "failed", "reason": "unknown adapter"})
            continue
        fn = getattr(adapter, action, None)
        if not fn:
            results.append({"step": step.get("name"), "status": "failed", "reason": "unknown action"})
            continue
        try:
            res = fn(params)
            results.append({"step": step.get("name"), "status": "ok", "result": res})
        except Exception as e:
            # Notify via Slack in case of failure (best-effort)
            slack_notifier.notify(f"Executor error on step {step.get('name')}: {e}")
            results.append({"step": step.get("name"), "status": "failed", "reason": str(e)})
    return results
