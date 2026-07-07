import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# --- 1. إعدادات النظام الاحترافية ---
st.set_page_config(page_title="AutoPro ERP Pro", layout="wide", initial_sidebar_state="expanded")

# --- 2. محرك التصميم العالمي (Advanced CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');
    
    /* الأساسيات */
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #f8fafc; }
    
    /* القائمة الجانبية الاحترافية */
    [data-testid="stSidebar"] { background-color: #0f172a !important; border-left: 1px solid #1e293b; }
    [data-testid="stSidebar"] * { color: #f8fafc !important; }
    
    /* إخفاء دوائر الراديو وتحويلها لأزرار قائمة */
    div[role="radiogroup"] { gap: 10px; padding-top: 20px; }
    div[role="radiogroup"] label {
        background-color: transparent;
        padding: 12px 15px !important;
        border-radius: 8px !important;
        border: none !important;
        transition: 0.3s;
        margin-bottom: 5px;
    }
    div[role="radiogroup"] label:hover { background-color: #1e293b !important; }
    div[role="radiogroup"] label[data-selected="true"] {
        background-color: #4f46e5 !important;
        color: white !important;
        font-weight: 600;
    }
    div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] p { font-size: 16px !important; }
    div[role="radiogroup"] div[data-testid="stWidgetSelectionMarker"] { display: none !important; }

    /* بطاقات KPI */
    .kpi-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    .kpi-card h5 { color: #64748b; margin-bottom: 10px; font-size: 14px; }
    .kpi-card h2 { color: #0f172a; margin: 0; font-size: 24px; }

    /* الأزرار والجداول */
    .stButton>button {
        background-color: #4f46e5;
        color: white;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stDataFrame { border: 1px solid #e2e8f0; border-radius: 8px; }
    
    /* إخفاء النقطة في الراديو بوتون */
    div[data-testid="stSelectionControlCard"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. إدارة قاعدة البيانات الداخلية (Session State) ---
if 'data' not in st.session_state:
    st.session_state.data = {
        'products': pd.DataFrame([
            {"ID": 1, "الصنف": "تيل فرامل تويوتا", "الكود": "BK-101", "المخزن": 50, "التكلفة": 400, "البيع": 600, "المورد": "شركة النيل"},
            {"ID": 2, "الصنف": "فلتر زيت كيا", "الكود": "OF-202", "المخزن": 100, "التكلفة": 100, "البيع": 150, "المورد": "أولاد علي"}
        ]),
        'sales': [],
        'purchases': [],
        'suppliers': pd.DataFrame([{"المورد": "شركة النيل", "الهاتف": "010000000", "المديونية": 5000}]),
        'customers': pd.DataFrame([{"العميل": "أحمد رأفت", "الهاتف": "012000000", "إجمالي المشتريات": 1200}]),
        'employees': pd.DataFrame([{"الاسم": "محمد علي", "الوظيفة": "كاشير", "الراتب": 5000, "الحالة": "نشط"}]),
        'attendance': [],
        'expenses': []
    }

# --- 4. القائمة الجانبية (Sidebar Navigation) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>AutoPro ERP</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>نظام الإدارة المتكامل</p>", unsafe_allow_html=True)
    st.divider()
    
    menu = st.radio("", [
        "📊 لوحة التحكم",
        "🛒 إدارة المبيعات",
        "📦 إدارة المخازن",
        "🧾 إدارة المشتريات",
        "🚛 إدارة الموردين",
        "👥 إدارة العملاء",
        "👔 إدارة الموظفين",
        "⏰ الحضور والانصراف",
        "💰 إدارة المرتبات",
        "📉 إدارة المصروفات",
        "📈 التقارير",
        "🔒 الصلاحيات"
    ])

# --- 5. موديولات النظام ---

# 1. لوحة التحكم (Dashboard)
if menu == "📊 لوحة التحكم":
    st.title("لوحة التحكم الاستراتيجية")
    
    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    total_sales = sum(s['إجمالي'] for s in st.session_state.data['sales']) if st.session_state.data['sales'] else 0
    total_expenses = sum(e['المبلغ'] for e in st.session_state.data['expenses']) if st.session_state.data['expenses'] else 0
    
    with c1: st.markdown(f"<div class='kpi-card'><h5>إجمالي المبيعات</h5><h2>{total_sales:,.0f} ج.م</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='kpi-card'><h5>قيمة المخزن</h5><h2>{ (st.session_state.data['products']['المخزن'] * st.session_state.data['products']['التكلفة']).sum():,.0f} ج.م</h2></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='kpi-card'><h5>المصروفات</h5><h2>{total_expenses:,.0f} ج.م</h2></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='kpi-card'><h5>صافي الربح</h5><h2>{total_sales - total_expenses:,.0f} ج.م</h2></div>", unsafe_allow_html=True)

    st.divider()
    col_chart, col_status = st.columns([2, 1])
    with col_chart:
        if st.session_state.data['sales']:
            df_s = pd.DataFrame(st.session_state.data['sales'])
            fig = px.area(df_s, x='التاريخ', y='إجمالي', title="منحنى نمو المبيعات")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("لا توجد مبيعات مسجلة اليوم")
            
    with col_status:
        st.subheader("حالة النواقص")
        low_stock = st.session_state.data['products'][st.session_state.data['products']['المخزن'] < 20]
        st.dataframe(low_stock[['الصنف', 'المخزن']], hide_index=True)

# 2. إدارة المبيعات (Sales/POS)
elif menu == "🛒 إدارة المبيعات":
    st.title("نقطة البيع (POS)")
    col_pos, col_cart = st.columns([2, 1])
    
    with col_pos:
        search = st.text_input("🔍 ابحث عن صنف...")
        items = st.session_state.data['products']
        filtered = items[items['الصنف'].str.contains(search) | items['الكود'].str.contains(search)]
        st.dataframe(filtered[['الكود', 'الصنف', 'البيع', 'المخزن']], use_container_width=True, hide_index=True)
        
        selected_code = st.selectbox("اختر الكود للبيع", filtered['الكود'])
        qty = st.number_input("الكمية", min_value=1, step=1)
        
    with col_cart:
        st.markdown("<div style='background:white; padding:20px; border-radius:10px;'>", unsafe_allow_html=True)
        st.subheader("الفاتورة الحالية")
        prod = items[items['الكود'] == selected_code].iloc[0]
        st.write(f"الصنف: {prod['الصنف']}")
        st.write(f"السعر: {prod['البيع']} ج.م")
        total = prod['البيع'] * qty
        st.markdown(f"### الإجمالي: {total} ج.م")
        
        if st.button("إتمام العملية وحفظ"):
            if prod['المخزن'] >= qty:
                # Update Stock
                st.session_state.data['products'].loc[st.session_state.data['products']['الكود'] == selected_code, 'المخزن'] -= qty
                # Record Sale
                st.session_state.data['sales'].append({"التاريخ": date.today(), "الصنف": prod['الصنف'], "إجمالي": total})
                st.success("تم البيع بنجاح!")
                st.rerun()
            else:
                st.error("الكمية لا تكفي!")
        st.markdown("</div>", unsafe_allow_html=True)

# 3. إدارة المخازن (Inventory)
elif menu == "📦 إدارة المخازن":
    st.title("المخازن والأصناف")
    st.dataframe(st.session_state.data['products'], use_container_width=True, hide_index=True)
    
    with st.expander("➕ إضافة صنف جديد للمخزن"):
        c1, c2, c3 = st.columns(3)
        n_name = c1.text_input("اسم الصنف")
        n_code = c2.text_input("الكود")
        n_sup = c3.selectbox("المورد الرئيسي", st.session_state.data['suppliers']['المورد'])
        n_cost = c1.number_input("سعر التكلفة")
        n_sale = c2.number_input("سعر البيع")
        n_stock = c3.number_input("الكمية الافتتاحية")
        
        if st.button("حفظ الصنف"):
            new_p = {"ID": len(st.session_state.data['products'])+1, "الصنف": n_name, "الكود": n_code, "المخزن": n_stock, "التكلفة": n_cost, "البيع": n_sale, "المورد": n_sup}
            st.session_state.data['products'] = pd.concat([st.session_state.data['products'], pd.DataFrame([new_p])], ignore_index=True)
            st.success("تمت الإضافة")
            st.rerun()

# 4. إدارة المشتريات
elif menu == "🧾 إدارة المشتريات":
    st.title("المشتريات وتوريد البضاعة")
    st.info("هنا يتم تسجيل فواتير الشراء لزيادة كميات المخزن")
    item_to_buy = st.selectbox("اختر الصنف المستلم", st.session_state.data['products']['الصنف'])
    qty_to_buy = st.number_input("الكمية المستلمة", min_value=1)
    
    if st.button("تحديث المخزن"):
        st.session_state.data['products'].loc[st.session_state.data['products']['الصنف'] == item_to_buy, 'المخزن'] += qty_to_buy
        st.success(f"تم إضافة {qty_to_buy} قطعة للمخزن")
        st.rerun()

# 5. إدارة الموردين
elif menu == "🚛 إدارة الموردين":
    st.title("سجل الموردين")
    st.dataframe(st.session_state.data['suppliers'], use_container_width=True)
    with st.expander("إضافة مورد جديد"):
        s_name = st.text_input("اسم المورد")
        s_phone = st.text_input("الهاتف")
        if st.button("حفظ المورد"):
            new_s = {"المورد": s_name, "الهاتف": s_phone, "المديونية": 0}
            st.session_state.data['suppliers'] = pd.concat([st.session_state.data['suppliers'], pd.DataFrame([new_s])], ignore_index=True)
            st.rerun()

# 6. إدارة العملاء
elif menu == "👥 إدارة العملاء":
    st.title("قاعدة بيانات العملاء")
    st.dataframe(st.session_state.data['customers'], use_container_width=True)

# 7. إدارة الموظفين
elif menu == "👔 إدارة الموظفين":
    st.title("شؤون الموظفين")
    st.dataframe(st.session_state.data['employees'], use_container_width=True)

# 8. الحضور والانصراف
elif menu == "⏰ الحضور والانصراف":
    st.title("⏰ الحضور والانصراف")
    emp = st.selectbox("اختر الموظف", st.session_state.data['employees']['الاسم'])
    c1, c2 = st.columns(2)
    if c1.button("تسجيل حضور"): st.success(f"تم تسجيل حضور {emp}")
    if c2.button("تسجيل انصراف"): st.warning(f"تم تسجيل انصراف {emp}")

# 9. إدارة المرتبات
elif menu == "💰 إدارة المرتبات":
    st.title("مسيرات الرواتب")
    st.dataframe(st.session_state.data['employees'][['الاسم', 'الراتب']], use_container_width=True)

# 10. إدارة المصروفات
elif menu == "📉 إدارة المصروفات":
    st.title("إدارة المصروفات")
    e_desc = st.text_input("وصف المصروف")
    e_amt = st.number_input("المبلغ", min_value=0)
    if st.button("تسجيل مصروف"):
        st.session_state.data['expenses'].append({"التاريخ": date.today(), "الوصف": e_desc, "المبلغ": e_amt})
        st.success("تم التسجيل")
        st.rerun()

# 11. التقارير
elif menu == "📈 التقارير":
    st.title("التقارير المالية والختامية")
    st.subheader("سجل المبيعات")
    st.dataframe(st.session_state.data['sales'], use_container_width=True)

# 12. الصلاحيات
elif menu == "🔒 الصلاحيات":
    st.title("الإعدادات والصلاحيات")
    st.write("إعدادات المستخدم: **المدير الرئيسي**")
    st.checkbox("تفعيل نظام الضرائب")
    st.checkbox("تفعيل الرسائل النصية للعملاء")
