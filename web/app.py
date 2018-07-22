from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import bcrypt
from pymongo import MongoClient
import spacy

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SimilarityDB
users = db["Users"]

def UserExist(username):
    if users.find({"username": username}).count() == 0:
        return False
    else:
        return True

class Register(Resource):
    def post(self):
        posted_data = request.get_json()

        username = posted_data["username"]
        password = posted_data["password"]

        # todo: check incoming post variables

        if UserExist(username):
            resp = {
                "status": 301,
                "message": "Invalid username"
            }
            return jsonify(resp)
        
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert({
            "username": username,
            "password": hashed_pw,
            "Tokens": 6
        })

        resp = {
            "status": 200,
            "message": "Successfully signed up for the API"
        }

        return jsonify(resp)

def verifyPw(username, pw):
     hashed_pw = users.find(
         {"username": username}
     )[0]["password"]

     if bcrypt.hashpw(pw.encode('utf8'), hashed_pw.encode('utf8')) == hashed_pw:
         return True
     else:
         return False

def countTokens(username):
    return users.find({"username": username})[0]["Tokens"]

class Detect(Resource):
    def post(self):
        posted_data = request.get_json()

        username = posted_data["username"]
        password = posted_data["password"]
        text1 = posted_data["text1"]
        text2 = posted_data["text2"]

        # todo: check incoming post variables

        if not UserExist(username):
            resp = {
                "status": 301,
                "message": "Invalid username"
            }
            return jsonify(resp)
        
        correct_pw = verifyPw(username, password)

        if not correct_pw:
            resp = {
                "status": 302
            }
            return jsonify(resp)
        
        num_of_tokens = countTokens(username)

        if num_of_tokens <= 0:
            resp = {
                "status": 301,
                "message": "Out of tokens"
            }
            return jsonify(resp)

        nlp = spacy.load('en_core_web_sm')

        text1 = nlp(text1)
        text2 = nlp(text2)

        ratio = text1.similarity(text2)

        resp = {
            "status": 200,
            "similarity": ratio,
            "message": "Similarity score calculated successfully"
        }

        users.update({"username":username},
        {
            "$set": {"Tokens": num_of_tokens - 1}
        })

        return jsonify(resp)

class Refill(Resource):
    def post(self):
        posted_data = request.get_json()

        username = posted_data["username"]
        refill = posted_data["refill"]
        admin_pw = posted_data["admin_pw"]

        if not UserExist(username):
            resp = {
                "status": 301,
                "message": "sorry, invalid username"
            }

            return jsonify(resp)
        
        if not admin_pw == "password":
            resp = {
                "status": 304,
                "message": "Invalid password"
            }

            return jsonify(resp)
        
        current_tokens = countTokens(username)

        users.update(
            { "username": username},
            {
                "$set": { "Tokens": refill+current_tokens}
            }
        )

        resp = {
            "status": 200,
            "message": "Refilled successfully"
        }

        return jsonify(resp)

api.add_resource(Register, "/register")
api.add_resource(Detect, "/detect")
api.add_resource(Refill, "/refill")

@app.route('/')
def hello():
    return "HelloWorld"

if __name__ == "__main__":
    app.run(host="0.0.0.0")


