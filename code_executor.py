"""
Secure code execution interface.

This module coordinates running student code against test cases using
the isolated Docker sandbox backend.
"""

from dataclasses import dataclass, asdict
from typing import List, Optional
from execution_service import execute_python_in_sandbox


EXECUTION_AVAILABLE = True


@dataclass
class TestCaseResult:
    test_case_id: int
    is_sample: bool
    input_data: str
    expected_output: str
    actual_output: Optional[str] = None
    passed: Optional[bool] = None
    error: Optional[str] = None
    status: str = "not_executed"
    execution_time: float = 0.0


@dataclass
class ExecutionResult:
    execution_available: bool
    status: str
    passed: int
    total: int
    test_results: List[TestCaseResult]
    message: str
    score: float = 0.0
    max_score: float = 0.0

    def to_dict(self):
        return {
            "execution_available": self.execution_available,
            "status": self.status,
            "passed": self.passed,
            "total": self.total,
            "score": self.score,
            "max_score": self.max_score,
            "message": self.message,
            "test_results": [asdict(r) for r in self.test_results],
        }


def run_against_test_cases(
    code: str,
    language: str,
    test_cases,
    max_score: int,
    hide_hidden_details: bool = False
) -> ExecutionResult:
    """
    Run student code against the provided test cases using the secure sandbox.
    """
    lang = (language or '').strip().lower()
    total_count = len(test_cases)

    if lang != 'python':
        results = [
            TestCaseResult(
                test_case_id=tc.id,
                is_sample=tc.is_sample,
                input_data=tc.input_data if (tc.is_sample or not hide_hidden_details) else "[Hidden]",
                expected_output=tc.expected_output if (tc.is_sample or not hide_hidden_details) else "[Hidden]",
                actual_output=None,
                passed=False,
                error=f"{lang.capitalize()} execution is not yet supported in the sandbox. Please select Python.",
                status="unsupported_language",
            )
            for tc in test_cases
        ]
        return ExecutionResult(
            execution_available=False,
            status="Unsupported Language",
            passed=0,
            total=total_count,
            test_results=results,
            message=f"{lang.capitalize()} execution is not yet configured in this sandbox.",
            score=0.0,
            max_score=float(max_score),
        )

    results = []
    passed_count = 0
    first_failure_status = None

    for tc in test_cases:
        res = execute_python_in_sandbox(code, tc.input_data)
        actual_output = res.get('stdout', '').strip()
        expected_output = (tc.expected_output or '').strip()
        exec_status = res.get('status', 'Runtime Error')
        passed = (exec_status == 'Success' and actual_output == expected_output)

        if passed:
            passed_count += 1
        elif first_failure_status is None:
            if exec_status in ('Time Limit Exceeded', 'Runtime Error', 'Sandbox Failure'):
                first_failure_status = exec_status if exec_status != 'Sandbox Failure' else 'Runtime Error'
            else:
                first_failure_status = 'Wrong Answer'

        is_sample = bool(tc.is_sample)
        should_hide = hide_hidden_details and not is_sample

        results.append(
            TestCaseResult(
                test_case_id=tc.id,
                is_sample=is_sample,
                input_data="[Hidden]" if should_hide else tc.input_data,
                expected_output="[Hidden]" if should_hide else expected_output,
                actual_output=None if should_hide else (actual_output if exec_status == 'Success' else None),
                passed=passed,
                error=None if should_hide else (res.get('stderr', '') if exec_status != 'Success' else None),
                status=exec_status if (is_sample or not hide_hidden_details) else ('passed' if passed else 'failed'),
                execution_time=res.get('execution_time', 0.0),
            )
        )

    if total_count == 0:
        overall_status = "Accepted"
        score = float(max_score)
        message = "No test cases configured."
    elif passed_count == total_count:
        overall_status = "Accepted"
        score = float(max_score)
        message = "All test cases passed!"
    else:
        overall_status = first_failure_status or "Wrong Answer"
        score = round((passed_count / total_count) * max_score, 2)
        message = f"{passed_count} of {total_count} test cases passed."

    return ExecutionResult(
        execution_available=True,
        status=overall_status,
        passed=passed_count,
        total=total_count,
        test_results=results,
        message=message,
        score=score,
        max_score=float(max_score),
    )
