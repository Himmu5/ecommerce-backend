from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://adityacha703:zHzsSj1iOs1JVsQJ@cluster0.g8euxgb.mongodb.net/"
client = AsyncIOMotorClient(MONGO_URL)
database = client["ecommerceDb"]

def get_product_collection():
    return database["products"];

def get_user_collection():
    return database["users"];

def get_cart_collection():
    return database["cart"]