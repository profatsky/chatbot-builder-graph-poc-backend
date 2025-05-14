from datetime import datetime
from uuid import UUID

from sqlalchemy import func, DateTime, UniqueConstraint, ForeignKey, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.actions.enums import ActionType
from src.core.db import Base


class ActionModel(Base):
    __tablename__ = 'actions'

    action_id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    sequence_number: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    group_id: Mapped[UUID] = mapped_column(ForeignKey('groups.group_id', ondelete='CASCADE'))
    group: Mapped['GroupModel'] = relationship(back_populates='actions')

    type: Mapped[ActionType] = mapped_column(Enum(ActionType).values_callable)

    __mapper_args__ = {
        'polymorphic_identity': 'actions',
        'polymorphic_on': 'type',
    }
    __table_args__ = (
        UniqueConstraint('action_id', 'sequence_number'),
    )


class TextMessageActionModel(ActionModel):
    __tablename__ = 'text_message_actions'

    action_id: Mapped[UUID] = mapped_column(
        ForeignKey('actions.action_id', ondelete='CASCADE'),
        primary_key=True,
    )

    text: Mapped[str] = mapped_column(String(4096))

    __mapper_args__ = {
        'polymorphic_identity': ActionType.TEXT_MESSAGE,
    }


class ImageMessageActionModel(ActionModel):
    __tablename__ = 'image_message_actions'

    action_id: Mapped[UUID] = mapped_column(
        ForeignKey('actions.action_id', ondelete='CASCADE'),
        primary_key=True,
    )

    image_path: Mapped[str] = mapped_column(String(4096))

    __mapper_args__ = {
        'polymorphic_identity': ActionType.IMAGE_MESSAGE,
    }
