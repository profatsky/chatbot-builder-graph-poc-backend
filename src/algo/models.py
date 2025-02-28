from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, func, String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.algo.enums import InputType
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

    inputs: Mapped[list['InputModel']] = relationship(
        back_populates='group',
        foreign_keys='InputModel.group_id',
    )
    parents_inputs: Mapped[list['InputModel']] = relationship(
        back_populates='destination_group',
        foreign_keys='InputModel.destination_group_id',
    )

    buttons: Mapped[list['ButtonModel']] = relationship(
        back_populates='group',
        foreign_keys='ButtonModel.group_id',
    )
    parents_buttons: Mapped[list['ButtonModel']] = relationship(
        back_populates='destination_group',
        foreign_keys='ButtonModel.destination_group_id',
    )


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

    group_id: Mapped[UUID] = mapped_column(ForeignKey('groups.group_id', ondelete='CASCADE'))
    group: Mapped['GroupModel'] = relationship(
        back_populates='inputs',
        foreign_keys='InputModel.group_id',
    )

    destination_group_id: Mapped[UUID] = mapped_column(ForeignKey('groups.group_id', ondelete='SET NULL'))
    destination_group: Mapped['GroupModel'] = relationship(
        back_populates='parents_inputs',
        foreign_keys='InputModel.destination_group_id',
    )


class ButtonModel(Base):
    __tablename__ = 'buttons'

    button_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    text: Mapped[str] = mapped_column(String(64))
    # TODO: payload might be json
    payload: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    group_id: Mapped[UUID] = mapped_column(ForeignKey('groups.group_id', ondelete='CASCADE'))
    group: Mapped['GroupModel'] = relationship(
        back_populates='buttons',
        foreign_keys='ButtonModel.group_id',
    )

    destination_group_id: Mapped[UUID] = mapped_column(ForeignKey('groups.group_id', ondelete='SET NULL'))
    destination_group: Mapped['GroupModel'] = relationship(
        back_populates='parents_buttons',
        foreign_keys='ButtonModel.destination_group_id',
    )
