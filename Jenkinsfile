pipeline {
    agent any

    environment {
        PYTHON_PATH = 'python'
        PROJECT_NAME = 'AI_Project_Idea_Generator'
    }

    stages {
        stage('Checkout') {
            steps {
                echo "=========================================="
                echo " Stage 1: Checkout Repository from GitHub"
                echo "=========================================="
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "=========================================="
                echo " Stage 2: Installing Python Requirements"
                echo "=========================================="
                bat 'python -m pip install --upgrade pip'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                echo "=========================================="
                echo " Stage 3: Executing Pytest Test Suite"
                echo "=========================================="
                bat 'python -m pytest tests/ -v'
            }
        }

        stage('Build Verification') {
            steps {
                echo "=========================================="
                echo " Stage 4: Verifying Application Compilation"
                echo "=========================================="
                bat 'python -m py_compile app.py database.py models.py'
                echo "✅ Compilation check passed successfully."
            }
        }

        stage('Deployment Simulation') {
            steps {
                echo "=========================================="
                echo " Stage 5: Simulating Production Deployment"
                echo "=========================================="
                echo "🚀 Preparing deployment artifact..."
                echo "📦 Checking database file readiness at database/projectideas.db..."
                bat 'python -c "import database; database.init_db(); print(\'Database verification successful.\')"'
                echo "🎉 DEPLOYMENT SUCCESSFUL: AI-Powered Project Idea Generator is production ready!"
            }
        }
    }

    post {
        always {
            echo "Pipeline run completed."
        }
        success {
            echo "✅ Jenkins Pipeline Status: SUCCESS! All stages passed cleanly."
        }
        failure {
            echo "❌ Jenkins Pipeline Status: FAILED! Check build logs for details."
        }
    }
}
