"""Hostel Room Allocation REST API (Flask + SQLite). Base URL: http://localhost:3000/api/rooms"""
import os
import sqlite3

from flask import Flask, jsonify, request

import database as db
from validation import validate_room


def create_app() -> Flask:
    app = Flask(__name__)
    db.init_db()

    def read_json():
        """Returns the JSON object from the request body, or None if missing/malformed."""
        data = request.get_json(force=True, silent=True)
        return data if isinstance(data, dict) else None

    def bad_body():
        return jsonify(error="Request body must be a valid JSON object"), 400

    def not_found(room_id):
        return jsonify(error=f"Room with id {room_id} not found"), 404

    def invalid(errors):
        return jsonify(error="Validation failed", details=errors), 400

    def conflict(exc):
        if "UNIQUE" in str(exc):
            return jsonify(error="A room with this room number already exists"), 409
        return jsonify(error="Data violates a database rule"), 400

    # ---------------------------------------------------------------- CREATE
    @app.post("/api/rooms")
    def create_room():
        data = read_json()
        if data is None:
            return bad_body()
        clean, errors = validate_room(data)
        if errors:
            return invalid(errors)
        try:
            new_id = db.create_room(clean)
        except sqlite3.IntegrityError as exc:
            return conflict(exc)
        resp = jsonify(db.get_room(new_id))
        resp.status_code = 201
        resp.headers["Location"] = f"/api/rooms/{new_id}"
        return resp

    # ---------------------------------------------------------------- READ
    @app.get("/api/rooms")
    def get_all_rooms():
        flag = request.args.get("available")
        if flag is not None and flag.lower() not in ("true", "false"):
            return jsonify(error="Query parameter 'available' must be true or false"), 400
        return jsonify(db.list_rooms(only_available=(flag or "").lower() == "true")), 200

    @app.get("/api/rooms/<int:room_id>")
    def get_one_room(room_id):
        room = db.get_room(room_id)
        if room is None:
            return not_found(room_id)
        return jsonify(room), 200

    # ---------------------------------------------------------------- UPDATE
    @app.put("/api/rooms/<int:room_id>")
    def update_room(room_id):
        data = read_json()
        if data is None:
            return bad_body()
        if db.get_room(room_id) is None:
            return not_found(room_id)
        clean, errors = validate_room(data)
        if errors:
            return invalid(errors)
        try:
            db.update_room(room_id, clean)
        except sqlite3.IntegrityError as exc:
            return conflict(exc)
        return jsonify(db.get_room(room_id)), 200

    # ---------------------------------------------------------------- DELETE
    @app.delete("/api/rooms/<int:room_id>")
    def delete_room(room_id):
        if not db.delete_room(room_id):
            return not_found(room_id)
        return jsonify(message="Room deleted successfully", id=room_id), 200

    # ---------------------------------------------------------------- errors
    @app.errorhandler(404)
    def handle_404(_):
        return jsonify(error="Resource not found"), 404

    @app.errorhandler(405)
    def handle_405(_):
        return jsonify(error="Method not allowed"), 405

    @app.errorhandler(500)
    def handle_500(_):
        return jsonify(error="Internal server error"), 500

    return app


if __name__ == "__main__":
    port = int(os.getenv("PORT", "3000"))
    print(f"API running at http://localhost:{port}/api/rooms")
    create_app().run(host="127.0.0.1", port=port, debug=False)
