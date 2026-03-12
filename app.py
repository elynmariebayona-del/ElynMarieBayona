from flask import Flask, jsonify, request, render_template_string, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = "students.json"

# Load students from file or start empty
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        students = json.load(f)
else:
    students = []
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=4)

# Save students helper
def save_students():
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=4)

# Home / Dashboard
@app.route('/', methods=['GET', 'POST'])
def home():
    message = ""
    if request.method == 'POST':
        # Add new student
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
            message = f"{name} added successfully!"
        else:
            message = "All fields are required!"

    html = """
    <html>
    <head>
        <title>Student Dashboard</title>
        <style>
            body{font-family:Arial; background:linear-gradient(135deg,#ffb6c1,#ffc0cb,#ff69b4); text-align:center; padding:30px;}
            h1{color:#880e4f;}
            table{margin:auto; border-collapse:collapse; width:80%; background:white; box-shadow:0 10px 20px rgba(0,0,0,0.2);}
            th,td{border:1px solid #ddd; padding:12px;}
            th{background:#ff69b4; color:white;}
            tr:nth-child(even){background:#ffe4ec;}
            tr:hover{background:#ffc1e3;}
            form{margin-top:20px;}
            input{padding:8px; margin:5px; border-radius:6px; border:1px solid #ff69b4;}
            button{padding:6px 12px; margin:2px; border:none; border-radius:6px; cursor:pointer;}
            .btn-add{background:#ff1493; color:white;}
            .btn-add:hover{background:#c2185b;}
            .btn-edit{background:#ff69b4; color:white;}
            .btn-edit:hover{background:#d81b60;}
            .btn-delete{background:#f50057; color:white;}
            .btn-delete:hover{background:#c51162;}
            .message{color:#4a148c; font-weight:bold; margin-bottom:10px;}
        </style>
    </head>
    <body>
        <h1>🌸 Student Dashboard 🌸</h1>
        {% if message %}
            <div class="message">{{message}}</div>
        {% endif %}
        <table>
            <tr>
                <th>ID</th><th>Name</th><th>Grade</th><th>Section</th><th>Actions</th>
            </tr>
            {% for student in students %}
            <tr>
                <td>{{student.id}}</td>
                <td>{{student.name}}</td>
                <td>{{student.grade}}</td>
                <td>{{student.section}}</td>
                <td>
                    <a href="/edit/{{student.id}}"><button class="btn-edit">Edit</button></a>
                    <a href="/delete/{{student.id}}" onclick="return confirm('Are you sure?')"><button class="btn-delete">Delete</button></a>
                </td>
            </tr>
            {% endfor %}
        </table>

        <h2>Add New Student</h2>
        <form method="POST">
            <input type="text" name="name" placeholder="Student Name" required>
            <input type="text" name="grade" placeholder="Grade" required>
            <input type="text" name="section" placeholder="Section" required>
            <button type="submit" class="btn-add">Add Student</button>
        </form>
    </body>
    </html>
    """
    return render_template_string(html, students=students, message=message)

# Edit student
@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit_student(id):
    student = next((s for s in students if s["id"] == id), None)
    if not student:
        return redirect(url_for('home'))

    message = ""
    if request.method == 'POST':
        name = request.form.get('name')
        grade = request.form.get('grade')
        section = request.form.get('section')
        if name and grade and section:
            student["name"] = name
            student["grade"] = grade
            student["section"] = section
            save_students()
            return redirect(url_for('home'))
        else:
            message = "All fields are required!"

    html = """
    <html>
    <head>
        <title>Edit Student</title>
        <style>
            body{font-family:Arial; background:linear-gradient(135deg,#ffb6c1,#ffc0cb,#ff69b4); text-align:center; padding:50px;}
            input{padding:8px; margin:5px; border-radius:6px; border:1px solid #ff69b4;}
            button{padding:8px 15px; border:none; border-radius:6px; cursor:pointer; background:#ff1493; color:white;}
            button:hover{background:#c2185b;}
            .message{color:#4a148c; font-weight:bold;}
        </style>
    </head>
    <body>
        <h1>Edit Student</h1>
        {% if message %}<div class="message">{{message}}</div>{% endif %}
        <form method="POST">
            <input type="text" name="name" value="{{student.name}}" required>
            <input type="text" name="grade" value="{{student.grade}}" required>
            <input type="text" name="section" value="{{student.section}}" required>
            <button type="submit">Update Student</button>
        </form>
        <p><a href="/">Back to Dashboard</a></p>
    </body>
    </html>
    """
    return render_template_string(html, student=student, message=message)

# Delete student
@app.route('/delete/<int:id>')
def delete_student(id):
    global students
    students = [s for s in students if s["id"] != id]
    # Reassign IDs to keep sequential
    for i, s in enumerate(students, start=1):
        s["id"] = i
    save_students()
    return redirect(url_for('home'))

# API: get all students
@app.route('/students')
def get_students():
    return jsonify(students)

# API: get student by id
@app.route('/student/<int:id>')
def get_student_api(id):
    student = next((s for s in students if s["id"]==id), None)
    if student:
        return jsonify(student)
    return jsonify({"message":"Student not found"}),404

# API: add student via JSON POST
@app.route('/add_student', methods=['POST'])
def add_student_api():
    data = request.json
    new_student = {
        "id": len(students)+1,
        "name": data["name"],
        "grade": data["grade"],
        "section": data["section"]
    }
    students.append(new_student)
    save_students()
    return jsonify({"message":"Student added","student":new_student})

# 404 handler
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error":"Route not found"}),404

if __name__=="__main__":
    app.run(debug=True)
