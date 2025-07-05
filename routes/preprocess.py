from flask import Blueprint, request, jsonify
from utils.preprocessing import preprocess_pcap_csv
import os

preprocess_bp = Blueprint('preprocess', __name__)

@preprocess_bp.route('/preprocess', methods=['POST'])
def preprocess():
    try:
        # Read request JSON
        data = request.get_json()
        file_path = data.get('file_path')
        scaler_save_path = 'models/'

        print(f"Received file_path: {file_path}")

        # Validate file exists
        if not os.path.exists(file_path):
            return jsonify({'error': f'File not found: {file_path}'}), 400

        # Preprocess CSV
        try:
            X_scaled, y, scaler, preview = preprocess_pcap_csv(
                file_path,
                os.path.join(scaler_save_path, 'scaler.pkl')
            )
        except Exception as preprocess_error:
            print(f"Error in preprocess_pcap_csv: {preprocess_error}")
            return jsonify({'error': f'Failed to preprocess: {str(preprocess_error)}'}), 500

        # Return features
        return jsonify({
            'message': 'Preprocessing successful',
            'features': X_scaled.columns.tolist(),
            'columns': preview.columns.tolist(),  # Include all columns for dropdown
            'preview': preview.to_dict(orient='records'),
            'X_path': 'data/X_scaled.csv',
            'y_path': 'data/y.csv',
        }), 200

    except Exception as e:
        print(f"General error: {e}")
        return jsonify({'error': str(e)}), 500
