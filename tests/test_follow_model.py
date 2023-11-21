from app import create_app, db
from app.models import User, Follow
from tests.test_basics import BasicTestCase


class FollowModelTestCase(BasicTestCase):
    def test_follow_timestamp(self):
        follower = User(username='follower', email='follower@example.com', password='password')
        followed = User(username='followed', email='followed@example.com', password='password')
        db.session.add_all([follower, followed])
        db.session.commit()

        follow = Follow(follower=follower, followed=followed)
        db.session.add(follow)
        db.session.commit()

        self.assertIsNotNone(follow.timestamp)

    def test_follow_relationships(self):
        follower = User(username='follower', email='follower@example.com', password='password')
        followed = User(username='followed', email='followed@example.com', password='password')
        db.session.add_all([follower, followed])
        db.session.commit()

        follow = Follow(follower=follower, followed=followed)
        db.session.add(follow)
        db.session.commit()

        self.assertEqual(follow.follower, follower)
        self.assertEqual(follow.followed, followed)
