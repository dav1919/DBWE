import sqlalchemy as sa
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth  #Keep both, Basic is needed for initial login to create tokens.
from app import db
from app.models import User
from app.api.errors import error_response #Keep to avoid crashes.


basic_auth = HTTPBasicAuth() #Keep
token_auth = HTTPTokenAuth()




@basic_auth.verify_password
def verify_password(username, password):
    user = db.session.scalar(sa.select(User).where(User.username == username))
    if user and user.check_password(password):
        return user




@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)




@token_auth.verify_token
def verify_token(token):
    return User.check_token(token) if token else None




@token_auth.error_handler
def token_auth_error(status):
   return error_response(status)