import json
from datetime import datetime

DATA_FILE = "bank_accounts.json"


# ---------- File Handling Functions ----------
def save_accounts(accounts):
    """Save all account data to a JSON file"""
    data = {}
    for acc_no, acc in accounts.items():
        data[acc_no] = {
            "acc_no": acc.acc_no,
            "acc_holder": acc.acc_holder,
            "pin": acc.pin,
            "balance": acc.balance,
            "transactions": acc.transactions
        }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print("💾 Data saved successfully!")


def load_accounts():
    """Load account data from a JSON file if available"""
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        accounts = {}
        for acc_no, info in data.items():
            acc = BankAccount(
                info["acc_no"],
                info["acc_holder"],
                info["pin"],
                info["balance"]
            )
            acc.transactions = info["transactions"]
            accounts[int(acc_no)] = acc
        print("✅ Accounts loaded successfully!")
        return accounts
    except FileNotFoundError:
        print("⚠️ No saved data found. Starting fresh.")
        return {}


# ---------- BankAccount Class ----------
class BankAccount:
    BANK_NAME = "Python Bank of India"
    IFSC_CODE = "HYD500000"  # class variable

    def __init__(self, acc_no, acc_holder, pin, balance=0):
        self.acc_no = acc_no
        self.acc_holder = acc_holder
        self.pin = pin
        self.balance = balance
        self.transactions = []

    # Security Methods
    def verify_pin(self, entered_pin):
        return entered_pin == self.pin

    def change_pin(self, old_pin, new_pin):
        if self.verify_pin(old_pin):
            self.pin = new_pin
            return "✅ PIN changed successfully!"
        else:
            return "❌ Incorrect old PIN. PIN change failed."

    # Account Operations
    def display(self):
        return (f"\n---{self.BANK_NAME}---\n"
                f"Account No: {self.acc_no}\n"
                f"Holder    : {self.acc_holder}\n"
                f"IFSC Code : {self.IFSC_CODE}\n"
                f"Balance   : ₹{self.balance:.2f}\n")

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"{datetime.now()} - Deposited ₹{amount:.2f}, New Balance: ₹{self.balance:.2f}")
        return f"Deposited ₹{amount:.2f}, New Balance: ₹{self.balance:.2f}"

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.transactions.append(f"{datetime.now()} - Withdrew ₹{amount:.2f}, Remaining Balance: ₹{self.balance:.2f}")
            return f"Withdrew ₹{amount:.2f}, Remaining Balance: ₹{self.balance:.2f}"
        else:
            self.transactions.append(f"{datetime.now()} - Failed Withdrawal ₹{amount:.2f} - Insufficient funds!")
            return f"❌ Insufficient funds! Current balance: ₹{self.balance:.2f}"

    def check_balance(self):
        return f"Available Balance: ₹{self.balance:.2f}"

    def show_transactions(self):
        if not self.transactions:
            return "No transactions yet."
        result = "\nTransaction History:\n"
        for i, t in enumerate(self.transactions, start=1):
            result += f"{i}. {t}\n"
        return result.strip()

    def transfer(self, recipient, amount):
        if self.acc_no == recipient.acc_no:
            return "❌ Cannot transfer to the same account."
        if amount <= 0:
            return "❌ Transfer amount must be positive."
        if amount > self.balance:
            self.transactions.append(f"{datetime.now()} - Failed Transfer ₹{amount:.2f} to {recipient.acc_holder} - Insufficient funds!")
            return f"❌ Insufficient balance to transfer ₹{amount:.2f}."
        self.balance -= amount
        recipient.balance += amount
        self.transactions.append(f"{datetime.now()} - Transferred ₹{amount:.2f} to {recipient.acc_holder}, Remaining Balance: ₹{self.balance:.2f}")
        recipient.transactions.append(f"{datetime.now()} - Received ₹{amount:.2f} from {self.acc_holder}, New Balance: ₹{recipient.balance:.2f}")
        return f"✅ Successfully transferred ₹{amount:.2f} to {recipient.acc_holder}. Your remaining balance: ₹{self.balance:.2f}"


# ---------- Load or Create Accounts ----------
try:
    accounts = load_accounts()
except NameError:
    accounts = {}

if not accounts:
    accounts = {
        101: BankAccount(101, "Satya", "1234", 5000),
        102: BankAccount(102, "Ravi", "5678", 3000),
        103: BankAccount(103, "Lakshmi", "9999", 8000),
        104: BankAccount(104, "Chandu", "8877", 4000),
        105: BankAccount(105, "Kumar", "7799", 3000)
    }


# ---------- Main Banking Loop ----------
logged_in = None

while True:
    if not logged_in:
        print(f"\nWelcome to {BankAccount.BANK_NAME}")
        try:
            acc_no = int(input("Enter your account number: "))
        except ValueError:
            print("❌ Invalid input! Account number must be numeric.")
            continue

        entered_pin = input("Enter your 4-digit PIN to login: ")
        account = accounts.get(acc_no)
        if account and account.verify_pin(entered_pin):
            print(f"✅ Login successful! Welcome, {account.acc_holder}.")
            logged_in = account
        else:
            print("❌ Invalid account number or PIN.")
            continue

    print("\n" + "=" * 40)
    print(f"{BankAccount.BANK_NAME}")
    print("=" * 40)
    print("1. View Account Details")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Check Balance")
    print("5. View Transaction History")
    print("6. Change PIN")
    print("7. Logout")
    print("8. Exit")
    print("9. Transfer Money")
    print("=" * 40)

    choice = input("Enter your choice (1 - 9): ")

    if choice == "1":
        print(logged_in.display())

    elif choice == "2":
        try:
            amount = round(float(input("Enter amount to deposit ₹")), 2)
            if amount <= 0:
                print("❌ Deposit amount must be positive.")
            else:
                print(logged_in.deposit(amount))
        except ValueError:
            print("❌ Invalid amount! Please enter a number.")

    elif choice == "3":
        try:
            amount = round(float(input("Enter amount to withdraw ₹")), 2)
            if amount <= 0:
                print("❌ Withdrawal amount must be positive.")
            else:
                print(logged_in.withdraw(amount))
        except ValueError:
            print("❌ Invalid amount! Please enter a number.")

    elif choice == "4":
        print(logged_in.check_balance())

    elif choice == "5":
        print(logged_in.show_transactions())

    elif choice == "6":
        old_pin = input("Enter your old PIN: ")
        new_pin = input("Enter your new 4-digit PIN: ")
        confirm_pin = input("Confirm new PIN: ")
        if new_pin != confirm_pin:
            print("❌ New PINs do not match. Try again.")
        elif not (new_pin.isdigit() and len(new_pin) == 4):
            print("❌ PIN must be exactly 4 digits.")
        else:
            print(logged_in.change_pin(old_pin, new_pin))

    elif choice == "7":
        print(f"🔒 Logged out from account {logged_in.acc_no}")
        logged_in = None

    elif choice == "8":
        print(f"\nThank you for banking with {BankAccount.BANK_NAME}!")
        save_accounts(accounts)
        break

    elif choice == "9":
        try:
            recipient_acc = int(input("Enter recipient account number: "))
        except ValueError:
            print("❌ Invalid input! Account number must be numeric.")
            continue
        recipient = accounts.get(recipient_acc)
        if not recipient:
            print("❌ Recipient account does not exist.")
            continue
        try:
            amount = round(float(input(f"Enter amount to transfer to {recipient.acc_holder} ₹")), 2)
        except ValueError:
            print("❌ Invalid amount! Please enter a number.")
            continue
        print(logged_in.transfer(recipient, amount))

    else:
        print("❌ Invalid choice. Please select between 1 and 9.")
