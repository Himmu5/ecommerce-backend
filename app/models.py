from pydantic import BaseModel, EmailStr
from typing import Dict

class Product(BaseModel):
    id: int
    title: str
    description: str
    price: float
    discount_percentage: float
    thumbnail: str
    category: str
    brand: str
    
class SIGNIN_REQUEST(BaseModel):
    email: EmailStr
    password: str
    
class SIGNUP_REQUEST(BaseModel):
    email: EmailStr
    password: str
    fullName: str

class User(BaseModel):
    id: str
    email: EmailStr
    fullName: str
    
class SIGNIN_RESPONSE(BaseModel):
    user: User
    token: str
    
class Cart_Type(BaseModel):
    data: Dict[int, int]

    