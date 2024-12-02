from fastapi import APIRouter
from app.api.v1.endpoints import auth, calendar, chat, image

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(calendar.router, prefix="/calendar", tags=["calendar"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(image.router, prefix="/image", tags=["image"]) 