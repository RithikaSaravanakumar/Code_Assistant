from flask import Flask, jsonify, render_template
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    # Fallback to JSON if requested or if templates aren't ready
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

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception:
        return jsonify({
            "message": "Welcome to the Online Coding Assessment Platform!",
            "status": "Server running, templates initializing"
        })

@app.route('/health')
def health_check():
    try:
        # Check database connection
        db.session.execute(db.text('SELECT 1'))
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "database": f"error: {str(e)}"}), 500

if __name__ == '__main__':
    with app.app_context():
        # Create database tables
        db.create_all()
        print("Database tables initialized/created successfully.")
    app.run(debug=True)
