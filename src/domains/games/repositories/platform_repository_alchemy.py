from dataclasses import dataclass
from sqlalchemy.orm import Session


from src.domains.games.entities import PlatformEntity
from src.domains.games.models import PlatformModel
from src.domains.games.repositories.platform_repository import PlatformRepository


@dataclass
class PlatformRepositoryAlchemy(PlatformRepository):
    session: Session

    def create_platform(self, platform_data: PlatformEntity) -> PlatformEntity:
        platform_model = PlatformModel(**platform_data.model_dump())

        self.session.add(platform_model)
        self.session.commit()
        self.session.refresh(platform_model)

        platform_entity = PlatformEntity.transform_model_to_entity(model=platform_model)

        return platform_entity
