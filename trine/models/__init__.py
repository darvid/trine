from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


WorldDBSession = scoped_session(sessionmaker())
DeclarativeBase = declarative_base()


def initialize_world_db_connection(engine):
    WorldDBSession.configure(bind=engine)
    DeclarativeBase.metadata.bind = engine
    DeclarativeBase.metadata.create_all(engine)