from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from bcrypt import hashpw, gensalt, checkpw

engine = create_engine('sqlite:///finance_tracker.db')

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password_hash = Column(String)  

    transactions = relationship('Transaction', back_populates='user')
    goals = relationship('Goal', back_populates='user')
    investments = relationship('Investment', back_populates='user')

    def set_password(self, password):
        salt = gensalt()
        password_hash = hashpw(password.encode('utf-8'), salt)
        self.password_hash = password_hash.decode('utf-8')

    def check_password(self, password):
        return checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    amount = Column(Float)
    date = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('expense_categories.id'))

    user = relationship('User', back_populates='transactions')
    category = relationship('ExpenseCategory', back_populates='transactions')

class ExpenseCategory(Base):
    __tablename__ = 'expense_categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    transactions = relationship('Transaction', back_populates='category')

class Goal(Base):
    __tablename__ = 'goals'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    target_amount = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='goals')

class Investment(Base):
    __tablename__ = 'investments'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    initial_amount = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='investments')

Base.metadata.create_all(engine)