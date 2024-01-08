import sys
from abc import ABC, abstractmethod
from typing import TypeVar, Type, Generic

import pandas as pd
import streamlit as st
from sqlalchemy import desc
from sqlalchemy.orm import Session, Query

from app.frontend.confiugration import Selection
from common.configurations import ConfigurationId
from common.db_config import SessionMaker
from model import Base

S = TypeVar('S', bound=Selection)
T = TypeVar('T', bound=Base)


def hash_query(query: Query) -> str:
    return str(query.statement.compile(compile_kwargs={"literal_binds": True}))


class BaseConfigurationMiddleware(ABC, Generic[S, T]):
    @abstractmethod
    def get_model_type(self) -> Type[T]:
        ...

    @abstractmethod
    def to_database_object(self, selection: S) -> T:
        ...

    def to_display_dataframe(self, selections: list[S]) -> pd.DataFrame:
        return pd.DataFrame([self._to_display_dict(selection) for selection in selections])

    @abstractmethod
    def _to_display_dict(self, selection: S) -> dict:
        """
        This function should return a dict that has all the fields needed for display,
        Similarly to the output of get_display_dataframe
        """
        ...

    @abstractmethod
    def _compose_query_for_display(self, session: Session) -> Query:
        ...

    def get_display_dataframe(self) -> pd.DataFrame:
        session = SessionMaker()
        query = self._compose_query_for_display(session)
        query = query.order_by(desc('id'))
        return self._cached_pd_read_sql(query)

    @st.cache_data(show_spinner="Loading data...", hash_funcs={Query: hash_query})
    def _cached_pd_read_sql(_self, query: Query) -> pd.DataFrame:
        return pd.read_sql(query.statement, query.session.bind, index_col='id')


from .google_active_postback_middleware import GoogleActivePostbackMiddleware
from .google_external_product_middleware import GoogleExternalProductMiddleware
from .google_siteclick_postback_middleware import GoogleSiteclickPostbackMiddleware
from .google_parallel_predictions_middleware import GoogleParallelPredictionsMiddleware
from .google_postback_with_commission_middleware import GooglePostbackWithCommissionMiddleware

_google_active_postback_middleware = GoogleActivePostbackMiddleware()
_google_external_product_middleware = GoogleExternalProductMiddleware()
_google_siteclick_postback_middleware = GoogleSiteclickPostbackMiddleware()
_google_parallel_predictions_middleware = GoogleParallelPredictionsMiddleware()
_google_postback_with_commission_middleware = GooglePostbackWithCommissionMiddleware()


def get_middleware(config_id: ConfigurationId) -> BaseConfigurationMiddleware:
    this_module = sys.modules[__name__]
    return getattr(this_module, f'_{config_id}_middleware')



