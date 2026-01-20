#!/bin/bash
BASE="http://localhost:8000"

# Onboard request (will be low risk)
curl -s -X POST "$BASE/requests/" -H "Content-Type: application/json" -d '{
  "action_type": "onboard",
  "actor": "recruiter_1",
  "name": "Alice Example",
  "email": "alice@example.com",
  "role": "engineer",
  "start_date": "2026-02-01",
  "new_salary": 80000
}' | jq

# High salary change (requires approval)
curl -s -X POST "$BASE/requests/" -H "Content-Type: application/json" -d '{
  "action_type": "salary_change",
  "actor": "hr_1",
  "employee_id": "emp-123",
  "old_salary": 60000,
  "new_salary": 90000,
  "employee_email": "bob@example.com"
}' | jq

# Attendance correction small (auto)
curl -s -X POST "$BASE/requests/" -H "Content-Type: application/json" -d '{
  "action_type": "attendance_correction",
  "actor": "employee_1",
  "employee_id": "emp-45",
  "hours": 1.5,
  "manager_email": "mgr@example.com"
}' | jq
