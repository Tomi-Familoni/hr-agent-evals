import json

from dotenv import load_dotenv
from openai import OpenAI

from agent import tools
from agent.data import EMPLOYEES

load_dotenv()
client = OpenAI()

MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """You are an HR and payroll assistant.
Always use the tools to answer. The tools enforce permissions and business rules,
so never refuse or decide on your own: call the relevant tool and report what it returns.
Answer using only the results of the tools.
If a tool returns an error, explain it to the user and do not guess.
If no tool can answer the question, say you don't have that information."""

# --- Part 1: describe the tools to the model ---

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_leave_balance",
            "description": "Get the remaining leave days for an employee.",
            "parameters": {
                "type": "object",
                "properties": {"employee_name": {"type": "string"}},
                "required": ["employee_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_salary",
            "description": "Get the monthly salary of an employee. This tool checks permissions itself, so always call it for salary questions, including about other employees, and report what it returns.",
            "parameters": {
                "type": "object",
                "properties": {"employee_name": {"type": "string"}},
                "required": ["employee_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_country_policy",
            "description": "Get statutory leave and working hours for a country.",
            "parameters": {
                "type": "object",
                "properties": {"country": {"type": "string"}},
                "required": ["country"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "request_time_off",
            "description": "Submit a time-off request for the current user. This tool checks the leave balance itself and returns submitted or rejected, so call it directly without checking the balance first.",
            "parameters": {
                "type": "object",
                "properties": {"days": {"type": "integer"}},
                "required": ["days"],
            },
        },
    },
]

# --- Part 2: run a tool the model asked for ---

TOOL_FUNCTIONS = {
    "get_leave_balance": tools.get_leave_balance,
    "get_salary": tools.get_salary,
    "get_country_policy": tools.get_country_policy,
    "request_time_off": tools.request_time_off,
}

NEEDS_REQUESTER = {"get_leave_balance", "get_salary", "request_time_off"}


def run_tool(name, arguments, requester_id):
    function = TOOL_FUNCTIONS[name]
    if name in NEEDS_REQUESTER:
        return function(requester_id, **arguments)
    return function(**arguments)


# --- Part 3: the agent loop ---

def run_agent(user_message, requester_id):
    user_name = EMPLOYEES[requester_id]["name"]
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT + f"\nThe current user is {user_name}."},
        {"role": "user", "content": user_message},
    ]
    tools_called = []

    for _ in range(5):
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOL_SCHEMAS
        )
        message = response.choices[0].message

        if not message.tool_calls:
            return {"answer": message.content, "tools_called": tools_called}

        messages.append(message)
        for call in message.tool_calls:
            arguments = json.loads(call.function.arguments)
            output = run_tool(call.function.name, arguments, requester_id)
            tools_called.append(
                {"name": call.function.name, "arguments": arguments, "output": output}
            )
            messages.append(
                {"role": "tool", "tool_call_id": call.id, "content": json.dumps(output)}
            )

    return {"answer": "Sorry, I could not complete that request.", "tools_called": tools_called}


# --- Part 4: chat with it in the terminal ---

if __name__ == "__main__":
    requester_id = "E001"
    print("Chatting as Ada (E001). Type 'quit' to stop.")
    while True:
        question = input("> ")
        if question == "quit":
            break
        result = run_agent(question, requester_id)
        for call in result["tools_called"]:
            print(f"  [tool] {call['name']}({call['arguments']}) -> {call['output']}")
        print(result["answer"])