from flask import Flask, jsonify, request, render_template_string
import json
import os

app = Flask(__name__)
DATA_FILE = "students.json"

# Load students from file or create default if file doesn't exist
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        students = json.load(f)
else:
    students = [
        {"id": 1, "name": "ELYN MARIE BAYONA", "grade": "3rd yr", "section": "ANDROID"},
        {"id": 2, "name": "MARIA LOPEZ", "grade": "2nd yr", "section": "WEB DEV"},
        {"id": 3, "name": "JOHN DOE", "grade": "1st yr", "section": "NETWORKING"}
    ]
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=4)

# Helper to save students
def save_students():
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=4)

# Home page with table + form
@app.route('/', methods=['GET', 'POST'])
def home():
    message = ""
    if request.method == 'POST':
        name = request.form.get('name')
        grade = request.form.get('grade')
        section = request.form.get('section')
        if name and grade and section:
            new_student = {
                "id": len(students) + 1,
                "name": name,
                "grade": grade,
                "section": section
            }
            students.append(new_student)
            save_students()
            message = f"Student {name} added successfully!"
        else:
            message = "All fields are required!"
    
    html = """
    <html>
        <head>
            <title>Student API</title>
            <style>
                body { font-family: Arial; background: #f2f2f2; text-align: center; padding: 30px; }
                h1 { color: #333; }
                table { margin: 20px auto; border-collapse: collapse; width: 70%; }
                th, td { border: 1px solid #999; padding: 10px; }
                th { background-color: #4CAF50; color: white; }
                tr:nth-child(even) { background-color: #ddd; }
                tr:hover { background-color: #ccc; }
                form { margin-top: 20px; }
                input { padding: 5px; margin: 5px; }
                .message { color: green; font-weight: bold; }
            </style>
        </head>
        <body>
            <h1>Student List</h1>
            {% if message %}
            <div class="message">{{ message }}</div>
            {% endif %}
            <table>
                <tr><th>ID</th><th>Name</th><th>Grade</th><th>Section</th></tr>
                {% for student in students %}
                <tr>
                    <td>{{ student.id }}</td>
                    <td>{{ student.name }}</td>
                    <td>{{ student.grade }}</td>
                    <td>{{ student.section }}</td>
                </tr>
                {% endfor %}
            </table>
            
            <h2>Add New Student</h2>
            <form method="POST">
                <input type="text" name="name" placeholder="Name" required>
                <input type="text" name="grade" placeholder="Grade" required>
                <input type="text" name="section" placeholder="Section" required>
                <input type="submit" value="Add Student">
            </form>
        </body>
    </html>
    """
    return render_template_string(html, students=students, message=message)

# API route to get all students
@app.route('/students')
def get_students():
    return jsonify(students)

# API route to get student by ID
@app.route('/student/<int:id>')
def get_student(id):
    for student in students:
        if student["id"] == id:
            return jsonify(student)
    return jsonify({"message": "Student not found"}), 404

# API route to add student via JSON POST
@app.route('/add_student', methods=['POST'])
def add_student_api():
    data = request.json
    new_student = {
        "id": len(students) + 1,
        "name": data["name"],
        "grade": data["grade"],
        "section": data["section"]
    }
    students.append(new_student)
    save_students()
    return jsonify({"message": "Student added successfully", "student": new_student})

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Route not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
