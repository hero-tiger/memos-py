from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from typing import List, Optional
from app.db.session import get_db
from app.schemas.schemas import MemoResponse
from app.db.models import Memo, MemoVisibility, User
from app.core.deps import get_current_active_user, get_current_user_optional
import re

router = APIRouter()


class SearchService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def search_memos(
        self,
        query: str,
        creator_id: Optional[int] = None,
        visibility: Optional[str] = None,
        tag: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Memo]:
        db_query = select(Memo).options(selectinload(Memo.creator))
        
        conditions = []
        
        if query:
            search_pattern = f"%{query}%"
            conditions.append(Memo.content.ilike(search_pattern))
        
        if creator_id:
            conditions.append(Memo.creator_id == creator_id)
        
        if visibility:
            conditions.append(Memo.visibility == visibility)
        
        if tag:
            conditions.append(Memo.tags.contains([tag]))
        
        if conditions:
            db_query = db_query.where(and_(*conditions))
        
        db_query = db_query.order_by(Memo.created_ts.desc()).offset(skip).limit(limit)
        result = await self.db.execute(db_query)
        return result.scalars().all()
    
    async def filter_memos(
        self,
        creator_id: Optional[int] = None,
        visibility: Optional[str] = None,
        tag: Optional[str] = None,
        pinned: Optional[bool] = None,
        content_contains: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Memo]:
        db_query = select(Memo).options(selectinload(Memo.creator))
        
        conditions = []
        
        if creator_id:
            conditions.append(Memo.creator_id == creator_id)
        
        if visibility:
            conditions.append(Memo.visibility == visibility)
        
        if tag:
            conditions.append(Memo.tags.contains([tag]))
        
        if pinned is not None:
            conditions.append(Memo.pinned == pinned)
        
        if content_contains:
            conditions.append(Memo.content.ilike(f"%{content_contains}%"))
        
        if date_from:
            from datetime import datetime
            try:
                dt_from = datetime.fromisoformat(date_from)
                conditions.append(Memo.created_ts >= dt_from)
            except ValueError:
                pass
        
        if date_to:
            from datetime import datetime
            try:
                dt_to = datetime.fromisoformat(date_to)
                conditions.append(Memo.created_ts <= dt_to)
            except ValueError:
                pass
        
        if conditions:
            db_query = db_query.where(and_(*conditions))
        
        db_query = db_query.order_by(Memo.created_ts.desc()).offset(skip).limit(limit)
        result = await self.db.execute(db_query)
        return result.scalars().all()
    
    async def get_all_tags(self, creator_id: Optional[int] = None) -> List[str]:
        db_query = select(Memo)
        
        if creator_id:
            db_query = db_query.where(Memo.creator_id == creator_id)
        
        result = await self.db.execute(db_query)
        memos = result.scalars().all()
        
        all_tags = set()
        for memo in memos:
            if memo.tags:
                all_tags.update(memo.tags)
        
        return sorted(list(all_tags))
    
    async def get_memo_stats(self, creator_id: Optional[int] = None) -> dict:
        from sqlalchemy import func
        
        db_query = select(Memo)
        
        if creator_id:
            db_query = db_query.where(Memo.creator_id == creator_id)
        
        result = await self.db.execute(db_query)
        memos = result.scalars().all()
        
        total_memos = len(memos)
        pinned_memos = sum(1 for m in memos if m.pinned)
        
        visibility_counts = {}
        for v in MemoVisibility:
            visibility_counts[v.value] = sum(1 for m in memos if m.visibility == v)
        
        all_tags = set()
        for memo in memos:
            if memo.tags:
                all_tags.update(memo.tags)
        
        return {
            "total_memos": total_memos,
            "pinned_memos": pinned_memos,
            "visibility_counts": visibility_counts,
            "total_tags": len(all_tags),
            "unique_tags": sorted(list(all_tags))
        }


@router.get("/search/memos", response_model=List[MemoResponse])
async def search_memos(
    query: str = Query(..., min_length=1),
    creator_id: Optional[int] = Query(None),
    visibility: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    search_service = SearchService(db)
    
    if not current_user:
        visibility = "PUBLIC"
    elif not creator_id:
        creator_id = current_user.id
    
    memos = await search_service.search_memos(
        query=query,
        creator_id=creator_id,
        visibility=visibility,
        tag=tag,
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


@router.get("/filter/memos", response_model=List[MemoResponse])
async def filter_memos(
    creator_id: Optional[int] = Query(None),
    visibility: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    pinned: Optional[bool] = Query(None),
    content_contains: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    search_service = SearchService(db)
    
    if not current_user:
        visibility = "PUBLIC"
    elif not creator_id:
        creator_id = current_user.id
    
    memos = await search_service.filter_memos(
        creator_id=creator_id,
        visibility=visibility,
        tag=tag,
        pinned=pinned,
        content_contains=content_contains,
        date_from=date_from,
        date_to=date_to,
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


@router.get("/tags")
async def get_tags(
    creator_id: Optional[int] = Query(None),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    search_service = SearchService(db)
    
    if not creator_id and current_user:
        creator_id = current_user.id
    
    tags = await search_service.get_all_tags(creator_id=creator_id)
    return {"tags": tags}


@router.get("/stats")
async def get_stats(
    creator_id: Optional[int] = Query(None),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    search_service = SearchService(db)
    
    if not creator_id and current_user:
        creator_id = current_user.id
    
    stats = await search_service.get_memo_stats(creator_id=creator_id)
    return stats
