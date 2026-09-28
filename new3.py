"""Simple ATM - a beginner OOP project. Run:  python atm.py
Demo cards -> 1111 / PIN 1234 (Asha),  2222 / PIN 4321 (Ravi)
"""


class InsufficientFundsError(Exception):
    pass


class Account:
    """Holds money. The balance is private (encapsulation)."""

    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance
        self.history = []          # list of transaction strings

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive.")
        self._balance += amount
        self.history.append(f"Deposited  +{amount}")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive.")
        if amount > self._balance:
            raise InsufficientFundsError("Not enough balance.")
        self._balance -= amount
        self.history.append(f"Withdrew   -{amount}")


class Card:
    """Linked to one account. Locks after 3 wrong PINs."""

    MAX_ATTEMPTS = 3

    def __init__(self, number, pin, account):
        self.number = number
        self._pin = pin
        self.account = account
        self._failed = 0
        self.locked = False

    def verify_pin(self, pin):
        if self.locked:
            return False
        if pin == self._pin:
            self._failed = 0
            return True
        self._failed += 1
        if self._failed >= self.MAX_ATTEMPTS:
            self.locked = True
        return False

    def attempts_left(self):
        return self.MAX_ATTEMPTS - self._failed

    def change_pin(self, old, new):
        if old != self._pin:
            raise ValueError("Old PIN is incorrect.")
        if not (new.isdigit() and len(new) == 4):
            raise ValueError("New PIN must be 4 digits.")
        self._pin = new


class ATM:
    """Talks to the user and uses Card and Account objects."""

    def __init__(self, cards):
        self.cards = {c.number: c for c in cards}

    def login(self):
        number = input("\nInsert card (enter card number): ").strip()
        card = self.cards.get(number)
        if card is None:
            print("Card not recognised.")
            return None
        if card.locked:
            print("This card is LOCKED. Contact your bank.")
            return None
        while not card.locked:
            if card.verify_pin(input("Enter PIN: ").strip()):
                print(f"Welcome, {card.account.owner}!")
                return card
            if card.locked:
                print("Too many wrong attempts. Card LOCKED.")
            else:
                print(f"Wrong PIN. {card.attempts_left()} attempt(s) left.")
        return None

    def session(self, card):
        acc = card.account
        while True:
            print("\n1. Balance  2. Deposit  3. Withdraw  4. Mini statement  5. Change PIN  6. Exit")
            choice = input("Choose: ").strip()
            try:
                if choice == "1":
                    print(f"Balance: {acc.balance}")
                elif choice == "2":
                    acc.deposit(float(input("Amount: ")))
                    print(f"Done. Balance: {acc.balance}")
                elif choice == "3":
                    acc.withdraw(float(input("Amount: ")))
                    print(f"Please take your cash. Balance: {acc.balance}")
                elif choice == "4":
                    for line in acc.history[-5:] or ["No transactions yet."]:
                        print(line)
                elif choice == "5":
                    card.change_pin(input("Old PIN: "), input("New PIN: "))
                    print("PIN changed.")
                elif choice == "6":
                    print("Goodbye!")
                    return
                else:
                    print("Invalid choice.")
            except (ValueError, InsufficientFundsError) as err:
                print(f"Error: {err}")

    def run(self):
        print("=== Welcome to Python ATM ===")
        while True:
            card = self.login()
            if card:
                self.session(card)
            if input("\nAnother customer? (y/n): ").lower() != "y":
                break


if __name__ == "__main__":
    asha = Card("1111", "1234", Account("Asha", 5000))
    ravi = Card("2222", "4321", Account("Ravi", 1200))
    ATM([asha, ravi]).run()