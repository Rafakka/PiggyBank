from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Home"

if __name__ == "__name__":
    app.run(debug=True)
