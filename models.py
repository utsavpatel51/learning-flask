from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash

db = SQLAlchemy()
class User(db.Model):
    __tablename__='users'
    uid=db.Column(db.Integer,primary_key=True)
    f_name=db.Column(db.String(100))
    l_name=db.Column(db.String(100))
    email=db.Column(db.String(120),unique=True)
    pwdhash=db.Column(db.String(54))

    def __init__(self,f_name,l_name,email,passwd):
        self.f_name=f_name.title()
        self.l_name=l_name.title()
        self.email=email.lower()
        self.set_passwd(passwd)
    
    def set_passwd(self,passwd):
        self.pwdhash=generate_password_hash(passwd)
    def check_passwd(self,pwd):
        return check_password_hash(self.pwdhash,pwd)