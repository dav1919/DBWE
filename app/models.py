from datetime import datetime, timezone
from hashlib import md5
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
import secrets
from flask import url_for  # KEEP THIS


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))
    tasks: so.WriteOnlyMapped['Task'] = so.relationship(back_populates='user')
    token: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True, nullable=True)
    token_expiration: so.Mapped[datetime] = so.mapped_column(nullable=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def get_token(self):
        if self.token:
            return self.token

        self.token = secrets.token_urlsafe(32)
        #CRITICAL: token_expiration not being set
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token = None
        self.token_expiration = None
        #db.session.add(self)

    @staticmethod
    def check_token(token):
        user = db.session.scalar(sa.select(User).where(User.token == token))
        return user # Returns the user, if exists.



@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class Task(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(128))
    description: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)
    due_date: so.Mapped[datetime] = so.mapped_column(nullable=True)
    completed: so.Mapped[bool] = so.mapped_column(default=False)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(
           index=True, default=lambda: datetime.now(timezone.utc)) #Use now()
    user: so.Mapped[User] = so.relationship(back_populates='tasks')

    def __repr__(self):
        return '<Task {}>'.format(self.title)
    #Removed _links to prevent Errors.
    def to_dict(self):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.isoformat() + 'Z' if self.due_date else None,
            'completed': self.completed,
        }
        return data