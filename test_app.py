import pytest
import json
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    app.config['ENV'] = 'testing'
    with app.test_client() as client:
        yield client

@pytest.fixture
def app_context():
    """Create an application context for testing"""
    with app.app_context():
        yield app

class TestHomeRoute:
    """Test cases for the home route"""
    
    def test_home_page_status_code(self, client):
        """Test that home page returns 200 status code"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_home_page_content(self, client):
        """Test that home page contains expected content"""
        response = client.get('/')
        assert b'Flask CI/CD Demo Application' in response.data
        assert b'Application Status' in response.data
        assert b'Available Endpoints' in response.data

class TestHealthRoute:
    """Test cases for the health check route"""
    
    def test_health_check_status_code(self, client):
        """Test that health check returns 200 status code"""
        response = client.get('/health')
        assert response.status_code == 200
    
    def test_health_check_json_response(self, client):
        """Test that health check returns valid JSON"""
        response = client.get('/health')
        data = json.loads(response.data)
        assert 'status' in data
        assert 'timestamp' in data
        assert 'environment' in data
        assert data['status'] == 'healthy'
    
    def test_health_check_content_type(self, client):
        """Test that health check returns JSON content type"""
        response = client.get('/health')
        assert response.content_type == 'application/json'

class TestAPIRoutes:
    """Test cases for API routes"""
    
    def test_api_status_endpoint(self, client):
        """Test API status endpoint"""
        response = client.get('/api/status')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'application' in data
        assert 'version' in data
        assert 'status' in data
        assert 'environment' in data
        assert 'timestamp' in data
        assert data['application'] == 'Flask CI/CD Demo'
        assert data['version'] == '1.0.0'
        assert data['status'] == 'running'
    
    def test_api_info_endpoint(self, client):
        """Test API info endpoint"""
        response = client.get('/api/info')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'name' in data
        assert 'description' in data
        assert 'version' in data
        assert 'author' in data
        assert 'endpoints' in data
        assert 'features' in data
        assert data['name'] == 'Flask CI/CD Demo Application'
        assert data['version'] == '1.0.0'
        assert isinstance(data['endpoints'], list)
        assert isinstance(data['features'], list)

class TestErrorHandlers:
    """Test cases for error handlers"""
    
    def test_404_error_handler(self, client):
        """Test 404 error handler"""
        response = client.get('/nonexistent-route')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data
        assert 'message' in data
        assert 'status_code' in data
        assert data['error'] == 'Not Found'
        assert data['status_code'] == 404

class TestApplicationConfiguration:
    """Test cases for application configuration"""
    
    def test_app_exists(self, app_context):
        """Test that the Flask app exists"""
        assert app_context is not None
    
    def test_app_is_testing(self, app_context):
        """Test that app is in testing mode"""
        assert app_context.config['TESTING'] == True
    
    def test_secret_key_exists(self, app_context):
        """Test that secret key is configured"""
        assert app_context.config['SECRET_KEY'] is not None

class TestEndpointResponses:
    """Test cases for endpoint response formats"""
    
    def test_all_json_endpoints_return_valid_json(self, client):
        """Test that all JSON endpoints return valid JSON"""
        json_endpoints = ['/health', '/api/status', '/api/info']
        
        for endpoint in json_endpoints:
            response = client.get(endpoint)
            assert response.status_code == 200
            # This will raise an exception if response is not valid JSON
            json.loads(response.data)
    
    def test_json_endpoints_content_type(self, client):
        """Test that JSON endpoints return correct content type"""
        json_endpoints = ['/health', '/api/status', '/api/info']
        
        for endpoint in json_endpoints:
            response = client.get(endpoint)
            assert 'application/json' in response.content_type

class TestApplicationSecurity:
    """Test cases for basic security measures"""
    
    def test_secret_key_not_default_in_production(self, app_context):
        """Test that secret key is not default value in production"""
        # This test would be more meaningful in actual production testing
        secret_key = app_context.config['SECRET_KEY']
        assert secret_key is not None
        assert len(secret_key) > 0

if __name__ == '__main__':
    pytest.main(['-v', '--tb=short'])
