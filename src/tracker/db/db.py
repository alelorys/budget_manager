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
from tracker.db.utils import Base, initialize_db, create_objects, SessionLocal, delete_objects


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String)
    name = Column(String)
    lastname = Column(String)
    password = Column(String)

    model = relationship("Models")
    money = relationship("Money")
    bugdet = relationship("Predict")

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
    
class Models(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    date = Column(DateTime)
    state = Column(Boolean, default = False)
    model_path = Column(String)
    user_id = Column(Integer, ForeignKey(Users.id),nullable=False)
    
    def __repr__(self):
        return (f"Models(id = {self.id!r}, name = {self.name!r}, date = {self.date!r}, "
                f"state = {self.state!r}, model_path = {self.model_path!r}, user_id={self.user_id!r}")
class Money(Base):
    __tablename__ = 'money'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(Users.id),nullable=False)
    name = Column(String)
    type = Column(String)
    date = Column(DateTime)
    amount = Column(Float)
    category = Column(String, nullable=False)

    def __repr__(self):
        return f"Money(id={self.id!r},user_id={self.user_id!r},name={self.name!r},type={self.type!r},date={self.date!r}, amount={self.amount!r},category={self.category!r})"
    
class Budget(Base):
    __tablename__ = 'budget'

    id = Column(Integer, primary_key=True, autoincrement=True)
    budget_date = Column(DateTime)

    def __repr__(self):
        return f"Budget(id={self.id!r}, budget_date={self.budget_date!r})"
    
class BudgetItems(Base):
    __tablename__ = 'budget_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    budget_id = Column(Integer, ForeignKey("Budget.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("Category.id", nullable=False))
    planned_value = Column(Float)
    real_value = Column(Float)

    def __repr__(self):
        return f"BudgetItems(id={self.id!r},budget_id={self.budget_id!r},category_id={self.category_id!r},planned_value={self.planned_value!r},real_value={self.real_value!r})"
class Predict(Base):
    __tablename__ = "predict"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(Users.id),nullable=False)
    predicted = Column(Float)
    real = Column(Float)
    date = Column(DateTime)
    
class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)



def create_db():
    
    engine = initialize_db(echo=False)
    delete_objects(engine)

    engine = initialize_db(echo=False)
    create_objects(engine)
    
metadata = sa.MetaData()
engine = initialize_db(echo=False)
SessionLocal.configure(bind=engine)
metadata.reflect(bind=engine)