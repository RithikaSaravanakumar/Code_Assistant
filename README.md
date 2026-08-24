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
2. Start the Flask application:
   ```bash
   python app.py
   ```
3. Open your browser and navigate to `http://127.0.0.1:5000`.

## Admin Features
- Secure admin console routes.
- Question CRUD operations (MCQ & Coding).

## Student Features
- Session-based dashboard.
- Live-timer test-taking window.
- Score evaluations and history details.
- Ranking leaderboard.

## Development Progress

- [x] Project setup
- [x] MySQL database
- [x] Student authentication
- [x] Admin question management
- [x] MCQ assessment
- [x] Timer
- [ ] Automatic evaluation
- [ ] Result page
- [ ] Attempt history
- [ ] Leaderboard
- [ ] Coding questions
- [ ] Testing
