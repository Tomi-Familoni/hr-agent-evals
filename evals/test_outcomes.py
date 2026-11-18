import pytest
from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.test_case import SingleTurnParams

from evals.goldens import GOLDENS
from evals.helpers import build_test_case

JUDGE_MODEL = "gpt-4o-mini"


def correctness_metric():
    return GEval(
        name="Correctness",
        evaluation_steps=[
            "Identify the key facts in 'expected output': amounts, currencies, day counts and statuses such as submitted or rejected.",
            "Check that each key fact appears in 'actual output' with the same value.",
            "A person may be referred to by first name, full name or 'you'; treat these as the same.",
            "Extra explanation, politeness or length must not lower the score.",
            "Any key fact that is missing or contradicted means the answer is incorrect.",

        ],
        evaluation_params=[SingleTurnParams.ACTUAL_OUTPUT, SingleTurnParams.EXPECTED_OUTPUT],
        threshold=0.7,
        model=JUDGE_MODEL,
    )


@pytest.mark.parametrize("golden", GOLDENS, ids=[g["id"] for g in GOLDENS])
def test_answer_is_correct(golden):
    test_case, _ = build_test_case(golden)
    assert_test(test_case, [correctness_metric()])