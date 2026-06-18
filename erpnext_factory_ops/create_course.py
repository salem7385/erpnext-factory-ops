import frappe

def run():
    # 1. إنشاء مدرس جديد أولاً ليتم حفظه في النظام
    instructor = frappe.get_doc({
        "doctype": "Course Instructor",
        "instructor_name": "مدرب المصنع الرئيسي"
    })
    instructor.insert(ignore_permissions=True)
    frappe.db.commit() # تأكيد الحفظ ليصبح له ID

    # 2. إنشاء الكورس وربطه بالمدرس الذي أنشأناه للتو
    course = frappe.get_doc({
        "doctype": "LMS Course",
        "title": "erpnext-factory-ops-training",
        "course_name": "إدارة إنتاج مصنع تدوير الإطارات",
        "short_introduction": "دورة تدريبية متكاملة لمهندسي وعمال المصنع.",
        "description": "دورة تدريبية متكاملة لمهندسي وعمال المصنع.",
        "published": 1,
        "instructors": [{
            "instructor": instructor.name # الربط بالاسم البرمجي الذي تولد قبل ثانية
        }]
    })
    course.insert(ignore_permissions=True)

    # 3. إنشاء الفصل
    chapter = frappe.get_doc({
        "doctype": "Course Chapter", 
        "title": "مقدمة عن خطوط إعادة التدوير",
        "course": course.name
    })
    chapter.insert(ignore_permissions=True)

    # 4. إنشاء الدرس
    lesson = frappe.get_doc({
        "doctype": "Course Lesson",
        "title": "مقدمة في فرز الإطارات",
        "chapter": chapter.name,
        "course": course.name,
        "body": "محتوى الدرس: مراحل فرز الإطارات الأولية.",
        "published": 1
    })
    lesson.insert(ignore_permissions=True)

    frappe.db.commit()
    print(f"🎉 تم إنشاء الكورس بنجاح برقم: {course.name}")
