from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

DATA_FILE = "students.json"

# Load students from file or create default list if file doesn't exist
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        students = json.load(f)
else:
    students = [
        {"id": 1, "name": "elyn", "grade": "3rd yr", "section": "android"},
        {"id": 2, "name": "maria", "grade": "2nd yr", "section": "web dev"},
        {"id": 3, "name": "john", "grade": "1st yr", "section": "networking"}
    ]
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=4)

# Helper function to save students to file
def save_students():
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=4)

# Home route
@app.route('/')
def home():
    return "Welcome to my Flask API!"

# Get all students
@app.route('/students')
def get_students():
    return jsonify(students)

# Get student by ID
@app.route('/student/<int:id>')
def get_student(id):
    for student in students:
        if student["id"] == id:
            return jsonify(student)
    return jsonify({"message": "Student not found"}), 404

# Add new student
@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.json
    new_student = {
        "id": len(students) + 1,
        "name": data["name"],
        "grade": data["grade"],
        "section": data["section"]
    }
    students.append(new_student)
    save_students()  # save to JSON file
    return jsonify({"message": "Student added successfully", "student": new_student})

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Route not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
