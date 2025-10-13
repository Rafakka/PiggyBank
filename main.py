
# main.py
from operations import user_dashboard
from queries_user import init_db, create_user, get_user_by_username

def main():
    # Initialize database first
    init_db()
    
    print("Welcome to PiggyBank!\n")
    
    while True:
        print("1. Login")
        print("2. Sign up")
        print("3. Exit")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            username = input("Enter your username: ").strip()
            user = get_user_by_username(username)
            
            if user:
                # Extract values from the dictionary
                user_balance = user['balance']
                user_name = user['name']
                
                print(f"\nLogin successful! Welcome back {user_name}!")
                print(f"Your current balance: ${user_balance:.2f}")
                
                # Go to user dashboard
                user_dashboard(username)
            else:
                print("User not found! Please check your username or sign up.")
                
        elif choice == "2":
            username = input("Choose a username: ").strip()
            name = input("Enter your full name: ").strip()
            
            try:
                initial_balance = float(input("Enter initial deposit: $"))
                if initial_balance < 0:
                    print("Please enter a positive number!")
                    continue
                    
                user_id = create_user(username, name, initial_balance)
                if user_id:
                    print(f"Account created successfully! Welcome {name}!")
                    # No need for extra function call - we know the initial balance
                    print(f"Your starting balance: ${initial_balance:.2f}")
                    
            except ValueError:
                print("Please enter a valid number!")
                
        elif choice == "3":
            print("Thank you for using PiggyBank! Goodbye!")
            break
            
        else:
            print("Invalid choice! Please enter 1, 2, or 3.\n")

if __name__ == "__main__":
    main()