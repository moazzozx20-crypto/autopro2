import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- 1. إعدادات النظام ---
st.set_page_config(page_title="AutoPro ERP Pro", layout="wide", initial_sidebar_state="expanded")

# --- 2. ستايل احترافي (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"]  { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .sale-card { background: white; padding: 15px; border-radius: 10px; border-right: 5px solid #007bff; margin-bottom: 10px; color: #333; }
    .stButton>button { border-radius: 8px; font-weight: bold; height: 3em; width: 100%; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. تهيئة البيانات ---
if 'init' not in st.session_state:
    st.session_state.init = True
    st.session_state.pro_products = pd.DataFrame([
        {"كود": "BK-001", "الصنف": "تيل فرامل تويوتا", "الماركة": "TOYOTA", "التوافق": "Corolla 2015-2022", "الرف": "A1", "التكلفة": 450, "البيع": 650, "المخزن": 45},
        {"كود": "OF-002", "الصنف": "فلتر زيت هيونداي", "الماركة": "MOBIS", "التوافق": "Elantra/Tucson", "الرف": "B2", "التكلفة": 120, "البيع": 185, "المخزن": 110},
        {"كود": "SP-003", "الصنف": "بوجيهات NGK ليزر", "الماركة": "NGK", "التوافق": "Most Cars", "الرف": "C1", "التكلفة": 800, "البيع": 1150, "المخزن": 15},
    ])
    st.session_state.current_user = "أحمد محمد (المدير)"

# --- 4. القائمة الجانبية ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3003/3003184.png", width=80)
    st.title("AutoPro ERP")
    st.write(f"👤 {st.session_state.current_user}")
    st.divider()
    menu = st.radio("القائمة الرئيسية", ["📊 لوحة التحكم", "🛒 كاشير POS", "📦 المخازن", "💸 المالية", "👥 الموظفين", "📈 التقارير"])

# --- 5. موديول لوحة التحكم ---
if menu == "📊 لوحة التحكم":
    st.title("📊 ملخص الأداء اللحظي")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("مبيعات اليوم", "15,200 ج.م", "+12%")
    c2.metric("صافي الأرباح", "3,850 ج.م", "+5%")
    c3.metric("نواقص المخزن", "18 صنف", "-3", delta_color="inverse")
    c4.metric("نقدية الخزينة", "9,420 ج.م")

    st.divider()
    df_chart = pd.DataFrame({
        'اليوم': ['السبت', 'الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس'],
        'المبيعات': [5000, 7500, 6200, 11000, 9800, 15000]
    })
    fig = px.area(df_chart, x='اليوم', y='المبيعات', title="منحنى النمو الأسبوعي")
    st.plotly_chart(fig, use_container_width=True)

# --- 6. موديول الكاشير (POS) ---
elif menu == "🛒 كاشير POS":
    st.title("🛒 نقطة البيع السريع")
    col_search, col_cart = st.columns([2, 1])
    
    with col_search:
        search = st.text_input("🔍 بحث عن صنف...", placeholder="اكتب اسم القطعة أو الكود...")
        df = st.session_state.pro_products
        results = df[df['الصنف'].str.contains(search) | df['كود'].str.contains(search)]
        
        for idx, row in results.iterrows():
            st.markdown(f"<div class='sale-card'><b>{row['الصنف']}</b> | السعر: {row['البيع']} ج.م | الرف: {row['الرف']}</div>", unsafe_allow_html=True)
            if st.button(f"إضافة للفاتورة {idx}", key=f"btn_{idx}"):
                st.toast(f"تمت إضافة {row['الصنف']}")

    with col_cart:
        st.subheader("🧾 الفاتورة")
        st.write("1x تيل فرامل تويوتا = 650 ج.م")
        st.write("2x فلتر زيت هيونداي = 370 ج.م")
        st.divider()
        st.markdown("### الإجمالي: 1020 ج.م")
        if st.button("✅ حفظ وطباعة"):
            st.success("تم الحفظ بنجاح")

# --- 7. موديول المخازن ---
elif menu == "📦 المخازن":
    st.title("📦 إدارة المخزون")
    st.dataframe(st.session_state.pro_products, use_container_width=True)
    st.button("📥 استيراد بضاعة من Excel")

# --- 8. موديول المالية ---
elif menu == "💸 المالية":
    st.title("💸 المالية والمصروفات")
    st.metric("رصيد الخزينة الحالي", "9,420 ج.م")
    st.text_input("بند مصروف جديد")
    st.number_input("المبلغ")
    st.button("تسجيل مصروف")

# --- 9. موديول الموظفين ---
elif menu == "👥 الموظفين":
    st.title("👥 الموظفين والعمولات")
    st.table(pd.DataFrame([
        {"الموظف": "أحمد محمد", "المبيعات": 45000, "العمولة": 450, "الراتب": 5450},
        {"الموظف": "هاني شاكر", "المبيعات": 22000, "العمولة": 220, "الراتب": 4720},
    ]))

# --- 10. موديول التقارير ---
elif menu == "📈 التقارير":
    st.title("📈 التقارير المالية")
    st.info("صافي أرباح الشهر الحالي: 35,000 ج.م")
