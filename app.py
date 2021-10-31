from flask import Flask, render_template, session, redirect
from functools import wraps
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = b'^\xb3\xd0\xf5Er\x96w\xddS\xbb\xbf\xd0\xaf\xb70'

# Database

client = pymongo.MongoClient("mongodb+srv://rvm8989:PASSWORD@cluster0.6r8p9.mongodb.net/bank_account?retryWrites=true&w=majority",ssl=True,ssl_cert_reqs='CERT_NONE')
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


