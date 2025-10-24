from flask import Flask, request, jsonify

from queries_user import create_user

app = Flask(__name__)

@app.route("/")
def home():
    return "Home"

@app.route("/create_user/", methods=["POST"])
def getting_data():
    data = request.json()

    name =data["name"]
    username = data["username"]
    initial_balance = data["initial_balance"]

    user_data_id = create_user(username, name, initial_balance)
    return {"user_id": user_data_id}

if __name__ == "__name__":
    app.run(debug=True)
