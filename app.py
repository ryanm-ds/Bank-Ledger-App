from flask import Flask, render_template, session, redirect
from functools import wraps
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = b'^\xb3\xd0\xf5Er\x96w\xddS\xbb\xbf\xd0\xaf\xb70'

# Database

client = pymongo.MongoClient("MONGODBURI")
db = client.bank_accounts

# Decorators 
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')

    return wrap
# Routes
from user import routes

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


