from fastapi import APIRouter
from app.api.v1 import users, memos, tokens, attachments, search

api_router = APIRouter()

api_router.include_router(users.router, tags=["users"])
api_router.include_router(memos.router, tags=["memos"])
api_router.include_router(tokens.router, tags=["tokens"])
api_router.include_router(attachments.router, tags=["attachments"])
api_router.include_router(search.router, tags=["search"])
