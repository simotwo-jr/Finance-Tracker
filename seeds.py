from database import Session
from models import User, Transaction, Goal, Investment, ExpenseCategory
from sqlalchemy.orm.exc import NoResultFound

# Create a session to interact with the database
session = Session()

# Function to seed the database with expense categories
def seed_expense_categories():
    categories = [
        'Education', 'Food', 'Entertainment', 'Dining Out', 'Transportation', 
        'Health', 'Luxury', 'Utilities', 'Rent/Mortgage', 
        'Insurance (Health, Life, Auto, Homeowners)', 'Childcare', 
        'Pet Expenses', 'Travel/Vacation', 'Hobbies/Recreation', 
        'Gifts/Donations', 'Clothing/Apparel', 'Electronics/Gadgets', 
        'Home Improvement', 'Taxes', 'Subscriptions (Streaming, Magazines, Software)', 
        'Gym/Fitness', 'Personal Care', 'Home Maintenance', 
        'Furniture/Furnishings', 'Legal/Professional Fees', 
        'Transportation (Gas, Public Transit)', 'Savings/Investments'
    ]

    existing_categories = session.query(ExpenseCategory).all()
    existing_category_names = set(category.name for category in existing_categories)

    for category_name in categories:
        if category_name not in existing_category_names:
            category = ExpenseCategory(name=category_name)
            session.add(category)

    session.commit()

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
            
            print("User {} created.".format(username))

            break
        except ValueError as e:
            print("Error: {}".format(e))


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
    amount = get_positive_float_input("Enter transaction amount: ")

    categories = session.query(ExpenseCategory).all()
    print("Existing Expense Categories:")
    for category in categories:
        print("{}: {}".format(category.id, category.name))


    category_id = get_valid_category_id(categories)

    transaction = Transaction(description=description, amount=amount, user_id=user_id, category_id=category_id)
    session.add(transaction)
    session.commit()
    print("Transaction created for user {}.".format(user_id))


# Helper function to get a valid positive float input
def get_positive_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                raise ValueError("Value must be a positive number.")
            return value
        except ValueError:
            print("Error: Invalid input. Please enter a positive number.")

# Helper function to get a valid category ID
def get_valid_category_id(categories):
    while True:
        category_id = input("Select an expense category (ID): ")
        try:
            category_id = int(category_id)
            if not any(category.id == category_id for category in categories):
                raise ValueError("Invalid category ID.")
            return category_id
        except ValueError:
            print("Error: Invalid category ID. Please select a valid category.")

# Other functions (create_investment, create_goal, seed_expense_categories) remain unchanged...

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
                if choice == '2':
                   user = login()
            if user:
                user_id = user.id
        # create_investment(user_id)  # Remove this line
            if choice == '2':
                user = login()
            if user:
                user_id = user.id
        # create_goal(user_id)  # Remove this line

                
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

if __name__ == '__main__':
    # Add new expense categories if they don't already exist
    seed_expense_categories()

    # Start the main program
    main()

    
