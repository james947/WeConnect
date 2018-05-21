from api.base_model import db 


class Users(db.Model):
    "user models "
    __tablename__ = 'users'
    """create table users"""
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, 
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    businesses = db.relationship('Business',backref='owner', lazy='dynamic')

    reviews = db.relationship('Reviews', backref='reviewer', lazy='dynamic')

class Blacklist(db.Model):

    __tablename__ = "blacklist"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, nullable=False)


    def __init__(self,token):
        self.token = token

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
