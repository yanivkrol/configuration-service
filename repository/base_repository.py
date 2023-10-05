from typing import Type, TypeVar, Optional

import pandas as pd
import streamlit as st
from deprecation import deprecated
from sqlalchemy import desc
from sqlalchemy.orm import Session, DeclarativeBase, Query
import app.streamlitext.cache_data_api_ext as cache_data_ext


ModelT = TypeVar('ModelT', bound=DeclarativeBase)


class BaseRepository:
    def __init__(self, model: Type[ModelT], session: Session):
        self.model = model
        self.session = session

    def get(self) -> list[ModelT]:
        query = self._get_query()
        return self._cached_get(query)

    @staticmethod
    @st.cache_data(ttl=300, show_spinner="Loading data...", hash_funcs={Query: lambda q: str(q.statement)})
    def _cached_get(query: Query) -> list[ModelT]:
        return query.all()

    def _get_query(self) -> Query:
        return self.session.query(self.model)

    def get_as_df(self, limit: Optional[int] = None) -> pd.DataFrame:   # TODO remove limit in all places?
        query = self._get_as_df_query(limit)
        return self._cached_pd_read_sql(query)

    @staticmethod
    @st.cache_data(ttl=300, show_spinner="Loading data...", hash_funcs={Query: lambda q: str(q.statement)})
    def _cached_pd_read_sql(query: Query) -> pd.DataFrame:
        return pd.read_sql(query.statement, query.session.bind, index_col="id")

    def _get_as_df_query(self, limit: Optional[int] = None) -> Query:
        return self.session.query(self.model).order_by(desc(self.model.id)).limit(limit)

    @deprecated
    def clear_cache(self, limit: Optional[int] = None) -> None:
        cache_data_ext.clear(self._get_as_df_query(limit))
        cache_data_ext.clear(self._get_query())

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
