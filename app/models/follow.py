from datetime import datetime

from app import db


class Follow(db.Model):
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_kye=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
