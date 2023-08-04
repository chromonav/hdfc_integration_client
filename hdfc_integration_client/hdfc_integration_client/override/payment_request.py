import frappe
from erpnext.accounts.doctype.payment_request.payment_request import PaymentRequest

# from erpnext.accounts.doctype.tax_withholding_category.tax_withholding_category import get_party_tax_withholding_details
# from erpnext import get_default_company


class CustomPaymentRequest(PaymentRequest):
	def validate(self):
		if not self.is_adhoc:
			super().validate()
		else:
			if self.get("__islocal"):
				self.status = "Draft"
			if self.reference_doctype or self.reference_name:
				frappe.throw("Payments with references cannot be marked as ad-hoc")

		# if self.apply_tax_withholding_amount and self.tax_withholding_category:
		# 	if not self.net_total:
		# 		self.net_total = self.grand_total
		# 	tds_amount = self.calculate_pr_tds(self.net_total)
		# 	self.taxes_deducted = tds_amount
		# 	self.grand_total = self.net_total - self.taxes_deducted
		# else:
		# 	self.grand_total = self.net_total

	def on_submit(self):
		if not self.is_adhoc:
			super().on_submit()
		else:
			if self.payment_request_type == "Outward":
				self.db_set("status", "Initiated")
				return

	def create_payment_entry(self, submit=True):
		payment_entry = super().create_payment_entry(submit=submit)
		if payment_entry.docstatus != 1 and self.payment_type:
			payment_entry.paid_to = frappe.db.get_value("Payment Type", self.payment_type, "account") or ""
		return payment_entry
	
	# def calculate_pr_tds(self, amount):
	# 	doc = self
	# 	doc.supplier = self.party 
	# 	doc.company = get_default_company()
	# 	doc.tax_withholding_net_total = amount
	# 	doc.taxes = []
	# 	taxes = get_party_tax_withholding_details(doc, self.tax_withholding_category)
	# 	if taxes:
	# 		return taxes["tax_amount"]
	# 	else:
	# 		return 0