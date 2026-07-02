from uuid import UUID, uuid4
from sqlalchemy import Integer, String, Uuid
from src.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class RedirModel(Base):
    __tablename__ = "redirs"

    user_uuid: Mapped[UUID] = mapped_column(
        Uuid(),
        default=uuid4,
        nullable=False,
        index=True
    )
    default_url: Mapped[str] = mapped_column(
        String(255), 
        nullable=False
    )
    redir_url: Mapped[str] = mapped_column(
        String(255), 
        unique=True, 
        index=True, 
        nullable=False
    )
    redir_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )