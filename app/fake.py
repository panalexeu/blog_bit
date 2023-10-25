from random import randint
from faker import Faker
from sqlalchemy.exc import IntegrityError

from . import db
from . models import User, Post


def generate_users(amount=50):
    fake = Faker()

    for _ in range(amount):
        user = User(
            email=fake.email(),
            username=fake.user_name(),
            name=fake.name(),
            password='Faker',
            confirmed=True,
            about_me=fake.text(),
            member_since=fake.past_date()
        )

        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def generate_posts(amount=50):
    fake = Faker()
    user_count = User.query.count()

    for _ in range(amount):
        user = User.query.offset(randint(1, user_count)).first()
        post = Post(
            body=fake.text(),
            timestamp=fake.past_date(),
            author=user
        )
        db.session.add(post)
        db.session.commit()
