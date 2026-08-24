"""
Secure code execution interface.

This module defines the contract for running student code against test cases.
Actual execution MUST happen in an isolated sandbox/container — never in the
Flask web process. The MVP returns structured results without executing code.
"""

from dataclasses import dataclass, asdict
from typing import List, Optional


EXECUTION_AVAILABLE = False


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


def run_against_test_cases(code: str, language: str, test_cases, max_score: int) -> ExecutionResult:
    """
    Run student code against the provided test cases.

    When EXECUTION_AVAILABLE is False, returns infrastructure-ready results
    without executing untrusted code. Plug in a sandbox-backed implementation
    here when a secure execution service is deployed.
    """
    results = []
    for tc in test_cases:
        results.append(
            TestCaseResult(
                test_case_id=tc.id,
                is_sample=tc.is_sample,
                input_data=tc.input_data,
                expected_output=tc.expected_output,
                actual_output=None,
                passed=None,
                error=None,
                status="not_executed",
            )
        )

    if not EXECUTION_AVAILABLE:
        return ExecutionResult(
            execution_available=False,
            status="Execution Unavailable",
            passed=0,
            total=len(test_cases),
            test_results=results,
            message=(
                "Secure code execution is not configured. "
                "Test case infrastructure is ready — connect a sandboxed execution "
                "service to enable Run Code and automatic grading."
            ),
            score=0.0,
            max_score=float(max_score),
        )

    # Placeholder for future sandbox integration.
    raise NotImplementedError("Sandbox execution service is not yet implemented.")
