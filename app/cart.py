from fastapi import APIRouter, Request, HTTPException
from typing import List
from .models import Cart_Type
import json
from .jwt_auth import verify_token
from .db_config import get_cart_collection, get_product_collection
from .models import Cart_Response

cart_router = APIRouter()

@cart_router.get("/carts", response_model=List[Cart_Response])
async def getCart(request: Request):
    if "Authorization" not in request.headers:
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = request.headers["Authorization"]
    try:
        payload = dict(verify_token(token))
        user_email = payload.get("email")
        collection = get_cart_collection()
        product_collection = get_product_collection()
        # Check if cart already exists for the user
        existing_cart = await collection.find_one({"user_email": user_email})
        products = []
        if existing_cart:
            # Update existing cart
            cart_str = existing_cart.get("cart")
            cart_obj = json.loads(cart_str)
            ids = list(cart_obj.keys())
            for id in ids:
                product = await product_collection.find_one({"id": int(id)})
                product_object = { "product": product, "quantity": cart_obj[id] }
                products.append(product_object)
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail="something went wrong")    

@cart_router.post("/carts")
async def saveCart(request: Request, new_cart: Cart_Type):
    if "Authorization" not in request.headers:
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = request.headers["Authorization"]
    print("data: ", dict(new_cart.data))
    
    try:
        payload = dict(verify_token(token))
        user_email = payload.get("email")
        collection = get_cart_collection()

        # Check if cart already exists for the user
        existing_cart = await collection.find_one({"user_email": user_email})
        
        if existing_cart:
            # Update existing cart
            await collection.update_one({"user_email": user_email}, {"$set": {"cart": json.dumps(new_cart.data)}})
        else:
            # Create new cart
            cart_data = {
                "user_email": user_email,
                "cart": json.dumps(new_cart.data)
            }
            await collection.insert_one(cart_data)
        
        return {"message": "Cart updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")