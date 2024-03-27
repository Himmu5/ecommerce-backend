from fastapi import Request, HTTPException
from .jwt_auth import verify_token
from fastapi.routing import APIRoute
from typing import Callable

class AuthMiddleware(APIRoute):
    async def __call__(self, request: Request) -> Callable:
        if "Authorization" not in request.headers:
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = request.headers["Authorization"].replace("Bearer ", "")
        try:
            payload = verify_token(token)
            request.state.user = payload
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid token")

        return await super().__call__(request)
