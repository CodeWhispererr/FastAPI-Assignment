from .models import UserCreate
from passlib.context import CryptContext
from bson import ObjectId

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    user_dict = user.dict()
    user_dict["password"] = hashed_password
    result = db.users.insert_one(user_dict)
    user_id = result.inserted_id
    add_sample_user_preferences(db, user_id)
    return {"id": str(user_id), **user_dict}

def get_user_by_email(db, email: str):
    return db.users.find_one({"email": email})

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def link_id_to_user(db, email: str, id: str):
    result = db.users.update_one({"email": email}, {"$set": {"linked_id": id}})
    if result.modified_count == 1:
        return {"message": "ID linked successfully"}
    return {"message": "Failed to link ID"}

def delete_user_and_related_data(db, email: str):
    user = db.users.find_one({"email": email})
    if user:
        db.users.delete_one({"_id": user["_id"]})
        db.user_data.delete_many({"user_id": user["_id"]})
        db.user_preferences.delete_many({"user_id": user["_id"]})

def add_sample_user_preferences(db, user_id):
    sample_preferences = {
        "user_id": user_id,
        "theme": "dark",
        "notifications": True,
        "language": "en"
    }
    db.user_preferences.insert_one(sample_preferences)

def get_user_data_with_joins(db, email: str):
    pipeline = [
        {"$match": {"email": email}},
        {"$lookup": {
            "from": "user_data",
            "localField": "_id",
            "foreignField": "user_id",
            "as": "data"
        }},
        {"$lookup": {
            "from": "user_preferences",
            "localField": "_id",
            "foreignField": "user_id",
            "as": "preferences"
        }},
        {"$project": {
            "email": 1,
            "username": 1,
            "linked_id": 1,
            "data": 1,
            "preferences": {"$ifNull": [{"$arrayElemAt": ["$preferences", 0]}, {}]}
        }}
    ]
    result = list(db.users.aggregate(pipeline))
    return result[0] if result else None

def update_user_preferences(db, email: str, preferences: dict):
    user = db.users.find_one({"email": email})
    if user:
        db.user_preferences.update_one(
            {"user_id": user["_id"]},
            {"$set": preferences},
            upsert=True
        )
        return True
    return False