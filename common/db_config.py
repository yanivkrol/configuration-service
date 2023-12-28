import os
import urllib

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from common.parameter_store_api import ParameterStoreApi


def _get_engine():
    env = os.environ.get('ENV', 'dev')
    db_url = os.environ.get('DB_URL', "aurora-staging.va.naturalint.com:3306")
    secrets = ParameterStoreApi()
    user = secrets.get_param_value(f'cred_configo_aurora-username_{env}')
    password = urllib.parse.quote(secrets.get_param_value(f'cred_configo_aurora-password_{env}'))
    full_url = f"mysql://{user}:{password}@{db_url}/configo"
    return create_engine(full_url)


engine = _get_engine()
SessionMaker = sessionmaker(bind=engine)

Base = declarative_base()
