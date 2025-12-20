from django.test import TestCase

class DummyTest(TestCase):
    def test_pass(self):
        self.assertEqual(1, 1)
