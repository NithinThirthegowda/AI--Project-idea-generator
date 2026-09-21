import json
import re
from database import get_db_connection

def get_or_create_user(name):
    """Finds an existing user by name or creates a new user record."""
    name = name.strip() if name else "Guest Student"
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Users WHERE LOWER(name) = LOWER(?);", (name,))
    user = cursor.fetchone()
    
    if not user:
        cursor.execute("INSERT INTO Users (name) VALUES (?);", (name,))
        conn.commit()
        cursor.execute("SELECT * FROM Users WHERE id = LAST_INSERT_ROWID();")
        user = cursor.fetchone()
        
    user_dict = dict(user)
    conn.close()
    return user_dict

def get_all_projects():
    """Retrieves all projects from database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Projects ORDER BY id DESC;")
    rows = cursor.fetchall()
    conn.close()
    
    projects = []
    for r in rows:
        p = dict(r)
        p["implementation_steps"] = json.loads(p["implementation_steps"]) if isinstance(p["implementation_steps"], str) else p["implementation_steps"]
        p["future_enhancements"] = json.loads(p["future_enhancements"]) if isinstance(p["future_enhancements"], str) else p["future_enhancements"]
        projects.append(p)
    return projects

def get_project_by_id(project_id):
    """Retrieves a single project by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Projects WHERE id = ?;", (project_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    p = dict(row)
    p["implementation_steps"] = json.loads(p["implementation_steps"]) if isinstance(p["implementation_steps"], str) else p["implementation_steps"]
    p["future_enhancements"] = json.loads(p["future_enhancements"]) if isinstance(p["future_enhancements"], str) else p["future_enhancements"]
    return p

def recommend_projects(domain, skills="", difficulty="All"):
    """
    Intelligent Recommendation Engine:
    - Filters candidate projects by domain and difficulty.
    - Scores relevance based on matching skill keywords.
    - Guarantees at least 5 top-ranked project recommendations.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query database for candidates
    if domain == "All" or not domain:
        cursor.execute("SELECT * FROM Projects;")
    else:
        cursor.execute("SELECT * FROM Projects WHERE LOWER(domain) = LOWER(?);", (domain,))
        
    candidates = [dict(r) for r in cursor.fetchall()]
    
    # Fallback if domain candidates are fewer than 5: pull additional projects across all domains
    if len(candidates) < 5:
        cursor.execute("SELECT * FROM Projects WHERE LOWER(domain) != LOWER(?) LIMIT 10;", (domain or "",))
        extra = [dict(r) for r in cursor.fetchall()]
        candidates.extend(extra)

    conn.close()

    # Parse user skills list
    skill_list = [s.strip().lower() for s in re.split(r'[,; ]+', skills) if s.strip()]

    scored_projects = []
    for p in candidates:
        score = 0
        
        # Difficulty matching score
        if difficulty and difficulty != "All":
            if p["difficulty"].lower() == difficulty.lower():
                score += 10
            elif (difficulty == "Intermediate" and p["difficulty"] in ["Beginner", "Advanced"]):
                score += 5

        # Domain match bonus
        if domain and domain.lower() == p["domain"].lower():
            score += 20

        # Skill matching score
        tech_text = (p["technologies"] + " " + p["title"] + " " + p["description"]).lower()
        for skill in skill_list:
            if skill in tech_text:
                score += 8

        # Parse JSON fields safely
        try:
            p["implementation_steps"] = json.loads(p["implementation_steps"]) if isinstance(p["implementation_steps"], str) else p["implementation_steps"]
        except Exception:
            p["implementation_steps"] = ["Define core requirements.", "Design architecture.", "Develop prototype.", "Perform testing."]

        try:
            p["future_enhancements"] = json.loads(p["future_enhancements"]) if isinstance(p["future_enhancements"], str) else p["future_enhancements"]
        except Exception:
            p["future_enhancements"] = ["Deploy to cloud infrastructure.", "Add automated CI/CD pipeline."]

        p["match_score"] = score
        scored_projects.append(p)

    # Sort by match score descending
    scored_projects.sort(key=lambda x: x["match_score"], reverse=True)

    # Return at least top 5 recommendations
    recommendations = scored_projects[:5]

    # Dynamic fallback generation if fewer than 5 unique titles returned
    if len(recommendations) < 5:
        needed = 5 - len(recommendations)
        all_projects = get_all_projects()
        existing_ids = {p["id"] for p in recommendations}
        for item in all_projects:
            if item["id"] not in existing_ids:
                item["match_score"] = 5
                recommendations.append(item)
                if len(recommendations) >= 5:
                    break

    return recommendations

def save_project(user_id, project_id):
    """Saves a project recommendation to the user's saved library."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if already saved
    cursor.execute("SELECT * FROM SavedProjects WHERE user_id = ? AND project_id = ?;", (user_id, project_id))
    existing = cursor.fetchone()
    
    if not existing:
        cursor.execute("INSERT INTO SavedProjects (user_id, project_id) VALUES (?, ?);", (user_id, project_id))
        conn.commit()
        saved_id = cursor.lastrowid
    else:
        saved_id = existing["id"]
        
    conn.close()
    return saved_id

def get_saved_projects(user_id=None):
    """Fetches all saved projects along with associated user and project information."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if user_id:
        query = '''
            SELECT sp.id as saved_id, sp.saved_at, u.id as user_id, u.name as user_name, p.*
            FROM SavedProjects sp
            JOIN Users u ON sp.user_id = u.id
            JOIN Projects p ON sp.project_id = p.id
            WHERE u.id = ?
            ORDER BY sp.saved_at DESC;
        '''
        cursor.execute(query, (user_id,))
    else:
        query = '''
            SELECT sp.id as saved_id, sp.saved_at, u.id as user_id, u.name as user_name, p.*
            FROM SavedProjects sp
            JOIN Users u ON sp.user_id = u.id
            JOIN Projects p ON sp.project_id = p.id
            ORDER BY sp.saved_at DESC;
        '''
        cursor.execute(query)
        
    rows = cursor.fetchall()
    conn.close()
    
    saved_list = []
    for r in rows:
        item = dict(r)
        try:
            item["implementation_steps"] = json.loads(item["implementation_steps"]) if isinstance(item["implementation_steps"], str) else item["implementation_steps"]
        except Exception:
            item["implementation_steps"] = []
            
        try:
            item["future_enhancements"] = json.loads(item["future_enhancements"]) if isinstance(item["future_enhancements"], str) else item["future_enhancements"]
        except Exception:
            item["future_enhancements"] = []
            
        saved_list.append(item)
        
    return saved_list

def delete_saved_project(saved_id):
    """Deletes a saved project entry by saved_id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM SavedProjects WHERE id = ?;", (saved_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

def add_project(domain, title, description, technologies, difficulty, duration="4-6 Weeks", steps=None, enhancements=None):
    """Adds a new project entry to the database (Admin feature)."""
    if steps is None:
        steps = ["Requirement Gathering", "System Design", "Implementation", "Testing & Verification"]
    if enhancements is None:
        enhancements = ["Cloud Deployment", "Mobile App Extension"]
        
    steps_json = json.dumps(steps) if isinstance(steps, list) else steps
    enhancements_json = json.dumps(enhancements) if isinstance(enhancements, list) else enhancements

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Projects (domain, title, description, technologies, difficulty, duration, implementation_steps, future_enhancements)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    ''', (domain, title, description, technologies, difficulty, duration, steps_json, enhancements_json))
    
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def update_project(project_id, domain, title, description, technologies, difficulty, duration, steps, enhancements):
    """Updates an existing project in the database (Admin feature)."""
    steps_json = json.dumps(steps) if isinstance(steps, list) else steps
    enhancements_json = json.dumps(enhancements) if isinstance(enhancements, list) else enhancements

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Projects
        SET domain = ?, title = ?, description = ?, technologies = ?, difficulty = ?, duration = ?, implementation_steps = ?, future_enhancements = ?
        WHERE id = ?;
    ''', (domain, title, description, technologies, difficulty, duration, steps_json, enhancements_json, project_id))
    
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated

def delete_project(project_id):
    """Deletes a project entry from database (Admin feature)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Projects WHERE id = ?;", (project_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

def log_generation(user_name, domain, skills, difficulty):
    """Logs project generation statistics."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO GenerationLogs (user_name, domain, skills, difficulty)
        VALUES (?, ?, ?, ?);
    ''', (user_name, domain, skills, difficulty))
    conn.commit()
    conn.close()

def get_admin_stats():
    """Retrieves high-level application statistics for the admin dashboard."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Users;")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Projects;")
    total_projects = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM SavedProjects;")
    total_saved = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM GenerationLogs;")
    total_generations = cursor.fetchone()[0]

    # Domain breakdown statistics
    cursor.execute('''
        SELECT domain, COUNT(*) as count 
        FROM GenerationLogs 
        GROUP BY domain 
        ORDER BY count DESC;
    ''')
    domain_stats = [dict(r) for r in cursor.fetchall()]

    conn.close()

    return {
        "total_users": total_users,
        "total_projects": total_projects,
        "total_saved": total_saved,
        "total_generations": total_generations,
        "domain_stats": domain_stats
    }
