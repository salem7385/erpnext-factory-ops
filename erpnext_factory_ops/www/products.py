import frappe

def get_context(context):
    # جلب المنتجات التي تم تعليمها "Show in Website"
    context.items = frappe.get_all("Item", 
        filters={"show_in_website": 1, "disabled": 0},
        fields=["name", "item_name", "website_image", "standard_rate", "item_group", "description"]
    )
    context.title = "منتجات المصنع"
