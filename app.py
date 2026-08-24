import random
from datetime import datetime, timezone
from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from config import Config
from models import db, User, AssessmentAttempt, AttemptQuestion, Question, Answer, CodingSubmission

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    try:
        return render_template('errors/404.html'), 404
    except Exception:
        return jsonify({"error": "Page not found", "code": 404}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    try:
        return render_template('errors/500.html'), 500
    except Exception:
        return jsonify({"error": "Internal server error", "code": 500}), 500

@app.context_processor
def inject_now():
    return {'datetime_now': datetime.now()}

# Decorators for route protection
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        if session.get('role') != 'student':
            flash('Access denied. Student portal only.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception:
        return jsonify({
            "message": "Welcome to the Online Coding Assessment Platform!",
            "status": "Server running"
        })

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard' if session.get('role') == 'student' else 'admin_dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not username or not email or not password or not confirm_password:
            flash('All fields are required.', 'danger')
            return render_template('register.html')
            
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('register.html')
            
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')
            
        # Duplicate validations
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            if existing_user.username == username:
                flash('Username is already taken.', 'danger')
            else:
                flash('Email address is already registered.', 'danger')
            return render_template('register.html')
            
        # Create student user
        hashed_pw = generate_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_pw,
            role='student'
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please sign in.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard' if session.get('role') == 'student' else 'admin_dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Please enter email and password.', 'danger')
            return render_template('login.html')
            
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            
            flash(f'Welcome back, {user.username}!', 'success')
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
            return render_template('login.html')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@student_required
def dashboard():
    user_id = session['user_id']
    attempts_count = AssessmentAttempt.query.filter_by(user_id=user_id).count()
    
    avg_score = 0.0
    if attempts_count > 0:
        avg_score = db.session.query(db.func.avg(AssessmentAttempt.percentage)).filter_by(user_id=user_id).scalar() or 0.0
        
    # Find global rank
    student_scores = db.session.query(
        User.id,
        db.func.avg(AssessmentAttempt.percentage).label('avg_pct')
    ).join(AssessmentAttempt, User.id == AssessmentAttempt.user_id)\
     .filter(User.role == 'student')\
     .group_by(User.id)\
     .order_by(db.desc('avg_pct')).all()
     
    rank = None
    for idx, row in enumerate(student_scores):
        if row[0] == user_id:
            rank = idx + 1
            break
            
    return render_template(
        'dashboard.html',
        attempts_count=attempts_count,
        avg_score=avg_score,
        rank=rank
    )

# Decorator for admin route protection
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            flash('Access denied. Admin portal only.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Admin Routes
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    questions = Question.query.order_by(Question.id.desc()).all()
    return render_template('admin/dashboard.html', questions=questions)

@app.route('/admin/questions/add/mcq', methods=['GET', 'POST'])
@admin_required
def add_mcq():
    if request.method == 'POST':
        question_text = request.form.get('question_text', '').strip()
        option_a = request.form.get('option_a', '').strip()
        option_b = request.form.get('option_b', '').strip()
        option_c = request.form.get('option_c', '').strip()
        option_d = request.form.get('option_d', '').strip()
        correct_answer = request.form.get('correct_answer', '').strip()
        marks = int(request.form.get('marks', 1))
        
        if not question_text or not option_a or not option_b or not option_c or not option_d or not correct_answer:
            flash('All fields are required for MCQ questions.', 'danger')
            return render_template('admin/mcq_form.html')
            
        new_q = Question(
            question_text=question_text,
            question_type='mcq',
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_answer=correct_answer,
            marks=marks
        )
        db.session.add(new_q)
        db.session.commit()
        flash('MCQ Question added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
        
    return render_template('admin/mcq_form.html', question=None)

@app.route('/admin/questions/add/coding', methods=['GET', 'POST'])
@admin_required
def add_coding():
    if request.method == 'POST':
        question_text = request.form.get('question_text', '').strip()
        marks = int(request.form.get('marks', 1))
        
        if not question_text:
            flash('Problem description is required.', 'danger')
            return render_template('admin/coding_form.html')
            
        new_q = Question(
            question_text=question_text,
            question_type='coding',
            marks=marks
        )
        db.session.add(new_q)
        db.session.commit()
        flash('Coding Question added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
        
    return render_template('admin/coding_form.html', question=None)

@app.route('/admin/questions/edit/<int:question_id>', methods=['GET', 'POST'])
@admin_required
def edit_question(question_id):
    question = db.get_or_404(Question, question_id)
    
    if request.method == 'POST':
        question.question_text = request.form.get('question_text', '').strip()
        question.marks = int(request.form.get('marks', 1))
        
        if question.question_type == 'mcq':
            question.option_a = request.form.get('option_a', '').strip()
            question.option_b = request.form.get('option_b', '').strip()
            question.option_c = request.form.get('option_c', '').strip()
            question.option_d = request.form.get('option_d', '').strip()
            question.correct_answer = request.form.get('correct_answer', '').strip()
            
            if not question.question_text or not question.option_a or not question.option_b or not question.option_c or not question.option_d or not question.correct_answer:
                flash('All fields are required.', 'danger')
                return render_template('admin/mcq_form.html', question=question)
        else:
            if not question.question_text:
                flash('Problem description is required.', 'danger')
                return render_template('admin/coding_form.html', question=question)
                
        db.session.commit()
        flash('Question updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
        
    template = 'admin/mcq_form.html' if question.question_type == 'mcq' else 'admin/coding_form.html'
    return render_template(template, question=question)

@app.route('/admin/questions/delete/<int:question_id>', methods=['POST'])
@admin_required
def delete_question(question_id):
    question = db.get_or_404(Question, question_id)
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/take_assessment')
@student_required
def take_assessment():
    all_mcq = Question.query.filter_by(question_type='mcq').all()
    if not all_mcq:
        flash('No multiple choice assessments are available at this time.', 'warning')
        return redirect(url_for('dashboard'))

    user_id = session['user_id']

    # Resume existing unsubmitted attempt if it exists
    attempt = AssessmentAttempt.query.filter_by(
        user_id=user_id, submitted_at=None
    ).order_by(AssessmentAttempt.id.desc()).first()

    if attempt:
        # Check if this attempt has AttemptQuestion rows (new format).
        # If not (legacy attempt), discard it and start fresh.
        aq_count = AttemptQuestion.query.filter_by(attempt_id=attempt.id).count()
        if aq_count == 0:
            db.session.delete(attempt)
            db.session.commit()
            attempt = None

    if not attempt:
        # --- NEW ATTEMPT: randomly select 20 questions and shuffle options ---
        QUESTIONS_PER_ATTEMPT = 20
        selected = random.sample(all_mcq, min(QUESTIONS_PER_ATTEMPT, len(all_mcq)))
        random.shuffle(selected)  # randomise question order

        attempt = AssessmentAttempt(
            user_id=user_id,
            score=0.0,
            total_marks=sum(q.marks for q in selected),
            percentage=0.0,
            started_at=datetime.now(timezone.utc)
        )
        db.session.add(attempt)
        db.session.flush()  # obtain attempt.id before inserting AttemptQuestion rows

        labels = ['A', 'B', 'C', 'D']
        for idx, q in enumerate(selected):
            # Original option texts in positional order
            orig_opts = [q.option_a, q.option_b, q.option_c, q.option_d]
            orig_correct_idx = labels.index(q.correct_answer)  # 0-3

            # Shuffle the four positional indices
            positions = [0, 1, 2, 3]
            random.shuffle(positions)

            # Build shuffled option texts
            shuffled_opts = [orig_opts[p] for p in positions]

            # Find where the originally-correct option ended up after shuffle
            new_correct_pos = positions.index(orig_correct_idx)
            new_correct_label = labels[new_correct_pos]

            aq = AttemptQuestion(
                attempt_id=attempt.id,
                question_id=q.id,
                order_index=idx + 1,
                opt_a_text=shuffled_opts[0],
                opt_b_text=shuffled_opts[1],
                opt_c_text=shuffled_opts[2],
                opt_d_text=shuffled_opts[3],
                correct_label=new_correct_label
            )
            db.session.add(aq)

        db.session.commit()

    # Load persisted attempt questions (same set on every refresh)
    attempt_questions = AttemptQuestion.query.filter_by(
        attempt_id=attempt.id
    ).order_by(AttemptQuestion.order_index).all()

    started_at_ms = int(attempt.started_at.replace(tzinfo=timezone.utc).timestamp() * 1000)
    server_now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    return render_template(
        'take_assessment.html',
        attempt_questions=attempt_questions,
        attempt=attempt,
        server_now_ms=server_now_ms,
        started_at_ms=started_at_ms
    )

@app.route('/submit_assessment', methods=['POST'])
@student_required
def submit_assessment():
    attempt_id = request.form.get('attempt_id')
    if not attempt_id:
        flash('Invalid attempt ID.', 'danger')
        return redirect(url_for('dashboard'))

    attempt = db.session.get(AssessmentAttempt, attempt_id)
    if not attempt or attempt.submitted_at is not None:
        flash('This assessment attempt has already been submitted or is invalid.', 'warning')
        return redirect(url_for('dashboard'))

    # Load the 20 AttemptQuestion rows assigned to this specific attempt
    attempt_questions = AttemptQuestion.query.filter_by(attempt_id=attempt.id).all()

    score = 0.0
    total_marks = 0

    for aq in attempt_questions:
        # Form field name uses aq.id so there is no collision across attempts
        selected_val = request.form.get(f'aq_{aq.id}')
        if selected_val:
            selected_val = selected_val.strip()

        # Evaluate against the remapped correct label stored for this attempt
        is_correct = (selected_val == aq.correct_label)
        total_marks += aq.question.marks
        if is_correct:
            score += aq.question.marks

        ans = Answer(
            attempt_id=attempt.id,
            question_id=aq.question_id,
            selected_answer=selected_val,
            is_correct=is_correct
        )
        db.session.add(ans)

    attempt.score = score
    attempt.total_marks = total_marks
    attempt.percentage = (score / total_marks * 100) if total_marks > 0 else 0.0
    attempt.submitted_at = datetime.now(timezone.utc)
    db.session.commit()

    flash(f'Assessment submitted! You scored {int(score)}/{total_marks} ({attempt.percentage:.1f}%).', 'success')
    return redirect(url_for('result', attempt_id=attempt.id))

@app.route('/result/<int:attempt_id>')
@login_required
def result(attempt_id):
    attempt = db.get_or_404(AssessmentAttempt, attempt_id)

    # Security check: only own attempt or admin
    if session.get('role') != 'admin' and attempt.user_id != session.get('user_id'):
        flash('Access denied. You cannot view this assessment result.', 'danger')
        return redirect(url_for('dashboard'))

    # Load the attempt's 20 questions with their shuffled option layout
    attempt_qs = AttemptQuestion.query.filter_by(
        attempt_id=attempt_id
    ).order_by(AttemptQuestion.order_index).all()

    # Build a map of question_id -> Answer for O(1) lookup
    answers_map = {
        a.question_id: a
        for a in Answer.query.filter_by(attempt_id=attempt_id).all()
    }

    correct_count = 0
    incorrect_count = 0
    unanswered_count = 0
    question_details = []

    for aq in attempt_qs:
        ans = answers_map.get(aq.question_id)
        selected = ans.selected_answer if ans else None
        is_correct = ans.is_correct if ans else False

        if not selected:
            unanswered_count += 1
        elif is_correct:
            correct_count += 1
        else:
            incorrect_count += 1

        question_details.append({
            'question_text': aq.question.question_text,
            'opt_a_text': aq.opt_a_text,
            'opt_b_text': aq.opt_b_text,
            'opt_c_text': aq.opt_c_text,
            'opt_d_text': aq.opt_d_text,
            'correct_label': aq.correct_label,
            'selected_answer': selected,
            'is_correct': is_correct,
            'marks': aq.question.marks,
        })

    return render_template(
        'result.html',
        attempt=attempt,
        correct_count=correct_count,
        incorrect_count=incorrect_count,
        unanswered_count=unanswered_count,
        question_details=question_details
    )

@app.route('/coding_questions')
@student_required
def coding_questions():
    questions = Question.query.filter_by(question_type='coding').all()
    return render_template('coding_list.html', questions=questions)

@app.route('/coding_questions/<int:question_id>')
@student_required
def coding_question(question_id):
    question = db.get_or_404(Question, question_id)
    if question.question_type != 'coding':
        flash('Invalid coding challenge.', 'danger')
        return redirect(url_for('coding_questions'))
        
    user_id = session['user_id']
    submissions = CodingSubmission.query.filter_by(user_id=user_id, question_id=question_id)\
                                        .order_by(CodingSubmission.submitted_at.desc()).all()
                                        
    return render_template('coding_question.html', question=question, submissions=submissions)

@app.route('/coding_questions/<int:question_id>/submit', methods=['POST'])
@student_required
def submit_coding(question_id):
    question = db.get_or_404(Question, question_id)
    if question.question_type != 'coding':
        flash('Invalid coding challenge.', 'danger')
        return redirect(url_for('coding_questions'))
        
    code = request.form.get('code', '').strip()
    if not code:
        flash('Code solution cannot be empty.', 'danger')
        return redirect(url_for('coding_question', question_id=question.id))
        
    user_id = session['user_id']
    new_sub = CodingSubmission(
        user_id=user_id,
        question_id=question_id,
        code=code
    )
    db.session.add(new_sub)
    db.session.commit()
    
    flash('Coding solution submitted successfully!', 'success')
    return redirect(url_for('coding_question', question_id=question.id))

@app.route('/history')
@student_required
def history():
    user_id = session['user_id']
    attempts = AssessmentAttempt.query.filter_by(user_id=user_id)\
                                       .filter(AssessmentAttempt.submitted_at.isnot(None))\
                                       .order_by(AssessmentAttempt.submitted_at.desc()).all()
    return render_template('history.html', attempts=attempts)

@app.route('/leaderboard')
def leaderboard():
    leaderboard_data = db.session.query(
        User.username,
        db.func.max(AssessmentAttempt.percentage).label('max_pct'),
        db.func.max(AssessmentAttempt.score).label('max_score')
    ).join(AssessmentAttempt, User.id == AssessmentAttempt.user_id)\
     .filter(User.role == 'student')\
     .filter(AssessmentAttempt.submitted_at.isnot(None))\
     .group_by(User.id)\
     .order_by(db.desc('max_pct')).all()

    rankings = []
    current_rank = 0
    prev_pct = None
    count = 0
    
    for username, max_pct, max_score in leaderboard_data:
        count += 1
        if max_pct != prev_pct:
            current_rank = count
            prev_pct = max_pct
        rankings.append({
            'rank': current_rank,
            'username': username,
            'percentage': max_pct,
            'score': max_score
        })
        
    return render_template('leaderboard.html', rankings=rankings)

@app.route('/health')
def health_check():
    try:
        db.session.execute(db.text('SELECT 1'))
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "database": f"error: {str(e)}"}), 500

if __name__ == '__main__':
    with app.app_context():
        # Create database tables
        db.create_all()
        
        # Seed default admin user
        admin_user = User.query.filter_by(role='admin').first()
        if not admin_user:
            admin_pw = generate_password_hash('Rithika@123')
            new_admin = User(
                username='rithikaadmin',
                email='rithikaas005@gmail.com',
                password_hash=admin_pw,
                role='admin'
            )
            db.session.add(new_admin)
            db.session.commit()
            print("Default admin user created")
        else:
            print("Admin user already exists.")
            
        print("Database tables initialized/created successfully.")
    app.run(debug=True)
