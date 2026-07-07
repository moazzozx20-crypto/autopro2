import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date

# --- 1. الإعدادات العامة للمنصة ---
st.set_page_config(page_title="AutoPro ERP | Professional Edition", layout="wide", initial_sidebar_state="expanded")

# --- 2. التصميم الاحترافي (Advanced CSS Injection) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');
    
    /* الخط العام */
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    
    /* لون الخلفية العام */
    .main { background-color: #f0f2f6; }
    
    /* تصميم البطاقات الإحصائية */
    .metric-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border-bottom: 4px solid #1E3A8A;
        transition: transform 0.3s;
    }
    .metric-card:hover { transform: translateY(-5px); }
    
    /* تعديل شريط التنقل الجانبي */
    [data-testid="stSidebar"] { background-color: #1E3A8A; color: white; }
    [data-testid="stSidebar"] * { color: white !important; }
    
    /* تصميم الجداول */
    .stDataFrame { border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    
    /* أزرار مخصصة */
    .stButton>button {
        background-color: #1E3A8A;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        height: 3em;
        border: none;
        width: 100%;
    }
    .stButton>button:hover { background-color: #2563EB; border: none; }
    
    /* العناوين */
    h1, h2, h3 { color: #1E3A8A; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. إدارة حالة النظام (Session State) ---
if 'db' not in st.session_state:
    st.session_state.db = {
        "products": pd.DataFrame([
            {"كود": "BK-001", "الصنف": "تيل فرامل تويوتا", "المخزن": 45, "التكلفة": 450, "البيع": 650, "المورد": "النيل لقطع الغيار"},
            {"كود": "OF-002", "الصنف": "فلتر زيت هيونداي", "المخزن": 110, "التكلفة": 120, "البيع": 185, "المورد": "المركز التجاري"},
        ]),
        "sales": [],
        "purchases": [],
        "suppliers": ["النيل لقطع الغيار", "المركز التجاري", "عالم المحركات"],
        "customers": ["أحمد علي", "شركة النقل السريع", "عميل نقدي"],
        "employees": pd.DataFrame([
            {"الاسم": "محمد حسن", "الوظيفة": "بائع", "الراتب": 6000, "الحالة": "حاضر"},
            {"الاسم": "سارة محمود", "الوظيفة": "محاسب", "الراتب": 8000, "الحالة": "حاضر"},
        ]),
        "expenses": []
    }

# --- 4. القائمة الجانبية (Navigation Menu) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: white;'>AutoPro ERP</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 0.8em;'>نظام إدارة متكامل v2.0</p>", unsafe_allow_html=True)
    st.divider()
    
    # تقسيم الموديولات بشكل احترافي
    st.subheader("📊 العمليات والتقارير")
    menu = st.radio("", [
        "لوحة القيادة Dashboard",
        "إدارة المبيعات",
        "إدارة المخازن",
        "إدارة المشتريات",
        "إدارة الموردين",
        "إدارة العملاء",
        "إدارة الموظفين",
        "الحضور والانصراف",
        "المرتبات",
        "إدارة المصروفات",
        "التقارير المالية",
        "الصلاحيات والإعدادات"
    ])

# --- 5. منطق الموديولات ---

# 1. لوحة القيادة
if menu == "لوحة القيادة Dashboard":
    st.title("📈 لوحة القيادة")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown("<div class='metric-card'><h4>مبيعات اليوم</h4><h2>14,500 ج.م</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='metric-card'><h4>المشتريات</h4><h2>8,200 ج.م</h2></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='metric-card'><h4>إجمالي العملاء</h4><h2>245</h2></div>", unsafe_allow_html=True)
    with c4: st.markdown("<div class='metric-card'><h4>رصيد الخزينة</h4><h2>32,400 ج.م</h2></div>", unsafe_allow_html=True)
    
    st.divider()
    col_chart, col_recent = st.columns([2, 1])
    with col_chart:
        df_chart = pd.DataFrame({'الشهر': ['يناير', 'فبراير', 'مارس', 'ابريل'], 'المبيعات': [20, 35, 30, 45]})
        fig = px.bar(df_chart, x='الشهر', y='المبيعات', title="تحليل المبيعات الشهرية", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    with col_recent:
        st.subheader("آخر العمليات")
        st.info("تم بيع تيل فرامل لعميل أحمد علي")
        st.success("تم استلام بضاعة من مورد النيل")
        st.warning("مصروف: فاتورة كهرباء 450 ج.م")

# 2. إدارة المبيعات (POS)
elif menu == "إدارة المبيعات":
    st.title("🛒 نقطة البيع (POS)")
    col_pos, col_bill = st.columns([2, 1])
    with col_pos:
        st.text_input("🔍 بحث عن صنف (اسم أو كود)...")
        st.dataframe(st.session_state.db["products"][["الصنف", "كود", "البيع", "المخزن"]], use_container_width=True)
        if st.button("إضافة الصنف المختار للفاتورة"):
            st.toast("تمت إضافة الصنف")
    with col_bill:
        st.subheader("الفاتورة")
        st.write("1x تيل فرامل = 650 ج.م")
        st.divider()
        st.write("### الإجمالي: 650 ج.م")
        st.button("إتمام البيع وطباعة")

# 3. إدارة المخازن
elif menu == "إدارة المخازن":
    st.title("📦 إدارة المخازن")
    st.dataframe(st.session_state.db["products"], use_container_width=True)
    c1, c2 = st.columns(2)
    with c1: st.button("تعديل كمية صنف")
    with c2: st.button("تحميل تقرير الجرد (Excel)")

# 4. إدارة المشتريات
elif menu == "إدارة المشتريات":
    st.title("🧾 إدارة المشتريات")
    with st.expander("إضافة فاتورة مشتريات جديدة"):
        st.selectbox("المورد", st.session_state.db["suppliers"])
        st.text_input("رقم فاتورة المورد")
        st.date_input("تاريخ الاستلام")
        st.button("حفظ المشتريات وزيادة المخزن")

# 5. إدارة الموردين
elif menu == "إدارة الموردين":
    st.title("🚛 إدارة الموردين")
    st.table(pd.DataFrame({"اسم المورد": st.session_state.db["suppliers"], "الحساب": [12000, 0, 5400], "آخر توريد": ["2024-05-01", "2024-04-15", "2024-05-02"]}))
    st.button("إضافة مورد جديد")

# 6. إدارة العملاء
elif menu == "إدارة العملاء":
    st.title("👥 إدارة العملاء")
    st.table(pd.DataFrame({"اسم العميل": st.session_state.db["customers"], "إجمالي المشتريات": [1500, 12000, 450], "النقاط": [10, 120, 5]}))
    st.button("إضافة عميل")

# 7. إدارة الموظفين
elif menu == "إدارة الموظفين":
    st.title("👔 شؤون الموظفين")
    st.dataframe(st.session_state.db["employees"], use_container_width=True)
    st.button("إضافة موظف جديد")

# 8. الحضور والانصراف
elif menu == "الحضور والانصراف":
    st.title("⏰ سجل الحضور والانصراف")
    st.write("تاريخ اليوم:", date.today())
    st.table(pd.DataFrame({"الموظف": ["محمد حسن", "سارة محمود"], "وقت الحضور": ["09:00 ص", "08:55 ص"], "الحالة": ["منضبط", "منضبط"]}))
    st.button("تسجيل حضور موظف")

# 9. المرتبات
elif menu == "المرتبات":
    st.title("💸 مسيرات الرواتب")
    st.table(pd.DataFrame({"الموظف": ["محمد حسن", "سارة محمود"], "الراتب الأساسي": [6000, 8000], "العمولات": [450, 0], "الصافي": [6450, 8000]}))
    st.button("صرف الرواتب")

# 10. إدارة المصروفات
elif menu == "إدارة المصروفات":
    st.title("📉 إدارة المصروفات")
    c1, c2 = st.columns(2)
    with c1: st.text_input("بند المصروف")
    with c2: st.number_input("المبلغ")
    st.button("تسجيل مصروف")

# 11. التقارير المالية
elif menu == "التقارير المالية":
    st.title("📈 التقارير المالية والختامية")
    tab1, tab2 = st.tabs(["أرباح وخسائر", "كشف حساب"])
    with tab1:
        st.write("صافي الربح للفترة الحالية")
        st.success("45,000 ج.م")
    with tab2:
        st.write("تحميل كشوفات الحسابات التفصيلية")

# 12. الصلاحيات
elif menu == "الصلاحيات والإعدادات":
    st.title("⚙️ الإعدادات والصلاحيات")
    st.checkbox("السماح للبائع بالخصم")
    st.checkbox("تفعيل الفاتورة الإلكترونية")
    st.selectbox("صلاحية المستخدم", ["مدير", "محاسب", "كاشير"])
    st.button("حفظ الإعدادات")
