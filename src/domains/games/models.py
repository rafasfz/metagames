from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.resources.abstracts.models import AbstractModel

association_table = Table(
    "games_platforms",
    AbstractModel.metadata,
    Column("game_id", ForeignKey("games.id")),
    Column("platform_id", ForeignKey("platforms.id")),
)


class PlatformModel(AbstractModel):
    __tablename__ = "platforms"

    name: Mapped[str] = mapped_column("name", nullable=False, unique=True)
    games: Mapped[list["GameModel"]] = relationship(secondary=association_table)


class GameModel(AbstractModel):
    __tablename__ = "games"

    name: Mapped[str] = mapped_column("name", nullable=False, unique=True)
    description: Mapped[str] = mapped_column("description", nullable=False)
    platforms: Mapped[list["PlatformModel"]] = relationship(secondary=association_table)
