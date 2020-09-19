import os
import json
from sqlalchemy import Column, String, create_engine, Integer, DateTime, Numeric, ForeignKey, Float
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
database_path = "postgres://ophjtzvvuijlgd:b6be3f24a4954b3af0e42926508f7e1cac00c3f90c3f123199ba0597a46ad590@ec2-3-214-4-151.compute-1.amazonaws.com:5432/d1faggmdefrcoh"
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    # database initialization
    db.drop_all()
    db.create_all()


class Bookings(db.Model):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True)
    time_of_booking = Column(DateTime)
    name_of_booking = Column(String)
    number_of_players = Column(Integer)
    customer_id = Column(String)  # retrieved from token
    pitch_id = Column(Integer, ForeignKey('pitches.id'))
    booking_fee = Column(Float)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @hybrid_property
    def pitch_name(self):
        return self.pitch_booking.name

    def format(self):
        return{
            "id": self.id,
            "time_of_booking": self.time_of_booking,
            "name_of_booking": self.name_of_booking,
            "number_of_players": self.number_of_players,
            "customer_id": self.customer_id,
            "pitch_id": self.pitch_id,
            "booking_fee": self.booking_fee
            }


class Pitches(db.Model):
    __tablename__ = 'pitches'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # postcode = Column(String)
    address = Column(String)
    owner_id = Column(Integer, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return{
            "Pitch_id": self.id,
            "Pitch_name": self.name,
            "Pitch_address": self.address
        }
        