from flask import Blueprint, request, jsonify
import os
import pandas as pd

upload_bp = Blueprint('upload', __name__)

upload_folder = 'data/'
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

@upload_bp.route('/')
def home():
    return 'Welcome to NetSense! Go to /upload to upload a file.'

@upload_bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        # Simple HTML form for file upload
        return '''
            <form method="post" enctype="multipart/form-data">
                <input type="file" name="file">
                <input type="submit" value="Upload">
            </form>
        '''
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        try:
            file_path = os.path.join(upload_folder, file.filename)
            file.save(file_path)

            # Read CSV preview
            df = pd.read_csv(file_path)
            preview = df.head(10).to_dict(orient='records')
            columns = df.columns.tolist()

            return jsonify({
                'message': 'File uploaded successfully',
                'file_path': file_path,
                'preview': preview,
                'columns': columns
            }), 200

        except Exception as e:
            return jsonify({'error': f'File upload failed: {str(e)}'}), 500

    return jsonify({'error': 'File upload failed'}), 500
