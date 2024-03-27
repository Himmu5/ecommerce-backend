from fastapi import FastAPI
from .user_router import user_router
from .product_router import product_router
from .cart import cart_router
app = FastAPI()

app.include_router(user_router)
app.include_router(product_router)
app.include_router(cart_router)
