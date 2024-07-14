from tests import BaseTestCase
import json

class PostsTestCase(BaseTestCase):

    # Function to get auth token to use in the subsequent test cases
    def authenticate(self):
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
        return token

    # Create Post Check
    def test_create_post(self):
        token = self.authenticate()
        response = self.client.post('/api/v1/posts/', json={
            'title': 'Test Post',
            'content': 'This is a test post.'
        }, headers={'Authorization': f'Bearer {token}'})
        print("Create Post Status Code:", response.status_code)
        self.assertEqual(response.status_code, 200)

    # Create Post Check without auth token
    def test_create_post(self):
        token = self.authenticate()
        response = self.client.post('/api/v1/posts/', json={
            'title': 'Test Post',
            'content': 'This is a test post.'
        })
        print("Create Post Invalid Token Status Code:", response.status_code)
        self.assertEqual(response.status_code, 401)

    # Create Post Check without content 
    def test_create_post(self):
        token = self.authenticate()
        response = self.client.post('/api/v1/posts/', json={
            'title': 'Test Post',
            'content': ''
        }, headers={'Authorization': f'Bearer {token}'})
        print("Create Post Invalid Body Status Code:", response.status_code)
        self.assertEqual(response.status_code, 400)

    # Get all posts check
    def test_get_all_posts(self):
        token = self.authenticate()
        response = self.client.get('/api/v1/posts/', headers={'Authorization': f'Bearer {token}'})
        print("Get All Posts Status Code:", response.status_code)
        self.assertEqual(response.status_code, 200)

    # Get post by id check
    def test_get_post_by_id(self):
        token = self.authenticate()
        response = self.client.post('/api/v1/posts/', json={
            'title': 'Test Post',
            'content': 'This is a test post.'
        }, headers={'Authorization': f'Bearer {token}'})
        post_id = json.loads(response.data)['id']
        response = self.client.get(f'/api/v1/posts/{post_id}', headers={'Authorization': f'Bearer {token}'})
        print("Get Post By ID Status Code:", response.status_code)
        self.assertEqual(response.status_code, 200)

    # Get post by invalid id check
    def test_get_post_by_id(self):
        token = self.authenticate()
        response = self.client.post('/api/v1/posts/', json={
            'title': 'Test Post',
            'content': 'This is a test post.'
        }, headers={'Authorization': f'Bearer {token}'})
        post_id = json.loads(response.data)['id'] + 1
        response = self.client.get(f'/api/v1/posts/{post_id}', headers={'Authorization': f'Bearer {token}'})
        print("Get Post By Invalid ID Status Code:", response.status_code)
        self.assertEqual(response.status_code, 404)

    def test_update_post(self):
        token = self.authenticate()
        response = self.client.post('/api/v1/posts/', json={
            'title': 'Test Post',
            'content': 'This is a test post.'
        }, headers={'Authorization': f'Bearer {token}'})
        post_id = json.loads(response.data)['id']
        response = self.client.put(f'/api/v1/posts/{post_id}', json={
            'title': 'Updated Test Post',
            'content': 'This is an updated test post.'
        }, headers={'Authorization': f'Bearer {token}'})
        print("Update Post Status Code:", response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_delete_post(self):
        token = self.authenticate()
        response = self.client.post('/api/v1/posts/', json={
            'title': 'Test Post',
            'content': 'This is a test post.'
        }, headers={'Authorization': f'Bearer {token}'})
        post_id = json.loads(response.data)['id']
        response = self.client.delete(f'/api/v1/posts/{post_id}', headers={'Authorization': f'Bearer {token}'})
        print("Delete Post Status Code:", response.status_code)
        self.assertEqual(response.status_code, 204)
