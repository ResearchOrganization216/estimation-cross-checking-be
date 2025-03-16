from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid
import datetime
from flask import Flask, request, jsonify
from google.oauth2 import service_account
from google.cloud import storage
import os

app = Flask(__name__)

# Update the connection string below with your actual DB credentials, host, port, and database name.
# For example: 'postgresql://username:password@localhost:5432/yourdbname'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/InnoAInsure'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
BUCKET_NAME = "innoainsure-bucket"
key_path = "C:\\Users\\Sithija\\Documents\\keyfiles\\proven-answer-451215-k1-190fdb8da7df.json"
credentials = service_account.Credentials.from_service_account_file(key_path)
client = storage.Client(credentials=credentials, project="proven-answer-451215-k1")
bucket = client.bucket("innoainsure-bucket")

db = SQLAlchemy(app)

# SQLAlchemy model mapping to the "base"."ROLE" table
class Role(db.Model):
    __tablename__ = 'ROLE'
    __table_args__ = {'schema': 'base'}  # specify the schema name
    ROLE_CODE = db.Column(db.String(20), primary_key=True)
    ROLE_NAME = db.Column(db.String(500), nullable=False)
    UUID = db.Column(db.String(100), nullable=False)
    CREATED_USER_CODE = db.Column(db.String(20))
    CREATED_DATE = db.Column(db.DateTime)
    LAST_MOD_USER_CODE = db.Column(db.String(20))
    LAST_MOD_DATE = db.Column(db.DateTime)

@app.route('/api/role', methods=['POST'])
def add_role():
    data = request.get_json()

    # Validate required fields
    role_code = data.get('ROLE_CODE')
    role_name = data.get('ROLE_NAME')
    if not role_code or not role_name:
        return jsonify({"error": "ROLE_CODE and ROLE_NAME are required"}), 400

    # Use provided UUID or generate a new one
    role_uuid = data.get('UUID') or str(uuid.uuid4())

    # Use current UTC time if CREATED_DATE is not provided
    created_date = data.get('CREATED_DATE')
    if not created_date:
        created_date = datetime.datetime.utcnow()
    else:
        try:
            created_date = datetime.datetime.fromisoformat(created_date)
        except Exception as e:
            return jsonify({"error": "Invalid CREATED_DATE format. Please use ISO format."}), 400

    new_role = Role(
        ROLE_CODE=role_code,
        ROLE_NAME=role_name,
        UUID=role_uuid,
        CREATED_USER_CODE=data.get('CREATED_USER_CODE'),
        CREATED_DATE=created_date,
        LAST_MOD_USER_CODE=data.get('LAST_MOD_USER_CODE'),
        LAST_MOD_DATE=data.get('LAST_MOD_DATE') 
    )

    try:
        db.session.add(new_role)
        db.session.commit()
        return jsonify({"message": "Role added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@app.route('/upload', methods=['POST'])
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
        
        return jsonify({
            "message": "File uploaded successfully.",
            "file_url": blob.public_url  # Note: This URL is only accessible if public read is granted via IAM.
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Hello, Flask Backend!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
