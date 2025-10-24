from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError

from queries_user import clean_wipe_user_db, create_user, delete_user, get_all_users, get_user_by_user_id, get_user_by_username, update_balance

app = Flask(__name__)

class UserCreationRequest(BaseModel):
    name : str
    username : str
    balance : int

@app.route("/")
def home():
    return "Home"

@app.route("/create_user/", methods=["POST"])
def create_user_endpoint():
    try:

        request_data = UserCreationRequest(**request.get_json())
        
        user_id = create_user(
            name=request_data.name,
            username=request_data.username,
            initial_balance=request_data.balance)

        response_data = request_data.dict()
        response_data["user_id"] = user_id

        return jsonify(response_data)
    
    except ValidationError as e:
        return jsonify({"error":e.errors()}), 400

@app.route("/get_user/<username>",methods=["GET"])
def consult_user_endpoint(username):
    try:
        data = get_user_by_username(username)

        if data is None:
            return jsonify({"error":"Usuario nao encontrado."}),404
        else:
            return jsonify(data)
    
    except ValidationError as e:
        return jsonify({"error":e.errors}),400

@app.route("/delete_user/<username>", methods=["DELETE"])
def delete_user_endpoint(username):
    try:
        data = delete_user(username)
        if data is False:
            return jsonify({"error":"Usuario não encontrado!"}), 404
        else:
            return jsonify({"sucess":"Usuario removido com sucesso!"})
    
    except ValidationError as e:
        return jsonify({"error":e.errors}), 400

@app.route("/deposit_money/", methods=["POST"])
def update_balance_endpoint(username,amount):
    try:
        data = request.get_json()

        user_id = data.get("user_id")
        amount = data.get("amount")

        if amount is not int or float:
            return jsonify({"error":"Amount não é numero."})

        user_dict = get_user_by_user_id(user_id)

        if user_dict is None:
            return jsonify({"error":"Usuario nao encontrado."})
        
        

        return data
    except ValidationError as e:
        return jsonify({"error":e.errors})

@app.route("/get_all_users", methods=["GET"])
def get_all_users_endpoint():
    try:
        users = get_all_users()
        return jsonify(users)

    except ValidationError as e:
        return jsonify({"error":e.errors})

@app.route("/nuke_users", methods=["DELETE"])
def nuke_all_users_endpoint():
    try:
        users = clean_wipe_user_db()
        if users is True:
            return jsonify({"Sucess":"All users cleaned!"})
        else:
            return jsonify({"error":"Cant remove users."})
    except ValidationError as e:
        return jsonify({"error":e.errors})

if __name__ == "__main__":
    app.run(debug=True)
