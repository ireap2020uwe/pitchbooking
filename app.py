import os
import datetime
from flask import Flask, request, abort, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import  db_drop_and_create_all, setup_db, Bookings, Pitches
from auth import AuthError, requires_auth



#def create_app(test_config=None):
    # create and configure the app
def create_app(test_config=None):
    app = Flask(__name__)

    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Headers','GET, PUT, PATCH, POST, DELETE, OPTIONS')
        return response

    @app.route('/')
    def get_home():
        return "Hi, there. Welcome to the Pitch Booking Page"


    @app.route('/pitches',methods=['GET'])
    def get_pitches():
        pitches = Pitches.query.all()
        
        return jsonify({
            'success':True,
            'pitches': [pitch.format() for pitch in pitches]
        }),200


    @app.route('/pitches/<int:id>',methods=['GET'])
    @requires_auth('get:pitch')
    def get_pitches_by_id(payload, id):
        try:
            pitch = Pitches.query.filter(Pitches.id == id).one_or_none()
            pit = pitch.format()
        except BaseException:
            abort(422)

        return jsonify({'success':True,
                        'pitch':pit}),200


    @app.route('/pitches/<int:id>/booking', methods=['POST'])
    @requires_auth('post:booking')
    def create_booking(payload,id):
    
        req=request.get_json()
        try:
    
            t_o_b = req.get('time_of_booking')
            n_o_p = req.get('number_of_people')
            n_o_b = req.get('name_of_booking')
            c_id = req.get('customer_id')
            #c_id = req.get('customer_id')
            b_f = req.get('booking_fee')
            #customer_id = token.get('sub')
            booking = Bookings(id = id, time_of_booking = t_o_b, name_of_booking = n_o_b, number_of_players = n_o_p, customer_id = c_id, pitch_id = id, booking_fee = b_f)
            booking.insert()
            #bookings = Bookings.query.filter(Bookings.customer_id==c_id).all()
            #bookings=Bookings.query.all()
        except BaseException:
            abort(400)


        return jsonify({'success':True,
                        'upcoming_booking':[booking.format()]}),200


    @app.route('/pitches',methods=['POST'])
    @requires_auth('post:pitch')
    
    def post_pitch(payload):
        req=request.get_json()
        try:
            
            n_pitch = Pitches()
            # n_pitch.name = 'Harry'
            # n_pitch.id = 100
            # n_pitch.address = 'Harry'
            n_pitch.name = req['Pitch_name']
            n_pitch.id = req['Pitch_id']
            n_pitch.address = req['Pitch_address']
            #pitch=Pitches(owner_id=owner_id, pitch_name= pitch_name, pitch_address=pitch_address)
            n_pitch.insert()
        #pitches=Pitches.query.all()
        #users_pitch=Pitches.query.filter(Pitches.owner_id==owner_id).all()
        except BaseException:
            abort(400)

        return jsonify(
            {"success":True,
             "pitches":[n_pitch.format()]}),200


        # #pitch owner - patch: pitch
    @app.route('/pitches/<int:id>',methods=['PATCH'])
    @requires_auth('patch:pitch')
    #def update_pitch():
    def update_pitch(payload,id):
        
 
        req = request.get_json()
        #pitch=Pitches.query.get(edit_id)
    
        pitch = Pitches.query.filter(Pitches.id == id).one_or_none()
        if not pitch:
            abort(404)
        

        
        try:
            
            req_pitch_name = req.get('name')
            req_pitch_address = req.get('address')

            if req_pitch_name:
                pitch.name = req_pitch_name
            if req_pitch_address:
                pitch.address = req_pitch_address
            
            pitch.update()
            #updated_pitch=Pitches.query.get(edit_id)
        except BaseException:
            abort(422)

        return jsonify(
            {"success":True,
            "pitch":[pitch.format()]}),200
            
    #     # #Pitch owner - delete:pitch
    @app.route('/pitches/<int:id>',methods=['DELETE'])
    @requires_auth('delete:pitch')
    def delete_pitch(payload,id):
        
        pitch = Pitches.query.filter(Pitches.id == id).one_or_none()

        if not pitch:
            abort(404)

        
        
        try:
            pitch.delete()
        except BaseException:
            abort(422)
        
        return jsonify(
            {'success':True,
            'delete':id}),200


    @app.route('/login-results')
    def login_results():
        return "Welcome to Pitch Booking Page"
        

    # @app.route('/user')
    # @requires_auth('read:yourself')
    # def user (payload):
    #     return payload

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success":False,
            "error":404,
            "message":"Page not found"
        }),404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success":False,
            "error":422,
            "message":"unprocessable"
        }),422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success":False,
            "error":400,
            "message":"bad request"
        }),400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success":False,
            "error":405,
            "message":"bad request"
        }),405

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success":False,
            "error":500,
            "message":"internal server error"
        }),500

    return app



APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
#    # app.run()