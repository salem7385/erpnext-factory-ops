import frappe
from frappe import _
from frappe.model.document import Document


class TireReceipt(Document):
    def validate(self):
        self.validate_weights()
        self.calculate_net_weight()

    def validate_weights(self):
        gross = float(self.gross_weight or 0)
        tare = float(self.tare_weight or 0)

        if gross < 0 or tare < 0:
            frappe.throw(_("الوزن الإجمالي ووزن الفارغ لا يمكن أن يكونا أقل من صفر."))

        if gross and tare and gross < tare:
            frappe.throw(_("الوزن الإجمالي (Gross Weight) يجب أن يكون أكبر من أو يساوي وزن الفارغ (Tare Weight)."))

    def calculate_net_weight(self):
        if self.gross_weight is not None and self.tare_weight is not None:
            self.net_weight = float(self.gross_weight or 0) - float(self.tare_weight or 0)
