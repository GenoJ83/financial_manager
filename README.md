# Personal Finance Manager

A Python-based personal finance tracker refactored using Object-Oriented Design (OOD) principles.

## Project Overview

This application helps users track weekly expenses against a budget. It was originally a procedural script and has been refactored to follow OOP best practices.

---

## OOP Principles Applied

### 1. Encapsulation

**Definition:** Bundling data (attributes) and methods that operate on that data into a single unit (class), while restricting direct access to some components.

**Why:** Protects object integrity by preventing external code from modifying internal state directly. Changes to internal implementation won't break external code.

**Where Applied:**

| Class | Application |
|-------|-------------|
| `Transaction` | `self._description`, `self._amount`, `self._timestamp` are protected |
| `Budget` | `self._amount`, `self._spent` are managed only through class methods |
| `TransactionLog` | Internal list `self._transactions` is hidden |

```python
# Example: Validation happens inside the class
class Budget:
    def __init__(self, amount: float):
        if amount < 0:
            raise ValueError("Budget cannot be negative")
        self._amount = amount  # Protected attribute
```

---

### 2. Abstraction

**Definition:** Hiding complex implementation details behind a simple interface, exposing only what is necessary.

**Why:** Reduces complexity for users of the class. They don't need to understand internal calculations—they just use the interface.

**Where Applied:**

| Class | Method/Property | What It Hides |
|-------|-----------------|---------------|
| `Budget` | `remaining` | The subtraction logic `_amount - _spent` |
| `Budget` | `is_exceeded` | The comparison logic |
| `TransactionLog` | `get_total()` | The summation loop |
| `Transaction` | `@property` decorators | Direct attribute access |

```python
# User sees simple interface, not complex logic
@property
def remaining(self) -> float:
    """ABSTRACTION: Computed property - external code doesn't see the calculation."""
    return self._amount - self._spent
```

---

### 3. Polymorphism

**Definition:** Objects of different classes can be treated as objects of a common superclass. Python's duck typing enables this naturally.

**Why:** Allows code to work with different object types uniformly. Enables iteration protocols, comparison, and more.

**Where Applied:**

| Method | Purpose |
|--------|---------|
| `__repr__()` | Custom string representation for debugging |
| `__iter__()` | Enables `for t in transaction_log` |
| `__len__()` | Enables `len(transaction_log)` |

```python
# POLYMORPHISM: Can iterate directly over TransactionLog
for i, transaction in enumerate(transactions, start=1):
    print(f"{i}. {transaction.description}")
```

---

### 4. Single Responsibility Principle (SRP)

**Definition:** Each class should have one reason to change—one job.

**Why:** Makes code easier to maintain, test, and understand. Changes to one responsibility don't affect others.

| Class | Responsibility |
|-------|----------------|
| `Transaction` | Represents a single expense data |
| `Budget` | Manages budget calculations and validation |
| `TransactionLog` | Manages collection of transactions |
| `FinanceManager` | Orchestrates application flow |

---

### 5. Facade Pattern

**Definition:** Provides a simplified interface to a complex subsystem.

**Why:** Users interact with one class (`FinanceManager`) instead of managing `Budget`, `TransactionLog`, and `Transaction` separately.

```python
# User only needs to work with FinanceManager
manager = FinanceManager()
manager.run()  # Handles everything internally
```

---

## Clean Code Principles Applied

### 1. Meaningful Names

```python
# ✓ Good: Describes what the variable holds
total_spent = budget.total_spent

# ✗ Bad: Cryptic names
ts = b.ts
```

### 2. Small, Focused Functions

Each method does one thing:
- `get_budget()` → Gets budget from user
- `add_expense()` → Adds expense to budget
- `print_summary()` → Displays report

### 3. Type Hints

```python
def add_transaction(self, description: str, amount: float) -> Transaction:
    # Both input types and return type are explicitly declared
```

### 4. Docstrings

Every class and public method has a docstring explaining:
- What it does
- Parameters (if any)
- Return value (if any)

### 5. DRY (Don't Repeat Yourself)

Calculations like budget remaining are done in one place (`Budget.remaining` property) rather than scattered throughout the code.

### 6. Separation of Concerns

| Layer | Handles |
|-------|---------|
| Data Layer | `Transaction`, `Budget` |
| Collection Layer | `TransactionLog` |
| Application Layer | `FinanceManager` |

---

## Class Reference

### Transaction

Represents a single expense entry.

| Member | Type | Description |
|--------|------|-------------|
| `description` | property | Expense description (read-only) |
| `amount` | property | Expense amount (read-only) |
| `timestamp` | property | When transaction occurred (read-only) |

---

### Budget

Manages budget limits and spending.

| Member | Type | Description |
|--------|------|-------------|
| `total_budget` | property | Original budget amount |
| `total_spent` | property | Sum of all expenses |
| `remaining` | property | Budget minus spent |
| `is_exceeded` | property | True if spent > budget |
| `deficit` | property | Amount over budget (0 if within budget) |
| `add_expense()` | method | Add expense to total |

---

### TransactionLog

Manages a collection of transactions.

| Member | Type | Description |
|--------|------|-------------|
| `transactions` | property | List of all transactions |
| `count` | property | Number of transactions |
| `add_transaction()` | method | Add new transaction |
| `get_total()` | method | Sum of all amounts |
| `__iter__()` | method | Enable iteration |
| `__len__()` | method | Enable len() |

---

### FinanceManager

Main application orchestrator.

| Member | Type | Description |
|--------|------|-------------|
| `budget` | attribute | Current Budget instance |
| `transaction_log` | attribute | Current TransactionLog instance |
| `get_budget()` | method | Prompt user for budget |
| `get_transaction()` | method | Prompt user for expense |
| `check_budget_status()` | method | Warn if over budget |
| `print_summary()` | method | Display final report |
| `run()` | method | Start application |

---

## Running the Application

```bash
python3 financial_budget.py
```

**Sample Output:**
```
Welcome to the Personal Finance Manager

Enter your weekly budget: 500000

Enter at least 5 transactions.

Transaction 1
Enter expense description: groceries
Enter expense amount: 150000

Transaction 2
Enter expense description: transport
Enter expense amount: 50000
...

========== FINAL FINANCIAL SUMMARY ==========
Initial Budget: UGX 500000.00
Total Expenses: UGX 350000.00
Remaining Balance: UGX 150000.00

--- TRANSACTION LOG ---
1. groceries - UGX 150000.00 [14:30:22]
2. transport - UGX 50000.00 [14:31:05]
...
```

---

## File Structure

```
financial_manager/
├── financial_budget.py    # Main application (OOP refactored)
├── financial_budjet        # Original procedural script (preserved)
└── README.md              # This file
```

