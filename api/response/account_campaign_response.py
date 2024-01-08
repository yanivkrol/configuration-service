from typing import TypeVar

from api.response import Response
from common.model import Base

T = TypeVar('T', bound=Base)


class AccountCampaignResponse(Response[T]):
    def get_key(self, record: T) -> dict:
        return {
            'mcc_id': record.mcc_id,
            'account_id': record.account_id,
            'campaign_id': record.campaign_id,
        }
