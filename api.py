from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError

from queries_user import create_user, delete_user, get_user_by_username

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

        return jsonify(data)
    
    except ValidationError as e:
        return jsonify({"error":"Usuario não encontrado!"}),404

@app.route("/delete_user/<username>", methods=["DELETE"])
def delete_user_endpoint(username):
    try:
        delete_user(username)

        return jsonify({"sucess":"Usuario removido com sucesso!"})
    
    except ValidationError as e:
        return jsonify({"error":"Usuario não encontrado!"}), 404
    

if __name__ == "__main__":
    app.run(debug=True)
