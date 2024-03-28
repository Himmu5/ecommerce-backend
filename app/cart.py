from fastapi import APIRouter, Request, HTTPException
from .models import Cart_Type
from .jwt_auth import verify_token
from .db_config import get_cart_collection

cart_router = APIRouter()


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
            await collection.update_one({"user_email": user_email}, {"$set": {"cart": str(new_cart.data)}})
        else:
            # Create new cart
            cart_data = {
                "user_email": user_email,
                "cart": str(new_cart.data)
            }
            await collection.insert_one(cart_data)
        
        return {"message": "Cart updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")