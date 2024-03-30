from fastapi import FastAPI
from .user_router import user_router
from .product_router import product_router
from .cart import cart_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
    "https://ecommerce-site-himanshu.netlify.app"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    )
app.include_router(user_router)
app.include_router(product_router)
app.include_router(cart_router)

