import pymongo

client = pymongo.MongoClient("mongodb+srv://REDACTED_USER:REDACTED_PASSWORD@REDACTED_HOST/")
db = client["Intelligent_Travelling"]
users_collection = db["User"]


def change_password(email, newpassword):
    try:
        user = users_collection.find_one({"email": email})

        if user:
            users_collection.update_one({"email": email}, {"$set": {"password": newpassword}})
            return {'message': 'Password changed successfully!'}
        else:
            return {'message': 'User not found.'}
    except Exception as e:
        return {'message': f'An error occurred: {str(e)}'}
