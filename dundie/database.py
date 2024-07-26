from sqlmodel import Session, create_engine

from dundie import models  # IMPORTANT: This will create all CLASS on database
from dundie.settings import SQL_CONN_STRING

engine = create_engine(SQL_CONN_STRING, echo=False)
models.SQLModel.metadata.create_all(bind=engine)


def get_session() -> Session:
    return Session(engine)
