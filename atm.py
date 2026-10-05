MIN_BALANCE = 20.0


class Account:
    """Represents a single bank account."""

    def __init__(self, name, account_number, pin, balance):
        self.name = name
        self.account_number = account_number
        self.pin = str(pin)  # Stored as string for safe comparison
        self.balance = float(balance)

    def __str__(self):
        return (f"< Account {self.account_number} | {self.name} | "
                f"Balance GHS {self.balance:.2f} >")

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be greater than zero.")
            return

        self.balance += amount
        print(f"Successfully deposited GHS {amount:.2f}")
        print(f"{self}\n")

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be greater than zero.")
        elif self.balance <= MIN_BALANCE:
            print("Withdrawal denied: minimum balance requirement reached.")
        elif self.balance - amount < MIN_BALANCE:
            print(f"Insufficient balance. You must retain at least "
                  f"GHS {MIN_BALANCE:.2f} in your account.")
        else:
            self.balance -= amount
            print(f"Successfully withdrew GHS {amount:.2f}")
            print(self)
        print()


class ATM:
    """Handles authentication and the interactive menu for an account database."""

    def __init__(self, accounts):
        self.accounts = accounts

    def authenticate(self, max_attempts=3):
        print("=== Welcome to the ATM System ===")
        attempts = max_attempts

        while attempts > 0:
            acc_num = input("Enter your Account Number: ").strip()
            pin = input("Enter your 4-digit PIN: ").strip()

            account = self.accounts.get(acc_num)
            if account and account.pin == pin:
                print(f"\nAuthentication successful! Welcome, {account.name}.\n")
                return account

            attempts -= 1
            print(f"Invalid account number or PIN. Attempts remaining: {attempts}\n")

        print("Too many failed attempts. Program shutting down.")
        return None

    @staticmethod
    def _read_amount(prompt):
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input! Please enter a numerical value.\n")
            return None

    def run(self):
        account = self.authenticate()
        if account is None:
            return

        menu = (
            "---------------------------------\n"
            "Please choose an option:\n"
            "1. Check Balance / Account Info\n"
            "2. Deposit Money\n"
            "3. Withdraw Money\n"
            "Type 'end' to exit the system.\n"
            "---------------------------------"
        )

        while True:
            print(menu)
            choice = input("Enter your choice: ").strip().lower()

            if choice == '1':
                print(f"\n{account}\n")

            elif choice == '2':
                amount = self._read_amount("Enter deposit amount (GHS): ")
                if amount is not None:
                    account.deposit(amount)

            elif choice == '3':
                amount = self._read_amount("Enter withdrawal amount (GHS): ")
                if amount is not None:
                    account.withdraw(amount)

            elif choice == 'end':
                print("\nThank you for using our ATM. Goodbye!")
                break

            else:
                print("\nInvalid selection. Please enter 1, 2, 3, or 'end'.\n")


# Accounts database (keys are strings matching account numbers)
ACCOUNTS_DB = {
    "4010206845": Account("John Doe", "4010206845", "1234", 100.0),
    "4010206846": Account("Jane Smith", "4010206846", "5678", 250.0),
    "4010206847": Account("Kwame Mensah", "4010206847", "0000", 20.0),
}


def main():
    ATM(ACCOUNTS_DB).run()


if __name__ == "__main__":
    main()