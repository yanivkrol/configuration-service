from typing import Type, Optional

from sqlalchemy import desc, and_
from sqlalchemy.orm import Session, Query, DeclarativeBase

from model.configuration.impl.google_external_product import GoogleExternalProduct
from model.dim.impl.google_account import GoogleAccount
from model.dim.impl.google_account_campaigns_mapping import GoogleAccountCampaignMappings
from repository.configuration.configuration_repository import ConfigurationRepository


class GoogleExternalProductRepository(ConfigurationRepository):
    def __init__(self, model: Type[GoogleExternalProduct], session: Session):
        super().__init__(model, session)

    def _get_as_df_query(self, limit: Optional[int] = None) -> Query:
        return self.session.query(GoogleExternalProduct, GoogleAccount, GoogleAccountCampaignMappings) \
            .outerjoin(GoogleAccount, GoogleExternalProduct.account_id == GoogleAccount.account_id) \
            .outerjoin(GoogleAccountCampaignMappings, GoogleExternalProduct.campaign_id == GoogleAccountCampaignMappings.campaign_id) \
            .order_by(desc(GoogleExternalProduct.id)) \
            .limit(limit)

    def add_all_from_values(self, rows: list[dict[str, DeclarativeBase]]): # TODO better name, better API
        for row in rows:
            configuration = GoogleExternalProduct(
                account_id=row['account'].account_id,
                campaign_id=row['campaign'].campaign_id,
                active=1
            )
            self.add(configuration)
