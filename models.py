from datetime import datetime, timezone
# pyrefly: ignore [missing-import]
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # 'student' or 'admin'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    attempts = db.relationship('AssessmentAttempt', backref='user', lazy=True, cascade="all, delete-orphan")
    coding_submissions = db.relationship('CodingSubmission', backref='user', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False)  # 'mcq' or 'coding'
    option_a = db.Column(db.String(255), nullable=True)
    option_b = db.Column(db.String(255), nullable=True)
    option_c = db.Column(db.String(255), nullable=True)
    option_d = db.Column(db.String(255), nullable=True)
    correct_answer = db.Column(db.String(255), nullable=True)  # 'A', 'B', 'C', or 'D' for MCQ
    marks = db.Column(db.Integer, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    answers = db.relationship('Answer', backref='question', lazy=True, cascade="all, delete-orphan")
    coding_submissions = db.relationship('CodingSubmission', backref='question', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Question {self.id} ({self.question_type})>"

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

    def __repr__(self):
        return f"<AssessmentAttempt {self.id} - User {self.user_id}>"

class AttemptQuestion(db.Model):
    """
    Stores the 20 randomly selected questions for a specific assessment attempt,
    along with the shuffled option order and remapped correct answer label.
    This ensures:
      - Consistent questions on page refresh (no re-randomisation)
      - Correct evaluation even after options are shuffled per attempt
    """
    __tablename__ = 'attempt_questions'

    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('assessment_attempts.id', ondelete='CASCADE'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    order_index = db.Column(db.Integer, nullable=False)       # 1-20 display position
    opt_a_text = db.Column(db.String(500), nullable=False)    # Shuffled option A text
    opt_b_text = db.Column(db.String(500), nullable=False)    # Shuffled option B text
    opt_c_text = db.Column(db.String(500), nullable=False)    # Shuffled option C text
    opt_d_text = db.Column(db.String(500), nullable=False)    # Shuffled option D text
    correct_label = db.Column(db.String(1), nullable=False)   # Remapped correct label (A/B/C/D) after shuffle

    # Eager-load the source question for template access (aq.question.question_text, etc.)
    question = db.relationship('Question', foreign_keys=[question_id], lazy='joined')

    def __repr__(self):
        return f"<AttemptQuestion attempt={self.attempt_id} q={self.question_id} order={self.order_index}>"

class Answer(db.Model):
    __tablename__ = 'answers'
    
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('assessment_attempts.id', ondelete='CASCADE'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    selected_answer = db.Column(db.String(255), nullable=True)
    is_correct = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Answer {self.id} - Attempt {self.attempt_id} - Question {self.question_id}>"

class CodingSubmission(db.Model):
    __tablename__ = 'coding_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    code = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<CodingSubmission {self.id} - User {self.user_id} - Question {self.question_id}>"
