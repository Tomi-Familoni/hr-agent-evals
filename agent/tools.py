from agent.data import EMPLOYEES, COUNTRY_POLICIES


def find_employee_id(name):
    """Return the ID of the employee matching this name, or None."""
    for employee_id, employee in EMPLOYEES.items():
        if name.lower() in employee["name"].lower():
            return employee_id
    return None


def can_view(requester_id, employee_id):
    """You can see your own record. A manager can see their direct reports."""
    if requester_id == employee_id:
        return True
    return EMPLOYEES[employee_id]["manager_id"] == requester_id


def get_leave_balance(requester_id, employee_name):
    employee_id = find_employee_id(employee_name)
    if employee_id is None:
        return {"error": f"No employee named {employee_name}."}
    if not can_view(requester_id, employee_id):
        return {"error": "Permission denied: you cannot view this employee's records."}
    employee = EMPLOYEES[employee_id]
    return {"name": employee["name"], "leave_balance_days": employee["leave_balance_days"]}


def get_salary(requester_id, employee_name):
    employee_id = find_employee_id(employee_name)
    if employee_id is None:
        return {"error": f"No employee named {employee_name}."}
    if not can_view(requester_id, employee_id):
        return {"error": "Permission denied: you cannot view this employee's records."}
    employee = EMPLOYEES[employee_id]
    return {
        "name": employee["name"],
        "monthly_salary": employee["monthly_salary"],
        "currency": employee["currency"],
    }


def get_country_policy(country):
    if country not in COUNTRY_POLICIES:
        return {"error": f"No policy data for {country}."}
    return COUNTRY_POLICIES[country]


def request_time_off(requester_id, days):
    if days <= 0:
        return {"error": "Days must be greater than zero."}
    balance = EMPLOYEES[requester_id]["leave_balance_days"]
    if days > balance:
        return {"status": "rejected", "reason": f"Requested {days} days but only {balance} available."}
    return {"status": "submitted", "days": days}