"""
    trine.models
    ~~~~~~~~~~~~

    Provides SQLAlchemy table definitions for TrinityCore.

    :todo: add support for other emulators and databases (e.g. auth, character)

    :copyright: Copyright 2012 by David Gidwani
    :license: BSD, see LICENSE for details.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


WorldDBSession = scoped_session(sessionmaker())
DeclarativeBase = declarative_base()


def initialize_world_db_connection(engine):
    WorldDBSession.configure(bind=engine)
    DeclarativeBase.metadata.bind = engine
    DeclarativeBase.metadata.create_all(engine)