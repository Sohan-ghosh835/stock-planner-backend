from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
import bcrypt

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["stockapp"]
users = db["users"]

def register_user(email, password):
    if users.find_one({"email": email}):
        return {"error": "Email already exists"}
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    users.insert_one({"email": email, "password": hashed_pw, "history": [], "investments": []})
    return {"message": "User registered"}

def login_user(email, password):
    user = users.find_one({"email": email})
    if not user or not bcrypt.checkpw(password.encode(), user['password']):
        return {"error": "Invalid credentials"}
    return {"user_id": str(user['_id']), "email": user['email']}

def save_search(user_id, ticker):
    users.update_one({"_id": ObjectId(user_id)}, {"$push": {"history": ticker}})

def save_investment(user_id, ticker, note):
    users.update_one({"_id": ObjectId(user_id)}, {"$push": {"investments": {"ticker": ticker, "note": note}}})

def get_user_data(user_id):
    user = users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return {"error": "User not found"}
    return {"email": user['email'], "history": user.get('history', []), "investments": user.get('investments', [])}
