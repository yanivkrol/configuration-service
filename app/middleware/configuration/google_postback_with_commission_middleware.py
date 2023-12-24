from app.frontend.confiugration.google_postback_with_commission_frontend import GooglePostbackWithCommissionSelection
from app.middleware.configuration import BaseConfigurationMiddleware
from model.configuration.google_postback_with_commission import GooglePostbackWithCommission


class GooglePostbackWithCommissionMiddleware(BaseConfigurationMiddleware[GooglePostbackWithCommissionSelection, GooglePostbackWithCommission]):
    def to_database_object(self, selection: GooglePostbackWithCommissionSelection) -> GooglePostbackWithCommission:
        return GooglePostbackWithCommission(
            mcc_id=selection.account.mcc_id,
            account_id=selection.account.account_id,
            campaign_id=selection.campaign_mapping.campaign_id if selection.campaign_mapping else "__ALL__",
            active=selection.active,
        )
