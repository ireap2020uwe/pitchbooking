import os
import datetime
from flask import Flask, request, abort, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import  db_drop_and_create_all, setup_db, Bookings, Pitches
from auth import requires_auth



#def create_app(test_config=None):
    # create and configure the app
def create_app(test_config=None):
    app = Flask(__name__)

    setup_db(app)
    CORS(app)


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


    @app.route('/pitches/<int:id>')
    def get_pitches_by_id(id):
        try:
            pitch = Pitches.query.get(id)
            pit = pitch.format()
        except:
            abort(422)

        return jsonify({'success':True,
                        'pitch':pit}),200


    # @app.route('/pitches/<int:id>/booking', methods=['POST'])
    # #@requires_auth('post:booking')
    # #def create_booking(payload,id):
    # def create_booking():
    #     req=request.get_json()
    #     # try:
    #     #     t_o_b = req.get('time_of_booking')
    #     #     n_o_p = req.get('number_of_people')
    #     #     n_o_b = req.get('name_of_booking')
    #     #     c_id = req.get('customer_id')
    #     #     #customer_id = token.get('sub')
    #     #     booking = Bookings(cusomer_id = c_id, time_of_booking = t_of_b, number_of_people = n_of_p, name_of_booking = n_o_b)
    #     #     booking.insert()
    #     #     upcoming_booking = Bookings.query.filter(Bookings.customer_id==c_id).all()
    #     # except:
    #     #     abort(422)

    #     return jsonify({'success':True}),200
    #     #return jsonify({'success':True,
    #                     #'upcoming_booking':[booking.format() for booking in upcoming_booking]})


    @app.route('/pitches',methods=['POST'])
    #@requires_auth('post:pitches')
    def post_pitch():
    #def post_pitch(payload):
        body=request.get_json()
            #owner_id=token.get('sub')
        pitch = Pitches()
        pitch.Pitch_name = body.get('name')
        pitch.Pitch_id = body.get('id')
        pitch.pitch_address=body.get('address')
            #pitch=Pitches(owner_id=owner_id, pitch_name= pitch_name, pitch_address=pitch_address)
        pitch.insert()
            #users_pitch=Pitches.query.filter(Pitches.owner_id==owner_id).all()
        #except:
         #   abort(422)

        return jsonify(
            {"success":True,
             "pitches":[pitch.format()]}),200


        # #pitch owner - patch: pitch
    @app.route('/pitches/<int:id>',methods=['PATCH'])
    #@requires_auth('patch:pitch')
    def update_pitch():
    #def update_pitch(payload,id):
        edit_id = id
        #owner_id=payload.get('sub')
        body = request.get_json()
        #pitch=Pitches.query.get(edit_id)
        pitch=Pitches.query.filter(Pitches.id == id).one_or_none()

        if not pitch:
            abort(422)
        
        if owner_id!= pitch.owner_id:
            abort(401)
        
        try:
            
            req_pitch_name = body.get('name',None)
            req_pitch_address = body.get('address',None)

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
            "updated_pitch":[pitch.format()]}),200
            
        # #Pitch owner - delete:pitch
    @app.route('/pitches/<int:id>',methods=['DELETE'])
    #@requires_auth('delete:pitch')
    def delete_pitch(payload,id):
        owner_id=payload.get('sub')
        pitch= Pitches.query.filter(Pitches.id==id).one_or_none()

        if not pitch:
            abort(404)

        #check owner is true
        if owner_id!=pitch.owner_id:
            abort(401)
        
        try:
            pitch.delete()
        except BaseException:
            abort(400)
        
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



app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
#    # app.run()