import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from database import init_db
from models import (
    get_or_create_user,
    recommend_projects,
    save_project,
    get_saved_projects,
    delete_saved_project,
    get_all_projects,
    get_project_by_id,
    add_project,
    update_project,
    delete_project,
    log_generation,
    get_admin_stats
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "ai_project_idea_generator_secret_key_2026")

# Initialize SQLite database schema and seed data on startup
with app.app_context():
    init_db()

AVAILABLE_DOMAINS = [
    "Artificial Intelligence",
    "Machine Learning",
    "Cybersecurity",
    "Web Development",
    "Cloud Computing",
    "Internet of Things",
    "Mobile App Development",
    "Data Science",
    "Blockchain",
    "DevOps"
]

DIFFICULTY_LEVELS = ["Beginner", "Intermediate", "Advanced"]

@app.route('/')
def index():
    """Renders the Home page with project overview, platform features, and quick statistics."""
    stats = get_admin_stats()
    return render_template('index.html', stats=stats, domains=AVAILABLE_DOMAINS)

@app.route('/generator')
def generator():
    """Renders the Project Generator input form page."""
    return render_template('generator.html', domains=AVAILABLE_DOMAINS, difficulties=DIFFICULTY_LEVELS)

@app.route('/generate', methods=['POST'])
def generate():
    """Handles submission from the generator form and computes recommendation results."""
    student_name = request.form.get('student_name', '').strip() or "Guest Student"
    domain = request.form.get('domain', 'Artificial Intelligence')
    skills = request.form.get('skills', '').strip()
    difficulty = request.form.get('difficulty', 'Intermediate')

    # Get or create student record
    user = get_or_create_user(student_name)
    session['user_id'] = user['id']
    session['user_name'] = user['name']

    # Log generation statistics
    log_generation(student_name, domain, skills, difficulty)

    # Compute intelligent project recommendations
    recommendations = recommend_projects(domain, skills, difficulty)

    return render_template(
        'results.html',
        student_name=student_name,
        user_id=user['id'],
        domain=domain,
        skills=skills,
        difficulty=difficulty,
        recommendations=recommendations,
        total_found=len(recommendations)
    )

@app.route('/save_project', methods=['POST'])
def save_user_project():
    """API endpoint to save a recommended project for the user."""
    data = request.get_json() if request.is_json else request.form
    user_id = data.get('user_id') or session.get('user_id')
    project_id = data.get('project_id')
    student_name = data.get('student_name') or session.get('user_name', 'Guest Student')

    if not user_id:
        user = get_or_create_user(student_name)
        user_id = user['id']
        session['user_id'] = user_id
        session['user_name'] = user['name']

    if not project_id:
        if request.is_json:
            return jsonify({"status": "error", "message": "Missing project ID"}), 400
        flash("Failed to save: Missing project ID.", "danger")
        return redirect(url_for('generator'))

    saved_id = save_project(int(user_id), int(project_id))

    if request.is_json:
        return jsonify({
            "status": "success",
            "message": "Project saved successfully to your library!",
            "saved_id": saved_id
        })

    flash("Project successfully saved to your collection!", "success")
    return redirect(url_for('view_saved'))

@app.route('/saved')
def view_saved():
    """Renders the Saved Projects library page."""
    user_id = session.get('user_id')
    saved_projects = get_saved_projects(user_id)
    return render_template('saved.html', saved_projects=saved_projects)

@app.route('/delete_saved/<int:saved_id>', methods=['POST'])
def delete_saved(saved_id):
    """Deletes a saved project entry."""
    success = delete_saved_project(saved_id)
    if request.is_json:
        return jsonify({"status": "success" if success else "error"})
    
    if success:
        flash("Saved project removed successfully.", "info")
    else:
        flash("Failed to remove saved project.", "warning")
    return redirect(url_for('view_saved'))

# --- ADMIN PANEL ROUTES ---

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Handles admin login authentication."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == 'admin123':
            session['is_admin'] = True
            flash("Welcome back, Admin!", "success")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid username or password. Please try again.", "danger")

    return render_template('admin.html', login_mode=True)

@app.route('/admin/logout')
def admin_logout():
    """Logs out the admin session."""
    session.pop('is_admin', None)
    flash("Admin logged out successfully.", "info")
    return redirect(url_for('index'))

@app.route('/admin')
def admin_dashboard():
    """Admin Management Dashboard for managing project ideas and viewing analytics."""
    if not session.get('is_admin'):
        return render_template('admin.html', login_mode=True)

    projects = get_all_projects()
    stats = get_admin_stats()
    return render_template('admin.html', login_mode=False, projects=projects, stats=stats, domains=AVAILABLE_DOMAINS, difficulties=DIFFICULTY_LEVELS)

@app.route('/admin/project/add', methods=['POST'])
def admin_add_project():
    """Admin handler to insert a new project idea."""
    if not session.get('is_admin'):
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    domain = request.form.get('domain')
    title = request.form.get('title')
    description = request.form.get('description')
    technologies = request.form.get('technologies')
    difficulty = request.form.get('difficulty')
    duration = request.form.get('duration', '4-6 Weeks')
    
    steps_raw = request.form.get('steps', '')
    steps = [s.strip() for s in steps_raw.split('\n') if s.strip()] if steps_raw else ["Requirement Analysis", "Design", "Implementation", "Testing"]
    
    enhancements_raw = request.form.get('enhancements', '')
    enhancements = [e.strip() for e in enhancements_raw.split('\n') if e.strip()] if enhancements_raw else ["Cloud deployment", "CI/CD Integration"]

    add_project(domain, title, description, technologies, difficulty, duration, steps, enhancements)
    flash(f"Project '{title}' added successfully!", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/project/edit/<int:project_id>', methods=['POST'])
def admin_edit_project(project_id):
    """Admin handler to update an existing project idea."""
    if not session.get('is_admin'):
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    domain = request.form.get('domain')
    title = request.form.get('title')
    description = request.form.get('description')
    technologies = request.form.get('technologies')
    difficulty = request.form.get('difficulty')
    duration = request.form.get('duration', '4-6 Weeks')
    
    steps_raw = request.form.get('steps', '')
    steps = [s.strip() for s in steps_raw.split('\n') if s.strip()] if steps_raw else []
    
    enhancements_raw = request.form.get('enhancements', '')
    enhancements = [e.strip() for e in enhancements_raw.split('\n') if e.strip()] if enhancements_raw else []

    update_project(project_id, domain, title, description, technologies, difficulty, duration, steps, enhancements)
    flash(f"Project #{project_id} updated successfully!", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/project/delete/<int:project_id>', methods=['POST'])
def admin_delete_project(project_id):
    """Admin handler to delete a project idea."""
    if not session.get('is_admin'):
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    delete_project(project_id)
    flash("Project deleted successfully.", "info")
    return redirect(url_for('admin_dashboard'))

@app.route('/api/stats')
def api_stats():
    """API returning system statistics for dynamic dashboard updates."""
    stats = get_admin_stats()
    return jsonify(stats)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html', error="404 Page Not Found", stats=get_admin_stats(), domains=AVAILABLE_DOMAINS), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('index.html', error="500 Internal Server Error", stats=get_admin_stats(), domains=AVAILABLE_DOMAINS), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
