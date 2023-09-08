from abc import ABC


class Configuration(ABC):

    def __init__(self, name: str, db: str):
        self.name = name
        self.db = db
