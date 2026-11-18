# hr-agent-evals

A small HR and payroll assistant agent, plus an evaluation suite that tests it with [DeepEval](https://deepeval.com).

The agent exists so there is something realistic to evaluate. The evals are the point: they check whether an AI agent calls the right tools, gives correct answers, and respects permissions, the same way a regression suite checks traditional software.

All data is made up. Nothing here comes from a real company.

## What the agent does

The agent answers employee questions using four tools:

| Tool | What it does |
|---|---|
| `get_leave_balance` | Returns an employee's remaining leave days |
| `get_salary` | Returns an employee's monthly salary |
| `get_country_policy` | Returns statutory leave and working hours for a country |
| `request_time_off` | Submits a time-off request, rejected if over balance |

Permissions are enforced **in code, not in the prompt**. Employees can see their own records, and managers can see their direct reports'. The logged-in user's ID is passed in by the agent loop and is never chosen by the model, so the model can't claim to be someone else.

## Project structure

```
hr-agent-evals/
├── agent/
│   ├── data.py        # fake employees, payroll runs and country policies
│   ├── tools.py       # the functions the agent may call, with permission checks
│   └── agent.py       # tool schemas, the tool-calling loop, and a terminal chat
├── evals/
│   ├── goldens.py         # test cases: who asks, what, expected tools, expected answer
│   ├── helpers.py         # runs the agent and builds a DeepEval test case
│   ├── test_tools.py      # deterministic: did the agent call the right tool?
│   └── test_outcomes.py   # LLM-judged: is the answer factually correct? (G-Eval)
└── requirements.txt
```

The `agent/` and `evals/` split is deliberate, so the evals can be pointed at a different agent.

## Setup

Requires Python 3.9+ and an OpenAI API key.

```bash
git clone https://github.com/Tomi-Familoni/hr-agent-evals.git
cd hr-agent-evals
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
echo "OPENAI_API_KEY=your-key-here" > .env
```

`.env` is git-ignored. Never commit your key.

## Running it

Chat with the agent (as employee E001):

```bash
python -m agent.agent
```

Run the evals:

```bash
python -m pytest evals/ -v --tb=line
```

Run every case three times to check consistency, since AI output varies between runs:

```bash
python -m pytest evals/ --tb=line --count=3
```

## What the evals check

| Layer | Metric | Uses an LLM judge? | Catches |
|---|---|---|---|
| Tool use | DeepEval `ToolCorrectnessMetric` | No: deterministic, free, never flaky | Wrong, missing or skipped tool calls |
| Answer | DeepEval `GEval` correctness rubric | Yes (`gpt-4o-mini`) | Wrong numbers, statuses or facts in the answer |

The layers catch different bugs. An agent can call the right tool and still report the wrong number, or give a plausible answer without ever calling the tool that enforces a business rule.

## What the evals found

- **Over-refusal:** a manager asking for a direct report's salary was refused. The model decided by itself that salaries were private, bypassing the permission check in code.
- **A business rule bypassed:** an over-balance leave request was refused in chat but never submitted, so the system's own rule never ran. The answer looked correct.
- **A prompt fix that didn't work:** repeated runs showed a system-prompt change fixed neither issue (0 of 6). Moving the rule into the tool descriptions did (6 of 6, full suite 15 of 15).
- **A judge that was too strict:** the LLM judge marked correct answers as wrong for using a first name instead of a full name. The rubric is test code, and it needed fixing too.

## Known issues

- `test_outcomes.py::manager_views_report_salary` still fails intermittently (scores about 0.65–0.69 against a 0.7 threshold). The judge treats the full name in the reference answer as required. Next step: simplify the reference answer in `goldens.py`.

## Roadmap

- Guardrail tests: cross-employee data access, unknown countries (no made-up answers), and attempts to impersonate a manager
- Tracing with `@observe` and DeepEval's Task Completion metric
- A second judge model from a different provider, to reduce self-preference bias
- Running the suite in GitHub Actions on every push
