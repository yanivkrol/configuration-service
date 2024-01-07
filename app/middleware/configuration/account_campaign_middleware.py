from abc import ABC
from typing import TypeVar

from sqlalchemy import and_
from sqlalchemy.orm import Session, Query

from app.frontend.confiugration import Selection
from app.frontend.state_management import get_state, State
from app.middleware.configuration import BaseConfigurationMiddleware
from app.middleware.utils import allable_campaign
from model.dim.account import Account
from model.dim.account_campaign_mapping import AccountCampaignMapping
from model.serializable_model import SerializableModel

S = TypeVar('S', bound=Selection)
T = TypeVar('T', bound=SerializableModel)


class AccountCampaignMiddleware(BaseConfigurationMiddleware[S, T], ABC):
    def __init__(self, source_join: str):
        super().__init__()
        self._source_join = source_join

    def to_database_object(self, selection: S) -> T:
        model_type = self.get_model_type()
        return model_type(
            mcc_id=selection.account.mcc_id,
            account_id=selection.account.account_id,
            campaign_id=allable_campaign(selection.campaign_mapping),
            active=selection.active,
        )

    def _to_display_dict(self, selection: S) -> dict:
        return {
            'account_name': selection.account.account_name,
            'campaign_name': selection.campaign_mapping.campaign_name if selection.campaign_mapping else '__ALL__',
            'active': selection.active,
        }

    def _compose_query_for_display(self, session: Session) -> Query:
        model_type = self.get_model_type()
        return session.query(model_type, Account.account_name, AccountCampaignMapping.campaign_name) \
            .join(Account, and_(
                model_type.account_id == Account.account_id,
                Account.mcc_id == get_state(State.COMPANY)[f'{self._source_join}_id'],
                Account.source_join == self._source_join,
            )) \
            .outerjoin(AccountCampaignMapping, and_(
                model_type.campaign_id == AccountCampaignMapping.campaign_id,
                AccountCampaignMapping.source_join == self._source_join,
            ))
