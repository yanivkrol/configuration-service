from typing import Optional

import pandas as pd
import streamlit as st
from sqlalchemy.orm import DeclarativeBase


class BaseRepository:
    def __init__(self, cls: DeclarativeBase.__class__):
        self.connection = st.experimental_connection(
            "mysql",
            type="sql",

        )
        self.session = self.connection.session
        self.cls = cls
        self.table_name = cls.__tablename__

    def get_as_df(self, limit: Optional[int] = None, ttl: Optional[int] = 0) -> pd.DataFrame:
        query = f"SELECT * FROM {self.table_name}"
        if limit:
            query += f" LIMIT {limit}"
        df = self.connection.query(query, index_col="id", ttl=ttl)
        return df

    def get(self, limit: Optional[int] = None) -> list[DeclarativeBase]:
        return self.session.query(self.cls).limit(limit).all()

    def get_by_id(self, id: int) -> DeclarativeBase:
        return self.session.query(self.cls).filter(self.cls.id == id).first()

    def add(self, record):
        self.session.add(record)
        self.session.commit()

    def update(self, id: str, update: dict):
        self.session.query(self.cls).filter(self.cls.id == id).update(update)
        self.session.commit()

    def delete(self, id: int):
        record = self.get_by_id(id)
        self.session.delete(record)
        self.session.commit()

