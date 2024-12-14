import uuid

from sqlalchemy import (
    Column,
    UUID,
    String,
    DateTime,
    func,
    Boolean,
    Enum,
)
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from src.db.database import BaseUsers

class AuthToken(BaseUsers):
    __tablename__ = "auth"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token = Column(String(512), nullable=False, unique=True)
    entity_id = Column(UUID(as_uuid=True), nullable=False)  # ID пользователя
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Внешние связи (необязательно)
    user = relationship("User", foreign_keys="[AuthToken.entity_id]", viewonly=True)
