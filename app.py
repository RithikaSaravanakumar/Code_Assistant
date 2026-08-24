from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from config import Config
from models import db, User, AssessmentAttempt

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

from datetime import datetime

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

# Placeholder routes for other features to prevent routing errors
@app.route('/admin/dashboard')
def admin_dashboard():
    return jsonify({"message": "Admin dashboard is under development (Work Item 3)."}), 200

@app.route('/take_assessment')
@student_required
def take_assessment():
    return jsonify({"message": "MCQ assessment taking interface is under development (Work Item 4)."}), 200

@app.route('/coding_questions')
@student_required
def coding_questions():
    return jsonify({"message": "Coding question module is under development (Work Item 10)."}), 200

@app.route('/history')
@student_required
def history():
    return jsonify({"message": "Attempt history is under development (Work Item 8)."}), 200

@app.route('/leaderboard')
def leaderboard():
    return jsonify({"message": "Leaderboard is under development (Work Item 9)."}), 200

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
            admin_pw = generate_password_hash('adminpassword')
            new_admin = User(
                username='admin',
                email='admin@codeeval.com',
                password_hash=admin_pw,
                role='admin'
            )
            db.session.add(new_admin)
            db.session.commit()
            print("Default admin user created: admin@codeeval.com / adminpassword")
        else:
            print("Admin user already exists.")
            
        print("Database tables initialized/created successfully.")
    app.run(debug=True)
