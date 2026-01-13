from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.db.session import get_db
from app.schemas.schemas import AttachmentResponse
from app.services.services import AttachmentService
from app.core.deps import get_current_active_user
from app.db.models import User
import os
import uuid
from pathlib import Path
from app.config import settings

router = APIRouter()


async def save_upload_file(upload_file: UploadFile, user_id: int) -> tuple:
    file_extension = os.path.splitext(upload_file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    data_dir = Path(settings.DATA_DIR) / "attachments" / str(user_id)
    data_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = data_dir / unique_filename
    
    with open(file_path, "wb") as buffer:
        content = await upload_file.read()
        buffer.write(content)
    
    file_size = len(content)
    file_type = upload_file.content_type
    
    return str(file_path), file_type, file_size


@router.post("/attachments", response_model=AttachmentResponse, status_code=status.HTTP_201_CREATED)
async def upload_attachment(
    file: UploadFile = File(...),
    memo_id: Optional[int] = Form(None),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    attachment_service = AttachmentService(db)
    
    file_path, file_type, file_size = await save_upload_file(file, current_user.id)
    
    db_attachment = await attachment_service.create_attachment(
        filename=file.filename,
        file_type=file_type,
        file_size=file_size,
        storage_type="local",
        reference=file_path,
        creator_id=current_user.id,
        memo_id=memo_id
    )
    
    return db_attachment


@router.get("/attachments", response_model=List[AttachmentResponse])
async def list_attachments(
    memo_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    attachment_service = AttachmentService(db)
    attachments = await attachment_service.list_attachments(memo_id=memo_id, skip=skip, limit=limit)
    return attachments


@router.get("/attachments/{attachment_id}", response_model=AttachmentResponse)
async def get_attachment(
    attachment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    attachment_service = AttachmentService(db)
    attachment = await attachment_service.get_attachment_by_id(attachment_id)
    
    if not attachment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attachment not found"
        )
    
    if attachment.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return attachment


@router.delete("/attachments/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attachment(
    attachment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    attachment_service = AttachmentService(db)
    attachment = await attachment_service.get_attachment_by_id(attachment_id)
    
    if not attachment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attachment not found"
        )
    
    if attachment.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    if attachment.storage_type == "local" and attachment.reference:
        file_path = Path(attachment.reference)
        if file_path.exists():
            file_path.unlink()
    
    await db.delete(attachment)
    await db.commit()
