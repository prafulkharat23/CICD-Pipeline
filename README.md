# Flask CI/CD Pipeline Demo

A comprehensive demonstration of CI/CD pipelines using both Jenkins and GitHub Actions for a Flask web application.

## 🚀 Project Overview

This project showcases automated testing and deployment workflows for a Python Flask application using two popular CI/CD platforms:

- **Jenkins Pipeline**: Traditional CI/CD server with declarative pipeline
- **GitHub Actions**: Cloud-native CI/CD with YAML workflows

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Application Structure](#application-structure)
- [Jenkins Setup](#jenkins-setup)
- [GitHub Actions Setup](#github-actions-setup)
- [Testing](#testing)
- [Deployment](#deployment)
- [Docker Support](#docker-support)
- [Environment Configuration](#environment-configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## ✨ Features

### Application Features
- Simple Flask web application with multiple endpoints
- Health check endpoint for monitoring
- RESTful API endpoints
- Environment-based configuration
- Comprehensive error handling
- Security best practices

### CI/CD Features
- **Automated Testing**: Unit tests with pytest and coverage reporting
- **Code Quality**: Linting with flake8, formatting with black, security scanning
- **Multi-Environment Deployment**: Staging and production environments
- **Docker Support**: Containerized application with health checks
- **Notifications**: Email notifications for build status
- **Security Scanning**: Vulnerability detection with multiple tools
- **Parallel Execution**: Optimized pipeline performance

## 🔧 Prerequisites

### General Requirements
- Python 3.8+ installed
- Git installed
- Docker and Docker Compose (optional)
- GitHub account
- Basic knowledge of CI/CD concepts

### For Jenkins Setup
- Jenkins server (local or cloud-based)
- Jenkins plugins:
  - Pipeline
  - Git
  - Email Extension
  - HTML Publisher
  - GitHub Integration

### For GitHub Actions
- GitHub repository
- GitHub Secrets configured (for deployment)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd CICD-Pipeline
```

### 2. Set Up Local Environment
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your configuration
```

### 3. Run the Application
```bash
# Development mode
export FLASK_ENV=development
python app.py

# Or using Docker
docker-compose up --build
```

### 4. Access the Application
- **Local**: http://localhost:5000
- **Health Check**: http://localhost:5000/health
- **API Status**: http://localhost:5000/api/status

## 📁 Application Structure

```
CICD-Pipeline/
├── app.py                 # Main Flask application
├── config.py              # Configuration classes
├── requirements.txt       # Python dependencies
├── test_app.py           # Unit tests
├── pytest.ini           # Pytest configuration
├── Jenkinsfile           # Jenkins pipeline definition
├── .github/
│   └── workflows/
│       └── ci-cd.yml     # GitHub Actions workflow
├── Dockerfile            # Docker container definition
├── docker-compose.yml    # Docker Compose configuration
├── .dockerignore         # Docker ignore file
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## 🔨 Jenkins Setup

### Prerequisites for Jenkins

1. **Install Jenkins**
   ```bash
   # On Ubuntu/Debian
   wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
   sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
   sudo apt update
   sudo apt install jenkins

   # On macOS with Homebrew
   brew install jenkins-lts

   # Using Docker
   docker run -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts
   ```

2. **Required Jenkins Plugins**
   - Pipeline
   - Git Plugin
   - GitHub Integration Plugin
   - Email Extension Plugin
   - HTML Publisher Plugin
   - Workspace Cleanup Plugin

### Jenkins Configuration Steps

1. **Access Jenkins**
   - Open http://localhost:8080
   - Complete initial setup wizard
   - Install recommended plugins

2. **Configure System**
   - Go to "Manage Jenkins" → "Configure System"
   - Set up email notifications:
     ```
     SMTP Server: smtp.gmail.com
     Port: 587
     Username: your-email@gmail.com
     Password: your-app-password
     ```

3. **Create Pipeline Job**
   - Click "New Item"
   - Enter job name: "Flask-CI-CD-Pipeline"
   - Select "Pipeline"
   - In Pipeline section, select "Pipeline script from SCM"
   - Set SCM to Git and enter repository URL
   - Set Script Path to "Jenkinsfile"

4. **Configure GitHub Webhook** (Optional)
   - In GitHub repository settings → Webhooks
   - Add webhook URL: `http://your-jenkins-url/github-webhook/`
   - Select "Just the push event"

### Jenkins Pipeline Stages

The Jenkinsfile defines the following stages:

1. **Checkout**: Clone the repository
2. **Setup Environment**: Create Python virtual environment
3. **Install Dependencies**: Install required packages
4. **Code Quality & Security**: Run linting and security scans
5. **Run Tests**: Execute unit tests with coverage
6. **Build Application**: Test application startup
7. **Deploy to Staging**: Deploy to staging environment
8. **Integration Tests**: Run integration tests
9. **Deploy to Production**: Manual approval for production deployment

### Jenkins Environment Variables

Configure these in Jenkins job or system configuration:
```bash
PYTHON_VERSION=3.9
FLASK_ENV=testing
EMAIL_RECIPIENTS=devops@company.com
```

## 🐙 GitHub Actions Setup

### Prerequisites for GitHub Actions

1. **GitHub Repository**: Ensure your code is in a GitHub repository
2. **GitHub Secrets**: Configure sensitive information in repository secrets

### GitHub Secrets Configuration

Go to your repository → Settings → Secrets and variables → Actions, and add:

```bash
# Deployment secrets (example)
STAGING_HOST=staging.example.com
STAGING_USER=deploy
STAGING_KEY=<private-key-content>

PRODUCTION_HOST=production.example.com
PRODUCTION_USER=deploy
PRODUCTION_KEY=<private-key-content>

# Optional: External service tokens
CODECOV_TOKEN=<your-codecov-token>
SENTRY_DSN=<your-sentry-dsn>
```

### GitHub Actions Workflow

The workflow file `.github/workflows/ci-cd.yml` defines:

#### Jobs Overview
1. **test**: Run tests on multiple Python versions
2. **build**: Build and test application startup
3. **deploy-staging**: Deploy to staging on staging/main branch
4. **deploy-production**: Deploy to production on release
5. **security-scan**: Run security vulnerability scans

#### Workflow Triggers
- **Push**: to main, staging, develop branches
- **Pull Request**: to main, staging branches
- **Release**: when a release is published

#### Features
- **Matrix Testing**: Tests on Python 3.8, 3.9, 3.10
- **Caching**: Pip dependencies cached for faster builds
- **Artifacts**: Build artifacts stored for deployment
- **Security**: Trivy vulnerability scanning
- **Coverage**: Code coverage with Codecov integration

### Branch Strategy

The workflow supports this branching strategy:
- **develop**: Development branch for feature integration
- **staging**: Staging branch for pre-production testing
- **main**: Production-ready code
- **releases**: Tagged releases trigger production deployment

## 🧪 Testing

### Running Tests Locally

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test class
pytest test_app.py::TestHealthRoute -v

# Run with verbose output
pytest -v --tb=short
```

### Test Structure

The test suite includes:
- **Unit Tests**: Test individual functions and endpoints
- **Integration Tests**: Test API endpoints and responses
- **Security Tests**: Basic security validation
- **Configuration Tests**: Environment and config validation

### Coverage Requirements

- Minimum coverage: 80%
- Coverage reports generated in HTML format
- Coverage data uploaded to Codecov (in GitHub Actions)

## 🚀 Deployment

### Deployment Environments

#### Staging Environment
- **Trigger**: Push to `staging` or `main` branch
- **URL**: https://staging.example.com
- **Purpose**: Pre-production testing and validation
- **Auto-deployment**: Yes

#### Production Environment
- **Trigger**: Release tag creation
- **URL**: https://production.example.com
- **Purpose**: Live application serving users
- **Auto-deployment**: Manual approval required

### Deployment Process

1. **Code Push**: Developer pushes to staging/main branch
2. **CI Pipeline**: Automated testing and building
3. **Staging Deployment**: Automatic deployment to staging
4. **Smoke Tests**: Automated verification of staging deployment
5. **Production Release**: Create GitHub release for production deployment
6. **Manual Approval**: Required for production deployment
7. **Production Deployment**: Deploy to production environment
8. **Health Checks**: Verify production deployment

### Deployment Commands (Example)

```bash
# Manual deployment using Docker
docker build -t flask-app:latest .
docker run -d -p 5000:5000 --name flask-app flask-app:latest

# Using Docker Compose
docker-compose up -d

# Health check after deployment
curl -f http://your-domain.com/health
```

## 🐳 Docker Support

### Building the Docker Image

```bash
# Build the image
docker build -t flask-cicd-app .

# Run the container
docker run -p 5000:5000 flask-cicd-app

# Run with environment variables
docker run -p 5000:5000 -e FLASK_ENV=production -e SECRET_KEY=your-secret flask-cicd-app
```

### Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and start
docker-compose up --build
```

### Docker Features

- **Multi-stage builds**: Optimized image size
- **Non-root user**: Security best practices
- **Health checks**: Container health monitoring
- **Environment variables**: Configurable runtime settings

## ⚙️ Environment Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `FLASK_APP` | Flask application entry point | `app.py` | No |
| `FLASK_ENV` | Flask environment | `development` | No |
| `SECRET_KEY` | Flask secret key | `dev-secret-key` | Yes |
| `PORT` | Application port | `5000` | No |
| `DEBUG` | Debug mode | `True` | No |

### Configuration Files

- **`.env.example`**: Template for environment variables
- **`config.py`**: Python configuration classes
- **`pytest.ini`**: Test configuration
- **`docker-compose.yml`**: Docker services configuration

### Setting Up Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit with your values
nano .env

# Load environment variables
source .env
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Jenkins Issues

**Problem**: Jenkins pipeline fails at "Setup Environment" stage
```bash
Solution:
1. Ensure Python 3.8+ is installed on Jenkins agent
2. Check if python3 command is available in PATH
3. Verify Jenkins user has permission to create virtual environments
```

**Problem**: Email notifications not working
```bash
Solution:
1. Configure SMTP settings in Jenkins system configuration
2. Use app-specific passwords for Gmail
3. Test email configuration in Jenkins
```

**Problem**: GitHub webhook not triggering builds
```bash
Solution:
1. Check webhook URL format: http://jenkins-url/github-webhook/
2. Verify Jenkins GitHub plugin is installed
3. Ensure Jenkins is accessible from internet (for GitHub.com)
```

#### GitHub Actions Issues

**Problem**: Workflow fails with "Permission denied" errors
```bash
Solution:
1. Check repository secrets are correctly configured
2. Verify SSH keys have proper permissions
3. Ensure deployment user has necessary access rights
```

**Problem**: Tests fail in GitHub Actions but pass locally
```bash
Solution:
1. Check Python version matrix in workflow
2. Verify all dependencies are in requirements.txt
3. Check for environment-specific issues
```

**Problem**: Deployment step times out
```bash
Solution:
1. Increase timeout values in workflow
2. Check network connectivity to deployment target
3. Verify deployment scripts are executable
```

#### Application Issues

**Problem**: Application fails to start
```bash
Solution:
1. Check environment variables are set correctly
2. Verify all dependencies are installed
3. Check application logs for specific errors
4. Ensure port 5000 is available
```

**Problem**: Tests fail locally
```bash
Solution:
1. Activate virtual environment: source venv/bin/activate
2. Install test dependencies: pip install -r requirements.txt
3. Set test environment: export FLASK_ENV=testing
4. Run tests with verbose output: pytest -v
```

### Debug Commands

```bash
# Check application health
curl -f http://localhost:5000/health

# View application logs
docker logs flask-app

# Check environment variables
env | grep FLASK

# Test database connection (if applicable)
python -c "from app import app; print('App created successfully')"

# Run security scan locally
bandit -r app.py

# Check code formatting
black --check app.py
flake8 app.py
```

## 📊 Monitoring and Logging

### Health Checks

The application provides several monitoring endpoints:

- **`/health`**: Basic health check
- **`/api/status`**: Detailed application status
- **`/api/info`**: Application information and metadata

### Logging

```python
# Application logs are configured in app.py
# Logs include:
# - Request/response information
# - Error details
# - Performance metrics
# - Security events
```

### Metrics Collection

For production deployments, consider integrating:
- **Prometheus**: Metrics collection
- **Grafana**: Metrics visualization
- **Sentry**: Error tracking
- **ELK Stack**: Log aggregation

## 🤝 Contributing

### Development Workflow

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Make changes and add tests**
4. **Run tests locally**: `pytest`
5. **Commit changes**: `git commit -m 'Add amazing feature'`
6. **Push to branch**: `git push origin feature/amazing-feature`
7. **Create Pull Request**

### Code Standards

- **Python**: Follow PEP 8 style guide
- **Testing**: Maintain 80%+ code coverage
- **Documentation**: Update README for significant changes
- **Security**: Run security scans before committing

### Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Add description of changes
4. Request review from maintainers
5. Address review feedback
6. Merge after approval

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Flask framework and community
- Jenkins project and plugin developers
- GitHub Actions team
- Python testing ecosystem (pytest, coverage, etc.)
- Docker and containerization community

## 📞 Support

For questions and support:

- **Issues**: Create a GitHub issue
- **Documentation**: Check this README
- **Community**: Join relevant Discord/Slack channels
- **Email**: Contact the development team

---

## 📸 Screenshots

### Jenkins Pipeline View
![Jenkins Pipeline](docs/images/jenkins-pipeline.png)

### GitHub Actions Workflow
![GitHub Actions](docs/images/github-actions.png)

### Application Dashboard
![Application](docs/images/app-dashboard.png)

---

**Happy Coding! 🚀**
