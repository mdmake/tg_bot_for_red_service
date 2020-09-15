from sqlalchemy import create_engine, MetaData
from server.db import subscribers
import os

db_url = os.environ.get('DATABASE_URL')


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[subscribers])


if __name__ == '__main__':
    db_url = os.environ.get('DATABASE_URL')
    engine = create_engine(db_url, echo=True)
    create_tables(engine)
