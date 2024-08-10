from flask import Flask
from flask_cors import CORS
from routes import csv_routes
import sys

def create_app():
    app = Flask(__name__)
    sys.stdout.flush()
    CORS(app)  # Enable CORS for all routes and origins
    app.register_blueprint(csv_routes.bp)
    @app.route('/')
    def home():
        return 'Deployed'
    
    return app 

 

