from flask import Flask, jsonify, request, session, redirect, send_file
from flask.helpers import send_file, url_for
from flask.templating import render_template
from werkzeug.utils import redirect 
from passlib.hash import pbkdf2_sha256
from app import db
from datetime import datetime
import uuid
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from io import BytesIO

# from user.routes import deposit


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
            "balances": [{"current_balance":0.00,"previous_balance":0.00,"amount_entered":0.00,"action":'Account Creation',"date":datetime.now().strftime("%m/%d/%Y %-I:%M %p")}],
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
        "email":session['user']['email']})['balances'][-1]['current_balance']

        try:
            deposit_amount = float(request.form.get('deposit_withdraw'))
        except:
            return jsonify({"error": "Please enter a positive number"}), 401
 
        deposit_amount = float("{0:.2f}".format(float(request.form.get('deposit_withdraw'))))

        try:
            if len(str(deposit_amount).split('.')[-1]) >2:
                return jsonify({"error": "Enter amounts in dollars and/or cents"}), 401
        except:
            pass

        if  deposit_amount<0.01:
            return jsonify({"error": "Please enter a positive number"}), 401

        
        new_amount = float("{0:.2f}".format(current_amount+deposit_amount))        

        db.account.update({"_id":session["user"]["_id"]},{"$push":{"balances":{"current_balance":new_amount,"previous_balance":current_amount,
        "amount_entered":deposit_amount,"action":"Deposit","date":datetime.now().strftime("%m/%d/%Y %-I:%M %p")}}})

        user = db.account.find_one({"_id":session["user"]["_id"]})
        return self.start_session(user)
    
        
    
    def withdraw(self):
        current_amount = db.account.find_one({
        "email":session['user']['email']})['balances'][-1]['current_balance']

        try:
            withdraw_amount = float(request.form.get('deposit_withdraw'))
        except:
            return jsonify({"error": "Please enter a positive number"}), 401

        withdraw_amount = float("{0:.2f}".format(float(request.form.get('deposit_withdraw'))))

        try:
            if len(str(withdraw_amount).split('.')[-1]) >2:
                return jsonify({"error": "Enter amounts in dollars and/or cents"}), 401
        except:
            pass

        if  withdraw_amount<0.01:
            return jsonify({"error": "Please enter a positive number"}), 401
        
        if current_amount-withdraw_amount<0:
            return jsonify({"error": "Insufficient Funds to Withdraw"}), 401
        
        new_amount = float("{0:.2f}".format(current_amount-withdraw_amount))

        db.account.update({"_id":session["user"]["_id"]},{"$push":{"balances":{"current_balance":new_amount,"previous_balance":current_amount,
        "amount_entered":withdraw_amount,"action":"Withdraw","date":datetime.now().strftime("%m/%d/%Y %-I:%M %p")}}})

        user = db.account.find_one({"_id":session["user"]["_id"]})
        return self.start_session(user)

        
    
    def visualize(self):
       
        matplotlib.use('Agg')
        
        vis_data = db.account.find_one({"email":'ryan@ryan.com'})

        vis_data = pd.DataFrame(list(vis_data['balances'][-5:]))

        vis_data['x'] = [x for x in range(1,len(vis_data)+1)]


        sns.set_style('darkgrid')


        fig, ax = plt.subplots()


        for i in range(len(vis_data)-1):

            if vis_data['current_balance'].iloc[i+1] > vis_data['current_balance'].iloc[i]:
                plt.plot(vis_data['x'][i:i+2],vis_data['current_balance'][i:i+2],color='green')
            else:
                plt.plot(vis_data['x'][i:i+2],vis_data['current_balance'][i:i+2],color='red') 

        ax.tick_params(labelsize=12)

        ax.set_xticks(vis_data['x'])
        ax.set_xticklabels([label.replace(' ', '\n',1) for label in vis_data['date']],fontsize=12)
        ax.set_xlabel('Transaction Date and Time',fontsize=14,labelpad=10)



        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_ylabel('Amount ($)',fontsize=14)

        canvas = FigureCanvas(fig)

        img = BytesIO()
        fig.savefig(img,bbox_inches='tight',dpi=300)
        img.seek(0)


        return send_file(img, mimetype='image/png')




    