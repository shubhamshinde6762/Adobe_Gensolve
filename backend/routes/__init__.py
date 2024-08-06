from flask import Blueprint

bp = Blueprint('csv_routes', __name__)

from . import csv_routes
