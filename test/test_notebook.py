from unittest import TestCase
from radio_gyms.utils import IsNotebook

class TestNotebook(TestCase):

    def test_if_notebook(self):
        self.assertFalse(IsNotebook())
