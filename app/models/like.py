from app import db

from datetime import datetime


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
