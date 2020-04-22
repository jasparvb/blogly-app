from unittest import TestCase
from app import app
from models import db, User

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:41361@localhost/blogly_test"
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class BloglyViewsTestCase(TestCase):
    """Tests for views for Users"""

    def setUp(self):
        """Add sample user"""
        User.query.delete()

        user = User(first_name='Jaspar', last_name='von Bülow', image_url=None)
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
    
    def tearDown(self):
        """Clean up any fouled transaction"""
        db.session.rollback()

    def test_home_redirect(self):
        with app.test_client() as client:
            resp = client.get('/')

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, 'http://localhost/users')

    def test_users_list(self):
        with app.test_client() as client:
            resp = client.get('/users/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)
            self.assertIn('Jaspar von Bülow', html)
    
    def test_add_new_user(self):
        with app.test_client() as client:
            resp = client.post('/users/new', data={'first-name': 'Leo', 'last-name': 'Messi', 'image-url': ''}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)
            self.assertIn('Leo Messi', html)

    def test_user_details(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Jaspar von Bülow</h1>', html)
