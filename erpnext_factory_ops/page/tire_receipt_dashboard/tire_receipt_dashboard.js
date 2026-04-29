frappe.pages['tire-receipt-dashboard'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: __('إيصال استلام الإطارات'),
        single_column: true
    });

    // 1. إضافة الأزرار في الأعلى
    page.set_primary_action(__('حفظ الإيصال'), () => {
        frappe.msgprint(__('جاري الحفظ...'));
    }, 'octicon octicon-check');

    // 2. حقن هيكل التصميم (مستوحى من ملف الـ HTML الخاص بك)
    $(wrapper).find('.layout-main-section').html(`
        <div class="factory-dashboard" style="background-color: var(--bg-main); padding: var(--spacing-md); min-height: 80vh;">
            <div class="factory-card" style="max-width: 1000px; margin: auto; background: var(--bg-card); border-radius: var(--radius-standard); box-shadow: var(--shadow-sm); padding: var(--spacing-lg);">
                
                <div class="d-flex justify-content-between align-items-center mb-4" style="border-bottom: 2px solid var(--factory-primary-light); padding-bottom: 15px;">
                    <h3 style="color: var(--factory-primary); margin: 0;">
                        <i class="fa fa-truck"></i> توريد إطارات جديدة
                    </h3>
                    <span class="badge" style="background-color: var(--factory-primary-light); color: var(--factory-primary); padding: 8px 15px;">
                        رقم الإيصال: مؤقت
                    </span>
                </div>

                <div class="row">
                    <div class="col-md-6 mb-4">
                        <label class="text-muted font-weight-bold">المورد</label>
                        <div id="supplier-field"></div>
                    </div>
                    <div class="col-md-6 mb-4">
                        <label class="text-muted font-weight-bold">رقم لوحة الشاحنة</label>
                        <div id="plate-field"></div>
                    </div>
                </div>

                <div class="row" style="background-color: var(--bg-main); border-radius: var(--radius-standard); padding: 20px; margin: 0;">
                    <div class="col-md-4 mb-3">
                        <label class="text-muted small">نوع الإطارات</label>
                        <div id="item-field"></div>
                    </div>
                    <div class="col-md-4 mb-3">
                        <label class="text-muted small">الكمية (عدد)</label>
                        <div id="qty-field"></div>
                    </div>
                    <div class="col-md-4 mb-3">
                        <label class="text-muted small">الوزن (طن)</label>
                        <div id="weight-field"></div>
                    </div>
                </div>
            </div>
        </div>
    `);

    // 3. ربط الحقول بنماذج ERPNext الفعلية
    let field_group = new frappe.ui.FieldGroup({
        fields: [
            { fieldname: 'supplier', fieldtype: 'Link', options: 'Supplier', parent: $(wrapper).find('#supplier-field') },
            { fieldname: 'plate_no', fieldtype: 'Data', placeholder: 'مثال: أ ب ج 1234', parent: $(wrapper).find('#plate-field') },
            { fieldname: 'item', fieldtype: 'Link', options: 'Item', parent: $(wrapper).find('#item-field') },
            { fieldname: 'qty', fieldtype: 'Float', parent: $(wrapper).find('#qty-field') },
            { fieldname: 'weight', fieldtype: 'Float', parent: $(wrapper).find('#weight-field') }
        ]
    });
    field_group.make();
};
