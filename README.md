# Online Coding Assessment Platform

A modular, secure, and beginner-friendly Online Coding Assessment Platform built with Python (Flask) and MySQL. This system facilitates both multiple-choice assessments and coding-question storage, providing automatic scoring and ranking dashboards.

## Project Overview
This platform serves as a modern tool for educators and students. Admins can manage test suites (MCQs and coding problems), while students can take assessments under timed conditions, view instant evaluations, track their attempt logs, and compare results on a global leaderboard.

## Features
- **Student Portal**: Register, authenticate, take timed MCQ/Coding tests, review attempt history, and view grades.
- **Admin Console**: Manage question banks (Create, Read, Update, Delete for MCQs and coding prompts).
- **Evaluation System**: Automatic grading of MCQ assessments, calculating percentages, tracking durations, and saving submissions.
- **Leaderboard**: Displays student rankings based on grading score criteria.
- **Coding Sandbox MVP**: Allows students to submit code blocks for specific questions and stores them securely.
- **Question Seeding**: 50 placement-level technical MCQ questions pre-seeded across 11 CS topics.
- **Randomized Assessments**: Each attempt shows exactly 20 randomly selected questions with shuffled answer options.

## Technology Stack
- **Backend**: Python 3, Flask
- **Database**: MySQL, SQLAlchemy (Object-Relational Mapper)
- **Frontend**: HTML5, Vanilla CSS3 (custom dark/neon theme), JavaScript, Jinja2 Templates
- **Authentication**: Session-based authorization with secure password hashing via `Werkzeug`

## Project Structure
```text
Code_Assistant/
│
├── static/
│   └── css/
│       └── styles.css
│
├── templates/
│   ├── base.html
│   ├── index.html
│   └── errors/
│       ├── 404.html
│       └── 500.html
│
├── app.py
├── config.py
├── models.py
├── seed_questions.py      ← Run once to populate 50 MCQ questions
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Database Configuration
Make sure you have a local MySQL instance running. The schema tables are initialized automatically using SQLAlchemy when starting the Flask application.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/RithikaSaravanakumar/Code_Assistant.git
   cd Code_Assistant
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory following the format in `.env.example`:
   ```env
   FLASK_SECRET_KEY=your-secret-key
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=online_assessment
   ```

## How to Run

1. Make sure your MySQL server is running and the database specified in `.env` exists (or is created automatically).
2. Start the Flask application (this also auto-creates all DB tables):
   ```bash
   python app.py
   ```
3. **Seed the 50 MCQ questions** (run once; safe to run multiple times):
   ```bash
   python seed_questions.py
   ```
4. Open your browser and navigate to `http://127.0.0.1:5000`.

## Question Seeding

`seed_questions.py` inserts **50 placement-level technical MCQ questions** covering:

| Topic                    | Count |
|--------------------------|-------|
| Python                   | 5     |
| Java                     | 5     |
| JavaScript               | 5     |
| SQL                      | 5     |
| Data Structures & Algorithms | 5 |
| Object-Oriented Programming  | 5 |
| DBMS                     | 4     |
| Operating Systems        | 4     |
| Computer Networks        | 4     |
| HTML / CSS               | 4     |
| Software Engineering     | 4     |
| **Total**                | **50** |

The script is **idempotent** — it checks question text for duplicates before inserting and skips if 50+ MCQs already exist.

## Randomized Assessment System

Each time a student starts a new assessment attempt, the system:

1. **Randomly selects 20 questions** from the available 50 MCQ pool.
2. **Shuffles the question order** so no two attempts have the same sequence.
3. **Shuffles the answer options** (A/B/C/D positions) independently for each question in each attempt.
4. **Remaps the correct answer label** to match the shuffled option layout, ensuring evaluation is always accurate.
5. **Persists the selection** in the `attempt_questions` table — refreshing the page shows the same 20 questions in the same order.

This prevents answer memorisation across attempts while maintaining evaluation correctness.

## Admin Features
- Secure admin console routes.
- Question CRUD operations (MCQ & Coding).

## Student Features
- Session-based dashboard.
- Live-timer test-taking window (20 minutes for 20 questions).
- Score evaluations and history details.
- Ranking leaderboard.

## Development Progress

- [x] Project setup
- [x] MySQL database
- [x] Student authentication
- [x] Admin question management
- [x] MCQ assessment
- [x] Timer
- [x] Automatic evaluation
- [x] Result page
- [x] Attempt history
- [x] Leaderboard
- [x] Coding questions
- [x] 50 technical MCQ questions seeded
- [x] Randomized 20-question assessment selection
- [x] Shuffled answer options with correct evaluation
- [x] Refresh-safe attempt consistency
- [x] Testing
