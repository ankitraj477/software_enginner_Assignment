from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Initialize seats: 80 seats, divided into rows with the last row having 3 seats
seats = {
    row: ["free"] * (7 if row < 11 else 3)
    for row in range(1, 13)
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/seats")
def get_seats():
    # Convert seat status to a format suitable for the frontend
    seat_status = []
    for row, row_seats in seats.items():
        for col, status in enumerate(row_seats, start=1):
            seat_status.append({"seat": f"Row {row} Seat {col}", "status": status})
    return jsonify({"seats": seat_status})

@app.route("/book", methods=["POST"])
def book_seats():
    data = request.json
    num_seats = data.get("seats")

    if not num_seats or num_seats < 1 or num_seats > 7:
        return jsonify({"error": "Invalid number of seats. Must be between 1 and 7."}), 400

    # Try booking in a single row first
    booked_seats = []
    for row, row_seats in seats.items():
        if row_seats.count("free") >= num_seats:
            for i in range(len(row_seats)):
                if row_seats[i] == "free" and len(booked_seats) < num_seats:
                    row_seats[i] = "booked"
                    booked_seats.append(f"Row {row} Seat {i + 1}")
            return jsonify({"booked_seats": booked_seats})

    # If a single row isn't available, book nearby seats
    for row, row_seats in seats.items():
        for i in range(len(row_seats)):
            if row_seats[i] == "free" and len(booked_seats) < num_seats:
                row_seats[i] = "booked"
                booked_seats.append(f"Row {row} Seat {i + 1}")
            if len(booked_seats) == num_seats:
                return jsonify({"booked_seats": booked_seats})

    return jsonify({"error": "Not enough seats available."}), 400

if __name__ == "__main__":
    app.run(debug=True)


