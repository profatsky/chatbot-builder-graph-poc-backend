from datetime import datetime
from uuid import UUID

from sqlalchemy import func, ForeignKey, Enum, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.inputs.enums import InputType
from src.core.db import Base


class InputModel(Base):
    __tablename__ = 'inputs'

    input_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    type: Mapped[InputType] = mapped_column(
        Enum(InputType).values_callable,
        # nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    group_id: Mapped[UUID] = mapped_column(ForeignKey('groups.group_id', ondelete='CASCADE'))
    group: Mapped['GroupModel'] = relationship(
        back_populates='inputs',
        foreign_keys='InputModel.group_id',
    )

    destination_group_id: Mapped[UUID] = mapped_column(
        ForeignKey('groups.group_id', ondelete='SET NULL'),
        nullable=True,
    )
    destination_group: Mapped['GroupModel'] = relationship(
        back_populates='parents_inputs',
        foreign_keys='InputModel.destination_group_id',
    )

    __table_args__ = (
        UniqueConstraint('group_id', 'type'),
    )
