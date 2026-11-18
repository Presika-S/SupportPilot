from flask import Flask, request, jsonify, render_template

from classifier import process_ticket
from database import create_table, get_all_tickets, get_ticket_by_id

app = Flask(__name__)

create_table()


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/ticket", methods=["POST"])
def submit_ticket():
    try:
        data = request.get_json()

        required_fields = [
            "employee_name",
            "email",
            "title",
            "description"
        ]

        for field in required_fields:
            if not data or not data.get(field):
                return jsonify({
                    "error": f"Missing required field: {field}"
                }), 400

        result = process_ticket(
            employee_name=data["employee_name"],
            email=data["email"],
            title=data["title"],
            description=data["description"],
            business_impact=data.get("business_impact", "Medium"),
            department=data.get("department", "")
        )

        return jsonify({
            "message": "Ticket submitted successfully",
            "ticket": result
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/tickets", methods=["GET"])
def get_tickets():
    try:
        tickets = get_all_tickets()

        return jsonify({
            "total": len(tickets),
            "tickets": tickets
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/tickets/<int:ticket_id>", methods=["GET"])
def get_ticket(ticket_id):
    try:
        ticket = get_ticket_by_id(ticket_id)

        if ticket is None:
            return jsonify({"error": "Ticket not found"}), 404

        return jsonify({"ticket": ticket}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)