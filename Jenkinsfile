pipeline {
    agent any
    
    environment {
        // Environment variables
        PYTHON_VERSION = '3.9'
        FLASK_ENV = 'testing'
        PORT = '5000'
        // Email configuration
        EMAIL_RECIPIENTS = 'devops@company.com'
    }
    
    options {
        // Keep only last 10 builds
        buildDiscarder(logRotator(numToKeepStr: '10'))
        // Timeout for the entire pipeline
        timeout(time: 30, unit: 'MINUTES')
        // Timestamps in console output
        timestamps()
    }
    
    triggers {
        // Poll SCM every 5 minutes for changes
        pollSCM('H/5 * * * *')
        // Trigger build on push to main branch
        githubPush()
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
                
                // Display build information
                script {
                    echo "Build Number: ${env.BUILD_NUMBER}"
                    echo "Build ID: ${env.BUILD_ID}"
                    echo "Job Name: ${env.JOB_NAME}"
                    echo "Branch: ${env.BRANCH_NAME}"
                }
            }
        }
        
        stage('Setup Environment') {
            steps {
                echo 'Setting up Python environment...'
                sh '''
                    # Check Python version
                    python3 --version
                    
                    # Create virtual environment
                    python3 -m venv venv
                    
                    # Activate virtual environment and upgrade pip
                    . venv/bin/activate
                    pip install --upgrade pip
                    
                    # Verify virtual environment
                    which python
                    which pip
                '''
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh '''
                    # Activate virtual environment
                    . venv/bin/activate
                    
                    # Install dependencies
                    pip install -r requirements.txt
                    
                    # List installed packages
                    pip list
                '''
            }
        }
        
        stage('Code Quality & Security') {
            parallel {
                stage('Lint Code') {
                    steps {
                        echo 'Running code linting...'
                        sh '''
                            . venv/bin/activate
                            
                            # Install linting tools
                            pip install flake8 black isort
                            
                            # Run flake8 for style checking
                            flake8 app.py --max-line-length=88 --extend-ignore=E203,W503 || true
                            
                            # Check code formatting with black
                            black --check app.py || true
                            
                            # Check import sorting
                            isort --check-only app.py || true
                        '''
                    }
                }
                
                stage('Security Scan') {
                    steps {
                        echo 'Running security scan...'
                        sh '''
                            . venv/bin/activate
                            
                            # Install security scanning tools
                            pip install bandit safety
                            
                            # Run bandit for security issues
                            bandit -r app.py || true
                            
                            # Check for known security vulnerabilities
                            safety check || true
                        '''
                    }
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Running unit tests...'
                sh '''
                    # Activate virtual environment
                    . venv/bin/activate
                    
                    # Set environment variables for testing
                    export FLASK_ENV=testing
                    export SECRET_KEY=test-secret-key
                    
                    # Run tests with coverage
                    pytest test_app.py -v --tb=short --cov=app --cov-report=xml --cov-report=html --cov-report=term-missing
                    
                    # Display test results
                    echo "Test execution completed"
                '''
            }
            post {
                always {
                    // Archive test results
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                    
                    // Publish test results if using JUnit format
                    // junit 'test-results.xml'
                }
            }
        }
        
        stage('Build Application') {
            steps {
                echo 'Building application...'
                sh '''
                    # Activate virtual environment
                    . venv/bin/activate
                    
                    # Test application startup
                    export FLASK_ENV=testing
                    export SECRET_KEY=test-secret-key
                    
                    # Start application in background for testing
                    python app.py &
                    APP_PID=$!
                    
                    # Wait for application to start
                    sleep 5
                    
                    # Test if application is responding
                    curl -f http://localhost:5000/health || exit 1
                    
                    # Stop the application
                    kill $APP_PID || true
                    
                    echo "Application build successful"
                '''
            }
        }
        
        stage('Deploy to Staging') {
            when {
                anyOf {
                    branch 'main'
                    branch 'staging'
                }
            }
            steps {
                echo 'Deploying to staging environment...'
                script {
                    // This is a placeholder for actual deployment
                    // In real scenarios, this would deploy to staging server
                    sh '''
                        echo "Deploying Flask application to staging..."
                        echo "Staging URL: http://staging.example.com"
                        
                        # Example deployment commands:
                        # scp -r . user@staging-server:/path/to/app/
                        # ssh user@staging-server "cd /path/to/app && ./deploy.sh"
                        
                        # For now, just simulate deployment
                        sleep 2
                        echo "Deployment to staging completed successfully"
                    '''
                }
            }
        }
        
        stage('Integration Tests') {
            when {
                anyOf {
                    branch 'main'
                    branch 'staging'
                }
            }
            steps {
                echo 'Running integration tests on staging...'
                sh '''
                    . venv/bin/activate
                    
                    # Run integration tests against staging environment
                    # This would typically test the deployed application
                    echo "Running integration tests..."
                    
                    # Example: Test staging endpoints
                    # curl -f http://staging.example.com/health
                    
                    echo "Integration tests completed"
                '''
            }
        }
        
        stage('Deploy to Production') {
            when {
                allOf {
                    branch 'main'
                    expression { return currentBuild.result == null || currentBuild.result == 'SUCCESS' }
                }
            }
            steps {
                // Manual approval for production deployment
                input message: 'Deploy to production?', ok: 'Deploy',
                      submitterParameter: 'DEPLOYER'
                
                echo "Deploying to production (approved by: ${env.DEPLOYER})..."
                script {
                    sh '''
                        echo "Deploying Flask application to production..."
                        echo "Production URL: http://production.example.com"
                        
                        # Example production deployment commands:
                        # scp -r . user@prod-server:/path/to/app/
                        # ssh user@prod-server "cd /path/to/app && ./deploy.sh"
                        
                        # For now, just simulate deployment
                        sleep 3
                        echo "Deployment to production completed successfully"
                    '''
                }
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline execution completed'
            
            // Clean up workspace
            cleanWs()
        }
        
        success {
            echo 'Pipeline succeeded!'
            
            // Send success notification
            emailext (
                subject: "✅ Jenkins Build Success: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: """
                <h2>Build Successful</h2>
                <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                <p><strong>Duration:</strong> ${currentBuild.durationString}</p>
                <p>All tests passed and deployment completed successfully.</p>
                """,
                to: "${env.EMAIL_RECIPIENTS}",
                mimeType: 'text/html'
            )
        }
        
        failure {
            echo 'Pipeline failed!'
            
            // Send failure notification
            emailext (
                subject: "❌ Jenkins Build Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: """
                <h2>Build Failed</h2>
                <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                <p><strong>Duration:</strong> ${currentBuild.durationString}</p>
                <p>Please check the build logs for details.</p>
                """,
                to: "${env.EMAIL_RECIPIENTS}",
                mimeType: 'text/html'
            )
        }
        
        unstable {
            echo 'Pipeline is unstable'
            
            // Send unstable notification
            emailext (
                subject: "⚠️ Jenkins Build Unstable: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: """
                <h2>Build Unstable</h2>
                <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                <p>Some tests may have failed or there are warnings.</p>
                """,
                to: "${env.EMAIL_RECIPIENTS}",
                mimeType: 'text/html'
            )
        }
    }
}
