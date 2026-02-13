import unittest
from unittest.mock import MagicMock
import sys

# Mock frappe
sys.modules["frappe"] = MagicMock()
sys.modules["frappe.model.document"] = MagicMock()

from hrms.office.ai_assistant import get_sentiment_score

class TestAIAssistant(unittest.TestCase):
	def test_sentiment_score(self):
		self.assertGreater(get_sentiment_score("This employee is doing a great job!"), 2.5)
		self.assertLess(get_sentiment_score("The performance was poor and slow."), 2.5)
		# Empty string returns 0 as per my implementation
		self.assertEqual(get_sentiment_score(""), 0)

if __name__ == "__main__":
	unittest.main()
