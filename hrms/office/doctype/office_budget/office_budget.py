import frappe
from frappe.model.document import Document

class OfficeBudget(Document):
	def validate(self):
		self.remaining_amount = self.total_limit - self.spent_amount
