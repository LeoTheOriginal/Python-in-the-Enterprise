import random
import time
import multiprocessing


def person_generator(num_persons):
    first_names = ["John", "Jane", "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"]
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson"]
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego"]
    streets = ["Main St", "First St", "Second St", "Third St", "Fourth St", "Fifth St", "Sixth St", "Seventh St"]
    zip_codes = ["10001", "10002", "10003", "10004", "10005", "10006", "10007", "10008"]

    for _ in range(num_persons):
        yield Person(
            first_name=random.choice(first_names),
            last_name=random.choice(last_names),
            city=random.choice(cities),
            street=random.choice(streets),
            zip_code=random.choice(zip_codes),
            phone_number=f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
        )


class Person:
    def __init__(self, first_name, last_name, city, street, zip_code, phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.city = city
        self.street = street
        self.zip_code = zip_code
        self.phone_number = phone_number

    def __repr__(self):
        return f"{self.first_name} {self.last_name} from {self.city}, {self.street}, {self.zip_code}. Phone: {self.phone_number}"


class Account:
    def __init__(self, person, account_number, balance=0):
        self.person = person
        self.account_number = account_number
        self.balance = balance
        self.frozen = False

    def deposit(self, amount):
        if not self.frozen:
            self.balance += amount
            print(f"Deposited {amount} to account {self.account_number}. New balance: {self.balance}")
        else:
            print(f"Account {self.account_number} is frozen. Cannot deposit.")

    def withdraw(self, amount):
        if not self.frozen and self.balance >= amount:
            self.balance -= amount
            print(f"Withdrew {amount} from account {self.account_number}. New balance: {self.balance}")
        else:
            print(f"Account {self.account_number} is either frozen or has insufficient funds.")

    def transfer(self, amount, target_account):
        if not self.frozen and self.balance >= amount:
            self.balance -= amount
            target_account.balance += amount
            print(f"Transferred {amount} from account {self.account_number} to account {target_account.account_number}.")
        else:
            print(f"Account {self.account_number} is either frozen or has insufficient funds.")

    def freeze(self):
        self.frozen = True
        print(f"Account {self.account_number} has been frozen.")

    def unfreeze(self):
        self.frozen = False
        print(f"Account {self.account_number} has been unfrozen.")

    def __repr__(self):
        return f"Account {self.account_number} for {self.person} with balance {self.balance}"


class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = {}

    def create_account(self, person, initial_balance=0):
        account_number = str(random.randint(100000, 999999))
        new_account = Account(person, account_number, initial_balance)
        self.accounts[account_number] = new_account
        print(f"Created new account with number {account_number} for {person} with initial balance {initial_balance}.")
        return new_account

    def get_account(self, account_number):
        return self.accounts.get(account_number, None)


def create_account_for_person(person, bank, initial_balance, shared_accounts):
    account = bank.create_account(person, initial_balance)
    shared_accounts[account.account_number] = (person, account.balance)
    print(f"Created account {account.account_number} for {person}")


def bank_operations_generator(accounts):
    operations = ['deposit', 'withdraw', 'transfer', 'freeze', 'unfreeze']
    accounts_list = list(accounts)  # Convert dict_values to list
    while True:
        if not accounts_list:
            break  # Skip iteration if accounts list is empty
        operation = random.choice(operations)
        amount = random.randint(100, 1000)
        account = random.choice(accounts_list)
        if operation == 'transfer':
            target_account = random.choice([acc for acc in accounts_list if acc != account])
            yield operation, amount, account, target_account
        else:
            yield operation, amount, account


if __name__ == '__main__':
    print("Starting Bank simulation...")
    time.sleep(1)
    print("Bank simulation started.")
    time.sleep(1)

    bank = Bank("MyBank")
    persons = list(person_generator(5))

    with multiprocessing.Manager() as manager:
        shared_accounts = manager.dict()

        with multiprocessing.Pool() as pool:
            for person in persons:
                pool.apply_async(create_account_for_person, args=(person, bank, random.randint(1000, 5000), shared_accounts))

            pool.close()
            pool.join()

        print("\n--- Shared Accounts ---\n")
        for acc_number, (person, balance) in shared_accounts.items():
            print(f"Account Number: {acc_number}, Owner: {person}, Balance: {balance}")

    print("\n--- Bank Accounts ---\n")
    for account in bank.accounts.values():
        print(account)
    print("Bank simulation finished.")


