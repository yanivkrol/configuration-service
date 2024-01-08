from app.frontend.confiugration.account_campaign_frontend import AccountCampaignFrontend


class GooglePostbackWithCommissionFrontend(AccountCampaignFrontend):

    def __init__(self):
        super().__init__(
            source_join="google",
            label="Google - Postback with Commission",
        )
