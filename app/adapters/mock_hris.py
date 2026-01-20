from typing import Dict
import logging

logger = logging.getLogger(__name__)

EMPLOYEES = {}

def create_employee(params: Dict):
    emp_id = str(uuid.uuid4())
    EMPLOYEES[emp_id] = {
        "id": emp_id,
        "name": params.get("name"),
        "email": params.get("email"),
        "role": params.get("role"),
        "salary": params.get("salary"),
        "hire_date": params.get("start_date")
    }
    logger.info(f"[HRIS] Created employee {emp_id}")
    return {"employee_id": emp_id}

def provision_accounts(params: Dict):
    # Simulate provisioning accounts (Okta, GSuite, etc.)
    logger.info(f"[HRIS] Provisioning accounts for {params.get('email')}"))
    return {"provisioned": True}

def update_salary(params: Dict):
    emp_id = params.get("employee_id")
    new_salary = params.get("new_salary")
    if emp_id in EMPLOYEES:
        EMPLOYEES[emp_id]["salary"] = new_salary
        logger.info(f"[HRIS] Updated salary for {emp_id} to {new_salary}")
        return {"ok": True}
    else:
        raise Exception("employee not found")

def create_leave(params: Dict):
    logger.info(f"[HRIS] Leave request created for {params.get('employee_id')}")
    return {"ok": True}
