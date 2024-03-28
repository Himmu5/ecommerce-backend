from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
database = client["ecommerceDb"]

def get_product_collection():
    return database["products"];

def get_user_collection():
    return database["users"];

def get_cart_collection():
    return database["cart"]