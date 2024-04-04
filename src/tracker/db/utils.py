from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from contextlib import contextmanager

Base = declarative_base()
SessionLocal = scoped_session(sessionmaker())

url = 'postgresql://tracker-wystatkow:12345678@127.0.0.1:2323/tracker-wystatkow'

def initialize_db(echo: bool =False)->Engine:
    engine = create_engine(
        url,
        echo=echo,
        future=True
    )
    return engine

@contextmanager
def session_scope():
    session = SessionLocal()
    
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        
def create_objects(engine: Engine):
    Base.metadata.create_all(engine)
    
def delete_objects(engine: Engine):
    Base.metadata.drop_all(engine)

engine = initialize_db(echo=False)
create_objects(engine)