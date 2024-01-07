import os
import urllib

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from common.parameter_store_api import ParameterStoreApi


def _get_engine():
    env = _ensure_fully_quantified_env(os.environ.get('ENV'))
    db_authority = os.environ.get('DB_AUTHORITY')
    if env == 'development':
        user, password = _get_credentials_from_env()
    else:
        user, password = _get_credentials_from_secrets(env)
    full_url = f"mysql://{user}:{password}@{db_authority}/configuration_service"
    return create_engine(full_url)


def _ensure_fully_quantified_env(env: str) -> str:
    if env in ['development', 'staging', 'production']:
        return env
    if env == 'dev':
        return 'development'
    if env == 'stg':
        return 'staging'
    if env == 'prod':
        return 'production'
    raise Exception(f'Invalid env: {env}')


def _get_credentials_from_env() -> tuple[str, str]:
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    return user, password


def _get_credentials_from_secrets(env: str) -> tuple[str, str]:
    secrets = ParameterStoreApi()
    user = secrets.get_param_value(f'cred_configo_aurora-username_{env}')
    password = urllib.parse.quote(secrets.get_param_value(f'cred_configo_aurora-password_{env}'))
    return user, password


engine = _get_engine()
SessionMaker = sessionmaker(bind=engine)

Base = declarative_base()
