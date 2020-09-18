import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Bookings, Pitches
from app import create_app
        
class PitchbookingTestCase(unittest.TestCase):
    
    "This class represents the pitch booking test case"
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path= "postgres://postgres@localhost:5432/pitchbooking"

        setup_db(self.app, self.database_path)

        
    
    ###tokens??????

    #new pitch
        self.new_pitch = {
            'id':10,
            'name':'UWE pitch',
            'address':'Filton',
            'owner_id':2}


        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
                #create all tables
            self.db.create_all()
    #new pitch
    # self.change_pitch_address = {'address':'BS16 1QY'}

    # #post new booking
    # self.booking_info = {'time_of_reseravation':"2020-09-10 09:00:00",
    #                     'number_of_players':11,
    #                     'name_of_booking':"Harper"}
    
    def tearDown(self):
        "Executed after reach test"
        pass

    def test_get_home(self):
        booking = self.client().get('/')
        self.assertEqual(booking.status_code,200)

    def test_get_pitches(self):
        response=self.client().get('/pitches')
        data=json.loads(response.data)
        pitches=Pitches.query.all()
        pit=[pitch.format() for pitch in pitches]
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['pitches'],pit)


    def test_get_pitches_by_id(self):
        pit_id = 1
        response=self.client().get(f'/pitches/{pit_id}')
        data=json.loads(response.data)
        pitch=Pitches.query.get(pit_id)
        pit=pitch.format()
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['pitch'],pit)
    

    # def test_post_booking_with_valid_customer(self):
    #     pit_id = 1
    #     #response=self.client().post(f'/pitches/{pit_id}/booking',headers={"Authorization":"Bearer{}".format(self.customer)},json=self.booking_info)
    #     response=self.client().post(f'/pitches/{pit_id}/booking')
        
    #     data=json.loads(response.data)
    #     self.assertEqual(response.status_code,200)

    # def test_post_booking_with_invalid_customer(self):
    #     pit=self.client().post('/pitches/'+str(self.current_pit_id)+'/booking',headers={"Authorization":"Bearer{}".format(self.badtoken)},json=self.booking_info)
    #     data=json.loads(pit.data)
    #     self.asserEqual(pit.status_code,401)
    
    # def test_post_booking_with_nonexist_pitch(self):
    #     pit=self.client().post('/pitches/'+str(self.current_pit_id+5000)+'/booking',headers={"Authorization":"Bearer{}".format(self.badtoken)},json=self.booking_info)
    #     data=json.loads(pit.data)
    #     self.asserEqual(pit.status_code,422)
    
    # def test_post_pitch(self):
    #     #pit=self.client().post('/pitches',headers={"Authorization":"Bearer {}".format(self.manager)},json=self.new_pitch)
    #     response = self.client().post(f'/pitches',
    #                                 data=json.dumps(self.new_pitch))
    #                                # content_type='application/json')
    #     data=json.loads(response.data)
    #     self.assertEqual(response.status_code,200)
    #     self.assertEqual(data['success'],True)
        #self.assertEqual(data['pitches'])


    # def test_401_post_pitch_without_valid_token(self):
    #     pit=self.client().post('/pitches',headers={"Authorization":"Bearer {}".format(self.badtoken)},json=self.new_pitch)
    #     data=json.loads(pit.data)
    #     self.assertEqual(pit.status_code,401)
    #     self.assertEqual(data['success'],False)
    
    # def test_delete_pitch_with_valid_owner(self):
    #     pit=self.client().post('/pitches/'+str(self.current_pit_id),headers={"Authorization":"Bearer{}".format(self.manager)})
    #     deleted_pit=Pitches.query.get(self.current_pit_id)
    #     self.asserEqual(pit.status_code,200)
    #     self.assertEqual(delete_pit,None)

    # def test_delete_pitch_with_nonexist_pitch(self):
    #     pit=self.client().post('/pitches/'+str(self.current_pit_id+5000),headers={"Authorization":"Bearer{}".format(self.manager)})
    #     deleted_pit=Pitches.query.get(self.current_pit_id+5000)
    #     self.asserEqual(pit.status_code,422)
    #     self.assertEqual(deleted_pit,None)
    
    # def test_401_delete_pitch_without_valid_token(self):
    #     pit=self.client().post('/pitches/'+str(self.current_pit_id),headers={"Authorization":"Bearer{}".format(self.manager)})
    #     ata=json.loads(pit.data)
    #     self.assertEqual(pit.status_code,401)
    #     self.assertEqual(data['success'],False)


    def test_update_pitch_with_valid_id(self):
        pit_id = 2
        response=self.client().patch('/pitches/{pit_id}')
        data=json.loads(response.data)
        pitch=Pitches.query.filter(Pitches.id == pit_id).one_or_none()
        
        self.assertEqual(response.status_code,200)
        #self.asserEqual(data['updated_pitch'],['address'])


    # def test_edit_pitch_with_valid_id(self):
    #     pit=self.client().patch('/pitches/'+str(self.current_pit_id),headers={"Authorization":"Bearer{}".format(self.manager)},json=self.change_pitch_address)
    #     data=json.loads(pit.data)
    #     pitch=Pitches.query.get(self.current_pit_id)
    #     format_pit=pit.format()
    #     self.asserEqual(pit.status_code,200)
    #     self.asserEqual(data['updated_pitch'],['address'])
    
    # def test_edit_pitch_without_valid_id(self):
    #     pit=self.client().patch('/pitches/'+str(self.bad_pit_id),headers={"Authorization":"Bearer{}".format(self.manager)},json=self.change_pitch_address)
    #     self.asserEqual(pit.status_code,401)
    
    # def test_edit_pitch_nonexist(self):
    #     pit=self.client().patch('/pitches/'+str(self.current_pit_id+5000),headers={"Authorization":"Bearer{}".format(self.manager)},json=self.change_pitch_address)
    #     self.assertEqual(pit.status_code,422)
    
if __name__ == "__main__":
    unittest.main()
