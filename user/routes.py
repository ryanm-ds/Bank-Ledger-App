from flask import Flask
from app import app
from user.models import User


@app.route('/user/signup',methods=['POST'])
def signup():
    return User().signup()

@app.route('/user/signout')
def signout():
    return User().signout()

@app.route('/user/login',methods=['POST'])
def login():
    return User().login()

@app.route('/user/deposit',methods=['POST'])
def deposit():
    return User().deposit()

@app.route('/user/withdraw',methods=['POST'])
def withdraw():
    return User().withdraw()

@app.route('/user/visualize')
def visualize():
    return User().visualize()