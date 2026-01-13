from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.schemas.schemas import PersonalAccessTokenCreate, PersonalAccessTokenResponse
from app.services.services import PersonalAccessTokenService
from app.core.deps import get_current_active_user
from app.core.security import generate_pat_token
from app.db.models import User

router = APIRouter()


@router.post("/tokens", response_model=PersonalAccessTokenResponse, status_code=status.HTTP_201_CREATED)
async def create_pat(
    pat_data: PersonalAccessTokenCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    pat_service = PersonalAccessTokenService(db)
    token = generate_pat_token()
    db_pat = await pat_service.create_pat(pat_data, current_user.id, token)
    return db_pat


@router.get("/tokens", response_model=List[PersonalAccessTokenResponse])
async def list_pats(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    pat_service = PersonalAccessTokenService(db)
    pats = await pat_service.list_pats(current_user.id)
    return pats


@router.delete("/tokens/{token_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pat(
    token_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    pat_service = PersonalAccessTokenService(db)
    deleted = await pat_service.delete_pat(token_id, current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Token not found"
        )
