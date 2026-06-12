# ============================================================
# CodeCraftHub - Course Tracker API
# A beginner-friendly Flask REST API using JSON file storage
# ============================================================

from flask import Flask, jsonify, request
from datetime import datetime
import json
import os

# ------------------------------------
# App Setup
# ------------------------------------

app = Flask(__name__)

# Path to our JSON "database" file
DATA_FILE = "courses.json"


# ------------------------------------
# Helper Functions
# ------------------------------------

def read_courses():
    """
    Reads and returns all course data from courses.json.
    If the file doesn't exist yet, it creates a fresh one automatically.
    """
    if not os.path.exists(DATA_FILE):
        # First run — create the file with an empty courses list
        initial_data = {"courses": [], "next_id": 1}
        write_courses(initial_data)
        return initial_data

    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        # The file exists but is unreadable or corrupted
        raise RuntimeError(f"Could not read {DATA_FILE}: {str(e)}")


def write_courses(data):
    """
    Saves the given data dictionary back to courses.json.
    indent=2 makes the file human-readable when you open it.
    """
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        raise RuntimeError(f"Could not write to {DATA_FILE}: {str(e)}")


def validate_course_fields(body, require_all=True):
    """
    Checks that the request body has the fields we need.

    - require_all=True  → used on POST (all fields must be present)
    - require_all=False → used on PUT (only validate fields that were sent)

    Returns a list of error messages. An empty list means everything is valid.
    """
    errors = []
    valid_statuses = ["Not Started", "In Progress", "Completed"]

    required_fields = ["name", "description", "target_date", "status"]

    if require_all:
        # Every field must be present
        for field in required_fields:
            if not body.get(field):
                errors.append(f"'{field}' is required.")
    else:
        # Only validate fields that were actually sent in the request
        if "name" in body and not body["name"].strip():
            errors.append("'name' cannot be empty.")
        if "description" in body and not body["description"].strip():
            errors.append("'description' cannot be empty.")

    # Validate target_date format if provided
    if "target_date" in body and body["target_date"]:
        try:
            datetime.strptime(body["target_date"], "%Y-%m-%d")
        except ValueError:
            errors.append("'target_date' must be in YYYY-MM-DD format (e.g. 2026-08-01).")

    # Validate status value if provided
    if "status" in body and body["status"]:
        if body["status"] not in valid_statuses:
            errors.append(
                f"'status' must be one of: {', '.join(valid_statuses)}."
            )

    return errors


def find_course(courses_list, course_id):
    """
    Searches for a course by its integer ID.
    Returns (index, course_dict) if found, or (None, None) if not.
    """
    for i, course in enumerate(courses_list):
        if course["id"] == course_id:
            return i, course
    return None, None


# ------------------------------------
# Routes
# ------------------------------------

# ── POST /api/courses ──────────────────────────────────────
@app.route("/api/courses", methods=["POST"])
def create_course():
    """
    Add a new course.

    Expects JSON body:
    {
        "name":        "Flask for Beginners",
        "description": "Learn routing, templates, and REST basics",
        "target_date": "2026-08-01",
        "status":      "Not Started"
    }
    """
    body = request.get_json()

    # Reject the request if no JSON body was sent at all
    if not body:
        return jsonify({"error": "Request body must be JSON."}), 400

    # Validate all required fields
    errors = validate_course_fields(body, require_all=True)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        data = read_courses()
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

    # Build the new course object
    new_course = {
        "id":           data["next_id"],           # auto-incremented integer
        "name":         body["name"].strip(),
        "description":  body["description"].strip(),
        "target_date":  body["target_date"],
        "status":       body["status"],
        "created_at":   datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    }

    # Append to the list and bump the ID counter for next time
    data["courses"].append(new_course)
    data["next_id"] += 1

    try:
        write_courses(data)
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

    # 201 Created is the correct HTTP status for a successful POST
    return jsonify({
        "message": "Course created successfully.",
        "course":  new_course
    }), 201


# ── GET /api/courses ───────────────────────────────────────
@app.route("/api/courses", methods=["GET"])
def get_all_courses():
    """
    Return every course in the tracker.
    Supports an optional ?status= query parameter to filter results.

    Example: GET /api/courses?status=In Progress
    """
    try:
        data = read_courses()
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

    courses = data["courses"]

    # Optional filter by status
    status_filter = request.args.get("status")
    if status_filter:
        courses = [c for c in courses if c["status"] == status_filter]

    return jsonify({
        "total":   len(courses),
        "courses": courses
    }), 200


# ── GET /api/courses/<id> ──────────────────────────────────
@app.route("/api/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    """
    Return a single course by its numeric ID.
    <int:course_id> tells Flask to only match integer values in the URL.
    """
    try:
        data = read_courses()
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

    _, course = find_course(data["courses"], course_id)

    if course is None:
        # 404 Not Found — standard when a resource doesn't exist
        return jsonify({"error": f"Course with ID {course_id} not found."}), 404

    return jsonify({"course": course}), 200


# ── PUT /api/courses/<id> ──────────────────────────────────
@app.route("/api/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    """
    Update one or more fields of an existing course.
    Only the fields you send will be changed — everything else stays the same.

    Example body (partial update):
    {
        "status": "Completed"
    }
    """
    body = request.get_json()

    if not body:
        return jsonify({"error": "Request body must be JSON."}), 400

    # Validate only the fields that were sent
    errors = validate_course_fields(body, require_all=False)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        data = read_courses()
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

    index, course = find_course(data["courses"], course_id)

    if course is None:
        return jsonify({"error": f"Course with ID {course_id} not found."}), 404

    # Fields the user is allowed to update (id and created_at are immutable)
    updatable_fields = ["name", "description", "target_date", "status"]

    for field in updatable_fields:
        if field in body:
            # Strip whitespace from string fields before saving
            value = body[field]
            data["courses"][index][field] = value.strip() if isinstance(value, str) else value

    try:
        write_courses(data)
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "message": "Course updated successfully.",
        "course":  data["courses"][index]
    }), 200


# ── DELETE /api/courses/<id> ───────────────────────────────
@app.route("/api/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    """
    Permanently remove a course by its ID.
    """
    try:
        data = read_courses()
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

    index, course = find_course(data["courses"], course_id)

    if course is None:
        return jsonify({"error": f"Course with ID {course_id} not found."}), 404

    # Remove the course from the list by its index
    deleted_course = data["courses"].pop(index)

    try:
        write_courses(data)
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "message": f"Course '{deleted_course['name']}' deleted successfully.",
        "course":  deleted_course
    }), 200


# ------------------------------------
# 404 Handler
# ------------------------------------

@app.errorhandler(404)
def not_found(e):
    """Catches requests to any URL that doesn't match a defined route."""
    return jsonify({"error": "Endpoint not found. Check the URL and try again."}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    """Catches requests using the wrong HTTP method on a known route."""
    return jsonify({"error": "HTTP method not allowed on this endpoint."}), 405


# ------------------------------------
# Run the App
# ------------------------------------

if __name__ == "__main__":
    # debug=True → auto-reloads the server when you save app.py
    # Turn this OFF in production!
    print("🚀 CodeCraftHub API is running at http://127.0.0.1:5000")
    app.run(debug=True)