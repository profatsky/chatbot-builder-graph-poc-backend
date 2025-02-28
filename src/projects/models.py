import datetime
from uuid import UUID

from sqlalchemy import DateTime, func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base


class ProjectModel(Base):
    __tablename__ = 'projects'

    project_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    name: Mapped[str] = mapped_column(String(256))
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    groups: Mapped[list['GroupModel']] = relationship(back_populates='project')
