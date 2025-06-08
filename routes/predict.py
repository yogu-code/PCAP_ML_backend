from flask import Blueprint, request, jsonify
import os
from utils.preprocess_test import preprocess_test_file
import joblib

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        test_file_path = data.get('test_file_path')
        scaler_path = "models/"
        model_path = "models/"
        label_column = data.get('label_column')
        columns_to_drop = data.get('columns_to_drop', [])
        if not test_file_path:
            return jsonify({'error': 'test_file_path is required'}), 400
        X_test = preprocess_test_file(test_file_path, label_column, columns_to_drop, scaler_path, preview_rows=5)
        # Here we would load your model and make predictions
        predictions = {}
        for filename in os.listdir(model_path):
            if filename.endswith('.pkl') and not filename.startswith('scaler') and not filename.startswith('feature_columns'):
                model_name = filename.split('.')[0]
                model = joblib.load(os.path.join(model_path, filename))
                y_pred = model.predict(X_test)
                predictions[model_name] = y_pred.tolist()

                return jsonify({
                    'message': 'Prediction successful',
                    'predictions': predictions
                }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        