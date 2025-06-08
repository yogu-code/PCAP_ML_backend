from flask import Blueprint, request, jsonify
import os
from utils.train import train

train_bp = Blueprint('train', __name__)

@train_bp.route('/train', methods=['POST'])

def train_model():
    try:
        # Read request JSON
        data = request.get_json()
        X_path = data.get('X_path')
        y_path = data.get('y_path')
        
        if not X_path or not y_path:
            return jsonify({'error': 'X_path and y_path are required'}), 400
        
        results, trained_models = train(X_path, y_path)
        
        return jsonify({
            'message': 'Training successful',
            'results': results,
            'trained_models': {name: str(model) for name, model in trained_models.items()}
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
