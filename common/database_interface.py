from typing import Optional, TypeVar, Type, Generic

from sqlalchemy.orm import Session, DeclarativeBase

ModelT = TypeVar('ModelT', bound=DeclarativeBase)


class DatabaseInterface(Generic[ModelT]):
    def __init__(self, model: Type[ModelT], session: Session):
        self.model = model
        self.session = session

    def get_all(self) -> list[ModelT]:
        return self.session.query(self.model).all()

    def get_by_id(self, id: int) -> Optional[ModelT]:
        return self.session.query(self.model).where(self.model.id == id).first()

    def add(self, record) -> None:
        self.session.add(record)

    def update(self, id: str, update: dict) -> None:
        self.session.query(self.model).where(self.model.id == id).update(update)

    def delete(self, id: int) -> None:
        record = self.get_by_id(id)
        self.session.delete(record)
