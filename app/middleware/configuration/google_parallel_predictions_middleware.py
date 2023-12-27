from sqlalchemy import and_
from sqlalchemy.orm import Session, Query

from app.frontend.confiugration.google_parallel_predictions_frontend import GoogleParallelPredictionsSelection
from app.frontend.state_management import get_state, State
from app.middleware.configuration import BaseConfigurationMiddleware
from model.configuration.google_parallel_predictions import GoogleParallelPredictions
from model.dim.google_account import GoogleAccount
from model.dim.partner import Partner
from model.dim.partner_company import PartnerCompany


class GoogleParallelPredictionsMiddleware(BaseConfigurationMiddleware[GoogleParallelPredictionsSelection, GoogleParallelPredictions]):
    def get_model_type(self) -> type[GoogleParallelPredictions]:
        return GoogleParallelPredictions

    def to_database_object(self, selection: GoogleParallelPredictionsSelection) -> GoogleParallelPredictions:
        return GoogleParallelPredictions(
            account_id=selection.account.account_id,
            partner_id=selection.partner.partner_id,
            deal_type=selection.deal_type,
            active=selection.active,
        )

    def _to_display_dict(self, selection: GoogleParallelPredictionsSelection) -> dict:
        return {
            'account_name': selection.account.account_name,
            'name': selection.partner.name,
            'deal_type': selection.deal_type,
            'active': selection.active,
        }

    def _compose_query_for_display(self, session: Session) -> Query:
        return session.query(GoogleParallelPredictions, GoogleAccount.account_name, Partner.name) \
            .join(GoogleAccount, and_(
                GoogleParallelPredictions.account_id == GoogleAccount.account_id,
                GoogleAccount.mcc_id == get_state(State.COMPANY)['google_id'],
            )) \
            .join(PartnerCompany, and_(
                GoogleParallelPredictions.partner_id == PartnerCompany.partner_id,
                PartnerCompany.company == get_state(State.COMPANY)['shortened'],
            )) \
            .join(Partner,
                GoogleParallelPredictions.partner_id == Partner.partner_id
            )
