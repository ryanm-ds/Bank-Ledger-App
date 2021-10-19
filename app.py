from flask import Flask, render_template
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

# Database

# app.config['MONGO_URI'] = 'mongodb+srv://rvm8989:Omikron1!@cluster0.6r8p9.mongodb.net/bank_accounts?retryWrites=true&w=majority'

client = pymongo.MongoClient("mongodb+srv://rvm8989:Password@cluster0.6r8p9.mongodb.net/bank_account?retryWrites=true&w=majority",ssl=True,ssl_cert_reqs='CERT_NONE')
db = client.bank_accounts

# Routes
from user import routes

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/dashboard/')
def dashboard():
    return render_template('dashboard.html')


