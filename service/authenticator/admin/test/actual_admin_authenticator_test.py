import unittest

from service.authenticator.admin.actual_admin_authenticator import ActualAdminAuthenticator
from service.authenticator.admin.admin_authenticator import AdminAuthenticator
from service.authenticator.admin.repository.dummy_admin_password_repository import DummyAdminPasswordRepository
from service.authenticator.token.actual_token_processor import ActualTokenProcessor
from service.authenticator.token.model.token import Token


class ActualAdminAuthenticatorTest(unittest.TestCase):
    admin_authenticator: AdminAuthenticator

    def setUp(self):
        self.admin_authenticator = ActualAdminAuthenticator(
            DummyAdminPasswordRepository(),
            ActualTokenProcessor(),
        )

    def test_password_set(self):
        self.assertFalse(self.admin_authenticator.password_set())

        self.admin_authenticator.change_password(
            old_password=None,
            new_password='password',
        )
        self.assertTrue(self.admin_authenticator.password_set())

    def test_login(self):
        self.admin_authenticator.change_password(
            old_password=None,
            new_password='password',
        )

        token = self.admin_authenticator.login('password')
        self.assertIsInstance(token, Token)

    def test_login_incorrect_password(self):
        self.admin_authenticator.change_password(
            old_password=None,
            new_password='password',
        )

        with self.assertRaises(Exception):
            self.admin_authenticator.login('incorrect_password')

    def test_change_password(self):
        self.admin_authenticator.change_password(
            old_password=None,
            new_password='password',
        )

        token = self.admin_authenticator.login('password')
        self.assertIsInstance(token, Token)

    def test_change_password_incorrect_old_password(self):
        self.admin_authenticator.change_password(
            old_password=None,
            new_password='password',
        )

        with self.assertRaises(Exception):
            self.admin_authenticator.change_password(
                old_password='incorrect_password',
                new_password='new_password',
            )

        with self.assertRaises(Exception):
            self.admin_authenticator.change_password(
                old_password=None,
                new_password='new_password',
            )

    def test_change_password_password_too_short(self):
        with self.assertRaises(Exception):
            self.admin_authenticator.change_password(
                old_password=None,
                new_password='pass',
            )

    def test_require_authentication(self):
        self.admin_authenticator.change_password(
            old_password=None,
            new_password='password',
        )

        token = self.admin_authenticator.login('password')
        self.admin_authenticator.require_authentication(token)

    def test_require_authentication_incorrect_password(self):
        self.admin_authenticator.change_password(
            old_password=None,
            new_password='password',
        )

        token = self.admin_authenticator.login('password')

        self.admin_authenticator.change_password(
            old_password='password',
            new_password='new_password',
        )

        with self.assertRaises(Exception):
            self.admin_authenticator.require_authentication(token)


if __name__ == '__main__':
    unittest.main()
