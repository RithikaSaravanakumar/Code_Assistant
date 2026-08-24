from datetime import datetime, timezone
# pyrefly: ignore [missing-import]
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

SUPPORTED_LANGUAGES = ('python', 'java', 'javascript', 'cpp', 'c')
DIFFICULTY_LEVELS = ('Easy', 'Medium', 'Hard')

DEFAULT_STARTER_CODE = {
    'python': 'def solution():\n    pass\n',
    'java': 'public class Main {\n    public static void main(String[] args) {\n\n    }\n}\n',
    'javascript': 'function solution() {\n\n}\n',
    'cpp': '#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n\n}\n',
    'c': '#include <stdio.h>\n\nint main() {\n\n}\n',
}


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    attempts = db.relationship('AssessmentAttempt', backref='user', lazy=True, cascade="all, delete-orphan")
    coding_submissions = db.relationship('CodingSubmission', backref='user', lazy=True, cascade="all, delete-orphan")
    coding_sessions = db.relationship('CodingTimedSession', backref='user', lazy=True, cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False)
    option_a = db.Column(db.String(255), nullable=True)
    option_b = db.Column(db.String(255), nullable=True)
    option_c = db.Column(db.String(255), nullable=True)
    option_d = db.Column(db.String(255), nullable=True)
    correct_answer = db.Column(db.String(255), nullable=True)
    marks = db.Column(db.Integer, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    answers = db.relationship('Answer', backref='question', lazy=True, cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<Question {self.id} ({self.question_type})>"


class CodingQuestion(db.Model):
    __tablename__ = 'coding_questions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False, default='Easy')
    input_format = db.Column(db.Text, nullable=False)
    output_format = db.Column(db.Text, nullable=False)
    constraints = db.Column(db.Text, nullable=False)
    sample_input = db.Column(db.Text, nullable=False)
    sample_output = db.Column(db.Text, nullable=False)
    expected_time_complexity = db.Column(db.String(100), nullable=False, default='O(n)')
    expected_space_complexity = db.Column(db.String(100), nullable=False, default='O(n)')
    starter_code_python = db.Column(db.Text, nullable=True)
    starter_code_java = db.Column(db.Text, nullable=True)
    starter_code_javascript = db.Column(db.Text, nullable=True)
    starter_code_cpp = db.Column(db.Text, nullable=True)
    starter_code_c = db.Column(db.Text, nullable=True)
    marks = db.Column(db.Integer, default=100, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    test_cases = db.relationship('TestCase', backref='question', lazy=True, cascade="all, delete-orphan")
    submissions = db.relationship('CodingSubmission', backref='question', lazy=True, cascade="all, delete-orphan")

    def get_starter_code(self, language: str) -> str:
        lang = language.lower()
        field_map = {
            'python': self.starter_code_python,
            'java': self.starter_code_java,
            'javascript': self.starter_code_javascript,
            'cpp': self.starter_code_cpp,
            'c': self.starter_code_c,
        }
        custom = field_map.get(lang)
        if custom:
            return custom
        return DEFAULT_STARTER_CODE.get(lang, DEFAULT_STARTER_CODE['python'])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<CodingQuestion {self.id}: {self.title}>"


class TestCase(db.Model):
    __tablename__ = 'test_cases'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('coding_questions.id', ondelete='CASCADE'), nullable=False)
    input_data = db.Column(db.Text, nullable=False)
    expected_output = db.Column(db.Text, nullable=False)
    is_sample = db.Column(db.Boolean, default=False, nullable=False)
    is_hidden = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        kind = 'sample' if self.is_sample else 'hidden'
        return f"<TestCase {self.id} ({kind}) for Q{self.question_id}>"


class CodingSubmission(db.Model):
    __tablename__ = 'coding_submissions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('coding_questions.id', ondelete='CASCADE'), nullable=False)
    programming_language = db.Column(db.String(20), nullable=False, default='python')
    submitted_code = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    test_cases_passed = db.Column(db.Integer, default=0, nullable=False)
    test_cases_total = db.Column(db.Integer, default=0, nullable=False)
    score = db.Column(db.Float, default=0.0, nullable=False)
    execution_status = db.Column(db.String(100), nullable=False, default='Not Executed')
    is_run = db.Column(db.Boolean, default=False, nullable=False)
    submitted_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<CodingSubmission {self.id} - User {self.user_id} - Q {self.question_id}>"


class CodingTimedSession(db.Model):
    """Timed coding assessment session for a student."""
    __tablename__ = 'coding_timed_sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    duration_minutes = db.Column(db.Integer, default=60, nullable=False)
    started_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    ended_at = db.Column(db.DateTime, nullable=True)

    @property
    def is_active(self):
        if self.ended_at is not None:
            return False
        elapsed = (datetime.now(timezone.utc) - self.started_at.replace(tzinfo=timezone.utc)).total_seconds()
        return elapsed < self.duration_minutes * 60

    @property
    def expires_at_ms(self):
        start = self.started_at.replace(tzinfo=timezone.utc)
        return int((start.timestamp() + self.duration_minutes * 60) * 1000)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<CodingTimedSession {self.id} user={self.user_id}>"


class AssessmentAttempt(db.Model):
    __tablename__ = 'assessment_attempts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    score = db.Column(db.Float, default=0.0, nullable=False)
    total_marks = db.Column(db.Integer, default=0, nullable=False)
    percentage = db.Column(db.Float, default=0.0, nullable=False)
    started_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    submitted_at = db.Column(db.DateTime, nullable=True)

    answers = db.relationship('Answer', backref='attempt', lazy=True, cascade="all, delete-orphan")
    attempt_questions = db.relationship(
        'AttemptQuestion',
        lazy=True,
        cascade="all, delete-orphan",
        order_by="AttemptQuestion.order_index"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<AssessmentAttempt {self.id} - User {self.user_id}>"


class AttemptQuestion(db.Model):
    __tablename__ = 'attempt_questions'

    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('assessment_attempts.id', ondelete='CASCADE'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    order_index = db.Column(db.Integer, nullable=False)
    opt_a_text = db.Column(db.String(500), nullable=False)
    opt_b_text = db.Column(db.String(500), nullable=False)
    opt_c_text = db.Column(db.String(500), nullable=False)
    opt_d_text = db.Column(db.String(500), nullable=False)
    correct_label = db.Column(db.String(1), nullable=False)

    question = db.relationship('Question', foreign_keys=[question_id], lazy='joined')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<AttemptQuestion attempt={self.attempt_id} q={self.question_id} order={self.order_index}>"


class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('assessment_attempts.id', ondelete='CASCADE'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    selected_answer = db.Column(db.String(255), nullable=True)
    is_correct = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<Answer {self.id} - Attempt {self.attempt_id} - Question {self.question_id}>"
