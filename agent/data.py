# Fake data for the HR assistant. Nothing here is real.

EMPLOYEES = {
    "E001": {
        "name": "Ada Okafor",
        "country": "Germany",
        "role": "employee",
        "manager_id": "E003",
        "leave_balance_days": 12,
        "monthly_salary": 5200,
        "currency": "EUR",
    },
    "E002": {
        "name": "Bruno Silva",
        "country": "Portugal",
        "role": "employee",
        "manager_id": "E003",
        "leave_balance_days": 4,
        "monthly_salary": 3100,
        "currency": "EUR",
    },
    "E003": {
        "name": "Liam Chen",
        "country": "United Kingdom",
        "role": "manager",
        "manager_id": None,
        "leave_balance_days": 20,
        "monthly_salary": 7400,
        "currency": "GBP",
    },
}

PAYROLL_RUNS = {
    "2026-10": {"status": "paid", "pay_date": "2026-10-28"},
    "2026-11": {"status": "processing", "pay_date": "2026-11-27"},
}

# Illustrative values for the demo, not legal advice.
COUNTRY_POLICIES = {
    "Germany": {"statutory_annual_leave_days": 20, "standard_work_week_hours": 40},
    "Portugal": {"statutory_annual_leave_days": 22, "standard_work_week_hours": 40},
    "United Kingdom": {"statutory_annual_leave_days": 28, "standard_work_week_hours": 37.5},
}