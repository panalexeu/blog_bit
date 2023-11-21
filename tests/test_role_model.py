from app import create_app, db
from app.models import Role, Permission
from tests.test_basics import BasicTestCase


class RoleModelTestCase(BasicTestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_role_default_values(self):
        role = Role(name='TestRole')
        db.session.add(role)
        db.session.commit()

        self.assertFalse(role.default)
        self.assertEqual(role.permissions, 0)

    def test_add_permission(self):
        role = Role(name='TestRole')
        db.session.add(role)
        db.session.commit()

        role.add_permission(Permission.FOLLOW)
        role.add_permission(Permission.WRITE)

        self.assertTrue(role.has_permission(Permission.FOLLOW))
        self.assertTrue(role.has_permission(Permission.WRITE))
        self.assertFalse(role.has_permission(Permission.LIKE))

    def test_remove_permission(self):
        role = Role(name='TestRole', permissions=Permission.FOLLOW + Permission.WRITE)
        db.session.add(role)
        db.session.commit()

        role.remove_permission(Permission.FOLLOW)

        self.assertFalse(role.has_permission(Permission.FOLLOW))
        self.assertTrue(role.has_permission(Permission.WRITE))

    def test_reset_permissions(self):
        role = Role(name='TestRole', permissions=Permission.FOLLOW + Permission.WRITE)
        db.session.add(role)
        db.session.commit()

        role.reset_permissions()

        self.assertFalse(role.has_permission(Permission.FOLLOW))
        self.assertFalse(role.has_permission(Permission.WRITE))

    def test_has_permission(self):
        role = Role(name='TestRole', permissions=Permission.FOLLOW + Permission.WRITE)
        db.session.add(role)
        db.session.commit()

        self.assertTrue(role.has_permission(Permission.FOLLOW))
        self.assertTrue(role.has_permission(Permission.WRITE))
        self.assertFalse(role.has_permission(Permission.LIKE))

    def test_insert_roles(self):
        Role.insert_roles()

        user_role = Role.query.filter_by(name='User').first()
        moderator_role = Role.query.filter_by(name='Moderator').first()
        admin_role = Role.query.filter_by(name='Administrator').first()

        self.assertTrue(user_role is not None)
        self.assertTrue(moderator_role is not None)
        self.assertTrue(admin_role is not None)

        self.assertTrue(user_role.default)
        self.assertTrue(moderator_role.has_permission(Permission.MODERATE))
        self.assertTrue(admin_role.has_permission(Permission.ADMIN))