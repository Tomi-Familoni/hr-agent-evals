from deepeval.test_case import LLMTestCase, ToolCall

from agent.agent import run_agent


def build_test_case(golden):
    """Run the agent on one golden and package the result for DeepEval."""
    result = run_agent(golden["input"], golden["requester_id"])

    tools_called = [
        ToolCall(name=call["name"], input_parameters=call["arguments"], output=call["output"])
        for call in result["tools_called"]
    ]
    expected_tools = [ToolCall(name=name) for name in golden["expected_tools"]]

    test_case = LLMTestCase(
        input=golden["input"],
        actual_output=result["answer"],
        expected_output=golden["expected_output"],
        tools_called=tools_called,
        expected_tools=expected_tools,
    )
    return test_case, result