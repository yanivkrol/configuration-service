from abc import abstractmethod
from typing import TypeVar, Type

from sqlalchemy.orm import Session, DeclarativeBase

from model.configuration.base_configuration import BaseConfiguration
from repository.base_repository import BaseRepository

ConfigurationModelT = TypeVar('ConfigurationModelT', bound=BaseConfiguration)


class ConfigurationRepository(BaseRepository):
    def __init__(self, model: Type[ConfigurationModelT], session: Session):
        super().__init__(model, session)

    @abstractmethod
    def add_all_from_values(self, rows: list[dict[str, DeclarativeBase]]): # TODO better name
        ...
