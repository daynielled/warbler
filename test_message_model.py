import unittest
from flask import Flask
from models import db, User, Message

class YourTests(unittest.TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        # Create a test Flask app and connect it to the test database
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///warbler'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['TESTING'] = True

        # Create tables in the database
        with self.app.app_context():
            db.init_app(self.app)
            db.create_all()

    def tearDown(self):
        """Clean up at the end of every test."""
        
        # Drop all tables
        with self.app.app_context():
            db.drop_all()

    def test_message_creation(self):
        user = User.signup(username='testuser', email='test@example.com', password='testpassword', image_url='test.jpg')
        db.session.add(user)
        db.session.commit()

        message = Message(text='Test message', user_id=user.id)
        db.session.add(message)
        db.session.commit()

        self.assertIsNotNone(message.id)
        self.assertEqual(message.text, 'Test message')


    def test_repr_method(self):
        """Test if the repr method works as expected."""

        user = User(username='testuser', email='test@example.com', password='testpassword', image_url='test.jpg')
        db.session.add(user)
        db.session.commit()

        self.assertEqual(str(user), f"<User #{user.id}: {user.username}, {user.email}>")

    def test_is_following(self):
        """Test if is_following successfully detects when user1 is following user2."""

        user1 = User.signup(username='user1', email='user1@example.com', password='user1password', image_url='user1.jpg')
        user2 = User.signup(username='user2', email='user2@example.com', password='user2password', image_url='user2.jpg')

        db.session.add_all([user1, user2])
        db.session.commit()

        user1.following.append(user2)
        db.session.commit()

        self.assertTrue(user1.is_following(user2))

        """Test if is_following successfully detects when user1 is not following user2."""

        user1 = User.signup(username='user1', email='user1@example.com', password='user1password', image_url='user1.jpg')
        user2 = User.signup(username='user2', email='user2@example.com', password='user2password', image_url='user2.jpg')

        db.session.add_all([user1, user2])
        db.session.commit()

        self.assertFalse(user1.is_following(user2))

    def test_is_followed_by(self):
        """Test if is_followed_by successfully detects when user1 is followed by user2."""

        user1 = User.signup(username='user1', email='user1@example.com', password='user1password', image_url='user1.jpg')
        user2 = User.signup(username='user2', email='user2@example.com', password='user2password', image_url='user2.jpg')

        db.session.add_all([user1, user2])
        db.session.commit()

        user1.followers.append(user2)
        db.session.commit()

        self.assertTrue(user1.is_followed_by(user2))

    def test_is_not_followed_by(self):
        """Test if is_followed_by successfully detects when user1 is not followed by user2."""

        user1 = User.signup(username='user1', email='user1@example.com', password='user1password', image_url='user1.jpg')
        user2 = User.signup(username='user2', email='user2@example.com', password='user2password', image_url='user2.jpg')

        db.session.add_all([user1, user2])
        db.session.commit()

        self.assertFalse(user1.is_followed_by(user2))

    def test_create_user(self):
        """Test if User.create successfully creates a new user given valid credentials."""

        user = User.signup(username='testuser', email='test@example.com', password='testpassword', image_url='test.jpg')
        db.session.commit()

        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, 'testuser')

    def test_create_user_failure(self):
        """Test if User.create fails to create a new user if any of the validations fail."""

        user1 = User.signup(username='testuser', email='test@example.com', password='testpassword', image_url='test.jpg')
        db.session.commit()

        # Attempt to create a user with the same username (should fail)
        user2 = User.signup(username='testuser', email='test2@example.com', password='testpassword2', image_url='test2.jpg')

        with self.assertRaises(Exception):  # Adjust the specific exception type as needed
            db.session.commit()

    def test_authenticate_user(self):
        """Test if User.authenticate successfully returns a user when given a valid username and password."""

        user = User.signup(username='testuser', email='test@example.com', password='testpassword', image_url='test.jpg')
        db.session.commit()

        authenticated_user = User.authenticate(username='testuser', password='testpassword')
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user.id, user.id)

    def test_authenticate_user_failure_invalid_username(self):
        """Test if User.authenticate fails to return a user when the username is invalid."""

        user = User.signup(username='testuser', email='test@example.com', password='testpassword', image_url='test.jpg')
        db.session.commit()

        authenticated_user = User.authenticate(username='invaliduser', password='testpassword')
        self.assertFalse(authenticated_user)

    def test_authenticate_user_failure_invalid_password(self):
        """Test if User.authenticate fails to return a user when the password is invalid."""

        user = User.signup(username='testuser', email='test@example.com', password='testpassword', image_url='test.jpg')
        db.session.commit()

        authenticated_user = User.authenticate(username='testuser', password='invalidpassword')
        self.assertFalse(authenticated_user)


if __name__ == '__main__':
    unittest.main()
