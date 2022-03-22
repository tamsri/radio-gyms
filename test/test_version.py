import unittest
import radio_gyms


class TestVersion(unittest.TestCase):

    def test_version(self):
        """Check Version from radio_gyms"""
        self.assertEqual(radio_gyms.__version__, "0.1.1")


if __name__ == '__main__':
    unittest.main()