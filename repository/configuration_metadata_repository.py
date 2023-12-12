from db_config import db_session
from model.configuration_metadata import ConfigurationMetadata

from repository.base_repository import BaseRepository


configuration_metadata_repository = BaseRepository[ConfigurationMetadata](ConfigurationMetadata, db_session)
