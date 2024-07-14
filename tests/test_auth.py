from tests import BaseTestCase
import json

class AuthTestCase(BaseTestCase):

    # Register User Check
    def test_register(self):
        response = self.client.post('/api/v1/auth/register', json={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass'
        })
        print("Register Status Code:", response.status_code)
        self.assertEqual(response.status_code, 201)
        self.assertIn('User Created', str(response.data))

    # Correct Credentials Check
    def test_login(self):
        self.client.post('/api/v1/auth/register', json={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass'
        })
        response = self.client.post('/api/v1/auth/login', json={
            'email': 'testuser@example.com',
            'password': 'testpass'
        })
        print("Login Status Code:", response.status_code)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access', data['user'])

    # Wrong Credentials Check
    def test_login_wrong(self):
        self.client.post('/api/v1/auth/register', json={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass'
        })
        response = self.client.post('/api/v1/auth/login', json={
            'email': 'testuser@example.com',
            'password': 'test'
        })
        print("Login With Wrong Credentials Status Code:", response.status_code)
        self.assertEqual(response.status_code, 401)


    # Protected Endpoint Check
    def test_protected_endpoint(self):
        self.client.post('/api/v1/auth/register', json={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass'
        })
        login_response = self.client.post('/api/v1/auth/login', json={
            'email': 'testuser@example.com',
            'password': 'testpass'
        })
        token = json.loads(login_response.data)['user']['access']
        response = self.client.get('/api/v1/auth/me', headers={
            'Authorization': f'Bearer {token}'
        })
        print("Protected Endpoint Status Code:", response.status_code)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['username'], 'testuser')
