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
