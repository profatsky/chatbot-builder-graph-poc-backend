from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, func, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base


class ButtonModel(Base):
    __tablename__ = 'buttons'

    button_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    text: Mapped[str] = mapped_column(String(64))
    # TODO: payload might be json
    payload: Mapped[str] = mapped_column(String(64))

    sequence_number: Mapped[int]

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    group_id: Mapped[UUID] = mapped_column(ForeignKey('groups.group_id', ondelete='CASCADE'))
    group: Mapped['GroupModel'] = relationship(
        back_populates='buttons',
        foreign_keys='ButtonModel.group_id',
    )

    destination_group_id: Mapped[UUID] = mapped_column(
        ForeignKey('groups.group_id', ondelete='SET NULL'),
        nullable=True,
    )
    destination_group: Mapped['GroupModel'] = relationship(
        back_populates='parents_buttons',
        foreign_keys='ButtonModel.destination_group_id',
    )
