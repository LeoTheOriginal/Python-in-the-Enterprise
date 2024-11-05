import random
import time
import logging
import multiprocessing
import re
import json
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


def transaction_logger(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        logging.info(f"Transaction {func.__name__} executed.")
        return result

    return wrapper


class AccountFrozenException(Exception):
    pass


class AccountUnfrozenException(Exception):
    pass


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
            phone_number=f"{random.randint(100, 999)}-{random.randint(100, 999)}-"
                         f"{random.randint(1000, 9999)}"
        )


@dataclass
class Person:
    first_name: str
    last_name: str
    city: str
    street: str
    zip_code: str
    phone_number: str = field(default="000-000-0000", repr=False)   # dla przykładu nie chcemu
    # domyślnie wypisywać numeru telefonu

    def full_address(self):
        return f"Address: {self.city}, {self.street}, {self.zip_code}. Phone: {self.phone_number}"

    @staticmethod
    def validate_phone_number(phone_number):
        pattern = r"^\d{3}-\d{3}-\d{4}$"
        if re.match(pattern, phone_number):
            return True
        else:
            logging.warning(f"Invalid phone number format for {phone_number}")
            return False

    @staticmethod
    def validate_zip_code(zip_code):
        return zip_code.isdigit() and len(zip_code) == 5

    @classmethod
    def create_default_person(cls):
        return cls(
            first_name="John",
            last_name="Doe",
            city="Default City",
            street="Default Street",
            zip_code="00000",
            phone_number="000-000-0000"
        )


class Account:
    def __init__(self, person, account_number, balance=0):
        self.person = person
        self.account_number = account_number
        self.balance = balance
        self.frozen = False

        # Konfiguracja loggera dla konta
        self.logger = logging.getLogger(f"AccountLogger_{self.account_number}")
        handler = logging.FileHandler(f"{self.account_number}_operations.log")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.propagate = False  # Zapobiega duplikacji logów

    @transaction_logger
    def deposit(self, amount):
        if not self.frozen:
            self.balance += amount
            self.logger.info(f"Deposited {amount}. New balance: {self.balance}")
        else:
            self.logger.warning("Attempted deposit on a frozen account.")
            raise AccountFrozenException(f"Cannot deposit to account {self.account_number}")

    @transaction_logger
    def withdraw(self, amount):
        if self.frozen:
            self.logger.warning("Attempted withdrawal from a frozen account.")
            raise AccountFrozenException(f"Cannot withdraw from a frozen account {self.account_number}")
        elif self.balance < amount:
            self.logger.warning("Attempted withdrawal of insufficient funds.")
            raise ValueError(f"Cannot withdraw due to insufficient funds in account {self.account_number}.")
        else:
            self.balance -= amount
            self.logger.info(f"Withdrew {amount} from account {self.account_number}. New balance: {self.balance}")

    @transaction_logger
    def transfer(self, amount, target_account):
        if self.frozen:
            self.logger.warning("Attempted withdrawal from a frozen account.")
            raise AccountFrozenException(f"Cannot withdraw from a frozen account {self.account_number}")
        elif self.balance < amount:
            self.logger.warning("Attempted withdrawal of insufficient funds.")
            raise ValueError(f"Cannot withdraw due to insufficient funds in account {self.account_number}.")
        else:
            self.balance -= amount
            target_account.balance += amount
            self.logger.info(
                f"Transferred {amount} from account {self.account_number} to account {target_account.account_number}.")
            target_account.logger.info(
                f"Received {amount} from account {self.account_number}. New balance: {target_account.balance}")

    def freeze_and_notify(self):
        if self.frozen:
            self.logger.warning("Attempted freeze on already frozen account")
            raise AccountFrozenException(f"Cannot freeze already frozen account {self.account_number}")
        else:
            self.frozen = True
            logging.info(f"Account {self.account_number} has been frozen.")
            self.logger.info(f"Account {self.account_number} has been frozen.")

    def unfreeze_and_notify(self):
        if not self.frozen:
            self.logger.warning("Attempted unfreeze on already unfrozen account")
            raise AccountUnfrozenException(f"Cannot unfreeze already unfrozen account {self.account_number}")
        else:
            self.frozen = False
            logging.info(f"Account {self.account_number} has been unfrozen.")
            self.logger.info(f"Account {self.account_number} has been unfrozen.")

    def generate_statement(self, output_filename=None):
        log_filename = f"{self.account_number}_operations.log"
        if output_filename is None:
            output_filename = f"{self.account_number}_statements.txt"

        try:
            with open(log_filename, "r") as log_file, open(output_filename, "w") as output_file:
                output_file.write(f"Statement for Account {self.account_number}\n")
                output_file.write("=" * 30 + "\n")
                for line in log_file:
                    output_file.write(line)
            logging.info(f"Statement generated for account {self.account_number} in {output_filename}")
        except FileNotFoundError:
            logging.error(f"Log file {log_filename} not found for account {self.account_number}")
            raise FileNotFoundError(f"No operations logged for account {self.account_number}")

    def __repr__(self):
        if not self.frozen:
            return (f"Account {self.account_number} for {self.person.first_name} {self.person.last_name}"
                    f" with balance {self.balance}.")
        else:
            return f"Account {self.account_number} is currently frozen."


class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = {}

    @classmethod
    def create_account(cls, person, initial_balance=0):
        account_number = str(random.randint(100000, 999999))
        new_account = Account(person, account_number, initial_balance)
        logging.info(
            f"Created new account with number {account_number} for {person.first_name} {person.last_name} "
            f"with initial balance {initial_balance}.")
        return new_account

    def get_account(self, account_number):
        return self.accounts.get(account_number, None)

    def save_accounts_to_file(self, filename="accounts.json"):
        accounts_data = {}
        for acc in self.accounts.values():
            accounts_data[acc.account_number] = {
                "balance": acc.balance,
                "person": {
                    "first_name": acc.person.first_name,
                    "last_name": acc.person.last_name,
                    "city": acc.person.city,
                    "street": acc.person.street,
                    "zip_code": acc.person.zip_code,
                    "phone_number": acc.person.phone_number
                }
            }

        with open(filename, "w") as file:
            json.dump(accounts_data, file, indent=4)  # Dodano `indent=4` dla lepszej czytelności
        logging.info("Accounts saved to file.")

    @staticmethod
    def load_accounts_from_file(filename="accounts.json"):
        with open(filename, "r") as file:
            data = json.load(file)
            accounts = {}

            for account_number, account_data in data.items():
                # Tworzenie obiektu `Person` z zapisanych danych
                person_data = account_data["person"]
                person = Person(
                    first_name=person_data["first_name"],
                    last_name=person_data["last_name"],
                    city=person_data["city"],
                    street=person_data["street"],
                    zip_code=person_data["zip_code"],
                    phone_number=person_data["phone_number"]
                )

                account = Account(
                    person=person,
                    account_number=account_number,
                    balance=account_data["balance"]
                )

                accounts[account.account_number] = account

            logging.info("Accounts loaded from file.")
            return accounts

    def __str__(self):
        accounts_info = "\n".join(str(account) for account in self.accounts.values())
        return f"Bank: {self.name}\nAccounts:\n{accounts_info}\nNumber of accounts: {len(self.accounts)}\n"


def create_account_for_person(person, bank, initial_balance, shared_accounts):
    account = bank.create_account(person, initial_balance)
    shared_accounts[account.account_number] = (person, account.balance)
    print(f"Created account {account.account_number} for {person.first_name} {person.last_name}")


def execute_operation(operation, amount, account, target_account=None):
    try:
        match operation:
            case 'deposit':
                account.deposit(amount)
                logging.info(f"Deposited {amount} into account {account.account_number}")

            case 'withdraw':
                account.withdraw(amount)
                logging.info(f"Withdrew {amount} from account {account.account_number}")

            case 'transfer':
                if target_account is not None:
                    account.transfer(amount, target_account)
                    logging.info(f"Transferred {amount} from account {account.account_number} "
                                 f"to account {target_account.account_number}")

            case 'freeze':
                account.freeze_and_notify()
                logging.info(f"Froze account {account.account_number}")

            case 'unfreeze':
                account.unfreeze_and_notify()
                logging.info(f"Unfroze account {account.account_number}")

    except AccountFrozenException as e:
        logging.warning(f"Operation failed: {e}")
    except ValueError as e:
        logging.warning(f"Operation failed: {e}")


def bank_operations_generator(accounts, num_operations=10):
    operations = ['deposit', 'withdraw', 'transfer']    # aktualnie nie ma opcji freeze oraz unfreeze żeby w plikach
    # log oraz generowanych statements.txt zapisywanych było więcej operacji

    accounts_list = list(accounts)

    for _ in range(num_operations):
        operation = random.choice(operations)
        amount = random.randint(100, 1000)
        account = random.choice(accounts_list)

        if operation == 'transfer':
            target_account = random.choice([acc for acc in accounts_list if acc != account])
            execute_operation(operation, amount, account, target_account)
        else:
            execute_operation(operation, amount, account)


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
                pool.apply_async(create_account_for_person,
                                 args=(person, bank, random.randint(1000, 5000), shared_accounts))

            pool.close()
            pool.join()

        print("\n--- Shared Accounts ---\n")
        for acc_number, (person, balance) in shared_accounts.items():
            print(f"Account Number: {acc_number}, Owner: {person}, Balance: {balance}")

        for acc_number, (person, balance) in shared_accounts.items():
            bank.accounts[acc_number] = Account(person, acc_number, balance)

    print("\n--- Bank Accounts ---\n")
    for account in bank.accounts.values():
        print(account)

    print("\n--- Executing operations sequentially ---\n")

    bank_operations_generator(bank.accounts.values(), num_operations=50)

    print(f"\n--- Printing Bank: {bank.name} ---\n")
    print(bank)

    for account in bank.accounts.values():
        account.generate_statement()

    print("\n--- Accounts' statements generated ---\n")

    print("\n--- Saving Account to file accounts.json ---\n")
    bank.save_accounts_to_file()

    print("\n--- Loading accounts from file ---\n")
    bank_loaded_accounts = Bank.load_accounts_from_file()

    print("\n--- Printing loaded bank accounts from file accounts,json ---\n")
    for account in bank.accounts.values():
        print(account)

    print("Bank simulation finished.")
