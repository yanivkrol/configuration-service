from sqlalchemy import and_
from sqlalchemy.orm import Session, Query

from app.frontend.confiugration.google_active_postback_frontend import GoogleActivePostbackSelection
from app.frontend.state_management import get_state, State
from app.middleware.configuration import BaseConfigurationMiddleware
from model.configuration import GoogleActivePostback
from model.dim.account import Account
from model.dim.site import Site
from model.dim.vertical import Vertical


class GoogleActivePostbackMiddleware(BaseConfigurationMiddleware[GoogleActivePostbackSelection, GoogleActivePostback]):
    def get_model_type(self) -> type[GoogleActivePostback]:
        return GoogleActivePostback

    def to_database_object(self, selection: GoogleActivePostbackSelection) -> GoogleActivePostback:
        return GoogleActivePostback(
            mcc_id=selection.account.mcc_id,
            mcc_name=selection.account.mcc_name,
            account_id=selection.account.account_id,
            site_id=selection.site.id,
            vertical_id=selection.vertical.id,
            traffic_join=selection.traffic_join,
            active=selection.active,
        )

    def _to_display_dict(self, selection: GoogleActivePostbackSelection) -> dict:
        return {
            'account_name': selection.account.account_name,
            'site_name': selection.site.name,
            'vertical_name': selection.vertical.name,
            'traffic_join': selection.traffic_join,
            'active': selection.active,
        }

    def _compose_query_for_display(self, session: Session) -> Query:
        return session.query(GoogleActivePostback, Account.account_name, Site.name.label('site_name'), Vertical.name.label('vertical_name')) \
            .join(Account, and_(
                GoogleActivePostback.account_id == Account.account_id,
                Account.mcc_id == get_state(State.COMPANY)['google_id'],
                Account.source_join == 'google',
            )) \
            .join(Site, GoogleActivePostback.site_id == Site.id) \
            .join(Vertical, GoogleActivePostback.vertical_id == Vertical.id)
