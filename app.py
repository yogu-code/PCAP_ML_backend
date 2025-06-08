from flask import Flask
from flask_cors import CORS
from routes.upload import upload_bp
from routes.preprocess import preprocess_bp
from routes.train import train_bp
from routes.upload_test import upload_test_bp
from routes.predict import predict_bp

app = Flask(__name__)

# Enable CORS for all routes, allowing requests from port 3000
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

app.register_blueprint(upload_bp)
app.register_blueprint(preprocess_bp)
app.register_blueprint(train_bp)
app.register_blueprint(upload_test_bp)
app.register_blueprint(predict_bp)

if __name__ == '__main__':
    app.run(debug=True, port=8080) # Run the app on port 8080