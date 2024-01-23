import sqlite3
from config import DATABASE_NAME
from sqlalchemy.orm import DeclarativeBase, sessionmaker, mapped_column
from sqlalchemy import create_engine
from typing import Annotated

engine = create_engine(
    url=f"sqlite:///{DATABASE_NAME}"
)

sync_session = sessionmaker(engine)

id_pk = Annotated[int, mapped_column(primary_key=True)]
str_256 = Annotated[str, mapped_column(str(256))]

class Base(DeclarativeBase):
    pass


class OrmStart:
    @staticmethod
    def create_tables():
        # Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        
        