# Import necessary modules and classes from other files
from database import Session
from models import User, Transaction, Goal, Investment, ExpenseCategory
from sqlalchemy.orm.exc import NoResultFound

# Create a session to interact with the database
session = Session()

# Function to create a new user account
def create_user():
    while True:
        username = input("Enter username: ")
        email = input("Enter email: ")
        password = input("Enter password: ")

        try:
            # Create a new User instance with provided information
            user = User(username=username, email=email)
            user.set_password(password)
            
            # Add the user to the database and commit the transaction
            session.add(user)
            session.commit()
            
            print(f"User {username} created.")
            break
        except ValueError as e:
            print(f"Error: {e}")

# Function to log in an existing user
def login():
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")

        try:
            # Query the database for a user with the provided username
            user = session.query(User).filter_by(username=username).one()
            
            # Check if the provided password matches the stored password hash
            if user.check_password(password):
                print("Login successful.")
                return user
            else:
                print("Login failed. Please check your username and password.")
        except NoResultFound:
            print("User not found. Please check your username.")

# Function to create a new transaction for a user
def create_transaction(user_id):
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
        print(f"{category.id}: {category.name}")

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
    print(f"Transaction created for user {user_id}.")

# Function to create a new investment for a user
def create_investment(user_id):
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
    print(f"Investment created for user {user_id}.")

# Function to create a new financial goal for a user
def create_goal(user_id):
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
    print(f"Goal created for user {user_id}.")

# Function to seed the database with expense categories
def seed_expense_categories():
    categories = ['Education', 'Food', 'Entertainment', 'Dining Out', 'Transportation', 'Health', 'Luxury', 'Utilities',
    'Rent/Mortgage', 'Insurance (Health, Life, Auto, Homeowners)', 'Childcare', 'Pet Expenses', 'Travel/Vacation', 
    'Hobbies/Recreation', 'Gifts/Donations', 'Clothing/Apparel', 'Electronics/Gadgets', 'Home Improvement', 'Taxes', 
    'Subscriptions (Streaming, Magazines, Software)', 'Gym/Fitness', 'Personal Care', 'Home Maintenance', 
    'Furniture/Furnishings', 'Legal/Professional Fees', 'Transportation (Gas, Public Transit)', 'Savings/Investments']

    existing_categories = session.query(ExpenseCategory).all()
    existing_category_names = set(category.name for category in existing_categories)

    for category_name in categories:
        if category_name not in existing_category_names:
            category = ExpenseCategory(name=category_name)
            session.add(category)

    session.commit()



# Main program entry point
def main():
    print("Welcome to the Personal Finance Tracker!")
    while True:
        print("\nOptions:")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            create_user()
        elif choice == '2':
            user = login()
            if user:
                user_id = user.id
                create_transaction(user_id)
                create_investment(user_id)
                create_goal(user_id)
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == '__main__':
    # Add new expense categories if they don't already exist
    seed_expense_categories()

    # Start the main program
    main()