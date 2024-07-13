import unittest
from src import create_app, db
from src.database import User, Posts

class PostsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app({
            'TESTING': True,
            'SECRET_KEY': 'test_secret',
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SQL_TRACK_MODIFICATIONS': False,
            'JWT_SECRET_KEY': 'test_jwt_secret'
        })
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.init_database()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def init_database(self):
        posts = Posts(title="Test Posts", content ="Post content")
        db.session.add(posts)
        db.session.commit()

    def test_create_posts(self):
        response = self.client.post('/api/v1/posts', json={
            'title': 'My first blog post',
            'content': 'creating my first blog post ....pending'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['title'], 'My first blog post')

    def test_get_posts(self):
        response = self.client.get('/posts')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['title'], 'My first blog post')

    def test_get_post(self):
        post = Posts.query.first()
        response = self.client.get(f'/posts/{post.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['title'], 'My first blog post')

    def test_update_posts(self):
        post = Posts.query.first()
        response = self.client.put(f'/posts/{post.id}', json={
            'title': 'New title -- updated',
            'content': 'creating my first blog post ....updated'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['title'], 'New title -- updated')

    def test_delete_posts(self):
        post = Posts.query.first()
        response = self.client.delete(f'/posts/{post.id}')
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(Posts.query.get(post.id))

if __name__ == '__main__':
    unittest.main()
