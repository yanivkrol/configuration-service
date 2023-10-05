from abc import ABC
from typing import Type, TypeVar, Optional, Generic

import streamlit as st
from sqlalchemy.orm import Session, DeclarativeBase, Query


def hash_query(query: Query) -> str:
    return str(query.statement.compile(compile_kwargs={"literal_binds": True}))


ModelT = TypeVar('ModelT', bound=DeclarativeBase)


class BaseRepository(ABC, Generic[ModelT]):
    def __init__(self, model: Type[ModelT], session: Session):
        self.model = model
        self.session = session

    def get(self) -> list[ModelT]:
        query = self._get_query()
        return self._cached_get(query)

    def _get_query(self) -> Query:
        return self.session.query(self.model)

    @staticmethod
    @st.cache_data(ttl=300, show_spinner="Loading data...", hash_funcs={Query: hash_query})
    def _cached_get(query: Query) -> list[ModelT]:
        return query.all()

    def clear_cache(self, limit: Optional[int] = None) -> None:
        raise NotImplementedError("Should be used once streamlit provides a way to clear specific cache")
        # cache_data_ext.clear(self._get_as_df_query())
        # cache_data_ext.clear(self._get_query())

    def get_by_id(self, id: int) -> Optional[ModelT]:
        return self.session.query(self.model).filter(self.model.id == id).first()

    def add(self, record) -> None:
        self.session.add(record)
        self.session.commit()

    def update(self, id: str, update: dict) -> None:
        self.session.query(self.model).filter(self.model.id == id).update(update)
        self.session.commit()

    def delete(self, id: int) -> None:
        record = self.get_by_id(id)
        self.session.delete(record)
        self.session.commit()
