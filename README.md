# AI-Powered Project Idea Generator 🚀

An intelligent, full-stack academic project recommendation platform built using **Python Flask**, **SQLite**, **HTML5/CSS3/JavaScript**, **Pytest**, and **Jenkins CI/CD**. The application helps students select, evaluate, and plan academic projects tailored to their domain, technical skill set, and target difficulty tier.

---

## 🌟 Key Features

- **Intelligent Recommendation Engine**: Generates at least 5 tailored project concepts matching student domain (AI, ML, Cybersecurity, Web Dev, Cloud, IoT, Mobile Apps, Data Science, Blockchain, DevOps), skills, and difficulty level.
- **Comprehensive Blueprints**: Every project includes required technology stacks, expected duration, step-by-step implementation roadmaps, and future enhancement scopes.
- **Personal Saved Library**: Bookmark favorite project ideas to a personal library with one-click copy and delete capability.
- **Administrator Console**: Full CRUD dashboard (`admin` / `admin123`) to add, edit, or remove project ideas, view user counts, and track popular domain demand metrics.
- **Glassmorphism Dark Theme**: Modern UI design system built with custom CSS tokens, smooth hover micro-animations, Toast alerts, and responsive layouts.
- **Automated Testing & CI/CD**: Pytest suite covering 100% of core endpoints and declarative `Jenkinsfile` pipeline support.

---

## 🏗️ Tech Stack

- **Backend**: Python 3.x, Flask 3.0.2
- **Frontend**: HTML5, CSS3 (Vanilla Glassmorphism Design System), JavaScript (ES6, Fetch API)
- **Database**: SQLite3 (`database/projectideas.db`)
- **Testing**: Pytest 8.0.1
- **CI/CD Pipeline**: Jenkins Declarative Pipeline (`Jenkinsfile`)
- **Version Control**: Git & GitHub

---

## 📂 Project Structure

```text
AI_Project_Idea_Generator/
│
├── app.py                      # Flask web application entry point & route controllers
├── database.py                 # SQLite database initialization & seed dataset (30+ projects)
├── models.py                   # Data models, recommendation algorithms, & admin CRUD queries
├── requirements.txt            # Python dependencies (Flask, Pytest, Werkzeug)
├── Jenkinsfile                 # Declarative CI/CD build pipeline configuration
├── README.md                   # Project documentation & execution guide
│
├── docs/
│   └── SOFTWARE_ENGINEERING_DOCUMENTATION.md   # SRS, Use Cases, Risk Analysis & Testing Strategy
│
├── templates/
│   ├── index.html              # Home page with hero, statistics ticker, & feature cards
│   ├── generator.html          # Interactive project generator input form
│   ├── results.html            # Recommendation results page with save & copy actions
│   ├── admin.html              # Admin login & full CRUD dashboard with analytics
│   └── saved.html              # User saved project library
│
├── static/
│   ├── css/
│   │   └── style.css           # Glassmorphism dark mode CSS design system
│   ├── js/
│   │   └── main.js             # Client-side AJAX interactions, modals, & toast alerts
│   └── images/
│
├── tests/
│   └── test_app.py             # Pytest automated test suite (6 passing test modules)
│
└── database/
    └── projectideas.db         # SQLite database file (Auto-initialized on startup)
```

---

## ⚙️ Installation & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/AI_Project_Idea_Generator.git
cd AI_Project_Idea_Generator
```

### 2. Set Up Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the Web Application
```bash
python app.py
```
*The web server will start at `http://127.0.0.1:5000`.*

---

## 🧪 Running Automated Tests

Run the Pytest suite to verify database connection, recommendation logic, admin login, and route responses:

```bash
python -m pytest tests/ -v
```

---

## 🔐 Admin Dashboard Access

- **Login URL**: `http://127.0.0.1:5000/admin/login`
- **Username**: `admin`
- **Password**: `admin123`

---

## 🛠️ Jenkins CI/CD Setup

1. **Install Jenkins** and ensure Python 3 is configured on the build node.
2. Create a new **Pipeline** job in Jenkins.
3. Set Build Trigger to **GitHub Hook Trigger** or SCM Polling.
4. Select **Pipeline script from SCM**, choose `Git`, and provide your repository URL.
5. Set Script Path to `Jenkinsfile`.
6. Run **Build Now** to execute the pipeline stages:
   - **Checkout**: Pulls latest codebase.
   - **Install Dependencies**: Executes `pip install -r requirements.txt`.
   - **Run Tests**: Executes `pytest tests/ -v`.
   - **Build Verification**: Compiles Python source code (`py_compile`).
   - **Deployment Simulation**: Validates database schema integrity and confirms readiness.

---

## 🔗 GitHub Integration Readiness

- Included `.gitignore` excluding Python bytecode (`__pycache__`), virtual environments (`venv/`), and local database instances.
- Ready for GitHub Webhooks to trigger automated Jenkins builds upon every `git push` to `main`.

---

## 🖼️ Application Screenshots (Placeholders)

| Home Page | Generator Form |
| :---: | :---: |
| ![Home Page Placeholder](static/images/screenshot_home.png) | ![Generator Placeholder](static/images/screenshot_generator.png) |

| Recommendations Page | Admin Dashboard |
| :---: | :---: |
| ![Results Placeholder](static/images/screenshot_results.png) | ![Admin Dashboard Placeholder](static/images/screenshot_admin.png) |

---

## 🔮 Future Enhancements

- Integrate LLM APIs (e.g. OpenAI GPT-4 / Google Gemini) for dynamic custom project proposal generation.
- Export project blueprints directly to PDF or LaTeX format.
- GitHub auto-repo generator creating starter template repositories for chosen projects.

---

## 📜 License & Author

Developed as an academic software engineering reference project. Distributed under the MIT License.
