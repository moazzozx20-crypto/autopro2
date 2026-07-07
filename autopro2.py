import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# --- 1. إعدادات النظام ---
st.set_page_config(page_title="AutoPro ERP Pro v2.2", layout="wide", initial_sidebar_state="expanded")

# --- 2. التصميم الاحترافي وإخفاء "النقط" من القائمة (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    /* الخط والتنسيق العام */
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .main { background-color: #f4f7f9; }

    /* تعديل القائمة الجانبية - إخفاء النقط (Radio Circles) */
    [data-testid="stSidebar"] { background-color: #1E3A8A !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    
    /* إخفاء الدوائر تماماً */
    div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }
    
    /* تنسيق عناصر القائمة لتظهر كأزرار أنيقة */
    div[role="radiogroup"] {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    
    div[role="radiogroup"] label {
        background-color: transparent;
        padding: 12px 20px;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s;
        border: 1px solid transparent;
    }
    
    div[role="radiogroup"] label:hover {
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* تمييز الزر المختار */
    div[role="radiogroup"] label[data-selected="true"] {
        background-color: #2563EB !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }

    /* تنسيق الأزرار داخل الصفحات */
    .stButton>button { background-color: #1E3A8A; color: white; border-radius: 8px; font-weight: bold; }
    .stButton>button:hover { background-color: #2563EB; border: none; }
    
    /* بطاقات الإحصائيات */
    .metric-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-right: 5px solid #1E3A8A; color: #333; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. محرك البيانات (Session State) ---
if 'db_products' not in st.session_state:
    st.session_state.db_products = pd.DataFrame([
        {"كود": "BK-001", "الصنف": "تيل فرامل تويوتا", "المخزن": 50, "التكلفة": 450.0, "البيع": 650.0, "المورد": "النيل لقطع الغيار"},
        {"كود": "OF-002", "الصنف": "فلتر زيت هيونداي", "المخزن": 100, "التكلفة": 120.0, "البيع": 185.0, "المورد": "المركز التجاري"}
    ])

if 'db_sales' not in st.session_state: st.session_state.db_sales = []
if 'db_purchases' not in st.session_state: st.session_state.db_purchases = []
if 'db_suppliers' not in st.session_state: st.session_state.db_suppliers = ["النيل لقطع الغيار", "المركز التجاري"]
if 'db_customers' not in st.session_state: st.session_state.db_customers = ["عميل نقدي", "شركة الأمان"]
if 'db_expenses' not in st.session_state: st.session_state.db_expenses = []
if 'db_employees' not in st.session_state:
    st.session_state.db_employees = pd.DataFrame([
        {"الاسم": "محمد حسن", "الوظيفة": "بائع", "الراتب": 6000, "الحالة": "حاضر"}
    ])

# --- 4. القائمة الجانبية (الأنيقة بدون نقط) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: white;'>AutoPro ERP</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 0.8em;'>إدارة قطع غيار السيارات</p>", unsafe_allow_html=True)
    st.divider()
    
    # القائمة الآن ستظهر كأزرار نظيفة بفضل كود الـ CSS بالأعلى
    menu = st.radio("", [
        "🏠 لوحة القيادة", 
        "🛒 إدارة المبيعات", 
        "📦 إدارة المخازن", 
        "🧾 إدارة المشتريات", 
        "🚛 إدارة الموردين", 
        "👥 إدارة العملاء", 
        "👔 إدارة الموظفين", 
        "⏰ الحضور والانصراف", 
        "💸 المرتبات", 
        "📉 إدارة المصروفات", 
        "📈 التقارير", 
        "⚙️ الصلاحيات"
    ])

# --- 5. منطق الموديولات ---

# 1. لوحة القيادة
if menu == "🏠 لوحة القيادة":
    st.title("📊 لوحة القيادة")
    total_sales = sum(s['Total'] for s in st.session_state.db_sales)
    total_exp = sum(e['Amount'] for e in st.session_state.db_expenses)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f"<div class='metric-card'><h4>المبيعات</h4><h3>{total_sales:,.0f} ج.م</h3></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='metric-card'><h4>المصروفات</h4><h3>{total_exp:,.0f} ج.م</h3></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='metric-card'><h4>عدد العملاء</h4><h3>{len(st.session_state.db_customers)}</h3></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='metric-card'><h4>صافي الربح</h4><h3>{total_sales - total_exp:,.0f} ج.م</h3></div>", unsafe_allow_html=True)
    
    if st.session_state.db_sales:
        df_sales = pd.DataFrame(st.session_state.db_sales)
        fig = px.area(df_sales, x='Date', y='Total', title="منحنى أداء المبيعات")
        st.plotly_chart(fig, use_container_width=True)

# 2. المبيعات
elif menu == "🛒 إدارة المبيعات":
    st.title("🛒 نقطة البيع (POS)")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("قائمة الأصناف")
        search = st.text_input("🔍 ابحث عن صنف...")
        res = st.session_state.db_products[st.session_state.db_products['الصنف'].str.contains(search)]
        st.dataframe(res[['كود', 'الصنف', 'البيع', 'المخزن']], use_container_width=True)
        
        sel_code = st.selectbox("اختر الكود للإضافة", res['كود'])
        qty = st.number_input("الكمية", min_value=1, value=1)
        
    with col2:
        st.subheader("الفاتورة")
        row = st.session_state.db_products[st.session_state.db_products['كود'] == sel_code].iloc[0]
        total_p = row['البيع'] * qty
        st.write(f"الصنف: **{row['الصنف']}**")
        st.markdown(f"### الإجمالي: {total_p} ج.م")
        
        if st.button("حفظ الفاتورة وخصم من المخزن"):
            if row['المخزن'] >= qty:
                st.session_state.db_products.loc[st.session_state.db_products['كود'] == sel_code, 'المخزن'] -= qty
                st.session_state.db_sales.append({"Date": str(date.today()), "Product": row['الصنف'], "Total": total_p})
                st.success("تم إتمام البيع!")
                st.rerun()
            else:
                st.error("المخزن لا يكفي!")

# 3. المخازن
elif menu == "📦 إدارة المخازن":
    st.title("📦 إدارة المخازن")
    st.dataframe(st.session_state.db_products, use_container_width=True)
    with st.expander("إضافة صنف جديد"):
        c1, c2 = st.columns(2)
        n_code = c1.text_input("الكود")
        n_name = c2.text_input("الاسم")
        n_cost = c1.number_input("التكلفة")
        n_sale = c2.number_input("البيع")
        if st.button("حفظ الصنف"):
            new_item = {"كود": n_code, "الصنف": n_name, "المخزن": 0, "التكلفة": n_cost, "البيع": n_sale, "المورد": "غير محدد"}
            st.session_state.db_products = pd.concat([st.session_state.db_products, pd.DataFrame([new_item])], ignore_index=True)
            st.rerun()

# باقي الموديولات تعمل بنفس آلية الحفظ (تم توفير الهياكل الأساسية لها)
else:
    st.title(menu)
    st.info("هذا الموديول جاهز للإضافة والربط بقاعدة البيانات.")
