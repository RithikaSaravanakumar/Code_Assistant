"""
seed_questions.py
-----------------
Seeds 50 placement-level technical MCQ questions into the database.

SAFE TO RUN MULTIPLE TIMES:
  - Checks existing MCQ count before inserting.
  - Skips any question whose text already exists in the DB.

Usage:
  python seed_questions.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, Question

# ---------------------------------------------------------------------------
# 50 Technical MCQ Questions
# Topics: Python(5), Java(5), JavaScript(5), SQL(5), DSA(5),
#         OOP(5), DBMS(4), OS(4), Computer Networks(4), HTML/CSS(4), SE(4)
# ---------------------------------------------------------------------------
QUESTIONS = [
    # ── Python (5) ──────────────────────────────────────────────────────────
    {
        "question_text": "What is the output of `type([])` in Python?",
        "option_a": "<class 'tuple'>",
        "option_b": "<class 'list'>",
        "option_c": "<class 'array'>",
        "option_d": "<class 'dict'>",
        "correct_answer": "B",
        "marks": 1,
    },
    {
        "question_text": "Which keyword is used to define a generator function in Python?",
        "option_a": "return",
        "option_b": "lambda",
        "option_c": "yield",
        "option_d": "def",
        "correct_answer": "C",
        "marks": 1,
    },
    {
        "question_text": "What does the `__init__` method in a Python class do?",
        "option_a": "Destroys an object when it is no longer needed",
        "option_b": "Imports external modules into the class",
        "option_c": "Initialises object attributes when an instance is created",
        "option_d": "Defines static methods for the class",
        "correct_answer": "C",
        "marks": 1,
    },
    {
        "question_text": "Which built-in Python function returns the number of items in a list?",
        "option_a": "size()",
        "option_b": "count()",
        "option_c": "length()",
        "option_d": "len()",
        "correct_answer": "D",
        "marks": 1,
    },
    {
        "question_text": "In Python, which of the following is an immutable data type?",
        "option_a": "list",
        "option_b": "dict",
        "option_c": "tuple",
        "option_d": "set",
        "correct_answer": "C",
        "marks": 1,
    },

    # ── Java (5) ─────────────────────────────────────────────────────────────
    {
        "question_text": "Which of the following is NOT a Java primitive data type?",
        "option_a": "int",
        "option_b": "boolean",
        "option_c": "String",
        "option_d": "char",
        "correct_answer": "C",
        "marks": 1,
    },
    {
        "question_text": "What is the default value of an `int` variable declared as a class field in Java?",
        "option_a": "null",
        "option_b": "undefined",
        "option_c": "-1",
        "option_d": "0",
        "correct_answer": "D",
        "marks": 1,
    },
    {
        "question_text": "Which Java keyword is used to inherit from a parent class?",
        "option_a": "implements",
        "option_b": "super",
        "option_c": "inherits",
        "option_d": "extends",
        "correct_answer": "D",
        "marks": 1,
    },
    {
        "question_text": "What is the purpose of the `final` keyword when applied to a variable in Java?",
        "option_a": "The variable is automatically deleted after the method ends",
        "option_b": "The variable's value cannot be changed once assigned",
        "option_c": "The variable is shared across all instances",
        "option_d": "The variable is visible only within its package",
        "correct_answer": "B",
        "marks": 1,
    },
    {
        "question_text": "Which Java collection does NOT allow duplicate elements?",
        "option_a": "ArrayList",
        "option_b": "LinkedList",
        "option_c": "Vector",
        "option_d": "HashSet",
        "correct_answer": "D",
        "marks": 1,
    },

    # ── JavaScript (5) ───────────────────────────────────────────────────────
    {
        "question_text": "What is the output of `typeof null` in JavaScript?",
        "option_a": "\"null\"",
        "option_b": "\"undefined\"",
        "option_c": "\"object\"",
        "option_d": "\"string\"",
        "correct_answer": "C",
        "marks": 1,
    },
    {
        "question_text": "Which method adds an element to the end of a JavaScript array?",
        "option_a": "append()",
        "option_b": "add()",
        "option_c": "insert()",
        "option_d": "push()",
        "correct_answer": "D",
        "marks": 1,
    },
    {
        "question_text": "What does the `===` operator check in JavaScript?",
        "option_a": "Value only (loose equality)",
        "option_b": "Value and data type (strict equality)",
        "option_c": "Reference equality for objects",
        "option_d": "Assignment of a value",
        "correct_answer": "B",
        "marks": 1,
    },
    {
        "question_text": "Which keyword declares a block-scoped variable in JavaScript (ES6+)?",
        "option_a": "var",
        "option_b": "static",
        "option_c": "let",
        "option_d": "def",
        "correct_answer": "C",
        "marks": 1,
    },
    {
        "question_text": "What will `console.log(0.1 + 0.2 === 0.3)` output in JavaScript?",
        "option_a": "true",
        "option_b": "undefined",
        "option_c": "NaN",
        "option_d": "false",
        "correct_answer": "D",
        "marks": 1,
    },

    # ── SQL (5) ──────────────────────────────────────────────────────────────
    {
        "question_text": "Which SQL clause filters rows BEFORE aggregation?",
        "option_a": "HAVING",
        "option_b": "GROUP BY",
        "option_c": "ORDER BY",
        "option_d": "WHERE",
        "correct_answer": "D",
        "marks": 1,
    },
    {
        "question_text": "What is the key difference between `DELETE` and `TRUNCATE` in SQL?",
        "option_a": "They are identical in all respects",
        "option_b": "DELETE removes the table structure; TRUNCATE removes only data",
        "option_c": "TRUNCATE is faster and cannot be rolled back; DELETE can be rolled back within a transaction",
        "option_d": "DELETE cannot have a WHERE clause; TRUNCATE can",
        "correct_answer": "C",
        "marks": 1,
    },
    {
        "question_text": "Which SQL aggregate function returns the total number of rows in a result set?",
        "option_a": "SUM()",
        "option_b": "MAX()",
        "option_c": "COUNT()",
        "option_d": "LENGTH()",
        "correct_answer": "C",
        "marks": 1,
    },
    {
        "question_text": "What does the `DISTINCT` keyword do in a SQL SELECT statement?",
        "option_a": "Sorts the result set in ascending order",
        "option_b": "Filters all NULL values from the result",
        "option_c": "Joins two or more tables",
        "option_d": "Returns only unique (non-duplicate) values",
        "correct_answer": "D",
        "marks": 1,
    },
    {
        "question_text": "Which type of SQL JOIN returns all records from both tables, with NULLs where there is no match?",
        "option_a": "INNER JOIN",
        "option_b": "LEFT JOIN",
        "option_c": "RIGHT JOIN",
        "option_d": "FULL OUTER JOIN",
        "correct_answer": "D",
        "marks": 1,
    },

    # ── Data Structures & Algorithms (5) ─────────────────────────────────────
    {
        "question_text": "What is the average-case time complexity of Binary Search?",
        "option_a": "O(n)",
        "option_b": "O(n^2)",
        "option_c": "O(log n)",
        "option_d": "O(n log n)",
        "correct_answer": "C",
        "marks": 1,
    },
    {
        "question_text": "Which data structure follows the LIFO (Last In, First Out) principle?",
        "option_a": "Queue",
        "option_b": "Stack",
        "option_c": "Deque",
        "option_d": "Heap",
        "correct_answer": "B",
        "marks": 1,
    },
    {
        "question_text": "What is the worst-case time complexity of QuickSort?",
        "option_a": "O(n log n)",
        "option_b": "O(n)",
        "option_c": "O(log n)",
        "option_d": "O(n^2)",
        "correct_answer": "D",
        "marks": 1,
    },
    {
        "question_text": "Which binary tree traversal visits nodes in Left, Root, Right order?",
        "option_a": "Pre-order",
        "option_b": "Post-order",
        "option_c": "In-order",
        "option_d": "Level-order",
        "correct_answer": "C",
        "marks": 1,
    },
    {
        "question_text": "What is the space complexity of Merge Sort?",
        "option_a": "O(1)",
        "option_b": "O(log n)",
        "option_c": "O(n)",
        "option_d": "O(n^2)",
        "correct_answer": "C",
        "marks": 1,
    },

    # ── OOP (5) ──────────────────────────────────────────────────────────────
    {
        "question_text": "Which OOP concept allows a class to have multiple methods with the same name but different parameter lists?",
        "option_a": "Inheritance",
        "option_b": "Encapsulation",
        "option_c": "Method Overloading (Compile-time Polymorphism)",
        "option_d": "Abstraction",
        "correct_answer": "C",
        "marks": 1,
    },
    {
        "question_text": "Which OOP principle restricts direct access to an object's internal state?",
        "option_a": "Polymorphism",
        "option_b": "Inheritance",
        "option_c": "Abstraction",
        "option_d": "Encapsulation",
        "correct_answer": "D",
        "marks": 1,
    },
    {
        "question_text": "What is an abstract class?",
        "option_a": "A class with only static methods",
        "option_b": "A class that cannot be instantiated and may contain abstract methods",
        "option_c": "A class that cannot be inherited by any subclass",
        "option_d": "A class with no attributes",
        "correct_answer": "B",
        "marks": 1,
    },
    {
        "question_text": "Which concept allows a subclass to provide its own implementation of a method defined in the parent class?",
        "option_a": "Method Overloading",
        "option_b": "Encapsulation",
        "option_c": "Method Overriding (Runtime Polymorphism)",
        "option_d": "Abstraction",
        "correct_answer": "C",
        "marks": 1,
    },
    {
        "question_text": "What is the role of a constructor in OOP?",
        "option_a": "A method called when an object is garbage-collected",
        "option_b": "A static utility method shared by all instances",
        "option_c": "A special method automatically invoked when a new object is created to initialise its state",
        "option_d": "An abstract method that must be implemented by subclasses",
        "correct_answer": "C",
        "marks": 1,
    },

    # ── DBMS (4) ─────────────────────────────────────────────────────────────
    {
        "question_text": "Which Normal Form eliminates partial functional dependencies?",
        "option_a": "1NF",
        "option_b": "2NF",
        "option_c": "3NF",
        "option_d": "BCNF",
        "correct_answer": "B",
        "marks": 1,
    },
    {
        "question_text": "What is a foreign key in a relational database?",
        "option_a": "A key used solely for indexing to speed up queries",
        "option_b": "A key that uniquely identifies every row in its own table",
        "option_c": "A duplicate key shared between two tables",
        "option_d": "A column that references the primary key of another table",
        "correct_answer": "D",
        "marks": 1,
    },
    {
        "question_text": "Which SQL command permanently saves the changes made during a transaction?",
        "option_a": "ROLLBACK",
        "option_b": "SAVEPOINT",
        "option_c": "COMMIT",
        "option_d": "END TRANSACTION",
        "correct_answer": "C",
        "marks": 1,
    },
    {
        "question_text": "What does ACID stand for in database transactions?",
        "option_a": "Availability, Concurrency, Integrity, Dependency",
        "option_b": "Atomicity, Consistency, Isolation, Durability",
        "option_c": "Atomicity, Concurrency, Isolation, Dependency",
        "option_d": "Availability, Consistency, Integrity, Durability",
        "correct_answer": "B",
        "marks": 1,
    },

    # ── Operating Systems (4) ────────────────────────────────────────────────
    {
        "question_text": "What is a deadlock in an operating system?",
        "option_a": "A type of virus that freezes the operating system",
        "option_b": "A memory leak caused by an infinite loop",
        "option_c": "A situation where two or more processes wait indefinitely for resources held by each other",
        "option_d": "When a process consumes 100 percent CPU for an extended period",
        "correct_answer": "C",
        "marks": 1,
    },
    {
        "question_text": "Which page replacement algorithm replaces the page that has not been used for the longest period of time?",
        "option_a": "FIFO (First In First Out)",
        "option_b": "LRU (Least Recently Used)",
        "option_c": "Optimal Page Replacement",
        "option_d": "Clock Algorithm",
        "correct_answer": "B",
        "marks": 1,
    },
    {
        "question_text": "What is the key difference between a process and a thread?",
        "option_a": "A thread has its own dedicated memory space; a process shares memory",
        "option_b": "A process is a lightweight execution unit; a thread is heavyweight",
        "option_c": "There is no practical difference between a process and a thread",
        "option_d": "A thread shares memory with other threads in the same process; processes have separate memory spaces",
        "correct_answer": "D",
        "marks": 1,
    },
    {
        "question_text": "Which CPU scheduling algorithm can lead to starvation of lower-priority processes?",
        "option_a": "Round Robin",
        "option_b": "FCFS (First Come First Served)",
        "option_c": "Priority Scheduling",
        "option_d": "Shortest Job Next (SJN)",
        "correct_answer": "C",
        "marks": 1,
    },

    # ── Computer Networks (4) ────────────────────────────────────────────────
    {
        "question_text": "What does HTTP stand for?",
        "option_a": "High Transfer Text Protocol",
        "option_b": "Hyperlink Text Transport Protocol",
        "option_c": "HyperText Transfer Protocol",
        "option_d": "HyperText Transport Process",
        "correct_answer": "C",
        "marks": 1,
    },
    {
        "question_text": "At which OSI model layer is routing of packets between networks handled?",
        "option_a": "Data Link Layer (Layer 2)",
        "option_b": "Transport Layer (Layer 4)",
        "option_c": "Network Layer (Layer 3)",
        "option_d": "Session Layer (Layer 5)",
        "correct_answer": "C",
        "marks": 1,
    },
    {
        "question_text": "What is the primary purpose of DNS in networking?",
        "option_a": "Encrypts data during transmission",
        "option_b": "Translates human-readable domain names into IP addresses",
        "option_c": "Manages and allocates network bandwidth",
        "option_d": "Assigns MAC addresses to network devices",
        "correct_answer": "B",
        "marks": 1,
    },
    {
        "question_text": "Which protocol is used for secure, encrypted communication over the web?",
        "option_a": "HTTP",
        "option_b": "FTP",
        "option_c": "SMTP",
        "option_d": "HTTPS",
        "correct_answer": "D",
        "marks": 1,
    },

    # ── HTML / CSS (4) ───────────────────────────────────────────────────────
    {
        "question_text": "Which HTML tag is used to create a hyperlink?",
        "option_a": "<link>",
        "option_b": "<href>",
        "option_c": "<url>",
        "option_d": "<a>",
        "correct_answer": "D",
        "marks": 1,
    },
    {
        "question_text": "Which CSS property changes the text colour of an element?",
        "option_a": "font-color",
        "option_b": "text-color",
        "option_c": "color",
        "option_d": "foreground",
        "correct_answer": "C",
        "marks": 1,
    },
    {
        "question_text": "What are the four layers of the CSS box model from innermost to outermost?",
        "option_a": "Text, Image, Border, Shadow",
        "option_b": "Content, Spacing, Border, Layout",
        "option_c": "Content, Padding, Border, Margin",
        "option_d": "Header, Body, Footer, Navigation",
        "correct_answer": "C",
        "marks": 1,
    },
    {
        "question_text": "What is the default CSS `display` value of a `<div>` element?",
        "option_a": "inline",
        "option_b": "inline-block",
        "option_c": "flex",
        "option_d": "block",
        "correct_answer": "D",
        "marks": 1,
    },

    # ── Software Engineering (4) ─────────────────────────────────────────────
    {
        "question_text": "Which software development model is most appropriate when requirements are well-defined and unlikely to change?",
        "option_a": "Agile",
        "option_b": "Spiral",
        "option_c": "RAD (Rapid Application Development)",
        "option_d": "Waterfall",
        "correct_answer": "D",
        "marks": 1,
    },
    {
        "question_text": "What does the 'S' in the SOLID design principles stand for?",
        "option_a": "Scalability Principle",
        "option_b": "Single Responsibility Principle",
        "option_c": "Static Binding Principle",
        "option_d": "Sequential Design Principle",
        "correct_answer": "B",
        "marks": 1,
    },
    {
        "question_text": "What best describes a REST API?",
        "option_a": "A database management protocol",
        "option_b": "A compiled programming language",
        "option_c": "An architectural style for designing stateless web services using standard HTTP methods",
        "option_d": "A type of relational database",
        "correct_answer": "C",
        "marks": 1,
    },
    {
        "question_text": "Which level of software testing verifies that the complete integrated system meets its requirements?",
        "option_a": "Unit Testing",
        "option_b": "Integration Testing",
        "option_c": "System Testing",
        "option_d": "Acceptance Testing",
        "correct_answer": "C",
        "marks": 1,
    },
]


def seed():
    with app.app_context():
        # Fetch all existing MCQ question texts for duplicate-detection
        existing_texts = set(
            q.question_text
            for q in Question.query.filter_by(question_type='mcq').all()
        )
        existing_count = len(existing_texts)

        if existing_count >= 50:
            print(f"[SKIP] {existing_count} MCQ questions already exist. Seeding not required.")
            return

        print(f"[INFO] Found {existing_count} existing MCQ question(s). Seeding missing questions...")

        to_insert = [q for q in QUESTIONS if q["question_text"] not in existing_texts]

        if not to_insert:
            print("[SKIP] All 50 seed questions already present. Nothing to insert.")
            return

        for q_data in to_insert:
            new_q = Question(
                question_text=q_data["question_text"],
                question_type="mcq",
                option_a=q_data["option_a"],
                option_b=q_data["option_b"],
                option_c=q_data["option_c"],
                option_d=q_data["option_d"],
                correct_answer=q_data["correct_answer"],
                marks=q_data["marks"],
            )
            db.session.add(new_q)

        db.session.commit()

        final_count = Question.query.filter_by(question_type='mcq').count()
        print(f"[SUCCESS] Inserted {len(to_insert)} question(s).")
        print(f"[INFO] Total MCQ questions in database: {final_count}")


if __name__ == "__main__":
    seed()
