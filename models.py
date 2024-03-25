# Import necessary modules and classes from other files
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from bcrypt import hashpw, gensalt, checkpw

# Create an engine and bind it to the 'finance_tracker.db' SQLite database
engine = create_engine('sqlite:///finance_tracker.db')

# Create a base class for declarative class definitions
Base = declarative_base()

# Define a User class representing the 'users' table in the database
class User(Base):
    __tablename__ = 'users'

    # Define columns for the 'users' table
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password_hash = Column(String)  # Add password_hash column

    # Define relationships between User and other tables
    transactions = relationship('Transaction', back_populates='user')
    goals = relationship('Goal', back_populates='user')
    investments = relationship('Investment', back_populates='user')

    # Define a method to set the password hash for a user
    def set_password(self, password):
        salt = gensalt()
        password_hash = hashpw(password.encode('utf-8'), salt)
        self.password_hash = password_hash.decode('utf-8')

    # Define a method to check if a provided password matches the stored hash
    def check_password(self, password):
        return checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

# Define a Transaction class representing the 'transactions' table
class Transaction(Base):
    __tablename__ = 'transactions'

    # Define columns for the 'transactions' table
    id = Column(Integer, primary_key=True)
    description = Column(String)
    amount = Column(Float)
    date = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('expense_categories.id'))

    # Define relationships with User and ExpenseCategory
    user = relationship('User', back_populates='transactions')
    category = relationship('ExpenseCategory', back_populates='transactions')

# Define an ExpenseCategory class representing the 'expense_categories' table
class ExpenseCategory(Base):
    __tablename__ = 'expense_categories'

    # Define columns for the 'expense_categories' table
    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Define a relationship with Transaction
    transactions = relationship('Transaction', back_populates='category')

# Define a Goal class representing the 'goals' table
class Goal(Base):
    __tablename__ = 'goals'

    # Define columns for the 'goals' table
    id = Column(Integer, primary_key=True)
    description = Column(String)
    target_amount = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Define a relationship with User
    user = relationship('User', back_populates='goals')

# Define an Investment class representing the 'investments' table
class Investment(Base):
    __tablename__ = 'investments'

    # Define columns for the 'investments' table
    id = Column(Integer, primary_key=True)
    name = Column(String)
    initial_amount = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Define a relationship with User
    user = relationship('User', back_populates='investments')

# Create the database schema based on the defined classes
Base.metadata.create_all(engine)