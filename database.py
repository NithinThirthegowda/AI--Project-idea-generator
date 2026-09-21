import sqlite3
import os
import json

DB_DIR = os.path.join(os.path.dirname(__file__), 'database')
DB_PATH = os.path.join(DB_DIR, 'projectideas.db')

def get_db_connection():
    """Establishes and returns a SQLite database connection with row factory."""
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR, exist_ok=True)
        
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Initializes schema and seeds initial project ideas if database is empty."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    # Projects Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            technologies TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            duration TEXT DEFAULT '4-6 Weeks',
            implementation_steps TEXT NOT NULL,
            future_enhancements TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    # Saved Projects Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SavedProjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            project_id INTEGER NOT NULL,
            saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users (id) ON DELETE CASCADE,
            FOREIGN KEY (project_id) REFERENCES Projects (id) ON DELETE CASCADE
        );
    ''')

    # Generation Logs (for Admin analytics)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS GenerationLogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            domain TEXT NOT NULL,
            skills TEXT,
            difficulty TEXT NOT NULL,
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    conn.commit()

    # Seed data if Projects table is empty
    cursor.execute("SELECT COUNT(*) FROM Projects;")
    count = cursor.fetchone()[0]
    
    if count == 0:
        seed_projects(cursor)
        conn.commit()

    conn.close()

def seed_projects(cursor):
    """Populates the database with comprehensive pre-seeded project ideas across 10 domains."""
    sample_projects = [
        # Cybersecurity
        {
            "domain": "Cybersecurity",
            "title": "SQL Injection Detector",
            "description": "An automated security scanner tool that parses web application inputs and database queries to detect potential SQL injection vulnerabilities before deployment.",
            "technologies": "Python, Flask, SQLite, Regex, BeautifulSoup",
            "difficulty": "Intermediate",
            "duration": "4 Weeks",
            "steps": json.dumps([
                "Set up Flask web service to accept target URLs and input payloads.",
                "Develop pattern matching engine using customized regex signatures for SQL syntax.",
                "Build automated form parser to extract input fields and test payload vectors.",
                "Implement vulnerability reporting dashboard highlighting injection severity."
            ]),
            "enhancements": json.dumps([
                "Add AI-driven payload generation using machine learning.",
                "Integrate real-time notification alerts via Slack/Email webhook."
            ])
        },
        {
            "domain": "Cybersecurity",
            "title": "Password Strength Analyzer & Hash Cracker Simulator",
            "description": "An interactive security tool that evaluates password entropy, checks against breached databases, and simulates dictionary attack resistance.",
            "technologies": "Python, JavaScript, Cryptography, hashlib, zxcvbn",
            "difficulty": "Beginner",
            "duration": "2-3 Weeks",
            "steps": json.dumps([
                "Implement entropy calculation algorithms based on character set complexity.",
                "Integrate HaveIBeenPwned API to cross-reference exposed password hashes.",
                "Build web interface with real-time strength meter visual feedback.",
                "Develop simulated dictionary benchmark execution timer."
            ]),
            "enhancements": json.dumps([
                "Support GPU-accelerated hash comparison benchmarks.",
                "Generate custom corporate password policy rule validator."
            ])
        },
        {
            "domain": "Cybersecurity",
            "title": "Phishing Detection Tool",
            "description": "A machine learning and rule-based web security application that analyzes email headers, body content, and URL reputation to detect phishing attacks.",
            "technologies": "Python, Scikit-learn, Flask, NLTK, HTML/CSS",
            "difficulty": "Intermediate",
            "duration": "4-5 Weeks",
            "steps": json.dumps([
                "Collect and preprocess phishing and legitimate email datasets.",
                "Extract features like WHOIS lookup data, domain age, SSL certificate, and NLP keywords.",
                "Train Random Forest classifier to categorize emails into safe vs phishing.",
                "Build web portal allowing users to paste URLs or upload .eml files."
            ]),
            "enhancements": json.dumps([
                "Browser extension plugin for Chrome/Firefox real-time protection.",
                "Automated domain lookalike (typosquatting) scanner."
            ])
        },
        {
            "domain": "Cybersecurity",
            "title": "Vulnerability Scanner",
            "description": "A network and open port scanner that identifies active services, outdated software versions, and known CVE risks on local networks.",
            "technologies": "Python, Scapy, Nmap API, SQLite, Bootstrap",
            "difficulty": "Advanced",
            "duration": "6 Weeks",
            "steps": json.dumps([
                "Build ARP/IP scanner using Scapy to discover active network hosts.",
                "Perform TCP/UDP port scanning to identify running services.",
                "Cross-reference banner responses with NVD (National Vulnerability Database) CVE API.",
                "Display network map and severity matrix on dynamic web dashboard."
            ]),
            "enhancements": json.dumps([
                "PDF security audit report generator.",
                "Scheduled recurring automated network scans."
            ])
        },
        {
            "domain": "Cybersecurity",
            "title": "Secure File Sharing System",
            "description": "An end-to-end encrypted file exchange platform featuring self-destructing download links, AES-256 encryption, and zero-knowledge storage.",
            "technologies": "Python, Cryptography (AES-GCM), Flask, SQLite, Web Crypto API",
            "difficulty": "Advanced",
            "duration": "5 Weeks",
            "steps": json.dumps([
                "Implement client-side encryption using Web Crypto API prior to transmission.",
                "Build server-side storage handling ephemeral tokens and download counters.",
                "Design self-destruct mechanism triggered upon timer expiration or max downloads.",
                "Establish zero-knowledge architecture where server never stores master key."
            ]),
            "enhancements": json.dumps([
                "Multi-factor authentication (TOTP) for file access.",
                "Password-protected encrypted file vaults."
            ])
        },

        # Artificial Intelligence
        {
            "domain": "Artificial Intelligence",
            "title": "AI Resume Analyzer & Job Matcher",
            "description": "An intelligent resume evaluation system that extracts key skills, quantifies candidate experience against job descriptions, and provides ATS score feedback.",
            "technologies": "Python, PyPDF2, SpaCy, NLTK, Flask, Chart.js",
            "difficulty": "Intermediate",
            "duration": "4 Weeks",
            "steps": json.dumps([
                "Parse PDF and DOCX resume files into structured text tokens.",
                "Perform Named Entity Recognition (NER) to extract skills, degree, and work history.",
                "Calculate cosine similarity score between resume embedding and job description.",
                "Generate visual improvement suggestions and missing skill keyword alerts."
            ]),
            "enhancements": json.dumps([
                "Automated resume re-formatting tailored for target roles.",
                "Speech-to-text video cover letter analyzer."
            ])
        },
        {
            "domain": "Artificial Intelligence",
            "title": "Smart AI Chatbot with Knowledge Base",
            "description": "A conversational AI assistant backed by custom document indexing (RAG - Retrieval-Augmented Generation) for instant domain knowledge lookup.",
            "technologies": "Python, LangChain, Transformers, SQLite, Flask, JS",
            "difficulty": "Intermediate",
            "duration": "5 Weeks",
            "steps": json.dumps([
                "Build document ingestion pipeline for text, markdown, and PDF files.",
                "Generate vector embeddings and store in lightweight local index.",
                "Develop context retrieval mechanism to query top relevant chunks.",
                "Construct interactive UI with real-time streaming response simulation."
            ]),
            "enhancements": json.dumps([
                "Voice input/output integration.",
                "Multi-language translation support."
            ])
        },
        {
            "domain": "Artificial Intelligence",
            "title": "Sentiment Analysis System for Product Reviews",
            "description": "An NLP web app that ingests customer reviews from e-commerce platforms and classifies sentiment into positive, neutral, or negative with visual insights.",
            "technologies": "Python, VADER, TextBlob, Flask, HTML5, Chart.js",
            "difficulty": "Beginner",
            "duration": "3 Weeks",
            "steps": json.dumps([
                "Build web interface to accept bulk text or CSV product reviews.",
                "Apply text preprocessing (lowercasing, stopword removal, lemmatization).",
                "Perform aspect-based sentiment scoring using NLP libraries.",
                "Render real-time donut charts and key phrase word clouds."
            ]),
            "enhancements": json.dumps([
                "E-commerce API scraping integration (Amazon/eBay).",
                "Automated email summary reports for merchants."
            ])
        },
        {
            "domain": "Artificial Intelligence",
            "title": "AI Interview Assistant",
            "description": "An interactive interview preparation platform that generates technical questions based on candidate profile and provides real-time answer scoring.",
            "technologies": "Python, OpenAI API / Local LLM, Flask, JS Speech Recognition",
            "difficulty": "Advanced",
            "duration": "5 Weeks",
            "steps": json.dumps([
                "Implement user onboarding with domain, skill level, and target job selection.",
                "Generate adaptive mock interview questions dynamically.",
                "Capture audio speech or text answers and evaluate grammar, technical accuracy, and clarity.",
                "Provide detailed feedback report with sample optimal answers."
            ]),
            "enhancements": json.dumps([
                "Webcam facial expression & confidence analysis.",
                "Mock coding sandbox execution environment."
            ])
        },
        {
            "domain": "Artificial Intelligence",
            "title": "Intelligent Recommendation Engine",
            "description": "A collaborative and content-based recommendation system for academic research papers, online courses, and career learning paths.",
            "technologies": "Python, Pandas, NumPy, Scikit-learn, Flask, SQLite",
            "difficulty": "Intermediate",
            "duration": "4 Weeks",
            "steps": json.dumps([
                "Construct user preference vectors and item feature matrices.",
                "Implement Cosine Similarity and Matrix Factorization algorithm.",
                "Develop hybrid recommendation pipeline prioritizing novel content.",
                "Design responsive dashboard with item bookmarking and rating controls."
            ]),
            "enhancements": json.dumps([
                "Real-time clickstream tracking for dynamic vector updates.",
                "Social sharing and group recommendations."
            ])
        },

        # Machine Learning
        {
            "domain": "Machine Learning",
            "title": "Predictive Student Performance Analytics",
            "description": "A predictive analytics web application that estimates student academic outcomes based on attendance, quiz scores, and study habits.",
            "technologies": "Python, Scikit-learn, Flask, Pandas, Matplotlib/Seaborn",
            "difficulty": "Intermediate",
            "duration": "4 Weeks",
            "steps": json.dumps([
                "Gather historical student performance metrics dataset.",
                "Train Gradient Boosting and Linear Regression models.",
                "Build interactive predictor interface where educators input student metrics.",
                "Provide early intervention alerts for at-risk academic performance."
            ]),
            "enhancements": json.dumps([
                "Student study schedule generator based on predicted weak subjects.",
                "Integration with Canvas/Moodle LMS APIs."
            ])
        },
        {
            "domain": "Machine Learning",
            "title": "Image Classification & Object Detector",
            "description": "A computer vision web tool that classifies uploaded images into thousands of categories and draws bounding boxes around detected objects.",
            "technologies": "Python, PyTorch / TensorFlow, OpenCV, Flask, JavaScript",
            "difficulty": "Advanced",
            "duration": "5 Weeks",
            "steps": json.dumps([
                "Load pre-trained ResNet/YOLO model weights.",
                "Build file upload processing pipeline handling image resize and normalization.",
                "Run inference to obtain classification confidence scores and bounding boxes.",
                "Render interactive canvas overlay showing object labels."
            ]),
            "enhancements": json.dumps([
                "Real-time webcam stream processing.",
                "Custom dataset fine-tuning module."
            ])
        },
        {
            "domain": "Machine Learning",
            "title": "House Price Prediction Engine",
            "description": "A regression model application that estimates real estate market values based on location, square footage, amenities, and market trends.",
            "technologies": "Python, XGBoost, Flask, Leaflet JS, Pandas",
            "difficulty": "Beginner",
            "duration": "3 Weeks",
            "steps": json.dumps([
                "Clean housing dataset and perform one-hot encoding for categorical attributes.",
                "Train and tune XGBoost regressor model.",
                "Design map-based UI allowing users to pinpoint location and select parameters.",
                "Display estimated valuation range alongside comparable neighborhood listings."
            ]),
            "enhancements": json.dumps([
                "Mortgage payment calculator integration.",
                "Historical price trend visualization line graphs."
            ])
        },
        {
            "domain": "Machine Learning",
            "title": "Customer Churn Prediction Platform",
            "description": "A machine learning pipeline that identifies subscription customers likely to cancel service, enabling proactive retention strategies.",
            "technologies": "Python, Scikit-learn, Flask, SQLite, Chart.js",
            "difficulty": "Intermediate",
            "duration": "4 Weeks",
            "steps": json.dumps([
                "Preprocess customer usage statistics, billing history, and support tickets.",
                "Train Logistic Regression and Random Forest models.",
                "Calculate feature importance to determine primary churn drivers.",
                "Provide actionable retention offer suggestions based on customer risk tier."
            ]),
            "enhancements": json.dumps([
                "Automated email marketing campaign triggers.",
                "CLV (Customer Lifetime Value) forecasting."
            ])
        },

        # Web Development
        {
            "domain": "Web Development",
            "title": "Portfolio Builder",
            "description": "A customizable, interactive developer portfolio generator that allows students to input project experience and export ready-to-deploy static sites.",
            "technologies": "Python, Flask, HTML5, CSS3, JavaScript, Jinja2",
            "difficulty": "Beginner",
            "duration": "2-3 Weeks",
            "steps": json.dumps([
                "Design responsive, modern portfolio templates with CSS themes.",
                "Build dynamic form collector for bio, skills, projects, and contact info.",
                "Implement real-time preview iframe showing live layout adjustments.",
                "Provide one-click ZIP download containing compiled HTML/CSS/JS files."
            ]),
            "enhancements": json.dumps([
                "GitHub profile auto-sync integration.",
                "Custom domain deployment step-by-step assistant."
            ])
        },
        {
            "domain": "Web Development",
            "title": "Event Management System",
            "description": "A full-stack event creation, ticketing, and attendee tracking web platform with QR code check-in capability.",
            "technologies": "Python, Flask, SQLite, QRCode JS, HTML5, Vanilla CSS",
            "difficulty": "Intermediate",
            "duration": "4 Weeks",
            "steps": json.dumps([
                "Design relational schema for events, organizers, tickets, and attendees.",
                "Build organizer dashboard to publish events and set ticket availability.",
                "Generate unique QR code pass for each confirmed registration.",
                "Develop mobile-friendly scanner interface for event staff check-ins."
            ]),
            "enhancements": json.dumps([
                "Stripe payment gateway integration.",
                "Automated calendar invite (.ics) generation."
            ])
        },
        {
            "domain": "Web Development",
            "title": "Online Quiz Platform",
            "description": "An interactive assessment platform featuring timed quizzes, instant scoring, leaderboard rankings, and detailed analytics.",
            "technologies": "Python, Flask, SQLite, JavaScript (Fetch API), CSS3",
            "difficulty": "Beginner",
            "duration": "3 Weeks",
            "steps": json.dumps([
                "Create quiz schema supporting multiple choice, true/false, and short answer.",
                "Build candidate quiz taking UI with countdown timer and state persistence.",
                "Implement automatic answer verification and score computation.",
                "Render performance summary page with detailed topic breakdown."
            ]),
            "enhancements": json.dumps([
                "Anti-cheating tab-switch detection and timer penalty.",
                "Certificate PDF export upon quiz completion."
            ])
        },
        {
            "domain": "Web Development",
            "title": "Library Management System",
            "description": "A digital library catalog allowing users to search books, request borrows, track due dates, and manage digital inventory.",
            "technologies": "Python, Flask, SQLite, Bootstrap, JavaScript",
            "difficulty": "Beginner",
            "duration": "3 Weeks",
            "steps": json.dumps([
                "Create database tables for books, categories, users, and borrowing transactions.",
                "Build search engine with auto-complete filtering by title, author, or ISBN.",
                "Develop checkout and return workflow with automatic late fee estimation.",
                "Construct admin inventory management table with CSV export."
            ]),
            "enhancements": json.dumps([
                "E-book preview reader integration.",
                "SMS/Email automated due-date reminder system."
            ])
        },
        {
            "domain": "Web Development",
            "title": "Attendance Management System",
            "description": "A digital attendance tracking application for academic institutions supporting facial verification or geolocation pin-based check-in.",
            "technologies": "Python, Flask, SQLite, Geolocation API, Chart.js",
            "difficulty": "Intermediate",
            "duration": "4 Weeks",
            "steps": json.dumps([
                "Create course roster and timetable management backend.",
                "Build student attendance portal with GPS radius verification.",
                "Develop instructor dashboard displaying percentage attendance heatmaps.",
                "Implement warning alerts for low attendance thresholds."
            ]),
            "enhancements": json.dumps([
                "Biometric face recognition check-in.",
                "Automated parent notification portal."
            ])
        },

        # Cloud Computing
        {
            "domain": "Cloud Computing",
            "title": "Multi-Cloud Cost Optimization Dashboard",
            "description": "A centralized dashboard that monitors cloud resource utilization across AWS/Azure and suggests cost-saving reserved instances or idle shutdowns.",
            "technologies": "Python, Flask, AWS Boto3 SDK, Chart.js, SQLite",
            "difficulty": "Advanced",
            "duration": "5-6 Weeks",
            "steps": json.dumps([
                "Connect to cloud provider mock API endpoints or Boto3 SDK.",
                "Fetch compute instance metrics (CPU, Memory, Bandwidth usage).",
                "Apply rule-based heuristics to flag underutilized virtual machines.",
                "Render savings calculator and automated shutdown schedule planner."
            ]),
            "enhancements": json.dumps([
                "Automated slack alert for billing threshold spikes.",
                "Terraform auto-scaling configuration exporter."
            ])
        },
        {
            "domain": "Cloud Computing",
            "title": "Serverless Log Aggregator & Alerting Service",
            "description": "A cloud-native log collection service that parses application logs, detects error spikes, and triggers real-time webhook alerts.",
            "technologies": "Python, AWS Lambda / Flask, Docker, SQLite, Elasticsearch concept",
            "difficulty": "Intermediate",
            "duration": "4 Weeks",
            "steps": json.dumps([
                "Create HTTP ingestion API for client log payloads.",
                "Implement log parser for severity levels (INFO, WARN, ERROR, CRITICAL).",
                "Store logs in structured database and index for quick text search.",
                "Build dynamic alert engine triggering notifications when error rate exceeds threshold."
            ]),
            "enhancements": json.dumps([
                "Anomaly detection on log frequency using machine learning.",
                "S3 bucket cold storage archiving."
            ])
        },

        # Internet of Things
        {
            "domain": "Internet of Things",
            "title": "Smart Home Environmental Monitoring Dashboard",
            "description": "An IoT telemetry hub that collects sensor data (temperature, humidity, air quality) over MQTT/HTTP and renders real-time controls.",
            "technologies": "Python, Flask, MQTT, WebSockets, Chart.js, SQLite",
            "difficulty": "Intermediate",
            "duration": "4 Weeks",
            "steps": json.dumps([
                "Establish MQTT broker listener for incoming IoT device telemetry.",
                "Store continuous time-series data points in SQLite database.",
                "Use WebSockets to stream live sensor updates to browser dashboard.",
                "Build threshold trigger mechanisms (e.g. turn on fan simulation if temp > 30C)."
            ]),
            "enhancements": json.dumps([
                "ESP32 / Raspberry Pi physical hardware integration guide.",
                "Predictive maintenance alert for sensor failure."
            ])
        },
        {
            "domain": "Internet of Things",
            "title": "Smart Parking Space Management System",
            "description": "An IoT-enabled parking monitoring platform that tracks space availability via ultrasonic sensor feeds and provides mobile reservation.",
            "technologies": "Python, Flask, SQLite, HTML5, Leaflet Maps, WebSockets",
            "difficulty": "Intermediate",
            "duration": "4 Weeks",
            "steps": json.dumps([
                "Simulate parking sensor node updates (Occupied/Free status).",
                "Map parking slots visually on dynamic SVG floorplan.",
                "Develop user reservation system with timed expiration.",
                "Provide live occupancy analytics dashboard for garage admins."
            ]),
            "enhancements": json.dumps([
                "License plate recognition camera integration.",
                "Dynamic pricing engine based on peak hour demand."
            ])
        },

        # Mobile App Development
        {
            "domain": "Mobile App Development",
            "title": "Campus Student Companion Mobile App",
            "description": "A cross-platform mobile utility for college students featuring timetable schedules, campus navigation, GPA calculator, and peer noticeboards.",
            "technologies": "Python Flask (Backend API), Flutter / React Native / PWA JS, SQLite",
            "difficulty": "Intermediate",
            "duration": "5 Weeks",
            "steps": json.dumps([
                "Design RESTful API endpoints for schedule, grades, and announcements.",
                "Build responsive Progressive Web Application (PWA) / mobile frontend UI.",
                "Implement offline data caching using IndexedDB / LocalStorage.",
                "Develop GPA calculator module with target grade simulator."
            ]),
            "enhancements": json.dumps([
                "Push notifications for upcoming class deadlines.",
                "Peer-to-peer textbook marketplace."
            ])
        },
        {
            "domain": "Mobile App Development",
            "title": "Fitness & Meal Planner Mobile Application",
            "description": "A personal wellness tracking app for monitoring calorie intake, workout routines, water hydration, and habit consistency.",
            "technologies": "Python Flask, SQLite, HTML5 PWA, Chart.js, Web Storage",
            "difficulty": "Beginner",
            "duration": "3-4 Weeks",
            "steps": json.dumps([
                "Create food database with nutritional calorie macro values.",
                "Build daily workout logger with exercise sets and rep tracker.",
                "Develop interactive progress dashboard showing weight trend lines.",
                "Implement daily goal streak counter and motivational achievements."
            ]),
            "enhancements": json.dumps([
                "Barcode scanning for food packaging items.",
                "Wearable smartwatch step-count sync API."
            ])
        },

        # Data Science
        {
            "domain": "Data Science",
            "title": "Global Climate & Energy Data Visualization Hub",
            "description": "An interactive data science dashboard exploring global carbon emissions, renewable energy adoption, and climate indicators across countries.",
            "technologies": "Python, Pandas, Plotly / Dash, Flask, SQLite",
            "difficulty": "Intermediate",
            "duration": "4 Weeks",
            "steps": json.dumps([
                "Ingest open datasets from World Bank and Our World in Data.",
                "Perform data cleaning, normalization, and time-series aggregation.",
                "Build choropleth world maps and interactive filter controls.",
                "Include statistical trend forecasting using ARIMA / linear regression."
            ]),
            "enhancements": json.dumps([
                "Automated PDF data report exporter.",
                "Country comparison side-by-side benchmark tool."
            ])
        },
        {
            "domain": "Data Science",
            "title": "Financial Market Sentiment & News Analyzer",
            "description": "A financial data pipeline aggregating stock market news, quantifying market sentiment, and correlating tone with price volatility.",
            "technologies": "Python, Pandas, NLTK, YFinance API, Flask, Chart.js",
            "difficulty": "Advanced",
            "duration": "5 Weeks",
            "steps": json.dumps([
                "Fetch real-time stock quotes via YFinance and financial news RSS feeds.",
                "Perform sentiment analysis on headlines using specialized financial lexicon.",
                "Plot sentiment scores against stock price movements over custom timeframes.",
                "Highlight high-volatility news events on interactive charts."
            ]),
            "enhancements": json.dumps([
                "Crypto asset sentiment monitoring.",
                "Automated email digest of top bullish/bearish stocks."
            ])
        },

        # Blockchain
        {
            "domain": "Blockchain",
            "title": "Decentralized Academic Credentials Verification",
            "description": "A blockchain-based solution ensuring tamper-proof verification of university diplomas and certificates using cryptographic hashes.",
            "technologies": "Python, Flask, Web3.py, hashlib, SQLite, Smart Contract concept",
            "difficulty": "Advanced",
            "duration": "5 Weeks",
            "steps": json.dumps([
                "Generate unique SHA-256 cryptographic hashes for academic certificates.",
                "Simulate diploma registration onto immutable ledger block system.",
                "Build public verification portal where employers drop certificate files.",
                "Provide instant cryptographic proof of authenticity."
            ]),
            "enhancements": json.dumps([
                "Ethereum / Polygon testnet deployment.",
                "IPFS decentralized file hosting integration."
            ])
        },
        {
            "domain": "Blockchain",
            "title": "Transparent Supply Chain Tracker",
            "description": "A blockchain ledger prototype tracking product provenance from origin supplier to end consumer with tamper-evident audit trails.",
            "technologies": "Python, Flask, SQLite, SHA-256 Chain, QRCode JS",
            "difficulty": "Intermediate",
            "duration": "4-5 Weeks",
            "steps": json.dumps([
                "Implement custom Python blockchain data structure with SHA-256 proof-of-work.",
                "Create supply chain transaction events (Harvested, Processed, Shipped, Delivered).",
                "Generate QR codes for physical product packaging.",
                "Build public timeline view rendering full product journey."
            ]),
            "enhancements": json.dumps([
                "IoT temperature logger data verification on chain.",
                "Multi-party digital signature sign-off."
            ])
        },

        # DevOps
        {
            "domain": "DevOps",
            "title": "Automated Microservices Health & Uptime Monitor",
            "description": "A DevOps monitoring utility that performs continuous health checks on HTTP endpoints, tracks latency metrics, and generates SLA reports.",
            "technologies": "Python, Flask, APScheduler, Requests, Chart.js, SQLite",
            "difficulty": "Intermediate",
            "duration": "3-4 Weeks",
            "steps": json.dumps([
                "Build endpoint registration UI accepting URL target, method, and check interval.",
                "Implement background scheduled pings measuring response code and latency.",
                "Store metric histories and calculate uptime SLA percentages.",
                "Render real-time status page with response time graphs and incident logs."
            ]),
            "enhancements": json.dumps([
                "Slack, Discord, and Telegram incident alert bots.",
                "SSL certificate expiration tracking."
            ])
        },
        {
            "domain": "DevOps",
            "title": "CI/CD Pipeline Visualization & Failure Predictor",
            "description": "A DevOps analytics portal that parses build logs from Jenkins/GitHub Actions to detect flaky tests and predict deployment failures.",
            "technologies": "Python, Flask, SQLite, Pytest, Regex, Chart.js",
            "difficulty": "Advanced",
            "duration": "5 Weeks",
            "steps": json.dumps([
                "Construct log parser for Jenkins/GitHub build execution logs.",
                "Extract build metrics like stage duration, error stacktraces, and test pass rate.",
                "Identify flaky test candidates based on historic run variance.",
                "Render pipeline visualizer showing bottleneck stages and optimization recommendations."
            ]),
            "enhancements": json.dumps([
                "Webhook receiver for automatic GitHub/Jenkins event processing.",
                "Container build size trend tracking."
            ])
        }
    ]

    for p in sample_projects:
        cursor.execute('''
            INSERT INTO Projects (domain, title, description, technologies, difficulty, duration, implementation_steps, future_enhancements)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (p["domain"], p["title"], p["description"], p["technologies"], p["difficulty"], p["duration"], p["steps"], p["enhancements"]))
