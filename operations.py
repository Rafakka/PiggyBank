

from queries_user import delete_user, get_user_by_username, update_balance


def deposit_money(username, amount):
    """Deposit money into user's account"""
    if amount <= 0:
        print("Deposit amount must be positive!")
        return False
    
    success = update_balance(username, amount)
    if success:
        user = get_user_by_username(username)
        if user:
            new_balance = user['balance'] 
            print(f"Deposited ${amount:.2f}. New balance: ${new_balance:.2f}")
    return success

def withdraw_money(username, amount):
    """Withdraw money from user's account"""
    user = get_user_by_username(username)
    
    if not user:
        print("User not found!")
        return False
    
    current_balance = user['balance']
    
    if amount <= 0:
        print("Withdrawal amount must be positive!")
        return False
    
    if amount > current_balance:
        print("Insufficient funds!")
        return False
    
    success = update_balance(username, -amount)
    if success:
        user = get_user_by_username(username)
        new_balance = user['balance']  # Get updated balance from dictionary
        print(f"Withdrew ${amount:.2f}. New balance: ${new_balance:.2f}")
    return success

def user_dashboard(username):
    """Main dashboard after user logs in"""
    user = get_user_by_username(username)
    if not user:
        print("User not found!")
        return
    
    # Extract all user info from the dictionary
    balance = user['balance']
    name = user['name']
    user_id = user['id']
    
    print(f"\n=== Welcome {name} ===")
    print(f"User ID: {user_id}")
    print(f"Username: {username}")
    print(f"Current Balance: ${balance:.2f}")
    
    while True:
        print("\n--- PiggyBank Dashboard ---")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Logout")
        print("5. Delete Account")
        
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            # Just get fresh user data and extract balance
            user = get_user_by_username(username)
            current_balance = user['balance']
            print(f"Current balance: ${current_balance:.2f}")
            
            # Use the balance variable for calculations
            interest = current_balance * 0.05  # 5% interest example
            print(f"Potential monthly interest: ${interest:.2f}")
                
        elif choice == "2":
            try:
                amount = float(input("Enter deposit amount: $"))
                deposit_money(username, amount)
            except ValueError:
                print("Please enter a valid number!")
                
        elif choice == "3":
            try:
                amount = float(input("Enter withdrawal amount: $"))
                withdraw_money(username, amount)
            except ValueError:
                print("Please enter a valid number!")
                
        elif choice == "4":
            print("Logging out...")
            break

        elif choice == "5":
            print("Are you sure you want to Delete your account? \n")
            subChoice = str(input("Y or N?")).strip().lower()
            if subChoice == "y":
                print(f"Deleting{name},{user_id} with the balance of {balance}.\n")
                usernameR = str(input("Type your user.\n")).strip().lower()
                delete_user(usernameR)
                break
            else:
                print("Invalid choice")
                break

        else:
            print("Invalid choice!")
