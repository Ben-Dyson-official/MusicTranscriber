from App import login, db, app
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
import jwt
from time import time

class User(UserMixin, db.Model): #creates a class of user
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.String(100))

    def __repr__(self):
        return'<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size): #allows user to have an avatar
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
        digest, size)
    
    def get_reset_password_token(self, expires_in=1800):
        return jwt.encode({'reset_password':self.id, 'exp': time()+expires_in}, app.config['SECRET_KEY'], algorithm='HS256')
        
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

class Piece(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(64))
    author = db.Column(db.String(64))
    AudioDirectory = db.Column(db.String(256))
    SheetDirectory = db.Column(db.String(256))
    key = db.Column(db.String(64))
    bpm = db.Column(db.Integer)
    timeSignature = db.Column(db.String(4))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Piece {}>'.format(self.body)
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
