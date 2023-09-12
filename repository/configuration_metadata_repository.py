from model.configuration_metadata import ConfigurationMetadata
from repository.base_repository import BaseRepository


class ConfigurationMetadataRepository(BaseRepository):
    def __init__(self):
        super().__init__(ConfigurationMetadata)
