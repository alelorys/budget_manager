import sqlalchemy as sa 
from sqlalchemy import (
    ForeignKey,
    Column,
    Table,
    String,
    Boolean,
    Float,
    Integer,
    DateTime)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from tracker.db.utils import Base, initialize_db, create_objects, SessionLocal

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String)
    name = Column(String)
    lastname = Column(String)
    password = Column(String)

    money = relationship("Money")

    def __repr__(self):
        return f"Users(id={self.id!r}, login={self.login!r}, name={self.name!r}, lastname={self.lastname!r}, password={self.password!r})"
    
    def as_dict(self):
        return {
            self.login:{
                "id":self.id,
                "username":self.login,
                "password":self.password,
                "name":self.name,
                "lastname":self.lastname
            }
        }
class Money(Base):
    __tablename__ = 'money'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(Users.id),nullable=False)
    name = Column(String)
    type = Column(String)
    date = Column(DateTime)
    amount = Column(Float)
    category = Column(String)
    
class Predict(Base):
    __tablename__ = "predict"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    predicted = Column(Float)
    real = Column(Float)
    date = Column(DateTime)
    
metadata = sa.MetaData()
engine = initialize_db(echo=False)

create_objects(engine)
SessionLocal.configure(bind=engine)
metadata.reflect(bind=engine)