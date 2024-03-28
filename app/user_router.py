from fastapi import APIRouter,HTTPException,status,Header
from fastapi.responses import JSONResponse
from .models import SIGNIN_REQUEST,SIGNUP_REQUEST,SIGNIN_RESPONSE,User
from .jwt_auth import create_access_token, verify_token
from .db_config import get_user_collection
from fastapi.security import OAuth2PasswordBearer
import pymongo.errors

user_router = APIRouter()

@user_router.post("/login", response_model=SIGNIN_RESPONSE)
async def get_user(cred: SIGNIN_REQUEST):
    if not cred.email:
        return JSONResponse(content={"error": "Email not found"}, status_code=400)
    elif not cred.password:
        return JSONResponse(content={"error": "Password not found"}, status_code=400)
    else:
        user = await authenticate_user(cred.email, cred.password)
        if not user:
            return JSONResponse(content={"error": "Invalid credentials"}, status_code=404)
        else:
            data = {"email": cred.email,"password": cred.password}
            token ="Bearer "+create_access_token(data)
            user['id'] = str(user['_id'])
        return {"user": user, "token": token}

 
    
async def create_user(email: str, password: str, fullName: str):
    try:
        collection = get_user_collection()
        # Create the unique index on email if it doesn't exist yet
        collection.create_index("email", unique=True)
        created_user = await collection.insert_one({'email': email, 'password': password, 'fullName': fullName})
        return {
            'id': str(created_user.inserted_id),
            'email': email,
            'fullName': fullName
        }
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@user_router.post("/signup", response_model=SIGNIN_RESPONSE, status_code=status.HTTP_201_CREATED)
async def signup(cred: SIGNUP_REQUEST):
    if not cred.email or not cred.fullName or not cred.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input data")
    else:
        user = await create_user(cred.email, cred.password, cred.fullName)
        data = {"email": cred.email,"password": cred.password}
        token = "bearer "+create_access_token(data)
        return { "user": user, "token": token}
    
    
@user_router.get("/me",response_model=User)
async def reAuth(authorization: str = Header(...)):
    try:
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        token = authorization.replace("Bearer ", "")

        # Example: Replace with your token verification logic
        user = verify_token(token)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        # Example: Replace with your user authentication logic
        verified_user = await authenticate_user(user.get("email"), user.get("password"))
        if verified_user is None:
            raise HTTPException(status_code=401, detail="User not found")

        verified_user['id'] = str(verified_user['_id'])
        return verified_user
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
        
async def authenticate_user(email: str, password: str):
    collection = get_user_collection()
    return await collection.find_one({"email": email, "password": password})
    