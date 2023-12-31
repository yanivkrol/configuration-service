from sqlalchemy import and_
from sqlalchemy.orm import Session, Query

from app.frontend.confiugration.google_parallel_predictions_frontend import GoogleParallelPredictionsSelection
from app.middleware.configuration import BaseConfigurationMiddleware
from app.state_management import get_state, State
from common.model.configuration.google_parallel_predictions import GoogleParallelPredictions
from common.model.dim.account import Account
from common.model.dim.partner import Partner
from common.model.dim.partner_company import PartnerCompany


class GoogleParallelPredictionsMiddleware(BaseConfigurationMiddleware[GoogleParallelPredictionsSelection, GoogleParallelPredictions]):
    def get_model_type(self) -> type[GoogleParallelPredictions]:
        return GoogleParallelPredictions

    def to_database_object(self, selection: GoogleParallelPredictionsSelection) -> GoogleParallelPredictions:
        return GoogleParallelPredictions(
            account_id=selection.account.account_id,
            partner_id=selection.partner.id,
            deal_type=selection.deal_type,
            active=selection.active,
        )

    def _compose_query_for_display(self, session: Session) -> Query:
        return session.query(GoogleParallelPredictions, Account.account_name, Partner.name.label('partner_name')) \
            .join(Account, and_(
                GoogleParallelPredictions.account_id == Account.account_id,
                Account.mcc_id == get_state(State.COMPANY)['google_id'],
                Account.source_join == 'google',
            )) \
            .join(PartnerCompany, and_(
                GoogleParallelPredictions.partner_id == PartnerCompany.partner_id,
                PartnerCompany.company == get_state(State.COMPANY)['shortened'],
            )) \
            .join(Partner,
                GoogleParallelPredictions.partner_id == Partner.id
            )
