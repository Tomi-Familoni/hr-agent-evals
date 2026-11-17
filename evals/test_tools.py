import pytest
from deepeval import assert_test
from deepeval.metrics import ToolCorrectnessMetric

from evals.goldens import GOLDENS
from evals.helpers import build_test_case


@pytest.mark.parametrize("golden", GOLDENS, ids=[g["id"] for g in GOLDENS])
def test_agent_calls_the_right_tool(golden):
    test_case, _ = build_test_case(golden)
    metric = ToolCorrectnessMetric(threshold=1.0)
    assert_test(test_case, [metric])