from flask import Blueprint, request, jsonify
from config import Config
from google.oauth2 import service_account
from google.cloud import storage
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from app.types.user import User
import uuid
import datetime
import jwt

auth_bp = Blueprint('auth_bp', __name__)

# Setup Google Cloud Storage client using config values
if Config.KEY_PATH:
    credentials = service_account.Credentials.from_service_account_file(Config.KEY_PATH)
    storage_client = storage.Client(credentials=credentials, project=Config.PROJECT_ID)
else:
    # In Cloud Run, KEY_PATH will be empty so use the default credentials.
    storage_client = storage.Client(project=Config.PROJECT_ID)

@auth_bp.route('/register', methods=['POST'])
def register_user():
    # Retrieve form data (multipart/form-data)
    username = request.form.get('username')
    email = request.form.get('email')
    address = request.form.get('address')
    password = request.form.get('password')
    mobile = request.form.get('mobile')
    created_by = request.form.get('created_user')
    # Get UUID from form; if not provided, generate one
    user_uuid = request.form.get('uuid') or str(uuid.uuid4())

    # Validate required fields
    if not username or not email or not password:
        return jsonify({"error": "username, email, and password are required"}), 400

    # Process profile image if provided
    file = request.files.get('profile_image')
    profile_url = None
    if file:
        try:
            bucket = storage_client.bucket(Config.BUCKET_NAME)
            # Prepend the uuid to the filename and store under "user_attachments" folder
            new_filename = f"user_attachments/{user_uuid}_{file.filename}"
            blob = bucket.blob(new_filename)
            blob.upload_from_file(file)
            # Use blob.public_url if public access is enabled via IAM settings
            profile_url = blob.public_url
        except Exception as e:
            return jsonify({"error": "Failed to upload profile image: " + str(e)}), 500

    # Hash the password before storing
    password_hash = generate_password_hash(password)

    # Generate a user code (ensuring it fits within 20 characters)
    user_code = str(uuid.uuid4())[:20]

    new_user = User(
        USER_CODE=user_code,
        USER_NAME=username,
        UUID=user_uuid,  # Store the provided or generated UUID
        USER_EMAIL=email,
        USER_ADDRESS=address,
        USER_PASSWORD_HASH=password_hash,
        USER_IMAGE_PATH=profile_url,
        USER_MOBILE=mobile,
        USER_STATUS='A',  # Active
        CREATED_USER_CODE=created_by,
        CREATED_DATE=datetime.datetime.utcnow()
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully", "user_code": user_code}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error: " + str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON data"}), 400

    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(USER_EMAIL=email).first()
    if not user or not check_password_hash(user.USER_PASSWORD_HASH, password):
        return jsonify({"error": "Invalid email or password"}), 401

    payload = {
        "Email": user.USER_EMAIL,
        "Name": user.USER_NAME,
        "Mobile": user.USER_MOBILE,
        "Address": user.USER_ADDRESS,
        "image_path": user.USER_IMAGE_PATH,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }

    try:
        token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
    except Exception as e:
        return jsonify({"error": "Failed to generate token: " + str(e)}), 500

    response = jsonify({"message": "Login successful", "token": token})
    response.set_cookie("token", token, httponly=True)
    return response, 200
