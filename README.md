# Final Project of Full Stack Development
## Capstone Project: Pitch Booking system
**Heroku link:**  (https://pitchbookingfinal.herokuapp.com/)

## Motivations for project
This is the final project of Udacity Full Stack Development Nanodegree Training, which involve the following technical topics:
1.	Handling database using postgres and sqlalchemy (model.py)
2.	CRUD database through API with Flask (app.py)
3.	Testing using unittest (test_app.py)
4.	Role based authentification using Auth0 (auth.py)
5.	Deployment of app on Heroku
 
## Project dependencies, local development and hosting instructions 

### Project dependencies
1.	Python 3.7
2.	PostgresSQL
3.	PIP Dependencies


### Local development

1.Install the dependences through the terminal:

```
pip install -r requirements.txt
```

2.To run the server, execute:
```
export FLASK_APP=api.py
export FLASK_ENV=debug
flask run --reload
```

3.Run the migration commands to set up:
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

4.Set up authentication with Auth0, there are two roles in this project:

Pitch manager:

get: pitch

post: pitch

patch: pitch

delete: pitch

Customer:

get: pitch

post: booking

### Hosting instruction
The app will run on http:127.0.0.1:5000


## API behavior and RBAC controls

Endpoints summary:
1.	‘/’
2.	GET ‘/pitches’
3.	GET ‘/pitches/<int:id>’
4.	POST ‘/pitches/<int:id>/booking’
5.	POST ‘/pitches’
6.	PATCH ‘/pitches/<int:id>’
7.	DELETE ‘/pitches/<int:id>

`````
GET '/pitches'
-no authorization required
-get all pitches from the database
-reponse = {"pitches":[
{"Pitch_address":"Ashton","Pitch_id":1,"Pitch_name":"BRISTOLCITY"},
{"Pitch_address":"Swansea","Pitch_id":2,"Pitch_name":"SWANSEACITY"},
{"Pitch_address":"Cardiff","Pitch_id":3,"Pitch_name":"CARDIFFCITY"},
{"Pitch_address":"Birmingham","Pitch_id":4,"Pitch_name":"BIRMINGHAMCITY"},
{"Pitch_address":"London","Pitch_id":5,"Pitch_name":"QPRFC"}]
,"success":true}


GET ‘/pitches/<int:id>’
-Required Authorization with ‘Pitch manager’ or ‘Customer’ role
-Get the detailed information of a specific pitch
-<int:id> replaces the ID of pitch you want to see
-reponse = {"pitch":{"Pitch_address":"Ashton","Pitch_id":1,"Pitch_name":"BRISTOLCITY"}],"success":true}


POST ‘/pitches/<int:id>/booking’
-Required Authorization with ‘Customer’ role
-Post a booking for the specific pitch with id in <int:id>
-payload = {'id':20,
                     'time_of_booking':'2020-09-22T09:00:00',
                     'name_of_booking':"Harper",
                     'number_of_players':11,
                     'customer_id':20,
                     'pitch_id':1,
                     'booking_fee':100}
response = {
  	success: True,
  	upcoming_booking:{'id':20,
                     			'time_of_booking':'2020-09-22T09:00:00',
                     			'name_of_booking':"Harper",
                     			'number_of_players':11,
                     			'customer_id':20,
                    			'pitch_id':1,
                     			'booking_fee':100}}


POST ‘/pitches’
-Required Authorization with ‘Pitch owner’ role
-Post a new pitch
-payload = {
            'id':10,
            'name':'UWE pitch',
            'address':'Filton',
            'owner_id':2}
-response = {
success: True,
  	pitches:{ 'id':10,
            'name':'UWE pitch',
            'address':'Filton',
            'owner_id':2}
}


PATCH ‘/pitches/<int:id>’
-Required Authorization with ‘Pitch owner’ role
-Update the info a specific pitch
-payload = {
            'id':1,
            'name':'BristolBears',
            'address':'Bristol',
            'owner_id':3}
-response = {
success: True,
  	pitches:{ 'id':10,
            'name': BristolBears',
            'address':' Bristol',
            'owner_id':3}
}


DELETE ‘/pitches/<int:id>
-Required Authorization with ‘Pitch owner’ role
-Delete the info a specific pitch with id of <int:id>
-response = {
  success: True,
  delete: id
}



