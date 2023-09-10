from configuration.configuration import Configuration


class GoogleExternalProduct(Configuration):

    def __init__(self):
        super().__init__(
            name="Google - External Product",
            id_column="s2s_deal_type_mapping_id",
            tables=[
                {
                    "service": "resolver",
                    "name": "s2s_deal_type_mapping"
                }
            ],
            filter_column_choices={
                "resolver_deal_type": ["Sale", "Lead"]
            }
        )
