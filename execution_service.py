import subprocess
import tempfile
import time
import os
from typing import Dict, Any

TIMEOUT_SECONDS = 5
MAX_MEMORY = "256m"
MAX_OUTPUT_BYTES = 1_000_000  # 1 MB


def execute_python_in_sandbox(code: str, stdin_data: str = "") -> Dict[str, Any]:
    """
    Executes student Python code inside an isolated ephemeral Docker container.

    Constraints:
      - Memory: 256MB
      - CPU: 1.0 core
      - PIDs: 64
      - Network: none
      - Timeout: 5 seconds
      - Filesystem: read-only mount at /workspace

    Returns:
      dict with keys: 'status', 'stdout', 'stderr', 'execution_time'
    """
    stdin_data = (stdin_data or "").replace("\r\n", "\n")
    code = (code or "").replace("\r\n", "\n")

    with tempfile.TemporaryDirectory() as tmpdir:
        code_path = os.path.join(tmpdir, "solution.py")
        with open(code_path, "w", encoding="utf-8") as f:
            f.write(code)

        docker_cmd = [
            "docker", "run", "--rm",
            "-i",
            "--network", "none",
            "--memory", MAX_MEMORY,
            "--cpus", "1.0",
            "--pids-limit", "64",
            "-v", f"{tmpdir}:/workspace:ro",
            "-w", "/workspace",
            "codeeval-python-runner",
            "python", "solution.py"
        ]

        start_time = time.time()
        try:
            process = subprocess.run(
                docker_cmd,
                input=stdin_data.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=TIMEOUT_SECONDS
            )
            elapsed_time = round(time.time() - start_time, 3)

            stdout = process.stdout[:MAX_OUTPUT_BYTES].decode("utf-8", errors="replace")
            stderr = process.stderr[:MAX_OUTPUT_BYTES].decode("utf-8", errors="replace")

            if process.returncode != 0:
                return {
                    "status": "Runtime Error",
                    "stdout": stdout,
                    "stderr": stderr,
                    "execution_time": elapsed_time
                }

            return {
                "status": "Success",
                "stdout": stdout,
                "stderr": stderr,
                "execution_time": elapsed_time
            }

        except subprocess.TimeoutExpired:
            return {
                "status": "Time Limit Exceeded",
                "stdout": "",
                "stderr": f"Execution timed out ({TIMEOUT_SECONDS}s limit)",
                "execution_time": float(TIMEOUT_SECONDS)
            }
        except Exception as e:
            return {
                "status": "Sandbox Failure",
                "stdout": "",
                "stderr": f"Execution engine error: {str(e)}",
                "execution_time": 0.0
            }