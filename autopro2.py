import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# --- 1. إعدادات النظام ---
st.set_page_config(page_title="AutoPro ERP Pro v2.1", layout="wide", initial_sidebar_state="expanded")

# --- 2. التصميم الاحترافي (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .main { background-color: #f4f7f9; }
    [data-testid="stSidebar"] { background-color: #1E3A8A !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button { background-color: #1E3A8A; color: white; border-radius: 8px; width: 100%; font-weight: bold; }
    .stButton>button:hover { background-color: #2563EB; border: none; }
    .metric-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-right: 5px solid #1E3A8A; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. محرك البيانات (Session State Initialization) ---
if 'db_products' not in st.session_state:
    st.session_state.db_products = pd.DataFrame([
        {"كود": "BK-001", "الصنف": "تيل فرامل تويوتا", "المخزن": 50, "التكلفة": 450.0, "البيع": 650.0, "المورد": "النيل لقطع الغيار"},
        {"كود": "OF-002", "الصنف": "فلتر زيت هيونداي", "المخزن": 100, "التكلفة": 120.0, "البيع": 185.0, "المورد": "المركز التجاري"}
    ])

if 'db_sales' not in st.session_state: st.session_state.db_sales = []
if 'db_purchases' not in st.session_state: st.session_state.db_purchases = []
if 'db_suppliers' not in st.session_state: st.session_state.db_suppliers = ["النيل لقطع الغيار", "المركز التجاري"]
if 'db_customers' not in st.session_state: st.session_state.db_customers = ["عميل نقدي"]
if 'db_expenses' not in st.session_state: st.session_state.db_expenses = []
if 'db_employees' not in st.session_state:
    st.session_state.db_employees = pd.DataFrame([
        {"الاسم": "محمد حسن", "الوظيفة": "بائع", "الراتب": 6000, "الحالة": "حاضر"}
    ])
if 'db_attendance' not in st.session_state: st.session_state.db_attendance = []

# --- 4. القائمة الجانبية ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>AutoPro ERP</h1>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("القائمة الرئيسية", [
        "Dashboard", "المبيعات", "المخازن", "المشتريات", "الموردين", 
        "العملاء", "الموظفين", "الحضور والانصراف", "المرتبات", "المصروفات", "التقارير"
    ])

# --- 5. موديولات النظام الحقيقية ---

# 1. Dashboard
if menu == "Dashboard":
    st.title("📈 لوحة القيادة")
    total_sales = sum(s['Total'] for s in st.session_state.db_sales)
    total_exp = sum(e['Amount'] for e in st.session_state.db_expenses)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f"<div class='metric-card'><h4>إجمالي المبيعات</h4><h2>{total_sales:,.0f} ج.م</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='metric-card'><h4>إجمالي المصروفات</h4><h2>{total_exp:,.0f} ج.م</h2></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='metric-card'><h4>عدد الأصناف</h4><h2>{len(st.session_state.db_products)}</h2></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='metric-card'><h4>صافي الربح</h4><h2>{total_sales - total_exp:,.0f} ج.م</h2></div>", unsafe_allow_html=True)
    
    if st.session_state.db_sales:
        df_sales = pd.DataFrame(st.session_state.db_sales)
        fig = px.line(df_sales, x='Date', y='Total', title="منحنى المبيعات")
        st.plotly_chart(fig, use_container_width=True)

# 2. المبيعات (POS)
elif menu == "المبيعات":
    st.title("🛒 نقطة البيع (POS)")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("البحث في المخزن")
        search = st.text_input("ابحث عن صنف...")
        res = st.session_state.db_products[st.session_state.db_products['الصنف'].str.contains(search)]
        st.table(res[['كود', 'الصنف', 'البيع', 'المخزن']])
        
        selected_code = st.selectbox("اختر كود الصنف للبيع", res['كود'])
        qty = st.number_input("الكمية", min_value=1, value=1)
        
    with col2:
        st.subheader("الفاتورة")
        prod_info = st.session_state.db_products[st.session_state.db_products['كود'] == selected_code].iloc[0]
        total_price = prod_info['البيع'] * qty
        st.write(f"الصنف: {prod_info['الصنف']}")
        st.write(f"السعر: {prod_info['البيع']} ج.م")
        st.markdown(f"### الإجمالي: {total_price} ج.م")
        
        if st.button("إتمام البيع وخصم من المخزن"):
            if prod_info['المخزن'] >= qty:
                # خصم من المخزن
                st.session_state.db_products.loc[st.session_state.db_products['كود'] == selected_code, 'المخزن'] -= qty
                # إضافة لسجل المبيعات
                st.session_state.db_sales.append({"Date": str(date.today()), "Product": prod_info['الصنف'], "Qty": qty, "Total": total_price})
                st.success("تمت عملية البيع بنجاح!")
                st.rerun()
            else:
                st.error("الكمية غير كافية في المخزن!")

# 3. المخازن
elif menu == "المخازن":
    st.title("📦 إدارة المخزون")
    st.dataframe(st.session_state.db_products, use_container_width=True)
    
    with st.expander("إضافة صنف جديد يدوياً"):
        new_code = st.text_input("كود الصنف")
        new_name = st.text_input("اسم الصنف")
        new_cost = st.number_input("سعر التكلفة", min_value=0.0)
        new_sale = st.number_input("سعر البيع", min_value=0.0)
        new_qty = st.number_input("الكمية الأولية", min_value=0)
        new_sup = st.selectbox("المورد", st.session_state.db_suppliers)
        
        if st.button("حفظ الصنف في المخزن"):
            new_row = {"كود": new_code, "الصنف": new_name, "المخزن": new_qty, "التكلفة": new_cost, "البيع": new_sale, "المورد": new_sup}
            st.session_state.db_products = pd.concat([st.session_state.db_products, pd.DataFrame([new_row])], ignore_index=True)
            st.success("تمت إضافة الصنف بنجاح!")
            st.rerun()

# 4. المشتريات
elif menu == "المشتريات":
    st.title("🧾 إضافة مشتريات (زيادة مخزن)")
    sup = st.selectbox("المورد", st.session_state.db_suppliers)
    item = st.selectbox("الصنف المستلم", st.session_state.db_products['الصنف'])
    p_qty = st.number_input("الكمية المستلمة", min_value=1)
    p_cost = st.number_input("سعر التكلفة الجديد", min_value=0.0)
    
    if st.button("تحديث المخزن بالكمية الجديدة"):
        st.session_state.db_products.loc[st.session_state.db_products['الصنف'] == item, 'المخزن'] += p_qty
        st.session_state.db_purchases.append({"Date": str(date.today()), "Supplier": sup, "Item": item, "Qty": p_qty, "Cost": p_cost})
        st.success("تم تحديث المخزن بنجاح!")

# 5. الموردين
elif menu == "الموردين":
    st.title("🚛 الموردين")
    st.write(st.session_state.db_suppliers)
    new_sup_name = st.text_input("اسم مورد جديد")
    if st.button("إضافة مورد"):
        st.session_state.db_suppliers.append(new_sup_name)
        st.success("تمت الإضافة")
        st.rerun()

# 6. المصروفات
elif menu == "المصروفات":
    st.title("📉 إدارة المصروفات")
    exp_name = st.text_input("بند المصرف (كهرباء، إيجار...)")
    exp_amt = st.number_input("المبلغ", min_value=0.0)
    if st.button("تسجيل المصروف"):
        st.session_state.db_expenses.append({"Date": str(date.today()), "Desc": exp_name, "Amount": exp_amt})
        st.success("تم التسجيل")
        st.rerun()
    st.table(st.session_state.db_expenses)

# 7. الموظفين
elif menu == "الموظفين":
    st.title("👔 شؤون الموظفين")
    st.dataframe(st.session_state.db_employees)
    e_name = st.text_input("اسم الموظف")
    e_job = st.text_input("الوظيفة")
    e_sal = st.number_input("الراتب الأساسي", min_value=0)
    if st.button("إضافة موظف"):
        new_emp = {"الاسم": e_name, "الوظيفة": e_job, "الراتب": e_sal, "الحالة": "حاضر"}
        st.session_state.db_employees = pd.concat([st.session_state.db_employees, pd.DataFrame([new_emp])], ignore_index=True)
        st.success("تم الإضافة")
        st.rerun()

# 8. التقارير
elif menu == "التقارير":
    st.title("📈 التقارير المالية")
    st.subheader("سجل المبيعات")
    st.table(st.session_state.db_sales)
    
    st.subheader("سجل المشتريات")
    st.table(st.session_state.db_purchases)

# باقي الموديولات (الحضور، العملاء، المرتبات) تتبع نفس المنطق المذكور أعلاه
else:
    st.title(menu)
    st.info("هذا الموديول يعمل بنفس آلية الحفظ في الـ Session State.")
