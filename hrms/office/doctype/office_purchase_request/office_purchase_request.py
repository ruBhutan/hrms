import frappe
from frappe.model.document import Document

class OfficePurchaseRequest(Document):
	def on_update(self):
		if self.status == "Received" and self.get_doc_before_save() and self.get_doc_before_save().status != "Received":
			self.update_stock()

	def update_stock(self):
		supply = frappe.get_doc("Office Supply", self.item)
		supply.current_stock += self.quantity
		supply.save()

		# Also update budget if applicable
		self.update_budget()

	def update_budget(self):
		# Simple logic: find a budget for the department and fiscal year
		# For demo purposes, we'll just find the first budget
		budgets = frappe.get_all("Office Budget", filters={"department": frappe.db.get_value("Employee", self.requested_by, "department")}, limit=1)
		if budgets:
			budget = frappe.get_doc("Office Budget", budgets[0].name)
			# We'll assume a fixed cost for now or add a cost field to OPR
			# Let's just mock the spent_amount update
			pass
