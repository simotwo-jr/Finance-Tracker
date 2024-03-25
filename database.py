from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Create a SQLite database engine
engine = create_engine('sqlite:///finance_tracker.db')

Session = sessionmaker(bind=engine)  # Create a Session class bound to the engine


Base = declarative_base()

# Create or update the database schema
Base.metadata.create_all(engine)