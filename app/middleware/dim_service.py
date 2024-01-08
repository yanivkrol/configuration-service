import streamlit as st
from sqlalchemy import and_

from common.db_config import SessionMaker
from common.model.dim.account import Account
from common.model.dim.account_campaign_mapping import AccountCampaignMapping
from common.model.dim.partner import Partner
from common.model.dim.partner_company import PartnerCompany
from common.model.dim.site import Site
from common.model.dim.site_vertical_mapping import SiteVerticalMapping
from common.model.dim.vertical import Vertical

MINUTE = 60


class _DimensionsService:
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

    @st.cache_resource(ttl=1 * MINUTE)  # No reason to save for a long time, because it's for a specific site
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
                PartnerCompany.partner_id == Partner.id,
                PartnerCompany.company == company_shortened
            )) \
            .all()

    @st.cache_resource(ttl=10 * MINUTE)
    def get_sites(_self) -> list[Site]:
        return _self.session.query(Site).all()

    @st.cache_resource(ttl=1 * MINUTE)  # No reason to save for a long time, because it's for a specific site
    def get_site_verticals(_self, site_id: str) -> list[Vertical]:
        return _self.session.query(Vertical) \
            .join(SiteVerticalMapping, and_(
                SiteVerticalMapping.site_id == site_id,
                SiteVerticalMapping.vertical_id == Vertical.id,
            )) \
            .all()


dim_service = _DimensionsService()
