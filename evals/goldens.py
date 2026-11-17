# Each golden is one test case: who is asking, what they ask,
# which tools should be used, and what a correct answer says.

GOLDENS = [
    {
        "id": "own_leave_balance",
        "requester_id": "E001",
        "input": "How many leave days do I have left?",
        "expected_tools": ["get_leave_balance"],
        "expected_output": "Ada has 12 days of leave remaining.",
    },
    {
        "id": "country_policy",
        "requester_id": "E001",
        "input": "What is the statutory annual leave in Portugal?",
        "expected_tools": ["get_country_policy"],
        "expected_output": "Statutory annual leave in Portugal is 22 days.",
    },
    {
        "id": "manager_views_report_salary",
        "requester_id": "E003",
        "input": "What is Bruno's monthly salary?",
        "expected_tools": ["get_salary"],
        "expected_output": "Bruno Silva's monthly salary is 3100 EUR.",
    },
    {
        "id": "time_off_within_balance",
        "requester_id": "E002",
        "input": "Please book 3 days off for me.",
        "expected_tools": ["request_time_off"],
        "expected_output": "The request for 3 days off has been submitted.",
    },
    {
        "id": "time_off_over_balance",
        "requester_id": "E002",
        "input": "Book me 10 days off.",
        "expected_tools": ["request_time_off"],
        "expected_output": "The request was rejected because only 4 days are available.",
    },
]