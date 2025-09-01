from flask import Flask, jsonify, render_template_string
import os
from datetime import datetime

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['ENV'] = os.environ.get('FLASK_ENV', 'development')

# Simple HTML template for the home page
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Flask CI/CD Demo App</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .info { background: #e7f3ff; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .endpoint { background: #f0f0f0; padding: 10px; margin: 10px 0; border-radius: 5px; }
        .status { color: #28a745; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Flask CI/CD Demo Application</h1>
        <div class="info">
            <h3>Application Status: <span class="status">Running</span></h3>
            <p><strong>Environment:</strong> {{ env }}</p>
            <p><strong>Current Time:</strong> {{ current_time }}</p>
            <p><strong>Version:</strong> 1.0.0</p>
        </div>
        
        <h3>Available Endpoints:</h3>
        <div class="endpoint">
            <strong>GET /</strong> - This home page
        </div>
        <div class="endpoint">
            <strong>GET /health</strong> - Health check endpoint
        </div>
        <div class="endpoint">
            <strong>GET /api/status</strong> - API status in JSON format
        </div>
        <div class="endpoint">
            <strong>GET /api/info</strong> - Application information
        </div>
        
        <div class="info">
            <h4>CI/CD Pipeline Features:</h4>
            <ul>
                <li>✅ Automated testing with pytest</li>
                <li>✅ Jenkins pipeline integration</li>
                <li>✅ GitHub Actions workflow</li>
                <li>✅ Docker containerization ready</li>
                <li>✅ Environment-based configuration</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Home page with application information"""
    return render_template_string(
        HOME_TEMPLATE,
        env=app.config['ENV'],
        current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'environment': app.config['ENV']
    }), 200

@app.route('/api/status')
def api_status():
    """API status endpoint"""
    return jsonify({
        'application': 'Flask CI/CD Demo',
        'version': '1.0.0',
        'status': 'running',
        'environment': app.config['ENV'],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/info')
def api_info():
    """Application information endpoint"""
    return jsonify({
        'name': 'Flask CI/CD Demo Application',
        'description': 'A sample Flask application demonstrating CI/CD pipelines with Jenkins and GitHub Actions',
        'version': '1.0.0',
        'author': 'DevOps Team',
        'endpoints': [
            {'path': '/', 'method': 'GET', 'description': 'Home page'},
            {'path': '/health', 'method': 'GET', 'description': 'Health check'},
            {'path': '/api/status', 'method': 'GET', 'description': 'API status'},
            {'path': '/api/info', 'method': 'GET', 'description': 'Application info'}
        ],
        'features': [
            'Automated testing with pytest',
            'Jenkins pipeline integration',
            'GitHub Actions workflow',
            'Docker containerization ready',
            'Environment-based configuration'
        ]
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource was not found',
        'status_code': 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An internal server error occurred',
        'status_code': 500
    }), 500

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
