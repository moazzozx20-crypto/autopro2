import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- 1. إعدادات النظام المتقدمة ---
st.set_page_config(page_title="AutoPro ERP Pro", layout="wide", initial_sidebar_state="expanded")

# --- 2. تصحيح الستايل (Custom CSS) ---
# تم تصحيح unsafe_allow_html هنا
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

# --- 3. تهيئة البيانات (Database Simulation) ---
if 'init' not in st.session_state:
    st.session_state.init = True
    st.session_state.pro_products = pd.DataFrame([
        {"كود": "BK-001", "الصنف": "تيل فرامل تويوتا", "الماركة": "TOYOTA", "التوافق": "Corolla 2015-2022", "الرف": "A1", "التكلفة": 450, "البيع": 650, "المخزن": 45},
        {"كود": "OF-002", "الصنف": "فلتر زيت هيونداي", "الماركة": "MOBIS", "التوافق": "Elantra/Tucson", "الرف": "B2", "التكلفة": 120, "البيع": 185, "المخزن": 110},
        {"كود": "SP-003", "الصنف": "بوجيهات NGK ليزر", "الماركة": "NGK", "التوافق": "Most Japanese Cars", "الرف": "C1", "التكلفة": 800, "البيع": 1150, "المخزن": 15},
    ])
    st.session_state.current_user = "أحمد محمد (المدير)"

# --- 4. القائمة الجانبية ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3003/3003184.png", width=80)
    st.title("AutoPro ERP")
    st.write(f"👤 {st.session_state.current_user}")
    st.divider()
    menu = st.radio("القائمة الرئيسية", 
        ["📊 لوحة التحكم", "🛒 كاشير POS", "📦 المخازن", "💸 المالية", "👥 الموظفين", "📈 التقارير"])

# --- 5. موديول لوحة التحكم ---
if menu == "📊 لوحة التحكم":
    st.title("📊 ملخص الأداء اللحظي")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("مبيعات اليوم", "15,200 ج.م", "+12%")
    c2.metric("صافي الأرباح", "3,850 ج.م", "+5%")
    c3.metric("نواقص المخزن", "
