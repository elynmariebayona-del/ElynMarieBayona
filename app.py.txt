from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to my Flask API!"

@app.route('/student')
def get_student():
    return jsonify({
        "name": "elyn",
        "grade": "3rd yr",
        "section": "android"
    })

if __name__ == "__main__":
    app.run(debug=True)
