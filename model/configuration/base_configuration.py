from sqlalchemy.orm import DeclarativeBase

from model.serializable_model import SerializableModel


class BaseConfiguration(DeclarativeBase):
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
