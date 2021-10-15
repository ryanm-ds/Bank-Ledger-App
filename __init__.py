from flask import Flask


from .extensions import mongo
from .main.routes import main

def create_app():
    app = Flask(__name__)

    app.config['MONGO_URI'] = 'mongodb+srv://rvm8989:PASSWORD@cluster0.6r8p9.mongodb.net/account?retryWrites=true&w=majority'

    mongo.init_app(app)
    app.register_blueprint(main)
    return app