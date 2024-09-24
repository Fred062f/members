from flask import Flask, jsonify, request
from db import (
    init_db,
    fetch_members,
    fetch_member_by_id,
    delete_member_by_id,
    insert_member,
    update_member_by_id,
)

app = Flask(__name__)

init_db()


@app.route("/members", methods=["GET", "POST"])
def members():
    if request.method == "GET":
        try:
            members = fetch_members()
            return jsonify(members), 200
        except Exception as e:
            return jsonify({"error": "An error occurred: " + str(e)}), 500

    if request.method == "POST":
        member_data = request.get_json()
        try:
            insert_member(member_data)
            return jsonify({"message": "Member added successfully"}), 201
        except (ValueError, TypeError) as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "An error occurred: " + str(e)}), 500


@app.route("/members/<int:id>", methods=["GET", "DELETE", "PUT", "PATCH"])
def member(id):
    if request.method == "GET":
        try:
            member = fetch_member_by_id(id)
            if not member:
                return jsonify({"error": f"Member with ID {id} not found"}), 404
            return jsonify(member), 200
        except Exception as e:
            return jsonify({"error": "An error occurred: " + str(e)}), 500

    if request.method == "DELETE":
        try:
            member_deleted = delete_member_by_id(id)
            if not member_deleted:
                return jsonify({"error": f"Member with ID {id} not found"}), 404
            return "", 204
        except Exception as e:
            return jsonify({"error": "An error occurred: " + str(e)}), 500

    if request.method == "PATCH" or request.method == "PUT":
        try:
            member_data = request.get_json()
            member_updated = update_member_by_id(id, member_data)
            if not member_updated:
                return jsonify({"error": f"Member with ID {id} not found"}), 404
            return jsonify({"message": "Member's data updated successfully"}), 200
        except (ValueError, TypeError) as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "An error occurred: " + str(e)}), 500


app.run(debug=True)
