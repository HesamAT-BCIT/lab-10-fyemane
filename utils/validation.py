from __future__ import annotations

from flask import jsonify, request


def validate_profile_data(first_name, last_name, student_id):
    """Validate required profile fields."""
    if not first_name or not str(first_name).strip():
        return "All fields are required."
    if not last_name or not str(last_name).strip():
        return "All fields are required."
    if not student_id or not str(student_id).strip():
        return "All fields are required."
    return None


def normalize_profile_data(first_name, last_name, student_id):
    """Normalize profile fields for storage."""
    return {
        "first_name": str(first_name).strip() if first_name is not None else "",
        "last_name": str(last_name).strip() if last_name is not None else "",
        "student_id": str(student_id).strip() if student_id is not None else "",
    }


def require_json_content_type():
    """Ensure request content type is JSON."""
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    return None