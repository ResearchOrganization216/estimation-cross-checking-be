from flask import Blueprint, request, jsonify
from database import db
from app.types.role import Role
import uuid, datetime

role_bp = Blueprint('role_bp', __name__)

@role_bp.route('/', methods=['POST'])
def add_role():
    data = request.get_json()

    role_code = data.get('ROLE_CODE')
    role_name = data.get('ROLE_NAME')
    if not role_code or not role_name:
        return jsonify({"error": "ROLE_CODE and ROLE_NAME are required"}), 400

    role_uuid = data.get('UUID') or str(uuid.uuid4())

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
