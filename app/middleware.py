from fastapi import Request, HTTPException
from fastapi.routing import APIRoute
from typing import Callable
from .jwt_auth import verify_token

class AuthMiddleware(APIRoute):
    async def __call__(self, request: Request) -> Callable:
        async def call_next(request: Request) -> Callable:
            if "Authorization" not in request.headers:
                raise HTTPException(status_code=401, detail="Unauthorized")
    
            token = request.headers["Authorization"]
            print("token: ",token)
            try:
                payload = verify_token(token)
                request.state.user = payload
            except Exception as e:
                raise HTTPException(status_code=401, detail="Invalid token")

            return await self.endpoint(request)

        return await call_next(request)
