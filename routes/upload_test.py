from flask import Blueprint, request, jsonify
import os

upload_test_bp = Blueprint('upload_test', __name__)

upload_test_folder = 'data/test/'

if not os.path.exists(upload_test_folder):
    os.makedirs(upload_test_folder)

@upload_test_bp.route('/upload_test', methods=['GET', 'POST'])
def upload_test_file():
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
        file_path = os.path.join(upload_test_folder, file.filename)
        file.save(file_path)
        return jsonify({'message': 'Test file uploaded successfully', 'file_path': file_path}), 200
    
    return jsonify({'error': 'File upload failed'}), 500

