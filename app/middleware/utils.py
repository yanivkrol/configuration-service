from common.model.dim.account_campaign_mapping import AccountCampaignMapping


def allable_campaign(campaign_mapping: AccountCampaignMapping | None) -> str:
    return campaign_mapping.campaign_id if campaign_mapping else "__ALL__"
