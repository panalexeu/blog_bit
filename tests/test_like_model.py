from datetime import datetime

from app import create_app, db
from app.models import User, Post, Like
from tests.test_basics import BasicTestCase


class LikeModelTestCase(BasicTestCase):
    def test_like_timestamp(self):
        u = User(username='testuser', email='test@example.com', password='password')
        db.session.add(u)
        db.session.commit()

        post = Post(body='Test Post Body', author=u)
        db.session.add(post)
        db.session.commit()

        like = Like(user=u, post=post)
        db.session.add(like)
        db.session.commit()

        self.assertIsInstance(like.timestamp, datetime)

    def test_like_user_relationship(self):
        u = User(username='testuser', email='test@example.com', password='password')
        db.session.add(u)
        db.session.commit()

        post = Post(body='Test Post Body', author=u)
        db.session.add(post)
        db.session.commit()

        like = Like(user=u, post=post)
        db.session.add(like)
        db.session.commit()

        self.assertEqual(like.user, u)

    def test_like_post_relationship(self):
        u = User(username='testuser', email='test@example.com', password='password')
        db.session.add(u)
        db.session.commit()

        post = Post(body='Test Post Body', author=u)
        db.session.add(post)
        db.session.commit()

        like = Like(user=u, post=post)
        db.session.add(like)
        db.session.commit()

        self.assertEqual(like.post, post)
