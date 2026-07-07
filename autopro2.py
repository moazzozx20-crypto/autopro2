import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import random

# --- 1. إعدادات النظام الفائقة ---
st.set_page_config(page_title="AutoPro ERP - Enterprise AI", layout="wide", initial_sidebar_state="expanded")

# --- 2. المحرك البصري (Emerald Premium UI) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #f8fafc; }
    
    /* إخفاء حدود القائمة الجانبية نهائياً */
    [data-testid="stSidebar"] { background-color: #064e3b !important; border: none !important; }
    [data-testid="stSidebarNav"] { border: none !important; }
    section[data-testid="stSidebar"] > div { border: none !important; }
    [data-testid="stSidebar"] * { color: #ecfdf5 !important; }

    /* أزرار القائمة الجانبية */
    div[role="radiogroup"] { gap: 8px; padding: 10px; }
    div[role="radiogroup"] label {
        background-color: transparent; padding: 10px 15px !important;
        border-radius: 12px !important; transition: 0.3s; border: none !important;
    }
    div[role="radiogroup"] label:hover { background-color: #10b981 !important; }
    div[role="radiogroup"] label[data-selected="true"] { background-color: #10b981 !important; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    div[data-testid="stSelectionControlCard"] { display: none !important; }

    /* بطاقات ERP المتقدمة */
    .erp-card {
        background: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border-right: 6px solid #10b981; margin-bottom: 15px;
    }
    .stButton>button { background-color: #10b981; color: white; border-radius: 10px; font-weight: 600; border: none; height: 3em; width: 100%; }
    .stButton>button:hover { background-color: #059669; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. محرك البيانات الشامل (Integrated Database) ---
if 'erp' not in st.session_state:
    st.session_state.erp = {
        'coa': { # دليل الحسابات
            'الأصول': {'الخزينة': 100000.0, 'المخزن': 0.0, 'المدينون': 0.0},
            'الخصوم': {'الدائنون': 0.0, 'VAT': 0.0},
            'الإيرادات': {'المبيعات': 0.0},
            'المصروفات': {'تكلفة بضاعة': 0.0, 'رواتب': 0.0, 'نثريات': 0.0}
        },
        'inventory': pd.DataFrame(columns=["ID", "الماركة", "الموديل", "الصنف", "النوع", "الكمية", "التكلفة", "البيع"]),
        'customers': pd.DataFrame(columns=["ID", "الاسم", "الموبايل", "المديونية"]),
        'suppliers': pd.DataFrame(columns=["ID", "الاسم", "الموبايل", "المديونية"]),
        'employees': pd.DataFrame(columns=["ID", "الاسم", "الوظيفة", "الراتب"]),
        'ledger': [],
        'sales': []
    }
    # بيانات أولية للتجربة
    st.session_state.erp['inventory'] = pd.concat([st.session_state.erp['inventory'], pd.DataFrame([
        {"ID": 1, "الماركة": "تويوتا", "الموديل": "كورولا", "الصنف": "تيل فرامل", "النوع": "قطع غيار", "الكمية": 20, "التكلفة": 400, "البيع": 650},
        {"ID": 2, "الماركة": "هيونداي", "الموديل": "إلنترا", "الصنف": "فلتر زيت", "النوع": "قطع غيار", "الكمية": 50, "التكلفة": 100, "البيع": 180},
        {"ID": 3, "الماركة": "عالمي", "الموديل": "جميع الموديلات", "الصنف": "معطر سيارة", "النوع": "إكسسوار", "الكمية": 100, "التكلفة": 20, "البيع": 45}
    ])], ignore_index=True)

# --- 4. محرك المحاسبة و AI ---
def post_transaction(desc, dr_acc, cr_acc, amount):
    st.session_state.erp['ledger'].append({"التاريخ": date.today(), "البيان": desc, "مدين": dr_acc, "دائن": cr_acc, "المبلغ": amount})
    # تحديث الأرصدة
    for cat in st.session_state.erp['coa']:
        if dr_acc in st.session_state.erp['coa'][cat]: st.session_state.erp['coa'][cat][dr_acc] += amount
        if cr_acc in st.session_state.erp['coa'][cat]: st.session_state.erp['coa'][cat][cr_acc] -= amount

def ai_assistant(query):
    query = query.lower()
    inv = st.session_state.erp['inventory']
    if "مخزن" in query or "كمية" in query:
        low_stock = inv[inv['الكمية'] < 5]['الصنف'].tolist()
        return f"بناءً على بياناتي، المخزن يحتوي على {len(inv)} صنف. انتبه! هذه الأصناف قاربت على النفاد: {', '.join(low_stock) if low_stock else 'لا يوجد حالياً'}"
    elif "أرباح" in query or "فلوس" in query:
        sales = st.session_state.erp['coa']['الإيرادات']['المبيعات']
        return f"إجمالي مبيعاتك المسجلة حتى الآن هي {sales:,.2f} ج.م. هل تريد تحليل المصروفات أيضاً؟"
    return "أنا مساعد AutoPro الذكي، كيف يمكنني مساعدتك في إدارة المحل اليوم؟"

# --- 5. القائمة الجانبية ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>AutoPro ERP AI</h2>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("", [
        "🏠 لوحة التحكم", "🛒 المبيعات و POS", "📦 إدارة المخازن", "🧾 المشتريات", 
        "👥 إدارة العملاء", "🚛 إدارة الموردين", "👔 الموارد البشرية", "⚖️ المحاسبة والمالية", "🤖 مساعد AI"
    ])

# --- 6. الموديولات ---

# لوحة القيادة
if menu == "🏠 لوحة القيادة":
    st.title("التقرير الاستراتيجي")
    coa = st.session_state.erp['coa']
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f"<div class='erp-card'><h5>نقدية الخزينة</h5><h2>{coa['الأصول']['الخزينة']:,.0f}</h2></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='erp-card'><h5>إجمالي المبيعات</h5><h2>{coa['الإيرادات']['المبيعات']:,.0f}</h2></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='erp-card'><h5>عدد العملاء</h5><h2>{len(st.session_state.erp['customers'])}</h2></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='erp-card'><h5>عدد الأصناف</h5><h2>{len(st.session_state.erp['inventory'])}</h2></div>", unsafe_allow_html=True)
    
    st.divider()
    if st.session_state.erp['sales']:
        df_sales = pd.DataFrame(st.session_state.erp['sales'])
        st.plotly_chart(px.line(df_sales, x='Date', y='Total', title="نمو المبيعات اليومي"), use_container_width=True)

# إدارة العملاء
elif menu == "👥 إدارة العملاء":
    st.title("قاعدة بيانات العملاء")
    with st.expander("➕ إضافة عميل جديد"):
        with st.form("cust_form"):
            c_name = st.text_input("اسم العميل")
            c_phone = st.text_input("رقم الموبايل")
            if st.form_submit_button("حفظ العميل"):
                new_c = {"ID": len(st.session_state.erp['customers'])+1, "الاسم": c_name, "الموبايل": c_phone, "المديونية": 0}
                st.session_state.erp['customers'] = pd.concat([st.session_state.erp['customers'], pd.DataFrame([new_c])], ignore_index=True)
                st.success("تم الحفظ")
                st.rerun()
    st.dataframe(st.session_state.erp['customers'], use_container_width=True)

# مساعد AI
elif menu == "🤖 مساعد AI":
    st.title("🤖 مساعد AutoPro الذكي")
    st.info("اسألني عن المخزن، المبيعات، أو تحليل أداء المحل.")
    user_q = st.chat_input("بماذا يمكنني مساعدتك؟")
    if user_q:
        with st.chat_message("user"): st.write(user_q)
        with st.chat_message("assistant"): st.write(ai_assistant(user_q))

# المبيعات POS
elif menu == "🛒 المبيعات و POS":
    st.title("نقطة بيع متوافقة مع السيارات")
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("🔍 ابحث (مثلاً: تيل فرامل تويوتا)")
        inv = st.session_state.erp['inventory']
        filtered = inv[inv['الصنف'].str.contains(search) | inv['الماركة'].str.contains(search) | inv['الموديل'].str.contains(search)]
        st.dataframe(filtered[["الماركة", "الموديل", "الصنف", "الكمية", "البيع"]], use_container_width=True, hide_index=True)
        sel_p = st.selectbox("اختر الصنف للبيع", filtered['الصنف'])
        qty = st.number_input("الكمية", min_value=1)
        cust = st.selectbox("اختر العميل", st.session_state.erp['customers']['الاسم'] if not st.session_state.erp['customers'].empty else ["نقدي"])

    with col2:
        prod = inv[inv['الصنف'] == sel_p].iloc[0]
        total = prod['البيع'] * qty
        st.markdown(f"<div class='erp-card'><h5>إجمالي الفاتورة</h5><h2>{total:,.2f} ج.م</h2></div>", unsafe_allow_html=True)
        if st.button("تأكيد البيع وخصم المخزن"):
            if prod['الكمية'] >= qty:
                st.session_state.erp['inventory'].loc[inv['الصنف'] == sel_p, 'الكمية'] -= qty
                post_transaction(f"بيع {qty} {sel_p}", "الخزينة", "المبيعات", total)
                st.session_state.erp['sales'].append({"Date": date.today(), "Total": total})
                st.success("تم البيع وترحيل الحسابات!")
                st.rerun()
            else: st.error("الكمية غير كافية!")

# إدارة المخازن (مع أنواع السيارات)
elif menu == "📦 إدارة المخازن":
    st.title("إدارة المخزون العالمي")
    with st.expander("➕ إضافة قطعة غيار / إكسسوار جديد"):
        with st.form("inv_add"):
            c1, c2, c3 = st.columns(3)
            make = c1.selectbox("الماركة", ["تويوتا", "هيونداي", "كيا", "مرسيدس", "BMW", "شيري", "ميتسوبيشي", "إكسسوار عام"])
            model = c2.text_input("الموديل (مثلاً: كورولا / إلنترا)")
            type_p = c3.selectbox("النوع", ["قطع غيار ميكانيكا", "عفشة", "كهرباء", "إكسسوارات"])
            name_p = c1.text_input("اسم القطعة")
            qty_p = c2.number_input("الكمية")
            cost_p = c3.number_input("التكلفة")
            sale_p = c1.number_input("البيع")
            if st.form_submit_button("حفظ في السيستم"):
                new_item = {"ID": len(st.session_state.erp['inventory'])+1, "الماركة": make, "الموديل": model, "الصنف": name_p, "النوع": type_p, "الكمية": qty_p, "التكلفة": cost_p, "البيع": sale_p}
                st.session_state.erp['inventory'] = pd.concat([st.session_state.erp['inventory'], pd.DataFrame([new_item])], ignore_index=True)
                st.rerun()
    st.dataframe(st.session_state.erp['inventory'], use_container_width=True)

# المحاسبة المالية
elif menu == "⚖️ المحاسبة والمالية":
    st.title("النظام المحاسبي المتكامل")
    t1, t2, t3 = st.tabs(["📖 اليومية العامة", "📊 ميزان المراجعة", "📉 الأرباح والخسائر"])
    with t1:
        if st.session_state.erp['ledger']: st.table(pd.DataFrame(st.session_state.erp['ledger']))
        else: st.info("لا توجد قيود")
    with t2:
        rows = []
        for cat, subs in st.session_state.erp['coa'].items():
            for acc, val in subs.items(): rows.append({"الحساب": acc, "الرصيد": val})
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

# الموارد البشرية
elif menu == "👔 الموارد البشرية":
    st.title("إدارة الموظفين والرواتب")
    with st.expander("➕ إضافة موظف جديد"):
        with st.form("hr_form"):
            e_name = st.text_input("اسم الموظف")
            e_job = st.text_input("الوظيفة")
            e_sal = st.number_input("الراتب")
            if st.form_submit_button("حفظ"):
                new_e = {"ID": len(st.session_state.erp['employees'])+1, "الاسم": e_name, "الوظيفة": e_job, "الراتب": e_sal}
                st.session_state.erp['employees'] = pd.concat([st.session_state.erp['employees'], pd.DataFrame([new_e])], ignore_index=True)
                st.rerun()
    st.dataframe(st.session_state.erp['employees'], use_container_width=True)
