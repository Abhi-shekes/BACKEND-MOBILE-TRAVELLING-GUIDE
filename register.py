import pymongo

client = pymongo.MongoClient("mongodb+srv://REDACTED_USER:REDACTED_PASSWORD@REDACTED_HOST/")
db = client["Intelligent_Travelling"]

users_collection = db["User"]


def register_user(data):
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    city = data.get('city')

    user_data = {
        'name': name,
        'email': email,
        'password': password,
        'city': city
    }
    users_collection.insert_one(user_data)

    return {'message': 'User registered successfully!'}, 200