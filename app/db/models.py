from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum


class UserRole(str, enum.Enum):
    HOST = "HOST"
    ADMIN = "ADMIN"
    USER = "USER"


class MemoVisibility(str, enum.Enum):
    PUBLIC = "PUBLIC"
    PROTECTED = "PROTECTED"
    PRIVATE = "PRIVATE"


class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    nickname = Column(String(100))
    password_hash = Column(String(255), nullable=False)
    avatar_url = Column(String(500))
    role = Column(Enum(UserRole), default=UserRole.USER)
    description = Column(Text)
    created_ts = Column(DateTime(timezone=True), server_default=func.now())
    updated_ts = Column(DateTime(timezone=True), onupdate=func.now())
    
    memos = relationship("Memo", back_populates="creator", cascade="all, delete-orphan")
    attachments = relationship("Attachment", back_populates="creator", cascade="all, delete-orphan")
    personal_access_tokens = relationship("PersonalAccessToken", back_populates="user", cascade="all, delete-orphan")
    user_settings = relationship("UserSetting", back_populates="user", cascade="all, delete-orphan")


class Memo(Base):
    __tablename__ = "memo"
    
    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String(100), unique=True, index=True, nullable=False)
    creator_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    visibility = Column(Enum(MemoVisibility), default=MemoVisibility.PRIVATE)
    tags = Column(JSON, default=list)
    payload = Column(JSON, default=dict)
    pinned = Column(Boolean, default=False)
    created_ts = Column(DateTime(timezone=True), server_default=func.now())
    updated_ts = Column(DateTime(timezone=True), onupdate=func.now())
    
    creator = relationship("User", back_populates="memos")
    attachments = relationship("Attachment", back_populates="memo", cascade="all, delete-orphan")
    reactions = relationship("Reaction", back_populates="memo", cascade="all, delete-orphan")
    relations = relationship("MemoRelation", foreign_keys="[MemoRelation.memo_id]", back_populates="memo", cascade="all, delete-orphan")


class Attachment(Base):
    __tablename__ = "attachment"
    
    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String(100), unique=True, index=True, nullable=False)
    creator_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    memo_id = Column(Integer, ForeignKey("memo.id", ondelete="CASCADE"), nullable=True)
    filename = Column(String(500), nullable=False)
    file_type = Column(String(100))
    file_size = Column(Integer)
    storage_type = Column(String(50), default="local")
    reference = Column(String(1000))
    payload = Column(JSON, default=dict)
    created_ts = Column(DateTime(timezone=True), server_default=func.now())
    updated_ts = Column(DateTime(timezone=True), onupdate=func.now())
    
    creator = relationship("User", back_populates="attachments")
    memo = relationship("Memo", back_populates="attachments")


class Reaction(Base):
    __tablename__ = "reaction"
    
    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    memo_id = Column(Integer, ForeignKey("memo.id", ondelete="CASCADE"), nullable=False)
    reaction = Column(String(50), nullable=False)
    created_ts = Column(DateTime(timezone=True), server_default=func.now())
    
    creator = relationship("User")
    memo = relationship("Memo", back_populates="reactions")


class MemoRelation(Base):
    __tablename__ = "memo_relation"
    
    id = Column(Integer, primary_key=True, index=True)
    memo_id = Column(Integer, ForeignKey("memo.id", ondelete="CASCADE"), nullable=False)
    related_memo_id = Column(Integer, ForeignKey("memo.id", ondelete="CASCADE"), nullable=False)
    type = Column(String(50), nullable=False)
    created_ts = Column(DateTime(timezone=True), server_default=func.now())
    
    memo = relationship("Memo", foreign_keys=[memo_id], back_populates="relations")
    related_memo = relationship("Memo", foreign_keys=[related_memo_id])


class PersonalAccessToken(Base):
    __tablename__ = "personal_access_token"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(String(500))
    issued_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))
    
    user = relationship("User", back_populates="personal_access_tokens")


class UserSetting(Base):
    __tablename__ = "user_setting"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    key = Column(String(100), nullable=False)
    value = Column(Text)
    created_ts = Column(DateTime(timezone=True), server_default=func.now())
    updated_ts = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="user_settings")


class InstanceSetting(Base):
    __tablename__ = "instance_setting"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, index=True, nullable=False)
    value = Column(Text)
    description = Column(Text)
    created_ts = Column(DateTime(timezone=True), server_default=func.now())
    updated_ts = Column(DateTime(timezone=True), onupdate=func.now())
