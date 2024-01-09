from sqlalchemy.orm import Session, Query

from app.frontend.confiugration.google_active_postback_frontend import GoogleActivePostbackSelection
from app.middleware.configuration import BaseConfigurationMiddleware
from app.state_management import get_state, State
from common.model.configuration import GoogleActivePostback
from common.model.dim.site import Site
from common.model.dim.vertical import Vertical


class GoogleActivePostbackMiddleware(BaseConfigurationMiddleware[GoogleActivePostbackSelection, GoogleActivePostback]):
    def get_model_type(self) -> type[GoogleActivePostback]:
        return GoogleActivePostback

    def to_database_object(self, selection: GoogleActivePostbackSelection) -> GoogleActivePostback:
        return GoogleActivePostback(
            mcc_id=selection.account.mcc_id,
            mcc_name=selection.account.mcc_name,
            account_id=selection.account.account_id,
            account_name=selection.account.account_name,
            site_id=selection.site.id,
            vertical_id=selection.vertical.id,
            traffic_join=selection.traffic_join,
            active=selection.active,
        )

    def _compose_query_for_display(self, session: Session) -> Query:
        return session.query(GoogleActivePostback, Site.name.label('site_name'), Vertical.name.label('vertical_name')) \
            .where(GoogleActivePostback.mcc_id == get_state(State.COMPANY)['google_id'],) \
            .join(Site, GoogleActivePostback.site_id == Site.id) \
            .join(Vertical, GoogleActivePostback.vertical_id == Vertical.id)
