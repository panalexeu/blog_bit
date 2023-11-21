from datetime import datetime
from app import create_app, db
from app.models import User, Post, Permission, Role, Comment, Like
from tests.test_basics import BasicTestCase


class PostModelTestCase(BasicTestCase):
    def test_post_body_html_conversion(self):
        u = User(username='testuser', email='test@example.com', password='password')
        db.session.add(u)
        db.session.commit()

        post = Post(body='**Test Post**', author=u)
        db.session.add(post)
        db.session.commit()

        self.assertIsNotNone(post.body_html)
        self.assertIn('<strong>Test Post</strong>', post.body_html)

    def test_post_timestamp(self):
        u = User(username='testuser', email='test@example.com', password='password')
        db.session.add(u)
        db.session.commit()

        post = Post(body='Test Post Body', author=u)
        db.session.add(post)
        db.session.commit()

        self.assertIsInstance(post.timestamp, datetime)

    def test_post_disabled_default_false(self):
        u = User(username='testuser', email='test@example.com', password='password')
        db.session.add(u)
        db.session.commit()

        post = Post(body='Test Post Body', author=u)
        db.session.add(post)
        db.session.commit()

        self.assertFalse(post.disabled)

    def test_post_author_relationship(self):
        u = User(username='testuser', email='test@example.com', password='password')
        db.session.add(u)
        db.session.commit()

        post = Post(body='Test Post Body', author=u)
        db.session.add(post)
        db.session.commit()

        self.assertEqual(post.author, u)

    def test_post_comments_relationship(self):
        post = Post(body='Test Post Body')
        db.session.add(post)
        db.session.commit()

        comment = Comment(body='Test Comment Body', post=post)
        db.session.add(comment)
        db.session.commit()

        self.assertIn(comment, post.comments)

    def test_post_likes_relationship(self):
        post = Post(body='Test Post Body')
        db.session.add(post)
        db.session.commit()

        like = Like(user_id=1, post=post)
        db.session.add(like)
        db.session.commit()

        self.assertIn(like, post.likes)
