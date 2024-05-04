import unittest
from hash.hashed_str import hash_str, hash_matches


class HashedStrTest(unittest.TestCase):
    def test_hash_str(self):
        password = 'random_password'
        hashed_str = hash_str(password)
        self.assertEqual(hashed_str.value, hash_str(password, hashed_str.salt).value)
        self.assertNotEqual(hashed_str.value, hash_str('wrong_password', hashed_str.salt).value)

    def test_matches(self):
        password = 'random_password'
        hashed_str = hash_str(password)
        self.assertTrue(hash_matches(hashed_str, password))
        self.assertFalse(hash_matches(hashed_str, 'wrong_password'))


if __name__ == '__main__':
    unittest.main()
