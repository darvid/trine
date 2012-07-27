from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


DBSession = scoped_session(sessionmaker())
DeclarativeBase = declarative_base()


def initialize_db_connection(engine):
    DBSession.configure(bind=engine)
    DeclarativeBase.metadata.bind = engine
    DeclarativeBase.metadata.create_all(engine)