from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.db.session import get_db
from app.schemas.schemas import MemoCreate, MemoUpdate, MemoResponse
from app.services.services import MemoService
from app.core.deps import get_current_active_user, get_current_user_optional
from app.db.models import User, MemoVisibility

router = APIRouter()


@router.post("/memos", response_model=MemoResponse, status_code=status.HTTP_201_CREATED)
async def create_memo(
    memo_data: MemoCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    memo_service = MemoService(db)
    db_memo = await memo_service.create_memo(memo_data, current_user.id)
    return db_memo


@router.get("/memos", response_model=List[MemoResponse])
async def list_memos(
    creator_id: Optional[int] = Query(None),
    visibility: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    pinned: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    memo_service = MemoService(db)
    
    if not current_user:
        visibility = "PUBLIC"
    elif not creator_id:
        creator_id = current_user.id
    
    memos = await memo_service.list_memos(
        creator_id=creator_id,
        visibility=visibility,
        tag=tag,
        pinned=pinned,
        skip=skip,
        limit=limit
    )
    
    filtered_memos = []
    for memo in memos:
        if memo.visibility == MemoVisibility.PUBLIC:
            filtered_memos.append(memo)
        elif memo.visibility == MemoVisibility.PROTECTED and current_user:
            filtered_memos.append(memo)
        elif memo.visibility == MemoVisibility.PRIVATE and current_user and memo.creator_id == current_user.id:
            filtered_memos.append(memo)
    
    return filtered_memos


@router.get("/memos/{memo_id}", response_model=MemoResponse)
async def get_memo(
    memo_id: int,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    memo_service = MemoService(db)
    memo = await memo_service.get_memo_by_id(memo_id)
    
    if not memo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memo not found"
        )
    
    if memo.visibility == MemoVisibility.PRIVATE:
        if not current_user or memo.creator_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
    elif memo.visibility == MemoVisibility.PROTECTED:
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
    
    return memo


@router.get("/memos/uid/{uid}", response_model=MemoResponse)
async def get_memo_by_uid(
    uid: str,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    memo_service = MemoService(db)
    memo = await memo_service.get_memo_by_uid(uid)
    
    if not memo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memo not found"
        )
    
    if memo.visibility == MemoVisibility.PRIVATE:
        if not current_user or memo.creator_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
    elif memo.visibility == MemoVisibility.PROTECTED:
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
    
    return memo


@router.patch("/memos/{memo_id}", response_model=MemoResponse)
async def update_memo(
    memo_id: int,
    memo_data: MemoUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    memo_service = MemoService(db)
    memo = await memo_service.get_memo_by_id(memo_id)
    
    if not memo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memo not found"
        )
    
    if memo.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own memos"
        )
    
    updated_memo = await memo_service.update_memo(memo_id, memo_data)
    return updated_memo


@router.delete("/memos/{memo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_memo(
    memo_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    memo_service = MemoService(db)
    memo = await memo_service.get_memo_by_id(memo_id)
    
    if not memo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memo not found"
        )
    
    if memo.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own memos"
        )
    
    await memo_service.delete_memo(memo_id)
