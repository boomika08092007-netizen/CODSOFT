"""
╔══════════════════════════════════════════════════╗
║          ATM Machine Simulation                  ║
║          Object-Oriented Programming             ║
╚══════════════════════════════════════════════════╝

Concepts Used:
  - Classes & Objects
  - Encapsulation (private attributes with name mangling)
  - Methods (instance methods)
  - Input Validation
  - Exception Handling
"""

# ─────────────────────────────────────────────────────────────────────────────
#  Helper: pretty console formatting
# ─────────────────────────────────────────────────────────────────────────────
LINE  = "═" * 50
DLINE = "─" * 50

def header(title: str) -> None:
    """Print a section header."""
    print(f"\n{LINE}")
    print(f"   {title}")
    print(LINE)

def success(msg: str) -> None:
    print(f"\n  ✔  {msg}")

def error(msg: str) -> None:
    print(f"\n  ✘  {msg}")

def info(msg: str) -> None:
    print(f"\n  ℹ  {msg}")


# ─────────────────────────────────────────────────────────────────────────────
#  Class 1 – BankAccount
# ─────────────────────────────────────────────────────────────────────────────
class BankAccount:
    """
    Represents a customer's bank account.

    Attributes (private)
    --------------------
    __balance : float
        Current account balance.

    Methods
    -------
    deposit(amount)      → adds money to the account
    withdraw(amount)     → deducts money from the account
    check_balance()      → returns the current balance
    """

    def __init__(self, initial_balance: float = 0.0) -> None:
        """Initialise the account with an optional starting balance."""
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        self.__balance: float = initial_balance          # private attribute

    # ── public interface ──────────────────────────────────────────────────────

    def deposit(self, amount: float) -> bool:
        """
        Add *amount* to the account balance.

        Returns True on success, False if the amount is invalid.
        """
        if amount <= 0:
            error("Invalid Input – deposit amount must be greater than zero.")
            return False

        self.__balance += amount
        success(f"Transaction Successful  |  Deposited: ₹{amount:,.2f}")
        return True

    def withdraw(self, amount: float) -> bool:
        """
        Deduct *amount* from the account balance.

        Returns True on success, False on validation failure.
        """
        if amount <= 0:
            error("Invalid Input – withdrawal amount must be greater than zero.")
            return False

        if amount > self.__balance:
            error(f"Insufficient Balance  |  "
                  f"Requested ₹{amount:,.2f}, Available ₹{self.__balance:,.2f}")
            return False

        self.__balance -= amount
        success(f"Transaction Successful  |  Withdrawn: ₹{amount:,.2f}")
        return True

    def check_balance(self) -> float:
        """Return (and display) the current balance."""
        print(f"\n  {'Account Balance':.<30} ₹{self.__balance:>10,.2f}")
        return self.__balance

    # ── dunder helpers ────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return f"BankAccount(balance={self.__balance:.2f})"


# ─────────────────────────────────────────────────────────────────────────────
#  Class 2 – ATM
# ─────────────────────────────────────────────────────────────────────────────
class ATM:
    """
    Simulates an ATM terminal connected to a BankAccount.

    Attributes
    ----------
    __account : BankAccount
        The bank account this ATM session operates on.

    Methods
    -------
    run()               → main event loop (keeps running until Exit)
    __display_menu()    → renders the on-screen menu
    __get_amount()      → safely reads a positive numeric amount from the user
    __process(choice)   → delegates to the appropriate BankAccount method
    """

    MENU = {
        "1": "Withdraw",
        "2": "Deposit",
        "3": "Check Balance",
        "4": "Exit",
    }

    def __init__(self, account: BankAccount) -> None:
        """Bind this ATM to a BankAccount object."""
        if not isinstance(account, BankAccount):
            raise TypeError("ATM requires a valid BankAccount instance.")
        self.__account: BankAccount = account          # composition / has-a

    # ── public entry-point ────────────────────────────────────────────────────

    def run(self) -> None:
        """Start the ATM session – loops until the user selects Exit."""
        self.__welcome()
        while True:
            self.__display_menu()
            choice = input("\n  Enter your choice (1-4): ").strip()
            if not self.__process(choice):
                break                                  # user chose Exit
            input(f"\n{DLINE}\n  Press Enter to continue…")

        self.__goodbye()

    # ── private helpers ───────────────────────────────────────────────────────

    def __welcome(self) -> None:
        print(f"""
{LINE}
   ███████╗  █████╗  ████████╗███╗   ███╗
   ██╔══██║ ██╔══██╗╚══██╔══╝████╗ ████║
   ███████║ ███████║   ██║   ██╔████╔██║
   ██╔══██║ ██╔══██║   ██║   ██║╚██╔╝██║
   ██║  ██║ ██║  ██║   ██║   ██║ ╚═╝ ██║
   ╚═╝  ╚═╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚═╝
{LINE}
   Welcome!  Please use the menu below.
{LINE}""")

    def __display_menu(self) -> None:
        header("ATM – Main Menu")
        for key, label in self.MENU.items():
            print(f"   [{key}]  {label}")
        print(DLINE)

    def __get_amount(self, action: str) -> float | None:
        """
        Prompt the user for a monetary amount.

        Returns a positive float, or None if the input is invalid.
        """
        raw = input(f"\n  Enter amount to {action}: ₹").strip()
        try:
            amount = float(raw)
        except ValueError:
            error("Invalid Input – please enter a numeric value.")
            return None

        if amount < 0:
            error("Invalid Input – amount cannot be negative.")
            return None

        return amount

    def __process(self, choice: str) -> bool:
        """
        Execute the selected menu option.

        Returns False when the user selects Exit (signals the loop to stop),
        True otherwise.
        """
        if choice == "1":                              # ── Withdraw
            header("Withdraw Cash")
            amount = self.__get_amount("withdraw")
            if amount is not None:
                self.__account.withdraw(amount)

        elif choice == "2":                            # ── Deposit
            header("Deposit Cash")
            amount = self.__get_amount("deposit")
            if amount is not None:
                self.__account.deposit(amount)

        elif choice == "3":                            # ── Check Balance
            header("Account Balance")
            self.__account.check_balance()

        elif choice == "4":                            # ── Exit
            return False

        else:
            error("Invalid Input – please select an option from 1 to 4.")

        return True                                    # keep loop running

    def __goodbye(self) -> None:
        print(f"""
{LINE}
   Thank you for using our ATM.
   Please collect your card.  Have a great day!
{LINE}
""")


# ─────────────────────────────────────────────────────────────────────────────
#  Entry-point
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Create a BankAccount object with an initial balance
    my_account = BankAccount(initial_balance=10_000.00)

    # Create an ATM object and connect it to the account (composition)
    atm = ATM(account=my_account)

    # Start the ATM session
    atm.run()
