from flask import Blueprint, request, jsonify
from google.oauth2 import service_account
from google.cloud import storage
from config import Config  # Importing configuration values

upload_bp = Blueprint('upload_bp', __name__)

# Use configuration values from the Config class
BUCKET_NAME = Config.BUCKET_NAME
KEY_PATH = Config.KEY_PATH
PROJECT_ID = Config.PROJECT_ID

# Create credentials object and initialize the Storage client
credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
client = storage.Client(credentials=credentials, project=PROJECT_ID)

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected."}), 400

    try:
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file)
        
        # Not calling blob.make_public() since uniform bucket-level access is enabled.
        return jsonify({
            "message": "File uploaded successfully.",
            "file_url": blob.public_url
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
