import frappe

# جلب كافة حسابات شركة Ti-BGPS
accounts = frappe.get_all("Account", filters={"company": "Ti-BGPS"}, fields=["name", "account_name", "account_number"])

print(f"جاري معالجة {len(accounts)} حساب...")

for acc in accounts:
    # 1. استخراج الرقم الحالي (سواء من حقل الرقم أو من بداية الاسم)
    current_num = acc.account_number or "".join(filter(str.isdigit, acc.name.split(" - ")[0]))
    
    if current_num:
        # 2. تطبيق قاعدتك: إكمال الأصفار حتى يصل الطول إلى 10
        # دالة ljust(10, '0') تأخذ الرقم وتضيف أصفاراً عن يمينه حتى يكتمل العدد 10
        new_number = current_num.ljust(10, '0')
        
        # 3. بناء الاسم الجديد
        new_name = f"{new_number} - {acc.account_name} - Ti-BGPS"
        
        # 4. التحديث في قاعدة البيانات
        # تحديث الحساب نفسه
        frappe.db.sql("""
            UPDATE `tabAccount` 
            SET name = %s, account_number = %s 
            WHERE name = %s
        """, (new_name, new_number, acc.name))
        
        # تحديث مرجع الأب للأبناء
        frappe.db.sql("""
            UPDATE `tabAccount` 
            SET parent_account = %s 
            WHERE parent_account = %s
        """, (new_name, acc.name))

frappe.db.commit()
print("تمت عملية إكمال الأصفار بنجاح لجميع الحسابات (10 أرقام).")

# قائمة الحسابات التفصيلية للنقدية
cash_hierarchy = [
    {
        "num": "1101000000", 
        "name": "نقدية بالصندوق", 
        "parent": "1100000000 - أصول متداولة - Ti-BGPS",
        "is_group": 1
    },
    {
        "num": "1101010000", 
        "name": "النقدية", 
        "parent": "1101000000 - نقدية بالصندوق - Ti-BGPS",
        "is_group": 1
    },
    {
        "num": "1101010001", 
        "name": "صندوق المصنع - المركز الرئيسي", 
        "parent": "1101010000 - النقدية - Ti-BGPS",
        "is_group": 0 # هذا حساب المعاملات النهائي
    }
]

for item in cash_hierarchy:
    full_name = f"{item['num']} - {item['name']} - Ti-BGPS"
    
    # التأكد من عدم وجود الحساب قبل الإضافة
    if not frappe.db.exists("Account", full_name):
        acc = frappe.new_doc("Account")
        acc.account_name = item['name']
        acc.account_number = item['num']
        acc.parent_account = item['parent']
        acc.company = "Ti-BGPS"
        acc.is_group = item['is_group']
        acc.account_type = "Cash" # تحديد النوع للتعامل مع السندات
        acc.insert()
        print(f"تمت إضافة: {full_name}")
    else:
        print(f"الحساب موجود مسبقاً: {full_name}")

frappe.db.commit()
