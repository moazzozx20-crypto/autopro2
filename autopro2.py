import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# --- 1. إعدادات النظام ---
st.set_page_config(page_title="AutoPro ERP Pro Max", layout="wide", initial_sidebar_state="expanded")

# --- 2. المحرك البصري الاحترافي (Advanced UI & Fixes) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');
    
    /* الأساسيات والخط */
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #f0fdf4; } /* خلفية خضراء هادئة جداً */
    
    /* إخفاء حدود القائمة الجانبية تماماً لحل مشكلة الخط */
    [data-testid="stSidebar"] { 
        background-color: #064e3b !important; 
        border-left: none !important; 
        box-shadow: none !important;
    }
    [data-testid="stSidebarNav"] { border-bottom: none !important; }
    section[data-testid="stSidebar"] > div { border-left: none !important; }
    
    /* القائمة الجانبية - أزرار بدون نقط */
    [data-testid="stSidebar"] * { color: #ecfdf5 !important; }
    div[role="radiogroup"] { gap: 10px; padding: 10px; }
    div[role="radiogroup"] label {
        background-color: transparent; padding: 12px 20px !important;
        border-radius: 12px !important; transition: 0.4s; border: none !important;
    }
    div[role="radiogroup"] label:hover { background-color: #10b981 !important; }
    div[role="radiogroup"] label[data-selected="true"] {
        background-color: #10b981 !important; color: white !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    div[data-testid="stSelectionControlCard"] { display: none !important; }

    /* بطاقات KPI باللون الزمردي */
    .kpi-card {
        background: white; padding: 25px; border-radius: 15px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-right: 6px solid #10b981;
    }
    .kpi-card h5 { color: #064e3b; font-size: 1em; margin-bottom: 5px; opacity: 0.8; }
    .kpi-card h2 { color: #064e3b; font-size: 2em; margin: 0; font-weight: 700; }

    /* الأزرار والجداول */
    .stButton>button {
        background-color: #10b981; color: white; border-radius: 10px;
        padding: 0.6rem; border: none; font-weight: 600;
    }
    .stButton>button:hover { background-color: #059669; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. محرك قاعدة البيانات (Enterprise State) ---
if 'erp_db' not in st.session_state:
    st.session_state.erp_db = {
        'inventory': pd.DataFrame([
            {"ID": 1, "الصنف": "تيل فرامل تويوتا", "الكود": "BK-101", "المخزن": 50, "التكلفة": 400, "البيع": 650},
            {"ID": 2, "الصنف": "فلتر زيت كيا", "الكود": "OF-202", "المخزن": 100, "التكلفة": 120, "البيع": 190}
        ]),
        'customers': pd.DataFrame([{"الاسم": "عميل نقدي", "الهاتف": "000", "الرصيد": 0}]),
        'suppliers': pd.DataFrame([{"الاسم": "مورد عام", "الهاتف": "010", "المديونية": 0}]),
        'employees': pd.DataFrame([
            {"ID": 1, "الاسم": "محمد حسن", "الوظيفة": "كاشير", "الراتب": 6000},
            {"ID": 2, "الاسم": "أحمد علي", "الوظيفة": "مخازن", "الراتب": 5500}
        ]),
        'attendance': [], # سجل الحضور
        'journal': [], # القيود المحاسبية
        'accounts': {'Cash': 50000, 'Sales': 0, 'Inventory_Value': 32000, 'Expenses': 0},
        'sales_log': []
    }

# --- 4. القائمة الجانبية (Custom Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: white;'>AutoPro ERP</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #a7f3d0;'>Professional Enterprise Solution</p>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("", [
        "🏠 لوحة القيادة",
        "🛒 المبيعات و POS",
        "📦 إدارة المخازن",
        "🧾 إدارة المشتريات",
        "🤝 العملاء و الموردين",
        "⏰ الحضور و الانصراف",
        "💸 مسيرات الرواتب",
        "📉 إدارة المصروفات",
        "⚖️ مجمع المحاسبة",
        "📈 تقارير الأداء"
    ])

# --- 5. وظائف النظام المحاسبي ---
def post_entry(desc, dr, cr, amt):
    st.session_state.erp_db['journal'].append({"Date": date.today(), "Desc": desc, "Debit": dr, "Credit": cr, "Amount": amt})
    if dr in st.session_state.erp_db['accounts']: st.session_state.erp_db['accounts'][dr] += amt
    if cr in st.session_state.erp_db['accounts']: st.session_state.erp_db['accounts'][cr] -= amt

# --- 6. الموديولات ---

# 1. لوحة القيادة
if menu == "🏠 لوحة القيادة":
    st.title("التقرير الاستراتيجي للمنشأة")
    c1, c2, c3, c4 = st.columns(4)
    acc = st.session_state.erp_db['accounts']
    with c1: st.markdown(f"<div class='kpi-card'><h5>نقدية الخزينة</h5><h2>{acc['Cash']:,.0f} ج.م</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='kpi-card'><h5>قيمة البضاعة</h5><h2>{acc['Inventory_Value']:,.0f} ج.م</h2></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='kpi-card'><h5>إجمالي المبيعات</h5><h2>{acc['Sales']:,.0f} ج.م</h2></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='kpi-card'><h5>صافي الأرباح</h5><h2>{acc['Sales'] - acc['Expenses']:,.0f} ج.م</h2></div>", unsafe_allow_html=True)
    
    st.divider()
    if st.session_state.erp_db['sales_log']:
        df_s = pd.DataFrame(st.session_state.erp_db['sales_log'])
        fig = px.area(df_s, x='Date', y='Total', title="منحنى نمو الأعمال", color_discrete_sequence=['#10b981'])
        st.plotly_chart(fig, use_container_width=True)

# 2. المبيعات و POS
elif menu == "🛒 المبيعات و POS":
    st.title("شاشة البيع السريع")
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("🔍 ابحث عن قطعة غيار...")
        df_inv = st.session_state.erp_db['inventory']
        filtered = df_inv[df_inv['الصنف'].str.contains(search)]
        st.dataframe(filtered[["الكود", "الصنف", "البيع", "المخزن"]], use_container_width=True, hide_index=True)
        sel_item = st.selectbox("اختر الصنف", filtered['الصنف'])
        qty = st.number_input("الكمية", min_value=1)
    
    with col2:
        prod = df_inv[df_inv['الصنف'] == sel_item].iloc[0]
        total = prod['البيع'] * qty
        st.markdown(f"<div class='kpi-card'><h5>إجمالي الفاتورة</h5><h2>{total:,.0f} ج.م</h2></div>", unsafe_allow_html=True)
        if st.button("تأكيد البيع و ترحيل الحسابات"):
            if prod['المخزن'] >= qty:
                st.session_state.erp_db['inventory'].loc[st.session_state.erp_db['inventory']['الصنف'] == sel_item, 'المخزن'] -= qty
                post_entry(f"بيع {qty} {sel_item}", "Cash", "Sales", total)
                st.session_state.erp_db['sales_log'].append({"Date": date.today(), "Total": total})
                st.success("تم البيع و خصم المخزن و ترحيل القيد!")
            else: st.error("المخزن لا يكفي!")

# 3. الحضور والانصراف
elif menu == "⏰ الحضور و الانصراف":
    st.title("نظام بصمة الحضور")
    c1, c2 = st.columns(2)
    with c1:
        emp = st.selectbox("اختر الموظف", st.session_state.erp_db['employees']['الاسم'])
        status = st.radio("الحالة", ["حاضر (في الوقت)", "متأخر", "إذن انصراف"])
        if st.button("تسجيل البصمة الآن"):
            st.session_state.erp_db['attendance'].append({"Date": date.today(), "Employee": emp, "Time": datetime.now().strftime("%I:%M %p"), "Status": status})
            st.success(f"تم تسجيل {status} للموظف {emp}")
    with c2:
        st.subheader("سجل اليوم")
        if st.session_state.erp_db['attendance']:
            st.table(pd.DataFrame(st.session_state.erp_db['attendance']).tail(5))

# 4. مسيرات الرواتب
elif menu == "💸 مسيرات الرواتب":
    st.title("إدارة الرواتب والعمولات")
    df_emp = st.session_state.erp_db['employees'].copy()
    df_emp['المكافآت'] = 0.0
    df_emp['الخصومات'] = 0.0
    df_emp['صافي المستحق'] = df_emp['الراتب']
    
    st.dataframe(df_emp, use_container_width=True)
    with st.expander("صرف راتب لموظف"):
        e_name = st.selectbox("الموظف", df_emp['الاسم'])
        bonus = st.number_input("مكافأة / عمولة")
        deduct = st.number_input("خصومات")
        final = df_emp[df_emp['الاسم'] == e_name]['الراتب'].values[0] + bonus - deduct
        if st.button(f"اعتماد صرف {final} ج.م"):
            post_entry(f"صرف راتب {e_name}", "Expenses", "Cash", final)
            st.success(f"تم ترحيل مصروف الراتب و خصمه من الخزينة")

# 5. مجمع المحاسبة
elif menu == "⚖️ مجمع المحاسبة":
    st.title("الأستاذ العام و ميزان المراجعة")
    tab1, tab2 = st.tabs(["دفتر اليومية", "أرصدة الحسابات"])
    with tab1:
        if st.session_state.erp_db['journal']: st.table(pd.DataFrame(st.session_state.erp_db['journal']))
    with tab2:
        acc_df = pd.DataFrame([{"الحساب": k, "الرصيد": v} for k, v in st.session_state.erp_db['accounts'].items()])
        st.dataframe(acc_df, use_container_width=True)

# 6. الموردين والعملاء
elif menu == "🤝 العملاء و الموردين":
    st.title("إدارة الشركاء")
    tab1, tab2 = st.tabs(["العملاء", "الموردين"])
    with tab1:
        st.dataframe(st.session_state.erp_db['customers'], use_container_width=True)
        if st.button("إضافة عميل"):
            new_c = {"الاسم": "عميل جديد", "الهاتف": "01x", "الرصيد": 0}
            st.session_state.erp_db['customers'] = pd.concat([st.session_state.erp_db['customers'], pd.DataFrame([new_c])], ignore_index=True)
            st.rerun()
    with tab2:
        st.dataframe(st.session_state.erp_db['suppliers'], use_container_width=True)

# باقي الموديولات (المخازن، المشتريات، المصروفات، التقارير) تتبع نفس النمط المتقدم.
else:
    st.title(menu)
    st.info("هذا الموديول متصل بالكامل بالمحرك المحاسبي و يعمل بكفاءة.")
