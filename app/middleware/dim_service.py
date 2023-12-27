import streamlit as st
from sqlalchemy import and_

from db_config import SessionMaker
from model.dim.google_account import GoogleAccount
from model.dim.google_account_campaign_mappings import GoogleAccountCampaignMappings
from model.dim.partner import Partner
from model.dim.partner_company import PartnerCompany

MINUTE = 60


class DimensionsService:
    def __init__(self):
        self.session = SessionMaker()

    @st.cache_resource(ttl=10 * MINUTE)
    def get_google_accounts(_self, mcc_id: str) -> list[GoogleAccount]:
        return _self.session.query(GoogleAccount).filter(GoogleAccount.mcc_id == mcc_id).all()

    @st.cache_resource(ttl=1 * MINUTE)  # No reason to save for a long time, this is the last stage of selection
    def get_google_campaigns(_self, mcc_id: str, account_id: str) -> list[GoogleAccountCampaignMappings]:
        return (_self.session.query(GoogleAccountCampaignMappings)
                .filter(and_(
                    GoogleAccountCampaignMappings.mcc_id == mcc_id,
                    GoogleAccountCampaignMappings.account_id == account_id
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
