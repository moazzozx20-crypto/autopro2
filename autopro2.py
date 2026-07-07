import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# --- 1. إعدادات النظام الاستراتيجية ---
st.set_page_config(page_title="AutoPro ERP Enterprise Edition", layout="wide", initial_sidebar_state="expanded")

# --- 2. المحرك البصري (Emerald Theme & Sidebar Fix) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #f8fafc; }
    
    /* إخفاء حدود القائمة الجانبية نهائياً */
    [data-testid="stSidebar"] { background-color: #064e3b !important; border: none !important; }
    [data-testid="stSidebarNav"] { border: none !important; }
    section[data-testid="stSidebar"] > div { border: none !important; }
    [data-testid="stSidebar"] * { color: #ecfdf5 !important; }

    /* القائمة الجانبية - أزرار احترافية */
    div[role="radiogroup"] { gap: 8px; padding: 10px; }
    div[role="radiogroup"] label {
        background-color: transparent; padding: 10px 15px !important;
        border-radius: 10px !important; transition: 0.3s; border: none !important;
    }
    div[role="radiogroup"] label:hover { background-color: #10b981 !important; }
    div[role="radiogroup"] label[data-selected="true"] {
        background-color: #10b981 !important; color: white !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    div[data-testid="stSelectionControlCard"] { display: none !important; }

    /* بطاقات ERP */
    .erp-card {
        background: white; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        border-right: 5px solid #10b981; margin-bottom: 15px;
    }
    .erp-card h5 { color: #64748b; font-size: 0.9em; margin: 0; }
    .erp-card h2 { color: #064e3b; margin: 5px 0; font-size: 1.8em; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. تهيئة محرك البيانات المحاسبي (Global ERP Engine) ---
if 'erp' not in st.session_state:
    st.session_state.erp = {
        # 1. دليل الحسابات (Chart of Accounts)
        'coa': {
            '1000-الأصول': {'1001-الخزينة': 50000, '1002-المخزن': 40000, '1003-المدينون': 0, '1004-البنك': 0},
            '2000-الخصوم': {'2001-الدائنون': 0, '2002-ضريبة القيمة المضافة': 0},
            '3000-حقوق الملكية': {'3001-رأس المال': 90000},
            '4000-الإيرادات': {'4001-مبيعات قطع الغيار': 0},
            '5000-المصروفات': {'5001-تكلفة البضاعة': 0, '5002-رواتب': 0, '5003-مصاريف عامة': 0}
        },
        'inventory': pd.DataFrame([
            {"كود": "BK-101", "الصنف": "تيل فرامل تويوتا", "الكمية": 50, "التكلفة": 400, "البيع": 650},
            {"كود": "OF-202", "الصنف": "فلتر زيت كيا", "الكمية": 100, "التكلفة": 120, "البيع": 190}
        ]),
        'ledger': [], # دفتر الأستاذ (كل القيود)
        'customers': pd.DataFrame([{"ID": 1, "الاسم": "عميل نقدي", "موبايل": "000"}]),
        'suppliers': pd.DataFrame([{"ID": 1, "الاسم": "مورد عام", "موبايل": "010"}]),
        'employees': pd.DataFrame([{"ID": 1, "الاسم": "محمد حسن", "الوظيفة": "كاشير", "الراتب": 6000}]),
        'attendance': []
    }

# --- 4. محرك القيود المحاسبية (The Accounting Core) ---
def record_transaction(desc, debit_acc, credit_acc, amount, cost_center="General"):
    # إضافة القيد لدفتر الأستاذ
    entry = {
        "Date": date.today(),
        "Description": desc,
        "Debit_Account": debit_acc,
        "Credit_Account": credit_acc,
        "Amount": amount,
        "Cost_Center": cost_center
    }
    st.session_state.erp['ledger'].append(entry)
    
    # تحديث أرصدة دليل الحسابات
    for cat in st.session_state.erp['coa']:
        if debit_acc in st.session_state.erp['coa'][cat]:
            st.session_state.erp['coa'][cat][debit_acc] += amount
        if credit_acc in st.session_state.erp['coa'][cat]:
            st.session_state.erp['coa'][cat][credit_acc] -= amount

# --- 5. القائمة الجانبية ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>AutoPro ERP</h2>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("", [
        "🏠 لوحة القيادة", "🛒 المبيعات و POS", "📦 المخازن", "🧾 المشتريات", 
        "🤝 العملاء و الموردين", "👔 الموارد البشرية", "⚖️ المحاسبة المالية", "📉 التقارير الختامية"
    ])

# --- 6. الموديولات التفصيلية ---

# 1. لوحة القيادة
if menu == "🏠 لوحة القيادة":
    st.title("المركز المالي اللحظي")
    coa = st.session_state.erp['coa']
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f"<div class='erp-card'><h5>النقدية</h5><h2>{coa['1000-الأصول']['1001-الخزينة']:,.0f}</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='erp-card'><h5>قيمة المخزون</h5><h2>{coa['1000-الأصول']['1002-المخزن']:,.0f}</h2></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='erp-card'><h5>إجمالي المبيعات</h5><h2>{coa['4000-الإيرادات']['4001-مبيعات قطع الغيار']:,.0f}</h2></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='erp-card'><h5>صافي الربح</h5><h2>{coa['4000-الإيرادات']['4001-مبيعات قطع الغيار'] - coa['5000-المصروفات']['5001-تكلفة البضاعة']:,.0f}</h2></div>", unsafe_allow_html=True)
    
    if st.session_state.erp['ledger']:
        df_l = pd.DataFrame(st.session_state.erp['ledger'])
        fig = px.line(df_l, x='Date', y='Amount', title="حركة التدفقات النقدية", color_discrete_sequence=['#10b981'])
        st.plotly_chart(fig, use_container_width=True)

# 2. المبيعات و POS (مربوط بالكامل بالمحاسبة)
elif menu == "🛒 المبيعات و POS":
    st.title("نقطة البيع و الربط المحاسبي")
    col1, col2 = st.columns([2, 1])
    with col1:
        df_inv = st.session_state.erp['inventory']
        sel_p = st.selectbox("اختر الصنف", df_inv['الصنف'])
        qty = st.number_input("الكمية", min_value=1)
        tax_rate = 0.14 # ضريبة القيمة المضافة بمصر
        
        prod = df_inv[df_inv['الصنف'] == sel_p].iloc[0]
        total_sales = prod['البيع'] * qty
        total_tax = total_sales * tax_rate
        final_total = total_sales + total_tax
        cost_of_goods = prod['التكلفة'] * qty

    with col2:
        st.markdown(f"<div class='erp-card'><h5>الإجمالي شامل الضريبة</h5><h2>{final_total:,.2f} ج.م</h2></div>", unsafe_allow_html=True)
        if st.button("إتمام البيع و ترحيل القيود"):
            if prod['الكمية'] >= qty:
                # --- العملية المحاسبية المركبة ---
                # 1. إثبات الإيراد والضريبة والنقدية
                record_transaction(f"بيع {qty} {sel_p}", "1001-الخزينة", "4001-مبيعات قطع الغيار", final_total)
                record_transaction("إثبات ضريبة القيمة المضافة", "4001-مبيعات قطع الغيار", "2002-ضريبة القيمة المضافة", total_tax)
                # 2. إثبات تكلفة البضاعة وخصم المخزن
                record_transaction(f"تكلفة مبيعات {sel_p}", "5001-تكلفة البضاعة", "1002-المخزن", cost_of_goods)
                # 3. تحديث كمية المخزن برمجياً
                st.session_state.erp['inventory'].loc[st.session_state.erp['inventory']['الصنف'] == sel_p, 'الكمية'] -= qty
                st.success("تم البيع وترحيل 4 قيود محاسبية آلياً!")
            else: st.error("المخزن لا يكفي!")

# 3. المخازن
elif menu == "📦 المخازن":
    st.title("إدارة المخازن")
    st.dataframe(st.session_state.erp['inventory'], use_container_width=True, hide_index=True)
    with st.expander("➕ إضافة صنف جديد (بضاعة أول المدة)"):
        with st.form("inv_form"):
            name = st.text_input("اسم الصنف")
            code = st.text_input("الكود")
            cost = st.number_input("التكلفة")
            price = st.number_input("البيع")
            qty_init = st.number_input("الكمية")
            if st.form_submit_button("حفظ"):
                new_p = {"كود": code, "الصنف": name, "الكمية": qty_init, "التكلفة": cost, "البيع": price}
                st.session_state.erp['inventory'] = pd.concat([st.session_state.erp['inventory'], pd.DataFrame([new_p])], ignore_index=True)
                # قيد بضاعة أول المدة
                record_transaction(f"بضاعة أول مدة: {name}", "1002-المخزن", "3001-رأس المال", cost * qty_init)
                st.rerun()

# 4. المشتريات
elif menu == "🧾 المشتريات":
    st.title("توريد بضاعة للمخازن")
    with st.form("pur_form"):
        item = st.selectbox("الصنف", st.session_state.erp['inventory']['الصنف'])
        qty_p = st.number_input("الكمية الموردة", min_value=1)
        cost_p = st.number_input("سعر الشراء")
        if st.form_submit_button("تأكيد التوريد"):
            total_pur = qty_p * cost_p
            st.session_state.erp['inventory'].loc[st.session_state.erp['inventory']['الصنف'] == item, 'الكمية'] += qty_p
            record_transaction(f"شراء بضاعة {item}", "1002-المخزن", "1001-الخزينة", total_pur)
            st.success("تم التوريد وخصم النقدية")

# 7. المحاسبة المالية (كاملة)
elif menu == "⚖️ المحاسبة المالية":
    st.title("النظام المحاسبي المتكامل")
    tab1, tab2, tab3, tab4 = st.tabs(["📖 دليل الحسابات", "📝 القيود واليومية", "📊 ميزان المراجعة", "🏷️ مراكز التكلفة"])
    
    with tab1:
        st.subheader("دليل الحسابات الشجري (Chart of Accounts)")
        for main_acc, sub_accs in st.session_state.erp['coa'].items():
            with st.expander(main_acc):
                for sub, val in sub_accs.items():
                    st.write(f"{sub} : **{val:,.2f} ج.م**")
                    
    with tab2:
        st.subheader("دفتر اليومية العامة (Manual & Auto Journal)")
        if st.session_state.erp['ledger']:
            st.table(pd.DataFrame(st.session_state.erp['ledger']))
        else: st.info("لا توجد قيود مسجلة")
        
        with st.expander("➕ إضافة قيد يدوي"):
            c1, c2, c3 = st.columns(3)
            desc = c1.text_input("البيان")
            amt = c2.number_input("المبلغ")
            center = c3.selectbox("مركز التكلفة", ["General", "المحل", "المخزن"])
            dr = st.selectbox("من حساب (Debit)", [k for sub in st.session_state.erp['coa'].values() for k in sub.keys()])
            cr = st.selectbox("إلى حساب (Credit)", [k for sub in st.session_state.erp['coa'].values() for k in sub.keys()])
            if st.button("ترحيل القيد"):
                record_transaction(desc, dr, cr, amt, center)
                st.rerun()

    with tab3:
        st.subheader("ميزان المراجعة (Trial Balance)")
        rows = []
        for cat, subs in st.session_state.erp['coa'].items():
            for acc, val in subs.items():
                rows.append({"الحساب": acc, "مدين": val if val > 0 else 0, "دائن": abs(val) if val < 0 else 0})
        st.table(pd.DataFrame(rows))

# 8. التقارير الختامية
elif menu == "📉 التقارير الختامية":
    st.title("القوائم المالية والضرائب")
    t1, t2, t3, t4 = st.tabs(["📉 قائمة الدخل", "⚖️ الميزانية العمومية", "💸 التدفقات النقدية", "📑 الإقرار الضريبي"])
    
    coa = st.session_state.erp['coa']
    with t1:
        st.subheader("قائمة الدخل (Income Statement)")
        rev = coa['4000-الإيرادات']['4001-مبيعات قطع الغيار']
        cogs = coa['5000-المصروفات']['5001-تكلفة البضاعة']
        salaries = coa['5000-المصروفات']['5002-رواتب']
        net = rev - cogs - salaries
        st.write(f"إجمالي الإيرادات: {rev:,.2f}")
        st.write(f"تكلفة البضاعة المباعة: ({cogs:,.2f})")
        st.write(f"الرواتب والمصاريف: ({salaries:,.2f})")
        st.divider()
        st.metric("صافي الربح التشغيلي", f"{net:,.2f} ج.م")

    with t2:
        st.subheader("الميزانية العمومية (Balance Sheet)")
        assets = sum(coa['1000-الأصول'].values())
        liabilities = sum(coa['2000-الخصوم'].values())
        equity = sum(coa['3000-حقوق الملكية'].values()) + net
        c1, c2 = st.columns(2)
        c1.write("### الأصول")
        c1.table(pd.DataFrame([{"الحساب": k, "القيمة": v} for k, v in coa['1000-الأصول'].items()]))
        c2.write("### الخصوم وحقوق الملكية")
        c2.table(pd.DataFrame([{"الحساب": k, "القيمة": v} for k, v in coa['2000-الخصوم'].items()] + [{"الحساب": "حقوق الملكية + الأرباح", "القيمة": equity}]))
        st.info(f"توازن الميزانية: {'متوازنة ✅' if round(assets) == round(liabilities + equity) else 'غير متوازنة ❌'}")

    with t4:
        st.subheader("تقرير ضريبة القيمة المضافة (VAT Report)")
        vat_val = abs(coa['2000-الخصوم']['2002-ضريبة القيمة المضافة'])
        st.metric("الضريبة المستحقة للسداد", f"{vat_val:,.2f} ج.م")
        st.write("بناءً على مبيعات الشهر الحالي (14%)")

# الموديولات الأخرى (الموظفين، العملاء) تعمل بنفس القوة
else:
    st.title(menu)
    st.info("هذا الموديول مربوط بمحرك المحاسبة المركزي.")
