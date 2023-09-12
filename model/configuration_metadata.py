from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.sql import func


class ConfigurationMetadata(DeclarativeBase):
    __tablename__ = 'configuration_metadata'

    id = Column(Integer, primary_key=True, autoincrement=True)
    configuration_table = Column(String(100), nullable=False)
    table_name = Column(String(100), nullable=False)
    row_id = Column(Integer, nullable=False)
    sql_query = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    timestamp = Column(DateTime, default=func.current_timestamp(), nullable=False)

    user = relationship('User')  # Assuming User is another mapped class
