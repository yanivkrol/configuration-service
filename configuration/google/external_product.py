from configuration.configuration import Configuration


class GoogleExternalProduct(Configuration):

    def __init__(self):
        super().__init__("Google - External Product", "resolver")
        self.tables = [{"service": "resolver", "name": "s2s_deal_type_mapping"}]
