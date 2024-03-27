from fastapi import APIRouter, Request
from .models import Cart_Type
from .middleware import AuthMiddleware

cart_router = APIRouter(route_class=AuthMiddleware)

@cart_router.post("/carts")
def saveCart(request:Request ,new_cart: Cart_Type):
    return {"cart": new_cart}
