"""
Idempotent seeder for coding questions and test cases.
Run once after database tables are created:

    python seed_coding_questions.py
"""

from app import app
from models import db, CodingQuestion, TestCase, DEFAULT_STARTER_CODE

CODING_QUESTIONS = [
    {
        "title": "Reverse a String",
        "difficulty": "Easy",
        "description": (
            "Given a string S, return the string reversed.\n\n"
            "You may assume the string contains only lowercase English letters."
        ),
        "input_format": "A single line containing the string S.",
        "output_format": "Print the reversed string on one line.",
        "constraints": "1 <= len(S) <= 10^5",
        "sample_input": "hello",
        "sample_output": "olleh",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "marks": 100,
        "starter_code_python": "def reverse_string(s):\n    # return reversed string\n    pass\n\ns = input().strip()\nprint(reverse_string(s))",
        "test_cases": [
            {"input": "hello", "output": "olleh", "sample": True, "hidden": False},
            {"input": "a", "output": "a", "sample": False, "hidden": True},
            {"input": "racecar", "output": "racecar", "sample": False, "hidden": True},
        ],
    },
    {
        "title": "Find Maximum Element",
        "difficulty": "Easy",
        "description": "Given N integers, find and print the maximum value in the array.",
        "input_format": "First line: integer N. Second line: N space-separated integers.",
        "output_format": "Print the maximum element.",
        "constraints": "1 <= N <= 10^5, -10^9 <= each value <= 10^9",
        "sample_input": "5\n3 7 2 9 1",
        "sample_output": "9",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "marks": 100,
        "starter_code_python": "n = int(input())\narr = list(map(int, input().split()))\n# find and print maximum",
        "test_cases": [
            {"input": "5\n3 7 2 9 1", "output": "9", "sample": True, "hidden": False},
            {"input": "1\n42", "output": "42", "sample": False, "hidden": True},
            {"input": "4\n-5 -1 -10 -3", "output": "-1", "sample": False, "hidden": True},
        ],
    },
    {
        "title": "Check Palindrome",
        "difficulty": "Easy",
        "description": "Given a string, determine if it reads the same forwards and backwards. Print YES or NO.",
        "input_format": "A single line string S.",
        "output_format": "Print YES if palindrome, else NO.",
        "constraints": "1 <= len(S) <= 10^5",
        "sample_input": "madam",
        "sample_output": "YES",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "marks": 100,
        "starter_code_python": "s = input().strip()\n# print YES or NO",
        "test_cases": [
            {"input": "madam", "output": "YES", "sample": True, "hidden": False},
            {"input": "hello", "output": "NO", "sample": True, "hidden": False},
            {"input": "a", "output": "YES", "sample": False, "hidden": True},
        ],
    },
    {
        "title": "Count Vowels",
        "difficulty": "Easy",
        "description": "Count the number of vowels (a, e, i, o, u) in the given string. Case insensitive.",
        "input_format": "A single line string.",
        "output_format": "Print the vowel count.",
        "constraints": "1 <= len(S) <= 10^5",
        "sample_input": "Education",
        "sample_output": "5",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "marks": 100,
        "starter_code_python": "s = input().strip()\n# count vowels and print",
        "test_cases": [
            {"input": "Education", "output": "5", "sample": True, "hidden": False},
            {"input": "xyz", "output": "0", "sample": False, "hidden": True},
            {"input": "AEIOUaeiou", "output": "10", "sample": False, "hidden": True},
        ],
    },
    {
        "title": "Two Sum",
        "difficulty": "Easy",
        "description": (
            "Given an array of N integers and a target T, return the 0-based indices "
            "of two distinct elements that sum to T. Assume exactly one solution exists."
        ),
        "input_format": "Line 1: N and T. Line 2: N integers.",
        "output_format": "Two space-separated indices in ascending order.",
        "constraints": "2 <= N <= 10^4, -10^9 <= values, T <= 10^9",
        "sample_input": "4 9\n2 7 11 15",
        "sample_output": "0 1",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "marks": 100,
        "starter_code_python": "n, t = map(int, input().split())\narr = list(map(int, input().split()))\n# print two indices",
        "test_cases": [
            {"input": "4 9\n2 7 11 15", "output": "0 1", "sample": True, "hidden": False},
            {"input": "3 6\n3 2 4", "output": "1 2", "sample": False, "hidden": True},
            {"input": "2 7\n3 4", "output": "0 1", "sample": False, "hidden": True},
        ],
    },
    {
        "title": "Remove Duplicates",
        "difficulty": "Easy",
        "description": "Given a sorted array, print the array with duplicates removed, preserving order.",
        "input_format": "Line 1: N. Line 2: N sorted integers.",
        "output_format": "Space-separated unique elements.",
        "constraints": "1 <= N <= 10^5",
        "sample_input": "6\n1 1 2 2 3 4",
        "sample_output": "1 2 3 4",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "marks": 100,
        "starter_code_python": "n = int(input())\narr = list(map(int, input().split()))\n# print unique elements",
        "test_cases": [
            {"input": "6\n1 1 2 2 3 4", "output": "1 2 3 4", "sample": True, "hidden": False},
            {"input": "1\n5", "output": "5", "sample": False, "hidden": True},
            {"input": "3\n2 2 2", "output": "2", "sample": False, "hidden": True},
        ],
    },
    {
        "title": "Find Missing Number",
        "difficulty": "Easy",
        "description": "An array contains N distinct numbers from 0 to N. Find the missing number.",
        "input_format": "Line 1: N. Line 2: N integers (one missing from 0..N).",
        "output_format": "Print the missing number.",
        "constraints": "1 <= N <= 10^5",
        "sample_input": "3\n3 0 1",
        "sample_output": "2",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "marks": 100,
        "starter_code_python": "n = int(input())\narr = list(map(int, input().split()))\n# print missing number",
        "test_cases": [
            {"input": "3\n3 0 1", "output": "2", "sample": True, "hidden": False},
            {"input": "1\n1", "output": "0", "sample": False, "hidden": True},
            {"input": "5\n0 1 2 4 5", "output": "3", "sample": False, "hidden": True},
        ],
    },
    {
        "title": "Valid Parentheses",
        "difficulty": "Medium",
        "description": "Given a string of brackets ()[]{}, determine if it is valid. Print YES or NO.",
        "input_format": "A single line string.",
        "output_format": "YES or NO.",
        "constraints": "1 <= len(S) <= 10^4",
        "sample_input": "()[]{}",
        "sample_output": "YES",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "marks": 100,
        "starter_code_python": "s = input().strip()\n# print YES or NO",
        "test_cases": [
            {"input": "()[]{}", "output": "YES", "sample": True, "hidden": False},
            {"input": "(]", "output": "NO", "sample": True, "hidden": False},
            {"input": "([{}])", "output": "YES", "sample": False, "hidden": True},
        ],
    },
    {
        "title": "Binary Search",
        "difficulty": "Medium",
        "description": "Given a sorted array and target X, return the 0-based index of X or -1 if absent.",
        "input_format": "Line 1: N and X. Line 2: N sorted integers.",
        "output_format": "Print index or -1.",
        "constraints": "1 <= N <= 10^5",
        "sample_input": "5 3\n1 2 3 4 5",
        "sample_output": "2",
        "expected_time_complexity": "O(log n)",
        "expected_space_complexity": "O(1)",
        "marks": 100,
        "starter_code_python": "n, x = map(int, input().split())\narr = list(map(int, input().split()))\n# binary search",
        "test_cases": [
            {"input": "5 3\n1 2 3 4 5", "output": "2", "sample": True, "hidden": False},
            {"input": "4 7\n1 3 5 9", "output": "-1", "sample": False, "hidden": True},
            {"input": "1 10\n10", "output": "0", "sample": False, "hidden": True},
        ],
    },
    {
        "title": "Merge Two Sorted Arrays",
        "difficulty": "Medium",
        "description": "Merge two sorted arrays into one sorted array.",
        "input_format": "Line 1: N M. Line 2: N ints. Line 3: M ints.",
        "output_format": "Merged sorted array, space-separated.",
        "constraints": "0 <= N,M <= 10^5",
        "sample_input": "3 2\n1 3 5\n2 4",
        "sample_output": "1 2 3 4 5",
        "expected_time_complexity": "O(n + m)",
        "expected_space_complexity": "O(n + m)",
        "marks": 100,
        "starter_code_python": "n, m = map(int, input().split())\na = list(map(int, input().split())) if n else []\nb = list(map(int, input().split())) if m else []\n# merge and print",
        "test_cases": [
            {"input": "3 2\n1 3 5\n2 4", "output": "1 2 3 4 5", "sample": True, "hidden": False},
            {"input": "0 3\n\n1 2 3", "output": "1 2 3", "sample": False, "hidden": True},
            {"input": "2 0\n5 6\n", "output": "5 6", "sample": False, "hidden": True},
        ],
    },
    {
        "title": "Longest Substring Without Repeating Characters",
        "difficulty": "Medium",
        "description": "Find the length of the longest substring without repeating characters.",
        "input_format": "A single line string.",
        "output_format": "Print the length.",
        "constraints": "1 <= len(S) <= 10^5",
        "sample_input": "abcabcbb",
        "sample_output": "3",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "marks": 100,
        "starter_code_python": "s = input().strip()\n# print longest unique substring length",
        "test_cases": [
            {"input": "abcabcbb", "output": "3", "sample": True, "hidden": False},
            {"input": "bbbbb", "output": "1", "sample": True, "hidden": False},
            {"input": "pwwkew", "output": "3", "sample": False, "hidden": True},
        ],
    },
    {
        "title": "Maximum Subarray",
        "difficulty": "Medium",
        "description": "Find the maximum sum of any contiguous subarray (Kadane's algorithm).",
        "input_format": "Line 1: N. Line 2: N integers.",
        "output_format": "Print maximum subarray sum.",
        "constraints": "1 <= N <= 10^5",
        "sample_input": "5\n-2 1 -3 4 -1",
        "sample_output": "4",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "marks": 100,
        "starter_code_python": "n = int(input())\narr = list(map(int, input().split()))\n# kadane's algorithm",
        "test_cases": [
            {"input": "5\n-2 1 -3 4 -1", "output": "4", "sample": True, "hidden": False},
            {"input": "1\n5", "output": "5", "sample": False, "hidden": True},
            {"input": "3\n-1 -2 -3", "output": "-1", "sample": False, "hidden": True},
        ],
    },
    {
        "title": "Rotate Array",
        "difficulty": "Medium",
        "description": "Rotate array to the right by K steps. Print the result.",
        "input_format": "Line 1: N K. Line 2: N integers.",
        "output_format": "Rotated array, space-separated.",
        "constraints": "1 <= N <= 10^5, 0 <= K <= 10^5",
        "sample_input": "5 2\n1 2 3 4 5",
        "sample_output": "4 5 1 2 3",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(n)",
        "marks": 100,
        "starter_code_python": "n, k = map(int, input().split())\narr = list(map(int, input().split()))\n# rotate and print",
        "test_cases": [
            {"input": "5 2\n1 2 3 4 5", "output": "4 5 1 2 3", "sample": True, "hidden": False},
            {"input": "3 0\n1 2 3", "output": "1 2 3", "sample": False, "hidden": True},
            {"input": "4 4\n1 2 3 4", "output": "1 2 3 4", "sample": False, "hidden": True},
        ],
    },
    {
        "title": "First Non-Repeating Character",
        "difficulty": "Medium",
        "description": "Return the first character that does not repeat in the string. Print NONE if all repeat.",
        "input_format": "A single line lowercase string.",
        "output_format": "Single character or NONE.",
        "constraints": "1 <= len(S) <= 10^5",
        "sample_input": "leetcode",
        "sample_output": "l",
        "expected_time_complexity": "O(n)",
        "expected_space_complexity": "O(1)",
        "marks": 100,
        "starter_code_python": "s = input().strip()\n# print first non-repeating char",
        "test_cases": [
            {"input": "leetcode", "output": "l", "sample": True, "hidden": False},
            {"input": "aabb", "output": "NONE", "sample": True, "hidden": False},
            {"input": "z", "output": "z", "sample": False, "hidden": True},
        ],
    },
    {
        "title": "Longest Increasing Subsequence",
        "difficulty": "Hard",
        "description": "Find the length of the longest strictly increasing subsequence.",
        "input_format": "Line 1: N. Line 2: N integers.",
        "output_format": "Print LIS length.",
        "constraints": "1 <= N <= 2500",
        "sample_input": "6\n10 9 2 5 3 7",
        "sample_output": "3",
        "expected_time_complexity": "O(n log n)",
        "expected_space_complexity": "O(n)",
        "marks": 100,
        "starter_code_python": "n = int(input())\narr = list(map(int, input().split()))\n# compute LIS length",
        "test_cases": [
            {"input": "6\n10 9 2 5 3 7", "output": "3", "sample": True, "hidden": False},
            {"input": "1\n5", "output": "1", "sample": False, "hidden": True},
            {"input": "5\n5 4 3 2 1", "output": "1", "sample": False, "hidden": True},
        ],
    },
    {
        "title": "Number of Islands",
        "difficulty": "Hard",
        "description": (
            "Given an R x C grid of 0 (water) and 1 (land), count the number of islands. "
            "An island is surrounded by water and formed by connecting adjacent lands horizontally or vertically."
        ),
        "input_format": "Line 1: R C. Next R lines: C space-separated 0/1 values.",
        "output_format": "Print island count.",
        "constraints": "1 <= R,C <= 300",
        "sample_input": "3 3\n1 1 0\n1 0 0\n0 0 1",
        "sample_output": "2",
        "expected_time_complexity": "O(R * C)",
        "expected_space_complexity": "O(R * C)",
        "marks": 100,
        "starter_code_python": "r, c = map(int, input().split())\ngrid = [list(map(int, input().split())) for _ in range(r)]\n# count islands",
        "test_cases": [
            {"input": "3 3\n1 1 0\n1 0 0\n0 0 1", "output": "2", "sample": True, "hidden": False},
            {"input": "1 1\n0", "output": "0", "sample": False, "hidden": True},
            {"input": "2 2\n1 1\n1 1", "output": "1", "sample": False, "hidden": True},
        ],
    },
    {
        "title": "LRU Cache Simulation",
        "difficulty": "Hard",
        "description": (
            "Simulate an LRU cache of capacity K. Process operations: PUT key value or GET key. "
            "For GET, print the value or -1 if missing. PUT updates/inserts."
        ),
        "input_format": "Line 1: capacity K and Q queries. Next Q lines: PUT key val or GET key.",
        "output_format": "Print GET results only, one per line.",
        "constraints": "1 <= K <= 100, 1 <= Q <= 1000",
        "sample_input": "2 4\nPUT 1 10\nPUT 2 20\nGET 1\nGET 3",
        "sample_output": "10\n-1",
        "expected_time_complexity": "O(1) per operation",
        "expected_space_complexity": "O(K)",
        "marks": 100,
        "starter_code_python": "k, q = map(int, input().split())\n# process queries",
        "test_cases": [
            {"input": "2 4\nPUT 1 10\nPUT 2 20\nGET 1\nGET 3", "output": "10\n-1", "sample": True, "hidden": False},
            {"input": "1 3\nPUT 1 5\nPUT 2 6\nGET 2", "output": "6", "sample": False, "hidden": True},
        ],
    },
    {
        "title": "Merge Intervals",
        "difficulty": "Hard",
        "description": "Given N intervals [start, end], merge all overlapping intervals and print the result.",
        "input_format": "Line 1: N. Next N lines: start end.",
        "output_format": "Merged intervals, one per line as start end.",
        "constraints": "1 <= N <= 10^4",
        "sample_input": "3\n1 3\n2 6\n8 10",
        "sample_output": "1 6\n8 10",
        "expected_time_complexity": "O(n log n)",
        "expected_space_complexity": "O(n)",
        "marks": 100,
        "starter_code_python": "n = int(input())\nintervals = [tuple(map(int, input().split())) for _ in range(n)]\n# merge and print",
        "test_cases": [
            {"input": "3\n1 3\n2 6\n8 10", "output": "1 6\n8 10", "sample": True, "hidden": False},
            {"input": "1\n1 1", "output": "1 1", "sample": False, "hidden": True},
            {"input": "2\n1 4\n4 5", "output": "1 5", "sample": False, "hidden": True},
        ],
    },
    {
        "title": "Top K Frequent Elements",
        "difficulty": "Hard",
        "description": "Given an array and integer K, return the K most frequent elements in any order.",
        "input_format": "Line 1: N K. Line 2: N integers.",
        "output_format": "K space-separated integers.",
        "constraints": "1 <= K <= N <= 10^5",
        "sample_input": "6 2\n1 1 1 2 2 3",
        "sample_output": "1 2",
        "expected_time_complexity": "O(n log n)",
        "expected_space_complexity": "O(n)",
        "marks": 100,
        "starter_code_python": "n, k = map(int, input().split())\narr = list(map(int, input().split()))\n# print top k frequent",
        "test_cases": [
            {"input": "6 2\n1 1 1 2 2 3", "output": "1 2", "sample": True, "hidden": False},
            {"input": "3 1\n5 5 5", "output": "5", "sample": False, "hidden": True},
        ],
    },
    {
        "title": "Sum of Digits",
        "difficulty": "Easy",
        "description": "Given a non-negative integer N, compute the sum of its digits.",
        "input_format": "Single integer N.",
        "output_format": "Print digit sum.",
        "constraints": "0 <= N <= 10^18",
        "sample_input": "12345",
        "sample_output": "15",
        "expected_time_complexity": "O(log n)",
        "expected_space_complexity": "O(1)",
        "marks": 100,
        "starter_code_python": "n = input().strip()\n# print sum of digits",
        "test_cases": [
            {"input": "12345", "output": "15", "sample": True, "hidden": False},
            {"input": "0", "output": "0", "sample": False, "hidden": True},
            {"input": "999", "output": "27", "sample": False, "hidden": True},
        ],
    },
]


def seed():
    with app.app_context():
        existing = CodingQuestion.query.count()
        if existing >= 20:
            print(f"Skipping seed: {existing} coding questions already exist.")
            return

        added = 0
        for qdata in CODING_QUESTIONS:
            if CodingQuestion.query.filter_by(title=qdata["title"]).first():
                continue

            q = CodingQuestion(
                title=qdata["title"],
                description=qdata["description"],
                difficulty=qdata["difficulty"],
                input_format=qdata["input_format"],
                output_format=qdata["output_format"],
                constraints=qdata["constraints"],
                sample_input=qdata["sample_input"],
                sample_output=qdata["sample_output"],
                expected_time_complexity=qdata["expected_time_complexity"],
                expected_space_complexity=qdata["expected_space_complexity"],
                marks=qdata["marks"],
                starter_code_python=qdata.get("starter_code_python", DEFAULT_STARTER_CODE["python"]),
                starter_code_java=DEFAULT_STARTER_CODE["java"],
                starter_code_javascript=DEFAULT_STARTER_CODE["javascript"],
                starter_code_cpp=DEFAULT_STARTER_CODE["cpp"],
                starter_code_c=DEFAULT_STARTER_CODE["c"],
            )
            db.session.add(q)
            db.session.flush()

            for tc in qdata["test_cases"]:
                db.session.add(TestCase(
                    question_id=q.id,
                    input_data=tc["input"],
                    expected_output=tc["output"],
                    is_sample=tc.get("sample", False),
                    is_hidden=tc.get("hidden", True),
                ))

            added += 1

        db.session.commit()
        total = CodingQuestion.query.count()
        print(f"Seeded {added} new coding questions. Total: {total}.")


if __name__ == "__main__":
    seed()
