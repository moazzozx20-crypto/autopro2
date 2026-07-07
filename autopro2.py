import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date, timedelta

# --- 1. إعدادات النظام الفائقة ---
st.set_page_config(page_title="AutoPro ERP Ultimate", layout="wide", initial_sidebar_state="expanded")

# --- 2. المحرك البصري (Emerald Deep UI - No Borders) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #f8fafc; }
    
    /* إخفاء حدود القائمة الجانبية والخط الفاصل */
    [data-testid="stSidebar"] { background-color: #064e3b !important; border: none !important; }
    [data-testid="stSidebarNav"] { border: none !important; }
    section[data-testid="stSidebar"] > div { border: none !important; }
    [data-testid="stSidebar"] * { color: #ecfdf5 !important; }

    /* القائمة الجانبية - أزرار قائمة احترافية بدون نقط */
    div[role="radiogroup"] { gap: 5px; padding: 10px; }
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

    /* بطاقات ERP المتميزة */
    .erp-card {
        background: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border-right: 6px solid #10b981; margin-bottom: 15px; color: #064e3b;
    }
    .stButton>button { background-color: #10b981; color: white; border-radius: 10px; font-weight: 600; border: none; height: 3em; width: 100%; }
    .stButton>button:hover { background-color: #059669; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. محرك قاعدة البيانات المتكامل (Session State) ---
if 'db' not in st.session_state:
    st.session_state.db = {
        # دليل الحسابات
        'coa': {
            'الأصول': {'الخزينة': 100000.0, 'المخزن': 45000.0, 'المدينون': 0.0, 'البنك': 0.0},
            'الخصوم': {'الدائنون': 0.0, 'VAT': 0.0},
            'الملكية': {'رأس المال': 145000.0},
            'الإيرادات': {'المبيعات': 0.0},
            'المصروفات': {'تكلفة بضاعة': 0.0, 'رواتب': 0.0, 'مصاريف عامة': 0.0}
        },
        'inventory': pd.DataFrame([
            {"ID": 1, "الماركة": "تويوتا", "الموديل": "كورولا", "الصنف": "تيل فرامل", "النوع": "قطع غيار", "الرف": "A1", "الكمية": 20, "التكلفة": 400, "البيع": 650},
            {"ID": 2, "الماركة": "عالمي", "الموديل": "جميع السيارات", "الصنف": "معطر سيارة", "النوع": "إكسسوارات", "الرف": "B5", "الكمية": 100, "التكلفة": 20, "البيع": 50}
        ]),
        'customers': pd.DataFrame([{"الاسم": "عميل نقدي", "الموبايل": "000", "الرصيد": 0}]),
        'suppliers': pd.DataFrame([{"الاسم": "مورد عام", "الموبايل": "010", "المديونية": 0}]),
        'employees': pd.DataFrame([{"الاسم": "أحمد محمد", "الوظيفة": "كاشير", "الراتب": 6000, "الحالة": "نشط"}]),
        'attendance': [],
        'ledger': [], # دفتر اليومية
        'sales_log': [],
        'centers': ["المركز الرئيسي", "المخزن الفرعي"]
    }

# --- 4. وظائف المحرك المحاسبي والـ AI ---
def post_journal(desc, debit_acc, credit_acc, amount, center="General"):
    st.session_state.db['ledger'].append({
        "التاريخ": date.today(), "البيان": desc, "مدين": debit_acc, "دائن": credit_acc, "المبلغ": amount, "مركز التكلفة": center
    })
    # تحديث دليل الحسابات
    for cat in st.session_state.db['coa']:
        if debit_acc in st.session_state.db['coa'][cat]: st.session_state.db['coa'][cat][debit_acc] += amount
        if credit_acc in st.session_state.db['coa'][cat]: st.session_state.db['coa'][cat][credit_acc] -= amount

def ask_ai(query):
    query = query.lower()
    if "مخزن" in query:
        count = len(st.session_state.db['inventory'])
        low = st.session_state.db['inventory'][st.session_state.db['inventory']['الكمية'] < 5]
        return f"المخزن حالياً به {count} أصناف. الأصناف المنخفضة هي: {list(low['الصنف'])}"
    if "فلوس" in query or "خزينة" in query:
        cash = st.session_state.db['coa']['الأصول']['الخزينة']
        return f"الرصيد المتوفر في الخزينة الآن هو {cash:,.2f} ج.م"
    return "أنا مساعدك AutoPro. يمكنني إخبارك عن المخازن، الحسابات، أو المبيعات. ماذا تريد؟"

# --- 5. القائمة الجانبية الشاملة ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>AutoPro ERP</h2>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("", [
        "📊 لوحة القيادة", "🛒 المبيعات (POS)", "📦 إدارة المخازن", "🧾 إدارة المشتريات",
        "👥 إدارة العملاء", "🚛 إدارة الموردين", "👔 الموظفين والرواتب", "⏰ الحضور والانصراف",
        "📉 إدارة المصروفات", "⚖️ المحاسبة والمالية", "📈 القوائم الختامية", "🤖 مساعد AI"
    ])

# --- 6. تنفيذ الموديولات ---

# 1. لوحة القيادة
if menu == "📊 لوحة القيادة":
    st.title("لوحة القيادة المركزية")
    c1, c2, c3, c4 = st.columns(4)
    coa = st.session_state.db['coa']
    with c1: st.markdown(f"<div class='erp-card'><h5>نقدية الخزينة</h5><h2>{coa['الأصول']['الالخزينة']:,.0f}</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='erp-card'><h5>قيمة المخزون</h5><h2>{coa['الأصول']['المخزن']:,.0f}</h2></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='erp-card'><h5>صافي الربح</h5><h2>{coa['الإيرادات']['المبيعات'] - coa['المصروفات']['تكلفة بضاعة']:,.0f}</h2></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='erp-card'><h5>إجمالي الموردين</h5><h2>{len(st.session_state.db['suppliers'])}</h2></div>", unsafe_allow_html=True)
    
    st.divider()
    if st.session_state.db['sales_log']:
        st.plotly_chart(px.line(pd.DataFrame(st.session_state.db['sales_log']), x='Date', y='Total', title="نمو المبيعات"), use_container_width=True)

# 2. المبيعات و POS
elif menu == "🛒 المبيعات (POS)":
    st.title("نقطة البيع (POS)")
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("🔍 ابحث (قطعة، ماركة، موديل)...")
        inv = st.session_state.db['inventory']
        filtered = inv[inv['الصنف'].str.contains(search) | inv['الماركة'].str.contains(search)]
        st.dataframe(filtered, use_container_width=True, hide_index=True)
        sel_p = st.selectbox("اختر الصنف", filtered['الصنف'])
        qty = st.number_input("الكمية", min_value=1)
        cust = st.selectbox("العميل", st.session_state.db['customers']['الاسم'])
        
    with col2:
        prod = inv[inv['الصنف'] == sel_p].iloc[0]
        total = prod['البيع'] * qty
        tax = total * 0.14
        st.markdown(f"<div class='erp-card'><h5>الإجمالي شامل الضريبة</h5><h2>{total + tax:,.2f}</h2></div>", unsafe_allow_html=True)
        if st.button("إتمام البيع وترحيل الحسابات"):
            if prod['الكمية'] >= qty:
                # تحديث المخزن والمالية
                st.session_state.db['inventory'].loc[inv['الصنف'] == sel_p, 'الكمية'] -= qty
                post_journal(f"بيع {qty} {sel_p}", "الخزينة", "المبيعات", total + tax)
                post_journal("VAT مبيعات", "المبيعات", "VAT", tax)
                post_journal("تكلفة البضاعة", "تكلفة بضاعة", "المخزن", prod['التكلفة'] * qty)
                st.session_state.db['sales_log'].append({"Date": date.today(), "Total": total + tax})
                st.success("تم البيع!")
            else: st.error("الكمية لا تكفي!")

# 3. إدارة المخازن
elif menu == "📦 إدارة المخازن":
    st.title("إدارة المخزون والسيارات")
    st.dataframe(st.session_state.db['inventory'], use_container_width=True)
    with st.expander("➕ إضافة صنف جديد (قطع غيار / إكسسوارات)"):
        with st.form("inv_form"):
            c1, c2, c3 = st.columns(3)
            make = c1.selectbox("الماركة", ["تويوتا", "هيونداي", "كيا", "مرسيدس", "BMW", "ميتسوبيشي", "إكسسوار عام"])
            model = c2.text_input("الموديل / السنة")
            name = c3.text_input("اسم القطعة")
            qty_i = c1.number_input("الكمية")
            cost_i = c2.number_input("التكلفة")
            sale_i = c3.number_input("البيع")
            loc = c1.text_input("الرف")
            type_p = c2.selectbox("النوع", ["قطع غيار", "إكسسوارات"])
            if st.form_submit_button("حفظ"):
                new_p = {"ID": len(st.session_state.db['inventory'])+1, "الماركة": make, "الموديل": model, "الصنف": name, "النوع": type_p, "الرف": loc, "الكمية": qty_i, "التكلفة": cost_i, "البيع": sale_i}
                st.session_state.db['inventory'] = pd.concat([st.session_state.db['inventory'], pd.DataFrame([new_p])], ignore_index=True)
                post_journal(f"إضافة مخزن: {name}", "المخزن", "رأس المال", cost_i * qty_i)
                st.rerun()

# 4. المشتريات
elif menu == "🧾 إدارة المشتريات":
    st.title("المشتريات وتوريد البضاعة")
    with st.form("pur_form"):
        sup = st.selectbox("المورد", st.session_state.db['suppliers']['الاسم'])
        item = st.selectbox("الصنف", st.session_state.db['inventory']['الصنف'])
        qty_p = st.number_input("الكمية الموردة", min_value=1)
        cost_p = st.number_input("سعر التكلفة")
        if st.form_submit_button("اعتماد فاتورة المشتريات"):
            st.session_state.db['inventory'].loc[st.session_state.db['inventory']['الصنف'] == item, 'الكمية'] += qty_p
            post_journal(f"شراء من {sup}", "المخزن", "الخزينة", qty_p * cost_p)
            st.success("تم التوريد!")

# 5. العملاء والموردين
elif menu == "👥 إدارة العملاء":
    st.title("قاعدة بيانات العملاء")
    with st.expander("➕ إضافة عميل"):
        with st.form("cust_form"):
            n = st.text_input("الاسم")
            p = st.text_input("الموبايل")
            if st.form_submit_button("حفظ"):
                st.session_state.db['customers'] = pd.concat([st.session_state.db['customers'], pd.DataFrame([{"الاسم": n, "الموبايل": p, "الرصيد": 0}])], ignore_index=True)
                st.rerun()
    st.table(st.session_state.db['customers'])

elif menu == "🚛 إدارة الموردين":
    st.title("قاعدة الموردين")
    with st.expander("➕ إضافة مورد"):
        with st.form("sup_form"):
            n = st.text_input("اسم الشركة")
            p = st.text_input("الموبايل")
            if st.form_submit_button("حفظ"):
                st.session_state.db['suppliers'] = pd.concat([st.session_state.db['suppliers'], pd.DataFrame([{"الاسم": n, "الموبايل": p, "المديونية": 0}])], ignore_index=True)
                st.rerun()
    st.table(st.session_state.db['suppliers'])

# 6. الموظفين والرواتب
elif menu == "👔 الموظفين والرواتب":
    st.title("شؤون الموظفين")
    with st.expander("➕ إضافة موظف"):
        with st.form("hr_form"):
            n = st.text_input("الاسم")
            j = st.text_input("الوظيفة")
            s = st.number_input("الراتب")
            if st.form_submit_button("حفظ"):
                st.session_state.db['employees'] = pd.concat([st.session_state.db['employees'], pd.DataFrame([{"الاسم": n, "الوظيفة": j, "الراتب": s, "الحالة": "نشط"}])], ignore_index=True)
                st.rerun()
    st.table(st.session_state.db['employees'])
    if st.button("صرف الرواتب الشهرية"):
        total_sal = st.session_state.db['employees']['الراتب'].sum()
        post_journal("صرف رواتب الموظفين", "رواتب", "الخزينة", total_sal)
        st.success("تم خصم الرواتب من الخزينة")

# 7. الحضور والانصراف
elif menu == "⏰ الحضور والانصراف":
    st.title("سجل الحضور اليومي")
    emp = st.selectbox("الموظف", st.session_state.db['employees']['الاسم'])
    type_a = st.radio("العملية", ["حضور", "انصراف"])
    if st.button("تسجيل"):
        st.session_state.db['attendance'].append({"Date": date.today(), "Name": emp, "Time": datetime.now().strftime("%I:%M %p"), "Type": type_a})
        st.success(f"تم تسجيل {type_a} لـ {emp}")
    st.table(pd.DataFrame(st.session_state.db['attendance']).tail(10))

# 8. المحاسبة والمالية (دليل الحسابات، اليومية، ميزانية، مراكز تكلفة)
elif menu == "⚖️ المحاسبة والمالية":
    st.title("النظام المحاسبي المركزي")
    t1, t2, t3, t4 = st.tabs(["دليل الحسابات", "دفتر اليومية", "ميزان المراجعة", "مراكز التكلفة"])
    with t1:
        st.write(st.session_state.db['coa'])
    with t2:
        if st.session_state.db['ledger']: st.table(pd.DataFrame(st.session_state.db['ledger']))
        else: st.info("لا توجد قيود")
    with t3:
        rows = []
        for cat, subs in st.session_state.db['coa'].items():
            for acc, val in subs.items(): rows.append({"الحساب": acc, "الرصيد": val})
        st.table(pd.DataFrame(rows))

# 9. التقارير والضرائب
elif menu == "📈 القوائم الختامية":
    st.title("التقارير المالية والضرائب")
    coa = st.session_state.db['coa']
    rev = coa['الإيرادات']['المبيعات']
    exp = coa['المصروفات']['تكلفة بضاعة'] + coa['المصروفات']['رواتب']
    st.metric("صافي الربح", f"{rev - exp:,.2f} ج.م")
    st.divider()
    st.write("### تقرير ضريبة القيمة المضافة (VAT)")
    st.warning(f"الضريبة المستحقة للسداد: {abs(coa['الخصوم']['VAT']):,.2f} ج.م")

# 10. مساعد AI
elif menu == "🤖 مساعد AI":
    st.title("AutoPro AI Assistant")
    user_q = st.chat_input("اسألني عن المخزن، المبيعات أو الرواتب...")
    if user_q:
        with st.chat_message("user"): st.write(user_q)
        with st.chat_message("assistant"): st.write(ask_ai(user_q))

# 11. المصروفات
elif menu == "📉 إدارة المصروفات":
    st.title("تسجيل المصروفات")
    with st.form("exp_form"):
        desc = st.text_input("بند الصرف")
        amt = st.number_input("المبلغ")
        center = st.selectbox("مركز التكلفة", st.session_state.db['centers'])
        if st.form_submit_button("تسجيل"):
            post_journal(desc, "مصاريف عامة", "الخزينة", amt, center)
            st.success("تم الحفظ")
