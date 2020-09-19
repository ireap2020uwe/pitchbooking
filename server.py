# /server.py

from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

app = Flask(__name__)

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='sOHYI6pa0Tdmu1eXNzq9Yb6CSRHQpu1s',
    client_secret='_nBpuFWas2-DqTgNpA1olrQJCYOPyxlKQWy-j-NwHW7i2h5S0pDM5-3MoabQJdhx',
    api_base_url='https://xiaojun.eu.auth0.com',
    access_token_url='https://xiaojun.eu.auth0.com/oauth/token',
    authorize_url='https://xiaojun.eu.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)