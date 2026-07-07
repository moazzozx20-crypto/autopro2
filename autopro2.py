import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import uuid

# --- 1. إعدادات النظام المتقدمة ---
st.set_page_config(page_title="AutoPro ERP Pro", layout="wide", initial_sidebar_state="expanded")

# --- 2. ستايل احترافي (Custom CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"]  { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .sale-card { background: white; padding: 20px; border-radius: 15px; border-right: 5px solid #007bff; margin-bottom: 10px; }
    .stButton>button { border-radius: 8px; font-weight: bold; height: 3em; }
    </style>
    """, unsafe_allow_value=True)

# --- 3. تهيئة البيانات (Database Simulation) ---
if 'init' not in st.session_state:
    st.session_state.init = True
    # بيانات الأصناف (8000 صنف)
    st.session_state.pro_products = pd.DataFrame([
        {"كود": "BK-001", "الصنف": "تيل فرامل تويوتا", "الماركة": "TOYOTA", "التوافق": "Corolla 2015-2022", "الرف": "A1", "التكلفة": 450, "البيع": 650, "المخزن": 45},
        {"كود": "OF-002", "الصنف": "فلتر زيت هيونداي", "الماركة": "MOBIS", "التوافق": "Elantra/Tucson", "الرف": "B2", "التكلفة": 120, "البيع": 185, "المخزن": 110},
        {"كود": "SP-003", "الصنف": "بوجيهات NGK ليزر", "الماركة": "NGK", "التوافق": "Most Japanese Cars", "الرف": "C1", "التكلفة": 800, "البيع": 1150, "المخزن": 15},
    ])
    st.session_state.pro_sales = []
    st.session_state.pro_expenses = []
    st.session_state.current_user = "أحمد محمد (المدير)"

# --- 4. القائمة الجانبية المتقدمة ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3003/3003184.png", width=80)
    st.title("AutoPro ERP")
    st.caption("نسخة المحترفين v1.2")
    st.write(f"👤 {st.session_state.current_user}")
    st.divider()
    menu = st.radio("القائمة الرئيسية", 
        ["📊 لوحة التحكم", "🛒 كاشير POS", "📦 المخازن", "🧾 المشتريات", "💸 المالية", "👥 الموظفين", "📈 التقارير"],
        format_func=lambda x: x)

# --- 5. موديول لوحة التحكم (Dashboard) ---
if menu == "📊 لوحة التحكم":
    st.title("📊 ملخص الأداء اللحظي")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("مبيعات اليوم", "15,200 ج.م", "+12%")
    c2.metric("صافي الأرباح", "3,850 ج.م", "+5%")
    c3.metric("نواقص المخزن", "18 صنف", "-3", delta_color="inverse")
    c4.metric("نقدية الخزينة", "9,420 ج.م")

    st.divider()
    col_chart, col_low = st.columns([2, 1])
    with col_chart:
        df_chart = pd.DataFrame({
            'اليوم': ['السبت', 'الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس'],
            'المبيعات': [5000, 7500, 6200, 11000, 9800, 15000],
            'الأرباح': [1200, 1800, 1400, 2500, 2100, 3800]
        })
        fig = px.area(df_chart, x='اليوم', y=['المبيعات', 'الأرباح'], title="مؤشر النمو الأسبوعي", barmode='group')
        st.plotly_chart(fig, use_container_width=True)
    
    with col_low:
        st.subheader("⚠️ تنبيه النواقص")
        st.table(st.session_state.pro_products[st.session_state.pro_products['المخزن'] < 20][['الصنف', 'المخزن']])

# --- 6. موديول الكاشير (POS) ---
elif menu == "🛒 كاشير POS":
    st.title("🛒 نقطة البيع السريع")
    col_search, col_cart = st.columns([2, 1])
    
    with col_search:
        search = st.text_input("🔍 بحث ذكي (اسم، كود، توافق السيارة)...", placeholder="اكتب Corolla أو تيل فرامل...")
        df = st.session_state.pro_products
        results = df[df['الصنف'].str.contains(search) | df['كود'].str.contains(search) | df['التوافق'].str.contains(search)]
        
        for idx, row in results.iterrows():
            with st.container():
                st.markdown(f"""
                <div class='sale-card'>
                    <b>{row['الصنف']}</b> - {row['الماركة']}<br/>
                    <small>الكود: {row['كود']} | التوافق: {row['التوافق']} | <b>الرف: {row['الرف']}</b></small><br/>
                    <span style='color:green; font-weight:bold;'>السعر: {row['البيع']} ج.م</span>
                </div>
                """, unsafe_allow_value=True)
                if st.button(f"إضافة للفاتورة", key=f"btn_{idx}"):
                    st.toast(f"تمت إضافة {row['الصنف']}")

    with col_cart:
        st.subheader("🧾 الفاتورة")
        st.info("رقم الفاتورة: #INV-1092")
        st.write("---")
        st.write("1x تيل فرامل تويوتا = 650 ج.م")
        st.write("2x فلتر زيت هيونداي = 370 ج.م")
        st.divider()
        subtotal = 1020
        tax = subtotal * 0.14
        discount = st.number_input("الخصم (نسبة %)", 0, 100, 0)
        final = (subtotal + tax) * (1 - discount/100)
        
        st.markdown(f"### الإجمالي: {subtotal} ج.م")
        st.write(f"الضريبة (14%): {tax} ج.م")
        st.markdown(f"## الصافي: {final:.2f} ج.م")
        
        c1, c2 = st.columns(2)
        if c1.button("✅ حفظ وطباعة"): st.success("تم الحفظ")
        if c2.button("❌ إلغاء"): st.warning("تم الإلغاء")

# --- 7. موديول المخازن ---
elif menu == "📦 المخازن":
    st.title("📦 إدارة المخزون المركزي")
    st.dataframe(st.session_state.pro_products, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: st.button("📥 استيراد من Excel")
    with col2: st.button("📤 تصدير الجرد")
    with col3: st.button("🏷️ طباعة باركود الأصناف")

# --- 8. موديول المالية ---
elif menu == "💸 المالية":
    st.title("💸 المالية والمصروفات")
    tab1, tab2 = st.tabs(["سجل المصروفات", "حركة الخزينة"])
    with tab1:
        c1, c2, c3 = st.columns(3)
        desc = c1.text_input("بند الصرف")
        amt = c2.number_input("المبلغ", min_value=0)
        cat = c3.selectbox("التصنيف", ["إيجار", "كهرباء", "بوفيه", "نقل", "أخرى"])
        if st.button("تسجيل مصروف"): st.success("تم التسجيل")
        
    with tab2:
        st.metric("الرصيد الحالي في الخزينة", "9,420 ج.م")
        st.table(pd.DataFrame([
            {"التاريخ": "2024-05-01", "النوع": "مبيعات", "المبلغ": "+1500", "البيان": "فاتورة #1091"},
            {"التاريخ": "2024-05-01", "النوع": "مصروف", "المبلغ": "-200", "البيان": "كهرباء المحل"},
        ]))

# --- 9. موديول الموظفين ---
elif menu == "👥 الموظفين":
    st.title("👥 شؤون الموظفين والعمولات")
    st.table(pd.DataFrame([
        {"الموظف": "أحمد محمد", "الراتب": 5000, "المبيعات": 45000, "العمولة (1%)": 450, "إجمالي": 5450},
        {"الموظف": "هاني شاكر", "الراتب": 4500, "المبيعات": 22000, "العمولة (1%)": 220, "إجمالي": 4720},
    ]))
    st.button("إصدار مسيرات الرواتب الشهرية")

# --- 10. موديول التقارير ---
elif menu == "📈 التقارير":
    st.title("📈 التقارير الاستراتيجية")
    rep_type = st.selectbox("نوع التقرير", ["أرباح وخسائر", "حركة صنف", "الأكثر مبيعاً"])
    if rep_type == "أرباح وخسائر":
        st.write("تقرير الفترة من 1-5 إلى 30-5")
        st.json({"إجمالي المبيعات": 150000, "تكلفة البضاعة": 110000, "المصاريف": 5000, "صافي الربح": 35000})
