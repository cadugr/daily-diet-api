from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    meals = db.relationship("Meal", back_populates="user", cascade="all, delete-orphan")
