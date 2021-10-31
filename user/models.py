from flask import Flask, jsonify, request, session, redirect
from werkzeug.utils import redirect 
from passlib.hash import pbkdf2_sha256
from app import db
from datetime import datetime
import uuid

class User:

    def start_session(self, user):
        del user['password']

        session['logged_in'] = True
        session['user'] = user
        session['date'] = datetime.now()

        return jsonify(user), 200

    def signup(self):

        # Create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email":  request.form.get('email'),
            "balances": [{"current_balance":0,"date":datetime.now()}],
            "password":  request.form.get('password'),
            # "date": datetime.now()
        }

        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        #check for existing user
        if db.account.find_one({"email":user['email']}):
            return jsonify({"error":"Email address already in use"}),400

        if db.account.insert_one(user):
            return self.start_session(user)

        return jsonify({"error": "Signup failed"}), 400

    def signout(self):
        session.clear()
        return redirect('/')

    def login(self):

        user = db.account.find_one({
            "email":request.form.get('email')
        })

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)
        
        return jsonify({"error": "Invalid login credentials"}), 401
    
    def deposit(self):
        current_amount = db.account.find_one({
        "email":session['user']['email']}).balance

        deposit_ammount = request.form.get('deposit_withdraw')

        db.account.insert_one()
        


        return
    
    def withdraw(self):
        current_amount = db.account.find_one({
        "email":session['user']['email']}).balance

        deposit_ammount = request.form.get('deposit_withdraw')

        if current_amount == 0 and deposit_ammount < 0:
            return jsonify({"error": "Overdraft Error: Balance must be greater than $0 to withdraw funds"})