import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# --- 1. إعدادات النظام الاحترافية ---
st.set_page_config(page_title="AutoPro ERP Ultimate", layout="wide", initial_sidebar_state="expanded")

# --- 2. المحرك البصري (Emerald Premium UI - No Side Borders) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #f8fafc; }
    
    /* إخفاء حدود القائمة الجانبية تماماً */
    [data-testid="stSidebar"] { background-color: #064e3b !important; border: none !important; }
    [data-testid="stSidebarNav"] { border: none !important; }
    section[data-testid="stSidebar"] > div { border: none !important; }
    [data-testid="stSidebar"] * { color: #ecfdf5 !important; }

    /* أزرار القائمة الجانبية بدون نقط */
    div[role="radiogroup"] { gap: 5px; padding: 10px; }
    div[role="radiogroup"] label {
        background-color: transparent; padding: 10px 15px !important;
        border-radius: 12px !important; transition: 0.3s; border: none !important;
    }
    div[role="radiogroup"] label:hover { background-color: #10b981 !important; }
    div[role="radiogroup"] label[data-selected="true"] { 
        background-color: #10b981 !important; color: white !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    div[data-testid="stSelectionControlCard"] { display: none !important; }

    /* بطاقات ERP */
    .erp-card {
        background: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border-right: 6px solid #10b981; margin-bottom: 15px; color: #064e3b;
    }
    .stButton>button { background-color: #10b981 !important; color: white !important; border-radius: 10px; font-weight: 600; border: none; height: 3em; width: 100%; }
    .stButton>button:hover { background-color: #059669 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. محرك قاعدة البيانات المتكامل (Session State Engine) ---
if 'erp' not in st.session_state:
    st.session_state.erp = {
        'coa': { # دليل الحسابات
            'الأصول': {'الخزينة': 150000.0, 'المخزن': 45000.0, 'المدينون': 0.0},
            'الخصوم': {'الدائنون': 0.0, 'VAT_Payable': 0.0},
            'الملكية': {'رأس المال': 195000.0},
            'الإيرادات': {'المبيعات': 0.0},
            'المصروفات': {'تكلفة_بضاعة': 0.0, 'رواتب': 0.0, 'مصاريف_عامة': 0.0}
        },
        'inventory': pd.DataFrame([
            {"ID": 1, "الماركة": "تويوتا", "الموديل": "كورولا", "الصنف": "تيل فرامل", "النوع": "قطع غيار", "الرف": "A1", "الكمية": 20, "التكلفة": 400.0, "البيع": 650.0},
            {"ID": 2, "الماركة": "عالمي", "الموديل": "إكسسوار", "الصنف": "معطر سيارة", "النوع": "إكسسوارات", "الرف": "B5", "الكمية": 100, "التكلفة": 20.0, "البيع": 50.0}
        ]),
        'customers': pd.DataFrame([{"ID": 1, "الاسم": "عميل نقدي", "الموبايل": "000", "الرصيد": 0.0}]),
        'suppliers': pd.DataFrame([{"ID": 1, "الاسم": "مورد قطع غيار", "الموبايل": "010", "المديونية": 0.0}]),
        'employees': pd.DataFrame([{"ID": 1, "الاسم": "محمد حسن", "الوظيفة": "كاشير", "الراتب": 6000.0}]),
        'attendance': [],
        'ledger': [],
        'sales_log': [],
        'cost_centers': ["المحل الرئيسي", "المخزن"]
    }

# --- 4. المحرك المحاسبي والـ AI ---
def post_transaction(desc, dr_acc, cr_acc, amount, center="General"):
    st.session_state.erp['ledger'].append({
        "Date": date.today(), "Description": desc, "Debit": dr_acc, "Credit": cr_acc, "Amount": amount, "Center": center
    })
    # تحديث دليل الحسابات
    for cat in st.session_state.erp['coa']:
        if dr_acc in st.session_state.erp['coa'][cat]: st.session_state.erp['coa'][cat][dr_acc] += amount
        if cr_acc in st.session_state.erp['coa'][cat]: st.session_state.erp['coa'][cat][cr_acc] -= amount

def ask_ai(query):
    query = query.lower()
    inv = st.session_state.erp['inventory']
    if "مخزن" in query:
        return f"المخزن به {len(inv)} أصناف. الأصناف المنخفضة هي: {inv[inv['الكمية'] < 10]['الصنف'].tolist()}"
    if "فلوس" in query or "خزينة" in query:
        return f"رصيد الخزينة الحالي هو {st.session_state.erp['coa']['الأصول']['الخزينة']:,.2f} ج.م"
    return "أنا مساعد AutoPro AI، كيف أساعدك في إدارة ERP اليوم؟"

# --- 5. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>AutoPro ERP</h2>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("", [
        "📊 لوحة القيادة", "🛒 المبيعات و POS", "📦 إدارة المخازن", "🧾 إدارة المشتريات",
        "🤝 العملاء والموردين", "👔 الموارد البشرية", "⏰ الحضور والانصراف", "💸 الرواتب",
        "📉 إدارة المصروفات", "⚖️ المحاسبة والمالية", "📈 القوائم الختامية", "🤖 مساعد AI"
    ])

# --- 6. تنفيذ الموديولات ---

# 1. لوحة القيادة
if menu == "📊 لوحة القيادة":
    st.title("لوحة القيادة الاستراتيجية")
    coa = st.session_state.erp['coa']
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f"<div class='erp-card'><h5>نقدية الخزينة</h5><h2>{coa['الأصول']['الخزينة']:,.0f}</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='erp-card'><h5>قيمة المخزن</h5><h2>{coa['الأصول']['المخزن']:,.0f}</h2></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='erp-card'><h5>إجمالي المبيعات</h5><h2>{coa['الإيرادات']['المبيعات']:,.0f}</h2></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='erp-card'><h5>صافي الربح</h5><h2>{coa['الإيرادات']['المبيعات'] - coa['المصروفات']['تكلفة_بضاعة']:,.0f}</h2></div>", unsafe_allow_html=True)
    
    if st.session_state.erp['sales_log']:
        st.plotly_chart(px.area(pd.DataFrame(st.session_state.erp['sales_log']), x='Date', y='Total', title="منحنى نمو المبيعات"), use_container_width=True)

# 2. المبيعات و POS
elif menu == "🛒 المبيعات و POS":
    st.title("نقطة بيع متوافقة مع الضرائب")
    col1, col2 = st.columns([2, 1])
    inv = st.session_state.erp['inventory']
    with col1:
        search = st.text_input("🔍 ابحث عن قطعة غيار أو ماركة...")
        filtered = inv[inv['الصنف'].str.contains(search) | inv['الماركة'].str.contains(search)]
        st.dataframe(filtered, use_container_width=True, hide_index=True)
        sel_p = st.selectbox("اختر الصنف", filtered['الصنف'])
        qty = st.number_input("الكمية", min_value=1)
        cust = st.selectbox("اختر العميل", st.session_state.erp['customers']['الاسم'])
    with col2:
        prod = inv[inv['الصنف'] == sel_p].iloc[0]
        total = prod['البيع'] * qty
        tax = total * 0.14
        st.markdown(f"<div class='erp-card'><h5>الإجمالي شامل الضريبة (14%)</h5><h2>{total + tax:,.2f}</h2></div>", unsafe_allow_html=True)
        if st.button("تأكيد البيع وترحيل الحسابات"):
            if prod['الكمية'] >= qty:
                # ترحيل المحاسبة
                post_transaction(f"بيع {sel_p}", "الخزينة", "المبيعات", total + tax)
                post_transaction("ضريبة VAT مبيعات", "المبيعات", "VAT_Payable", tax)
                post_transaction(f"تكلفة مبيعات {sel_p}", "تكلفة_بضاعة", "المخزن", prod['التكلفة'] * qty)
                # تحديث المخزن
                st.session_state.erp['inventory'].loc[inv['الصنف'] == sel_p, 'الكمية'] -= qty
                st.session_state.erp['sales_log'].append({"Date": date.today(), "Total": total + tax})
                st.success("تم إتمام البيع و ترحيل 3 قيود محاسبية!")
                st.rerun()
            else: st.error("المخزن لا يكفي!")

# 3. إدارة المخازن
elif menu == "📦 إدارة المخازن":
    st.title("إدارة المخازن والسيارات")
    st.dataframe(st.session_state.erp['inventory'], use_container_width=True)
    with st.expander("➕ إضافة صنف جديد"):
        with st.form("add_inv"):
            c1, c2, c3 = st.columns(3)
            make = c1.selectbox("الماركة", ["تويوتا", "هيونداي", "كيا", "إكسسوار عام"])
            name = c2.text_input("اسم القطعة")
            qty_init = c3.number_input("الكمية")
            cost_i = c1.number_input("التكلفة")
            sale_i = c2.number_input("البيع")
            loc_i = c3.text_input("الرف")
            if st.form_submit_button("حفظ"):
                new_item = {"ID": len(st.session_state.erp['inventory'])+1, "الماركة": make, "الموديل": "عام", "الصنف": name, "النوع": "قطع غيار", "الرف": loc_i, "الكمية": qty_init, "التكلفة": cost_i, "البيع": sale_i}
                st.session_state.erp['inventory'] = pd.concat([st.session_state.erp['inventory'], pd.DataFrame([new_item])], ignore_index=True)
                post_transaction(f"إضافة مخزن: {name}", "المخزن", "رأس المال", cost_i * qty_init)
                st.rerun()

# 4. المشتريات
elif menu == "🧾 إدارة المشتريات":
    st.title("توليد أوامر الشراء")
    with st.form("pur_form"):
        sup = st.selectbox("المورد", st.session_state.erp['suppliers']['الاسم'])
        item = st.selectbox("الصنف", st.session_state.erp['inventory']['الصنف'])
        q_p = st.number_input("الكمية الموردة", min_value=1)
        c_p = st.number_input("سعر التكلفة")
        if st.form_submit_button("تأكيد الشراء والتوريد"):
            st.session_state.erp['inventory'].loc[st.session_state.erp['inventory']['الصنف'] == item, 'الكمية'] += q_p
            post_transaction(f"شراء من {sup}", "المخزن", "الخزينة", q_p * c_p)
            st.success("تم التوريد و خصم الخزينة!")

# 5. العملاء والموردين
elif menu == "🤝 العملاء والموردين":
    st.title("إدارة الشركاء")
    tab1, tab2 = st.tabs(["العملاء", "الموردين"])
    with tab1:
        st.dataframe(st.session_state.erp['customers'], use_container_width=True)
        with st.form("add_cust"):
            n = st.text_input("اسم العميل")
            p = st.text_input("الموبايل")
            if st.form_submit_button("إضافة"):
                st.session_state.erp['customers'] = pd.concat([st.session_state.erp['customers'], pd.DataFrame([{"ID": 2, "الاسم": n, "الموبايل": p, "الرصيد": 0.0}])], ignore_index=True)
                st.rerun()
    with tab2:
        st.dataframe(st.session_state.erp['suppliers'], use_container_width=True)

# 6. الموارد البشرية والحضور
elif menu == "👔 الموارد البشرية":
    st.title("إدارة الموظفين")
    st.dataframe(st.session_state.erp['employees'], use_container_width=True)
    with st.form("hr_form"):
        n = st.text_input("اسم الموظف")
        j = st.text_input("الوظيفة")
        s = st.number_input("الراتب")
        if st.form_submit_button("إضافة موظف"):
            st.session_state.erp['employees'] = pd.concat([st.session_state.erp['employees'], pd.DataFrame([{"ID": 3, "الاسم": n, "الوظيفة": j, "الراتب": s}])], ignore_index=True)
            st.rerun()

elif menu == "⏰ الحضور والانصراف":
    st.title("نظام الحضور")
    emp = st.selectbox("الموظف", st.session_state.erp['employees']['الاسم'])
    type_a = st.radio("العملية", ["حضور", "انصراف"])
    if st.button("تسجيل"):
        st.session_state.erp['attendance'].append({"Date": date.today(), "Name": emp, "Time": datetime.now().strftime("%I:%M %p"), "Type": type_a})
        st.success(f"تم تسجيل {type_a} لـ {emp}")
    st.table(pd.DataFrame(st.session_state.erp['attendance']).tail(10))

elif menu == "💸 الرواتب":
    st.title("مسيرات الرواتب")
    total_sal = st.session_state.erp['employees']['الراتب'].sum()
    st.metric("إجمالي مسير الرواتب", f"{total_sal:,.2f} ج.م")
    if st.button("اعتماد و صرف الرواتب"):
        post_transaction("صرف رواتب", "رواتب", "الخزينة", total_sal)
        st.success("تم الخصم من الخزينة وتسجيل المصروف")

# 7. المحاسبة المالية (القيود، دليل الحسابات، ميزان المراجعة)
elif menu == "⚖️ المحاسبة والمالية":
    st.title("المحاسبة المركزية")
    t1, t2, t3, t4 = st.tabs(["دليل الحسابات", "دفتر اليومية", "ميزان المراجعة", "مراكز التكلفة"])
    with t1: st.write(st.session_state.erp['coa'])
    with t2: st.table(pd.DataFrame(st.session_state.erp['ledger']))
    with t3:
        rows = []
        for cat, subs in st.session_state.erp['coa'].items():
            for acc, val in subs.items(): rows.append({"الحساب": acc, "مدين": val if val > 0 else 0, "دائن": abs(val) if val < 0 else 0})
        st.table(pd.DataFrame(rows))
    with t4:
        st.write("المصروفات حسب مراكز التكلفة")
        st.info("المركز الرئيسي: 100% من العمليات")

# 8. التقارير والضرائب
elif menu == "📈 القوائم الختامية":
    st.title("التقارير الختامية والضرائب")
    coa = st.session_state.erp['coa']
    rev = coa['الإيرادات']['المبيعات']
    cogs = coa['المصروفات']['تكلفة_بضاعة']
    sal = coa['المصروفات']['رواتب']
    st.metric("صافي الربح", f"{rev - cogs - sal:,.2f} ج.م")
    st.divider()
    st.write("### تقرير ضريبة القيمة المضافة (VAT)")
    st.warning(f"الضريبة المستحقة للسداد: {abs(coa['الخصوم']['VAT_Payable']):,.2f} ج.م")

# 9. مساعد AI
elif menu == "🤖 مساعد AI":
    st.title("AutoPro AI Assistant")
    q = st.chat_input("اسألني عن المخزن، المبيعات أو الرواتب...")
    if q:
        with st.chat_message("user"): st.write(q)
        with st.chat_message("assistant"): st.write(ask_ai(q))

# 10. المصروفات
elif menu == "📉 إدارة المصروفات":
    st.title("تسجيل المصروفات")
    with st.form("exp"):
        desc = st.text_input("البيان")
        amt = st.number_input("المبلغ")
        if st.form_submit_button("تسجيل"):
            post_transaction(desc, "مصاريف_عامة", "الخزينة", amt)
            st.success("تم الحفظ")
