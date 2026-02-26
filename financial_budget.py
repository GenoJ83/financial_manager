"""
Personal Finance Manager - Object-Oriented Implementation

OOP Principles Demonstrated:
- ENCAPSULATION: Bundling data (attributes) and methods together in classes
- ABSTRACTION: Hiding complex implementation details behind simple interfaces
- INHERITANCE: Creating new classes from existing ones (used internally by Python)
- POLYMORPHISM: Different classes can be used interchangeably via common interfaces
"""

from datetime import datetime
from typing import List, Optional


# ENCAPSULATION:

class Transaction:
    """
    Represents a single financial transaction.

    ENCAPSULATION: All transaction data (description, amount, timestamp)
    are bundled together with methods that operate on that data.
    """

    def __init__(self, description: str, amount: float):
        # Protected attributes
        self._description = description
        self._amount = amount
        self._timestamp = datetime.now()

    # ABSTRACTION:
    @property
    def description(self) -> str:
        """ABSTRACTION: Getter provides read-only access to description."""
        return self._description

    @property
    def amount(self) -> float:
        """ABSTRACTION: Getter provides read-only access to amount."""
        return self._amount

    @property
    def timestamp(self) -> datetime:
        """ABSTRACTION: Getter provides read-only access to timestamp."""
        return self._timestamp

    def __repr__(self) -> str:
        """
        POLYMORPHISM: __repr__ is a special method (dunder) that allows
        custom string representation of the object.
        """
        return f"Transaction(description='{self._description}', amount={self._amount})"


class Budget:
    """
    Manages budget and tracks spending.

    ENCAPSULATION: Budget logic (validation, calculations) is contained
    within the class - external code doesn't need to know HOW budget
    tracking works.
    """

    def __init__(self, amount: float):
        # ENCAPSULATION: Validation happens inside the class
        if amount < 0:
            raise ValueError("Budget cannot be negative")
        self._amount = amount
        self._spent = 0.0

    @property
    def total_budget(self) -> float:
        """ABSTRACTION: Returns total budget without exposing internal state."""
        return self._amount

    @property
    def total_spent(self) -> float:
        """ABSTRACTION: Returns total spent, computed internally."""
        return self._spent

    @property
    def remaining(self) -> float:
        """ABSTRACTION: Computed property - external code doesn't see the calculation."""
        return self._amount - self._spent

    @property
    def is_exceeded(self) -> bool:
        """ABSTRACTION: Returns boolean without exposing the comparison logic."""
        return self._spent > self._amount

    @property
    def deficit(self) -> float:
        """ABSTRACTION: Computes deficit only when needed."""
        return self._spent - self._amount if self.is_exceeded else 0

    def add_expense(self, amount: float) -> None:
        """
        ENCAPSULATION: Expense tracking logic is encapsulated.
        External code just calls this method - doesn't manage _spent directly.
        """
        if amount < 0:
            raise ValueError("Expense amount cannot be negative")
        self._spent += amount

    def __repr__(self) -> str:
        """POLYMORPHISM: Custom string representation."""
        return f"Budget(total={self._amount}, spent={self._spent})"


class TransactionLog:
    """
    Manages collection of transactions.

    ENCAPSULATION: The internal list and operations on it are hidden.
    ABSTRACTION: Users interact through simple methods without knowing
    the underlying data structure.
    """

    def __init__(self):
        # ENCAPSULATION: Internal storage is protected
        self._transactions: List[Transaction] = []

    def add_transaction(self, description: str, amount: float) -> Transaction:
        """
        ENCAPSULATION: Creates transaction and adds to internal list.
        External code doesn't need to know about the list at all.
        """
        transaction = Transaction(description, amount)
        self._transactions.append(transaction)
        return transaction

    @property
    def transactions(self) -> List[Transaction]:
        """ABSTRACTION: Returns copy or view to prevent direct modification."""
        return self._transactions

    @property
    def count(self) -> int:
        """ABSTRACTION: Returns count without exposing internal list."""
        return len(self._transactions)

    def get_total(self) -> float:
        """ABSTRACTION: Sum calculation hidden from caller."""
        return sum(t.amount for t in self._transactions)
    # POLYMORPHISM:
    # Python's built-in functions and operators.


    def __iter__(self):
        """
        POLYMORPHISM: Allows iteration: for t in transaction_log
        The class now behaves like a standard sequence.
        """
        return iter(self._transactions)

    def __len__(self):
        """POLYMORPHISM: Allows len(transaction_log)."""
        return len(self._transactions)

    def __repr__(self):
        """POLYMORPHISM: Custom string representation."""
        return f"TransactionLog(count={self.count})"


class FinanceManager:
    """
    Main class orchestrating the finance management application.

    FACADE PATTERN: This class provides a simplified interface to the
    entire finance management system. Users interact with this one class
    rather than dealing with Budget, TransactionLog, and Transaction directly.

    SINGLE RESPONSIBILITY: This class's only job is to orchestrate the
    flow of the application - it delegates specific tasks to other classes.
    """

    def __init__(self):
        # ENCAPSULATION: Manages its own related objects
        self.budget: Optional[Budget] = None
        self.transaction_log = TransactionLog()

    def get_budget(self) -> Budget:
        """Prompt user to enter a valid non-negative budget."""
        while True:
            try:
                amount = float(input("Enter your weekly budget: "))
                # Delegation: FinanceManager creates Budget, doesn't manage it directly
                self.budget = Budget(amount)
                return self.budget
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")

    def get_transaction(self) -> Transaction:
        """Capture a single transaction from the user."""
        description = input("Enter expense description: ")

        while True:
            try:
                amount = float(input("Enter expense amount: "))
                # Delegation to TransactionLog
                transaction = self.transaction_log.add_transaction(description, amount)
                # Delegation to Budget
                self.budget.add_expense(amount)
                return transaction
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")

    def check_budget_status(self) -> None:
        """Display budget warning if exceeded."""
        # ABSTRACTION: Just call is_exceeded - don't need to know the logic
        if self.budget.is_exceeded:
            print("WARNING: You have exceeded your budget!")

    def print_summary(self) -> None:
        """Display final financial report."""
        budget = self.budget
        transactions = self.transaction_log

        print("\n========== FINAL FINANCIAL SUMMARY ==========")
        print(f"Initial Budget: UGX {budget.total_budget:.2f}")
        print(f"Total Expenses: UGX {budget.total_spent:.2f}")

        # ABSTRACTION: Using properties hides the logic
        if budget.is_exceeded:
            print(f"Deficit: UGX {budget.deficit:.2f}")
        else:
            print(f"Remaining Balance: UGX {budget.remaining:.2f}")

        print("\n--- TRANSACTION LOG ---")
        # POLYMORPHISM: Can iterate directly over TransactionLog
        for i, transaction in enumerate(transactions, start=1):
            timestamp = transaction.timestamp.strftime("%H:%M:%S")
            print(f"{i}. {transaction.description} - UGX {transaction.amount:.2f} [{timestamp}]")

    def run(self) -> None:
        """
        Main application loop.

        SINGLE RESPONSIBILITY: This method coordinates the application flow
        but delegates actual work to other methods/classes.
        """
        print("Welcome to the Personal Finance Manager\n")

        self.get_budget()
        print("\nEnter at least 5 transactions.")

        for i in range(5):
            print(f"\nTransaction {i + 1}")
            self.get_transaction()
            self.check_budget_status()

        self.print_summary()


# MAIN ENTRY POINT
def main():
    """Entry point for the application."""

    manager = FinanceManager()
    manager.run()


if __name__ == "__main__":
    main()

