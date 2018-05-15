from api.baseModel import db

class Business(db.Model):
    __tablename__ = 'business'
    id = db.Column(db.Integer, primary_key=True)
    businessname = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    owner_id= db.Column(db.Integer, db.ForeignKey('users.id'))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    reviews = db.relationship('Reviews', backref='business', lazy='dynamic')

    


class Reviews(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(50),  nullable=False)
    review= db.Column(db.String(50),  nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    date_modified = db.Column(db.DateTime,
        default=db.func.current_timestamp(),
        onupdate= db.func.current_timestamp())





