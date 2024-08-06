from flask import request, jsonify
from io import StringIO
import pandas as pd
from services.csv_service import process_csv_data
from . import bp

@bp.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    if file and file.filename.endswith('.csv'):
        try:
            file_data = file.read().decode('utf-8')
            result = process_csv_data(file_data)
            return result, 200, {'Content-Type': 'text/csv'}
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Unsupported file type, only CSV allowed'}), 400
