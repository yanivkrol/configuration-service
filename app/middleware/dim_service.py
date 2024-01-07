import streamlit as st
from sqlalchemy import and_

from common.db_config import SessionMaker
from model.dim.account import Account
from model.dim.account_campaign_mapping import AccountCampaignMapping
from model.dim.partner import Partner
from model.dim.partner_company import PartnerCompany

MINUTE = 60


class DimensionsService:
    def __init__(self):
        self.session = SessionMaker()

    @st.cache_resource(ttl=10 * MINUTE)
    def get_accounts(_self, source_join: str, mcc_id: str) -> list[Account]:
        return (_self.session.query(Account)
                .where(and_(
                    Account.source_join == source_join,
                    Account.mcc_id == mcc_id,
                ))
                .all())

    @st.cache_resource(ttl=1 * MINUTE)  # No reason to save for a long time, this is the last stage of selection
    def get_campaigns(_self, source_join: str, account_id: str) -> list[AccountCampaignMapping]:
        return (_self.session.query(AccountCampaignMapping)
                .where(and_(
                    AccountCampaignMapping.source_join == source_join,
                    AccountCampaignMapping.account_id == account_id
                ))
                .all())

    @st.cache_resource(ttl=10 * MINUTE)
    def get_partners(_self, company_shortened: str) -> list[Partner]:
        return _self.session.query(Partner) \
            .join(PartnerCompany, and_(
                Partner.partner_id == PartnerCompany.partner_id,
                PartnerCompany.company == company_shortened
            )) \
            .all()
