from database import db

class Role(db.Model):
    __tablename__ = 'ROLE'
    __table_args__ = {'schema': 'base'}

    ROLE_CODE = db.Column(db.String(20), primary_key=True)
    ROLE_NAME = db.Column(db.String(500), nullable=False)
    UUID = db.Column(db.String(100), nullable=False)
    CREATED_USER_CODE = db.Column(db.String(20))
    CREATED_DATE = db.Column(db.DateTime)
    LAST_MOD_USER_CODE = db.Column(db.String(20))
    LAST_MOD_DATE = db.Column(db.DateTime)
