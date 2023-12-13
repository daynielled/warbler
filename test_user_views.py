import unittest
from flask import Flask
from models import create_app, db, User

class UserViewsTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_user_view_route(self):
        # Assuming you have a route for viewing a specific user
        response = self.client.get('/users/1')  # Adjust the URL as needed

        self.assertEqual(response.status_code, 200)
        # Add more assertions based on your specific views...

   
    def test_user_signup(self):
        response = self.client.post('/signup', data=dict(
            username='newuser',
            email='newuser@example.com',
            password='newuserpassword',
            image_url='newuser.jpg'
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, newuser!', response.data)
        # Add more assertions based on your specific views...

    def test_user_login(self):
        user = User.signup(username='testuser', email='test@example.com', password='testpassword', image_url='test.jpg')
        db.session.commit()

        response = self.client.post('/login', data=dict(
            username='testuser',
            password='testpassword',
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, testuser!', response.data)
        
if __name__ == '__main__':
    unittest.main()
