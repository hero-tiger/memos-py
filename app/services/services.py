from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_, or_
from sqlalchemy.orm import selectinload
from typing import List, Optional
from app.db.models import User, Memo, Attachment, Reaction, MemoRelation, PersonalAccessToken, UserSetting, InstanceSetting
from app.schemas.schemas import MemoCreate, MemoUpdate, UserCreate, UserUpdate, PersonalAccessTokenCreate
from datetime import datetime
import uuid


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_user(self, user_data: UserCreate, password_hash: str) -> User:
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            nickname=user_data.nickname,
            password_hash=password_hash,
            avatar_url=user_data.avatar_url,
            description=user_data.description
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()
    
    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user:
            for field, value in user_data.model_dump(exclude_unset=True).items():
                setattr(user, field, value)
            await self.db.commit()
            await self.db.refresh(user)
        return user
    
    async def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        result = await self.db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()


class MemoService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_memo(self, memo_data: MemoCreate, creator_id: int) -> Memo:
        db_memo = Memo(
            uid=str(uuid.uuid4()),
            creator_id=creator_id,
            content=memo_data.content,
            visibility=memo_data.visibility,
            tags=memo_data.tags,
            pinned=memo_data.pinned
        )
        self.db.add(db_memo)
        await self.db.commit()
        await self.db.refresh(db_memo)
        return db_memo
    
    async def get_memo_by_id(self, memo_id: int) -> Optional[Memo]:
        result = await self.db.execute(
            select(Memo)
            .options(selectinload(Memo.creator))
            .where(Memo.id == memo_id)
        )
        return result.scalar_one_or_none()
    
    async def get_memo_by_uid(self, uid: str) -> Optional[Memo]:
        result = await self.db.execute(
            select(Memo)
            .options(selectinload(Memo.creator))
            .where(Memo.uid == uid)
        )
        return result.scalar_one_or_none()
    
    async def update_memo(self, memo_id: int, memo_data: MemoUpdate) -> Optional[Memo]:
        result = await self.db.execute(select(Memo).where(Memo.id == memo_id))
        memo = result.scalar_one_or_none()
        if memo:
            for field, value in memo_data.model_dump(exclude_unset=True).items():
                setattr(memo, field, value)
            await self.db.commit()
            await self.db.refresh(memo)
        return memo
    
    async def delete_memo(self, memo_id: int) -> bool:
        result = await self.db.execute(select(Memo).where(Memo.id == memo_id))
        memo = result.scalar_one_or_none()
        if memo:
            await self.db.delete(memo)
            await self.db.commit()
            return True
        return False
    
    async def list_memos(
        self,
        creator_id: Optional[int] = None,
        visibility: Optional[str] = None,
        tag: Optional[str] = None,
        pinned: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Memo]:
        query = select(Memo).options(selectinload(Memo.creator))
        
        conditions = []
        if creator_id:
            conditions.append(Memo.creator_id == creator_id)
        if visibility:
            conditions.append(Memo.visibility == visibility)
        if tag:
            conditions.append(Memo.tags.contains([tag]))
        if pinned is not None:
            conditions.append(Memo.pinned == pinned)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        query = query.order_by(Memo.created_ts.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()


class AttachmentService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_attachment(
        self,
        filename: str,
        file_type: str,
        file_size: int,
        storage_type: str,
        reference: str,
        creator_id: int,
        memo_id: Optional[int] = None
    ) -> Attachment:
        db_attachment = Attachment(
            uid=str(uuid.uuid4()),
            creator_id=creator_id,
            memo_id=memo_id,
            filename=filename,
            file_type=file_type,
            file_size=file_size,
            storage_type=storage_type,
            reference=reference
        )
        self.db.add(db_attachment)
        await self.db.commit()
        await self.db.refresh(db_attachment)
        return db_attachment
    
    async def get_attachment_by_id(self, attachment_id: int) -> Optional[Attachment]:
        result = await self.db.execute(select(Attachment).where(Attachment.id == attachment_id))
        return result.scalar_one_or_none()
    
    async def list_attachments(self, memo_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Attachment]:
        query = select(Attachment)
        if memo_id:
            query = query.where(Attachment.memo_id == memo_id)
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()


class ReactionService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_reaction(self, memo_id: int, reaction: str, creator_id: int) -> Reaction:
        db_reaction = Reaction(
            creator_id=creator_id,
            memo_id=memo_id,
            reaction=reaction
        )
        self.db.add(db_reaction)
        await self.db.commit()
        await self.db.refresh(db_reaction)
        return db_reaction
    
    async def delete_reaction(self, reaction_id: int) -> bool:
        result = await self.db.execute(select(Reaction).where(Reaction.id == reaction_id))
        reaction = result.scalar_one_or_none()
        if reaction:
            await self.db.delete(reaction)
            await self.db.commit()
            return True
        return False
    
    async def list_reactions(self, memo_id: int) -> List[Reaction]:
        result = await self.db.execute(select(Reaction).where(Reaction.memo_id == memo_id))
        return result.scalars().all()


class PersonalAccessTokenService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_pat(self, pat_data: PersonalAccessTokenCreate, user_id: int, token: str) -> PersonalAccessToken:
        expires_at = None
        if pat_data.expires_in_days:
            expires_at = datetime.utcnow() + timedelta(days=pat_data.expires_in_days)
        
        db_pat = PersonalAccessToken(
            user_id=user_id,
            token=token,
            description=pat_data.description,
            expires_at=expires_at
        )
        self.db.add(db_pat)
        await self.db.commit()
        await self.db.refresh(db_pat)
        return db_pat
    
    async def delete_pat(self, pat_id: int, user_id: int) -> bool:
        result = await self.db.execute(
            select(PersonalAccessToken)
            .where(and_(PersonalAccessToken.id == pat_id, PersonalAccessToken.user_id == user_id))
        )
        pat = result.scalar_one_or_none()
        if pat:
            await self.db.delete(pat)
            await self.db.commit()
            return True
        return False
    
    async def list_pats(self, user_id: int) -> List[PersonalAccessToken]:
        result = await self.db.execute(
            select(PersonalAccessToken)
            .where(PersonalAccessToken.user_id == user_id)
        )
        return result.scalars().all()
