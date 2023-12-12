import sys
from abc import abstractmethod
from typing import TypeVar, Type, Optional

import pandas as pd
from sqlalchemy import desc
from sqlalchemy.orm import Session, Query

from configurations import ConfigurationId
from db_config import db_session
from model.serializable_model import SerializableModel
from repository.base_repository import BaseRepository

ConfigurationModelT = TypeVar('ConfigurationModelT', bound=SerializableModel)


class ConfigurationRepository(BaseRepository[ConfigurationModelT]):
    def __init__(self, model: Type[ConfigurationModelT], session: Session):
        super().__init__(model, session)

    def get_as_df(self, limit: Optional[int] = None) -> pd.DataFrame:  # TODO remove limit in all places?
        query = self._get_as_df_query().order_by(desc(self.model.id)).limit(limit)  # type: ignore
        return self._cached_pd_read_sql(query)

    @staticmethod
    # @st.cache_data(ttl=300, show_spinner="Loading data...", hash_funcs={Query: hash_query})
    def _cached_pd_read_sql(query: Query) -> pd.DataFrame:
        return pd.read_sql(query.statement, query.session.bind, index_col="id")

    @abstractmethod
    def _get_as_df_query(self) -> Query:
        ...


from repository.configuration.google_external_product import GoogleExternalProductRepository

_google_external_product_repository = GoogleExternalProductRepository(db_session)
# _google_siteclick_postback_repository = ConfigurationRepository(db_session)


def get_repository(config_id: ConfigurationId) -> ConfigurationRepository:
    this_module = sys.modules[__name__]
    return getattr(this_module, f'_{config_id}_repository')
