from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    HOST = "HOST"
    ADMIN = "ADMIN"
    USER = "USER"


class MemoVisibility(str, Enum):
    PUBLIC = "PUBLIC"
    PROTECTED = "PROTECTED"
    PRIVATE = "PRIVATE"


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    description: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    description: Optional[str] = None


class UserResponse(UserBase):
    id: int
    role: UserRole
    created_ts: datetime
    updated_ts: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None


class MemoBase(BaseModel):
    content: str = Field(..., min_length=1)
    visibility: MemoVisibility = MemoVisibility.PRIVATE
    tags: Optional[List[str]] = []
    pinned: bool = False


class MemoCreate(MemoBase):
    pass


class MemoUpdate(BaseModel):
    content: Optional[str] = None
    visibility: Optional[MemoVisibility] = None
    tags: Optional[List[str]] = None
    pinned: Optional[bool] = None


class MemoResponse(MemoBase):
    id: int
    uid: str
    creator_id: int
    creator: UserResponse
    created_ts: datetime
    updated_ts: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AttachmentBase(BaseModel):
    filename: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None


class AttachmentResponse(AttachmentBase):
    id: int
    uid: str
    creator_id: int
    memo_id: Optional[int] = None
    storage_type: str
    reference: Optional[str] = None
    created_ts: datetime
    
    class Config:
        from_attributes = True


class ReactionBase(BaseModel):
    reaction: str = Field(..., max_length=50)


class ReactionResponse(ReactionBase):
    id: int
    creator_id: int
    memo_id: int
    created_ts: datetime
    
    class Config:
        from_attributes = True


class PersonalAccessTokenCreate(BaseModel):
    description: Optional[str] = None
    expires_in_days: Optional[int] = None


class PersonalAccessTokenResponse(BaseModel):
    id: int
    token: str
    description: Optional[str] = None
    issued_at: datetime
    expires_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserSettingBase(BaseModel):
    key: str
    value: Optional[str] = None


class UserSettingResponse(UserSettingBase):
    id: int
    user_id: int
    created_ts: datetime
    updated_ts: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class InstanceSettingBase(BaseModel):
    key: str
    value: Optional[str] = None
    description: Optional[str] = None


class InstanceSettingResponse(InstanceSettingBase):
    id: int
    created_ts: datetime
    updated_ts: Optional[datetime] = None
    
    class Config:
        from_attributes = True
