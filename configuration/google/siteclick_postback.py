from typing import List

from streamlit.elements.lib.column_types import ColumnConfig

from configuration.configuration import Configuration


class GoogleSiteclickPostback(Configuration):

    def __init__(self):
        super().__init__("Google - Siteclick Postback", "google_postbacker")
        self.tables = [{"service": "resolver", "name": "s2s_deal_type_mapping"}]

    def column_order(self) -> List[str]:
        return []

    def column_config(self) -> dict[str, ColumnConfig]:
        return {}

