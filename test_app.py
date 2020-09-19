import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Bookings, Pitches
from app import create_app

token_name_one = os.environ['PITCH_MANAGER']  
token_name_two = os.environ['CUSTOMER']
headers={'Authorization': 'Bearer ' + str(token_name_one)}

class PitchbookingTestCase(unittest.TestCase):
    "This class represents the pitch booking test case"
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "postgres://postgres@localhost:5432/pitchbooking"

        setup_db(self.app, self.database_path)

        self.new_pitch = {
            'id': 10,
            'name': 'UWE pitch',
            'address': 'Filton',
            'owner_id': 2}

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        self.booking_info = {
            'id': 20,
            'time_of_booking': '2020-09-22T09:00:00',
            'name_of_booking': "Harper",
            'number_of_players': 11,
            'customer_id': 20,
            'pitch_id': 1,
            'booking_fee': 100}

    def tearDown(self):
        "Executed after reach test"
        pass

    def test_get_home(self):
        booking = self.client().get('/')
        self.assertEqual(booking.status_code, 200)

    def test_get_pitches(self):
        response = self.client().get('/pitches')
        data = json.loads(response.data)
        pitches = Pitches.query.all()
        pit = [pitch.format() for pitch in pitches]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['pitches'], pit)

    def test_get_pitches_by_id(self):
        pit_id = 1
        response = self.client().get(f'/pitches/{pit_id}')
        data = json.loads(response.data)
        pitch = Pitches.query.filter(Pitches.id == pit_id).one_or_none()
        pit = pitch.format()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['pitch'], pit)

    def test_get_pitches_by_id_with_nonexist_pitch(self):
        pit_id = 100
        response = self.client().get(f'/pitches/{pit_id}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)

    def test_post_booking(self):
        pit_id = 1
        response = self.client().post(f'/pitches/{pit_id}/booking')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_booking_with_nonexist_pitch(self):
        pit_id = 100
        response = self.client().post(f'/pitches/{pit_id}/booking')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)

    def test_delete_pitch(self):
        pit_id = 1
        response = self.client().delete('/pitches/{pit_id}')
        data = json.loads(response.data)
        deleted_pitch = Pitches.query.filter(Pitches.id == pit_id).one_or_none()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(deleted_pitch, None)

    def test_delete_pitch_nonexist_pitch(self):
        pit_id = 100
        response = self.client().delete('/pitches/{pit_id}')
        data = json.loads(response.data)
        deleted_pitch = Pitches.query.filter(Pitches.id == pit_id).one_or_none()
        self.assertEqual(response.status_code, 422)
        self.assertEqual(deleted_pitch, None)

    def test_update_pitch(self):
        pit_id = 1
        response = self.client().patch('/pitches/{pit_id}')
        data = json.loads(response.data)
        updated_pitch = Pitches.query.filter(Pitches.id == pit_id).one_or_none()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['updated_pitch'], ['address'])

    def test_update_pitch_with_valid_id(self):
        pit_id = 100
        response = self.client().patch('/pitches/{pit_id}')
        data = json.loads(response.data)
        updated_pitch = Pitches.query.filter(Pitches.id == pit_id).one_or_none()
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
