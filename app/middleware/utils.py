from model.dim.google_account_campaign_mappings import GoogleAccountCampaignMappings


def allable_campaign(campaign_mapping: GoogleAccountCampaignMappings | None) -> str:
    return campaign_mapping.campaign_id if campaign_mapping else "__ALL__"
