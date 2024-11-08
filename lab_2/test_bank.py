import unittest
from unittest.mock import patch, MagicMock
from task import Account, Person, AccountFrozenException, Bank, person_generator


class TestPerson(unittest.TestCase):
    def setUp(self):
        self.person = Person(
            first_name="John",
            last_name="Doe",
            city="Sample City",
            street="Sample Street",
            zip_code="12345",
            phone_number="123-456-7890"
        )

    def test_full_address(self):
        self.assertEqual(
            self.person.full_address(),
            "Address: Sample City, Sample Street, 12345. Phone: 123-456-7890"
        )

    def test_validate_phone_number_valid(self):
        self.assertTrue(Person.validate_phone_number("123-456-7890"))

    def test_validate_phone_number_invalid(self):
        self.assertFalse(Person.validate_phone_number("1234567890"))

    def test_validate_zip_code_valid(self):
        self.assertTrue(Person.validate_zip_code("12345"))

    def test_validate_zip_code_invalid(self):
        self.assertFalse(Person.validate_zip_code("1234"))

    def test_create_default_person(self):
        default_person = Person.create_default_person()
        self.assertEqual(default_person.first_name, "John")
        self.assertEqual(default_person.last_name, "Doe")
        self.assertEqual(default_person.city, "Default City")
        self.assertEqual(default_person.zip_code, "00000")


class TestAccount(unittest.TestCase):
    def setUp(self):
        self.person = Person("Jane", "Doe", "City", "Street", "54321")
        self.account = Account(self.person, "123456", 1000)

    def test_deposit(self):
        self.account.deposit(500)
        self.assertEqual(self.account.balance, 1500)

    def test_withdraw(self):
        self.account.withdraw(200)
        self.assertEqual(self.account.balance, 800)

    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(1200)

    def test_freeze_account(self):
        self.account.freeze_and_notify()
        self.assertTrue(self.account.frozen)
        with self.assertRaises(AccountFrozenException):
            self.account.deposit(100)

    def test_unfreeze_account(self):
        self.account.freeze_and_notify()
        self.account.unfreeze_and_notify()
        self.assertFalse(self.account.frozen)

    def test_transfer_funds(self):
        target_account = Account(self.person, "654321", 500)
        self.account.transfer(300, target_account)
        self.assertEqual(self.account.balance, 700)
        self.assertEqual(target_account.balance, 800)

    @patch('builtins.open', new_callable=MagicMock)
    def test_generate_statement(self, mock_open):
        self.account.generate_statement("test_statement.txt")
        mock_open.assert_called_with("test_statement.txt", "w")


class TestBank(unittest.TestCase):
    def setUp(self):
        self.bank = Bank("TestBank")
        self.person = Person("Alice", "Johnson", "City", "Street", "12345")

    def test_create_account(self):
        account = self.bank.create_account(self.person, 500)
        self.assertEqual(account.balance, 500)
        self.assertIsInstance(account, Account)

    @patch('json.dump')
    @patch('builtins.open')
    def test_save_accounts_to_file(self, mock_open, mock_json_dump):
        self.bank.accounts["123456"] = Account(self.person, "123456", 500)
        self.bank.save_accounts_to_file("test_accounts.json")
        mock_open.assert_called_with("test_accounts.json", "w")
        mock_json_dump.assert_called_once()

    @patch('json.load', return_value={
        "123456": {
            "balance": 500,
            "person": {
                "first_name": "Alice",
                "last_name": "Johnson",
                "city": "City",
                "street": "Street",
                "zip_code": "12345",
                "phone_number": "123-456-7890"
            }
        }
    })
    @patch('builtins.open')
    def test_load_accounts_from_file(self, mock_open, mock_json_load):
        accounts = self.bank.load_accounts_from_file("test_accounts.json")
        self.assertIn("123456", accounts)
        account = accounts["123456"]
        self.assertEqual(account.person.first_name, "Alice")
        self.assertEqual(account.balance, 500)


class TestPersonGenerator(unittest.TestCase):
    def test_person_generator(self):
        people = list(person_generator(5))
        self.assertEqual(len(people), 5)
        self.assertIsInstance(people[0], Person)
        self.assertTrue(all(Person.validate_phone_number(person.phone_number) for person in people))
        self.assertTrue(all(Person.validate_zip_code(person.zip_code) for person in people))


if __name__ == '__main__':
    unittest.main()
