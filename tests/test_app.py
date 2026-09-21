import pytest
import os
import sys
import tempfile
import sqlite3

# Ensure app directory is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
import database
from models import (
    get_or_create_user,
    recommend_projects,
    save_project,
    get_saved_projects,
    delete_saved_project,
    add_project,
    get_all_projects
)

@pytest.fixture
def client():
    """Sets up a Flask test client with an isolated temporary SQLite database."""
    db_fd, db_path = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'

    # Override database path for isolated testing
    database.DB_PATH = db_path

    with app.app_context():
        database.init_db()

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(db_path)

def test_homepage_loading(client):
    """Test 1: Verify homepage loads with HTTP 200 status code."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'IdeaGen AI' in response.data
    assert b'Discover Your Next' in response.data

def test_database_connection(client):
    """Test 2: Verify SQLite database connectivity and pre-seeded data loading."""
    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    # Query Projects table
    cursor.execute("SELECT COUNT(*) FROM Projects;")
    count = cursor.fetchone()[0]
    conn.close()
    
    assert count >= 20, "Database should contain at least 20 seeded project ideas."

def test_project_generation(client):
    """Test 3: Verify POST /generate processes input and returns 5+ recommendations."""
    payload = {
        'student_name': 'Test Student',
        'domain': 'Cybersecurity',
        'skills': 'Python, Flask, SQL',
        'difficulty': 'Intermediate'
    }
    response = client.post('/generate', data=payload, follow_redirects=True)
    assert response.status_code == 200
    assert b'Recommended Projects for' in response.data
    assert b'Test Student' in response.data
    assert b'Cybersecurity' in response.data

def test_admin_login_success_and_failure(client):
    """Test 4: Verify Admin login authentication logic."""
    # Test invalid credentials
    bad_login = client.post('/admin/login', data={'username': 'admin', 'password': 'wrongpassword'}, follow_redirects=True)
    assert b'Invalid username or password' in bad_login.data

    # Test valid credentials
    good_login = client.post('/admin/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
    assert b'Administrator Management Console' in good_login.data
    assert b'Welcome back, Admin!' in good_login.data

def test_save_and_delete_project_feature(client):
    """Test 5: Verify saving project recommendation and deleting saved entry."""
    with app.app_context():
        # Create test user and project
        user = get_or_create_user("SaveTestUser")
        projects = get_all_projects()
        assert len(projects) > 0
        target_project = projects[0]

        # Save project
        saved_id = save_project(user['id'], target_project['id'])
        assert saved_id is not None

        # Verify saved project retrieved
        saved_list = get_saved_projects(user['id'])
        assert len(saved_list) >= 1
        assert saved_list[0]['title'] == target_project['title']

        # Delete saved project
        deleted = delete_saved_project(saved_id)
        assert deleted is True

        # Verify list is updated
        updated_list = get_saved_projects(user['id'])
        assert len(updated_list) == 0

def test_saved_projects_route(client):
    """Test 6: Verify GET /saved page renders properly."""
    response = client.get('/saved')
    assert response.status_code == 200
    assert b'Your Saved Project Library' in response.data
