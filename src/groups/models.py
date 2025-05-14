from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, func, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base


class GroupModel(Base):
    __tablename__ = 'groups'

    group_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    name: Mapped[str] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    project_id: Mapped[UUID] = mapped_column(ForeignKey('projects.project_id', ondelete='CASCADE'))
    project: Mapped['ProjectModel'] = relationship(back_populates='groups')

    actions: Mapped[list['ActionModel']] = relationship(
        back_populates='group',
        lazy='selectin',
    )

    inputs: Mapped[list['InputModel']] = relationship(
        back_populates='group',
        foreign_keys='InputModel.group_id',
        lazy='selectin',
    )
    parents_inputs: Mapped[list['InputModel']] = relationship(
        back_populates='destination_group',
        foreign_keys='InputModel.destination_group_id',
    )

    buttons: Mapped[list['ButtonModel']] = relationship(
        back_populates='group',
        foreign_keys='ButtonModel.group_id',
        lazy='selectin',
    )
    parents_buttons: Mapped[list['ButtonModel']] = relationship(
        back_populates='destination_group',
        foreign_keys='ButtonModel.destination_group_id',
    )
