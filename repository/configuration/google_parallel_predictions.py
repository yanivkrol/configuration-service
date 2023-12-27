from sqlalchemy import and_
from sqlalchemy.orm import Session, Query

from app.frontend.state_management import get_state, State
from model.configuration.google_parallel_predictions import GoogleParallelPredictions
from model.dim.google_account import GoogleAccount
from model.dim.partner import Partner
from model.dim.partner_company import PartnerCompany
from repository.configuration import ConfigurationRepository


class GoogleParallelPredictionsRepository(ConfigurationRepository[GoogleParallelPredictions]):
    def __init__(self, session: Session):
        super().__init__(GoogleParallelPredictions, session)  # TODO fix types

    def _get_as_df_query(self) -> Query:
        return self.session.query(GoogleParallelPredictions, GoogleAccount, Partner) \
            .join(GoogleAccount, and_(
                GoogleParallelPredictions.account_id == GoogleAccount.account_id,
                GoogleAccount.mcc_id == get_state(State.COMPANY)['google_id'],  # TODO how not to use streamlit
            )) \
            .join(PartnerCompany, and_(
                GoogleParallelPredictions.partner_id == PartnerCompany.partner_id,
                PartnerCompany.company == get_state(State.COMPANY)['shortened'],  # TODO how not to use streamlit
            )) \
            .join(Partner,
                GoogleParallelPredictions.partner_id == Partner.partner_id
            )
