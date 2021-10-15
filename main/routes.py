from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request
from account_app.extentions import mongo
from bson.objectid import ObjectId

main = Blueprint('main',__name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/users',methods=['POST'])
def create_user():
    try:
        db_response = mongo.db.account.insert_one(user)
    except Exception as ex:
        print(ex)


@main.route('/get_user/<str:user>',methods=['POST'])
def user_insert(user):
    account_collection = mongo.db.account
    user_action = request.form.get('user') 

    user_check = [account_collection.find_one({'user':user_action})]

    if not user_check:



    return redirect(url_for('main.index'))

@main.route('/user/deposit', methods=['POST'])
def deposit():
    account_collection = mongo.db.account
    deposit_action = request.form.get('deposit')
    
    account_collection.find_one({'user':user_action})

    deposit_action.insert_one({'balance':deposit_action,'date':datetime.datetime.utcnow()})
    return redirect(url_for('main.index'))

