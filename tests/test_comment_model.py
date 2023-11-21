import unittest
from datetime import datetime
from app import create_app, db
from app.models import User, Post, Comment
from tests.test_basics import BasicTestCase


class CommentModelTestCase(BasicTestCase):
    def test_comment_body_html_conversion(self):
        u = User(username='testuser', email='test@example.com', password='password')
        db.session.add(u)
        db.session.commit()

        post = Post(body='Test Post Body', author=u)
        db.session.add(post)
        db.session.commit()

        comment = Comment(body='**Test Comment**', author=u, post=post)
        db.session.add(comment)
        db.session.commit()

        self.assertIsNotNone(comment.body_html)
        self.assertIn('<strong>Test Comment</strong>', comment.body_html)

    def test_comment_timestamp(self):
        u = User(username='testuser', email='test@example.com', password='password')
        db.session.add(u)
        db.session.commit()

        post = Post(body='Test Post Body', author=u)
        db.session.add(post)
        db.session.commit()

        comment = Comment(body='Test Comment Body', author=u, post=post)
        db.session.add(comment)
        db.session.commit()

        self.assertIsInstance(comment.timestamp, datetime)

    def test_comment_disabled_default_false(self):
        u = User(username='testuser', email='test@example.com', password='password')
        db.session.add(u)
        db.session.commit()

        post = Post(body='Test Post Body', author=u)
        db.session.add(post)
        db.session.commit()

        comment = Comment(body='Test Comment Body', author=u, post=post)
        db.session.add(comment)
        db.session.commit()

        self.assertFalse(comment.disabled)

    def test_comment_author_relationship(self):
        u = User(username='testuser', email='test@example.com', password='password')
        db.session.add(u)
        db.session.commit()

        post = Post(body='Test Post Body', author=u)
        db.session.add(post)
        db.session.commit()

        comment = Comment(body='Test Comment Body', author=u, post=post)
        db.session.add(comment)
        db.session.commit()

        self.assertEqual(comment.author, u)

    def test_comment_post_relationship(self):
        u = User(username='testuser', email='test@example.com', password='password')
        db.session.add(u)
        db.session.commit()

        post = Post(body='Test Post Body', author=u)
        db.session.add(post)
        db.session.commit()

        comment = Comment(body='Test Comment Body', author=u, post=post)
        db.session.add(comment)
        db.session.commit()

        self.assertEqual(comment.post, post)
