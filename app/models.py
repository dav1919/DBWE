from datetime import datetime, timezone, timedelta  # timedelta no longer strictly needed
from hashlib import md5
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
import secrets

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))
    tasks: so.WriteOnlyMapped['Task'] = so.relationship(back_populates='user')
    token: so.Mapped[str] = so.mapped_column(sa.String(32), index=True, unique=True, nullable=True)  # Allow NULL, for later.
    token_expiration: so.Mapped[datetime] = so.mapped_column(nullable=True) # Keep, but don't use it.

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
        #Simplified logic for *ONLY* forever tokens:
        if self.token:
            return self.token

        self.token = secrets.token_urlsafe(32)
        #CRITICAL:  Do NOT set token_expiration. Leave it as NULL.
        db.session.add(self) # For correct Saving.
        return self.token

    def revoke_token(self):
        # Revocation: simply clear the token.
        self.token = None
        self.token_expiration = None

    @staticmethod
    def check_token(token):
        user = db.session.scalar(sa.select(User).where(User.token == token))
        # Forever tokens:  just check if the user exists.
        return user

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
            index=True, default=lambda: datetime.now(timezone.utc))
    user: so.Mapped[User] = so.relationship(back_populates='tasks')

    def __repr__(self):
        return '<Task {}>'.format(self.title)

    def to_dict(self):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.isoformat() + 'Z' if self.due_date else None,  # ISO 8601 format
            'completed': self.completed,
            '_links': {
                'self': url_for('api.get_task', id=self.id),
                'user': url_for('api.get_user', id=self.user_id)
            }
        }
        return data

    def from_dict(self, data):
        for field in ['title', 'description', 'due_date', 'completed']:
            if field in data:
                setattr(self, field, data[field])
        if 'due_date' in data:
            self.due_date = datetime.fromisoformat(data['due_date'].rstrip('Z')) #Remove Z