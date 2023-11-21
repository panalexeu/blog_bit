from flask import current_app

from app.models import User, Permission, Role, Post
from tests.test_basics import BasicTestCase


class UserModelTestCase(BasicTestCase):
    def test_password_setter(self):
        u = User(password='cat', )
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password()

    def test_password_verification(self):
        u = User(password='cat')

        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_user_creation_with_role(self):
        u = User(username='testuser', email='test@example.com', password='password')
        self.assertIsNotNone(u.role)
        self.assertTrue(u.role.default)

    def test_user_creation_with_admin_role(self):
        admin_email = current_app.config['ADMIN']
        u = User(username='admin', email=admin_email, password='adminpass')
        self.assertIsNotNone(u.role)
        self.assertEqual(u.role.name, 'Administrator')

    def test_user_permissions(self):
        u = User(username='testuser', email='test@example.com', password='password')
        self.assertFalse(u.can(Permission.ADMIN))
        self.assertFalse(u.can(Permission.MODERATE))

        u.role = Role(name='Moderator', permissions=Permission.MODERATE)
        self.assertFalse(u.can(Permission.ADMIN))
        self.assertTrue(u.can(Permission.MODERATE))

    def test_confirmation_token(self):
        # Test user confirmation token generation and verification
        u = User(username='testuser', email='test@example.com', password='password')
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))
        self.assertFalse(u.confirm('invalid_token'))
