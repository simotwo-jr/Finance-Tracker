import click
from database import Session
from models import User, Transaction, Goal, Investment, ExpenseCategory
from sqlalchemy.orm.exc import NoResultFound

# Create a session to interact with the database
session = Session()

# Define a CLI group
@click.group()
def cli():
    """Personal Finance Tracker CLI"""

# Define a CLI command for user registration
@cli.command()
def register():
    """Register a new user"""
    while True:
        username = input("Enter username: ")
        email = input("Enter email: ")
        password = input("Enter password: ")

        try:
            user = User(username=username, email=email)
            user.set_password(password)
            session.add(user)
            session.commit()
            print("User {} created.".format(username))
            break
        except ValueError as e:
            print("Error: {}".format(e))


# Define a CLI command for user login
@cli.command()
def login():
    """Log in as an existing user"""
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")

        try:
            user = session.query(User).filter_by(username=username).one()
            if user.check_password(password):
                print("Login successful.")
                return user
            else:
                print("Login failed. Please check your username and password.")
        except NoResultFound:
            print("User not found. Please check your username.")

# Define a CLI command for creating a transaction
@cli.command()
@click.option("--user-id", prompt="Enter user ID", type=int)
def create_transaction(user_id):
    """Create a new transaction for a user"""
    description = input("Enter transaction description: ")
    amount = input("Enter transaction amount: ")

    while True:
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be a positive number.")
            break
        except ValueError:
            print("Error: Invalid amount. Please enter a positive number.")
            amount = input("Enter transaction amount: ")

    categories = session.query(ExpenseCategory).all()
    print("Existing Expense Categories:")
    for category in categories:
        print("{}: {}".format(category.id, category.name))


    while True:
        category_id = input("Select an expense category (ID): ")
        try:
            category_id = int(category_id)
            if not any(category.id == category_id for category in categories):
                raise ValueError("Invalid category ID.")
            break
        except ValueError:
            print("Error: Invalid category ID. Please select a valid category.")

    transaction = Transaction(description=description, amount=amount, user_id=user_id, category_id=category_id)
    session.add(transaction)
    session.commit()
    print("Transaction created for user {}.".format(user_id))


# Define a CLI command for creating an investment
@cli.command()
@click.option("--user-id", prompt="Enter user ID", type=int)
def create_investment(user_id):
    """Create a new investment for a user"""
    name = input("Enter investment name: ")
    initial_amount = input("Enter initial investment amount: ")

    while True:
        try:
            initial_amount = float(initial_amount)
            if initial_amount < 0:
                raise ValueError("Initial amount must be a non-negative number.")
            break
        except ValueError:
            print("Error: Invalid initial amount. Please enter a non-negative number.")
            initial_amount = input("Enter initial investment amount: ")

    investment = Investment(name=name, initial_amount=initial_amount, user_id=user_id)
    session.add(investment)
    session.commit()
    print("Investment created for user {}.".format(user_id))


# Define a CLI command for creating a financial goal
@cli.command()
@click.option("--user-id", prompt="Enter user ID", type=int)
def create_goal(user_id):
    """Create a new financial goal for a user"""
    description = input("Enter goal description: ")
    target_amount = input("Enter target amount: ")

    while True:
        try:
            target_amount = float(target_amount)
            if target_amount <= 0:
                raise ValueError("Target amount must be a positive number.")
            break
        except ValueError:
            print("Error: Invalid target amount. Please enter a positive number.")
            target_amount = input("Enter target amount: ")

    goal = Goal(description=description, target_amount=target_amount, user_id=user_id)
    session.add(goal)
    session.commit()
    print("Goal created for user {}.".format(user_id))


if __name__ == '__main__':
    cli()