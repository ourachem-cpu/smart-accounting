import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# 1. إعدادات المنصة الاحترافية للبيع
st.set_page_config(page_title="منصة المحاسب المحترف الذكية", page_icon="📈", layout="wide")

# تطبيق ثيم وتنسيق مريح جداً للعين للزبائن والتجار
st.markdown(
    """
    <style>
    .stApp { text-align: right; direction: rtl; background-color: #f8fafc; }
    div[data-testid="stMarkdownContainer"] > p { text-align: right; font-size: 16px; }
    label { text-align: right !important; display: block; width: 100%; font-weight: bold; color: #1e293b; }
    .stNumberInput input, .stTextInput input, .stSelectbox select { text-align: right !important; font-size: 17px; border-radius: 8px !important; }
    
    /* تنسيق كروت اللوحة الرئيسية */
    .dashboard-card { padding: 20px; border-radius: 12px; text-align: center; margin: 10px 0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); color: white; font-weight: bold; }
    .card-blue { background: linear-gradient(135deg, #1e3a8a, #3b82f6); }
    .card-green { background: linear-gradient(135deg, #065f46, #10b981); }
    .card-red { background: linear-gradient(135deg, #991b1b, #ef4444); }
    .login-box { background: white; padding: 40px; border-radius: 16px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); max-width: 450px; margin: 50px auto; }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. إدارة جلسة المستخدم (session_state)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""

# قاعدة بيانات المستخدمين المشتركين بالمنصة
USERS_DB = {
    "mohamed": {"password": "123456", "business_name": "شركة محمد للتجارة الذكية"},
    "admin": {"password": "admin", "business_name": "متجر الإدارة التجريبي"}
}

# شاشة تسجيل الدخول سهلة التصميم
if not st.session_state['logged_in']:
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.title("🎯 مرحباً بك في منصة المحاسب الذكي")
    st.write("أسهل نظام لإدارة تجارتك، فواتيرك، ومخازنك سحابياً.")
    st.divider()
    
    user_input = st.text_input("👤 اسم المستخدم:")
    pass_input = st.text_input("🔑 كلمة المرور:", type="password")
    
    if st.button("تسجيل الدخول الآمن", use_container_width=True, type="primary"):
        if user_input in USERS_DB and USERS_DB[user_input]["password"] == pass_input:
            st.session_state['logged_in'] = True
            st.session_state['username'] = user_input
            st.session_state['business_name'] = USERS_DB[user_input]["business_name"]
            st.success("🎉 تم تسجيل الدخول بنجاح!")
            st.rerun()
        else:
            st.error("❌ عذراً، بيانات الدخول غير صحيحة.")
    st.markdown("</div>", unsafe_allow_html=True)

# 3. تشغيل لوحة التحكم المتطورة بعد الدخول
else:
    user_id = st.session_state['username']
    DB_FILE = f"history_{user_id}.csv"
    EXPENSES_FILE = f"expenses_{user_id}.csv"

    # دالات التعامل الآمن مع البيانات لكل مستخدم
    def load_deals():
        if os.path.exists(DB_FILE):
            df = pd.read_csv(DB_FILE)
            df["التاريخ"] = pd.to_datetime(df["التاريخ"], errors='coerce')
            return df
        return pd.DataFrame(columns=["رقم الفاتورة", "التاريخ", "اسم المنتج", "الكمية المباعة", "إجمالي التكاليف", "إجمالي المبيعات", "صافي الربح/الخسارة"])

    def load_expenses():
        if os.path.exists(EXPENSES_FILE):
            df = pd.read_csv(EXPENSES_FILE)
            return df
        return pd.DataFrame(columns=["التاريخ", "التصنيف", "المبلغ"])

    deals_df = load_deals()
    expenses_df = load_expenses()

    # شريط علوي أنيق
    c_header, c_logout = st.columns([4, 1])
    with c_header:
        st.title(f"🏢 لوحة تحكم: {st.session_state['business_name']}")
    with c_logout:
        if st.button("🚪 خروج", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()
            
    st.divider()

    # تبويبات النظام الجديد (لوحة تحكم فورية بالبداية)
    tab_dash, tab_calc, tab_exp = st.tabs(["📊 نظرة عامة والملخص المالي", "🛍️ معالجة بيع وفاتورة جديدة", "💸 تسجيل نفقات عامة ومصاريف"])
    
    # التبويب الأول: اللوحة الذكية المتطورة للمستخدم
    with tab_dash:
        st.subheader("📈 الأداء العام للتجارة والمحل")
        
        # حسابات تراكمية سريعة
        total_sales_profit = deals_df["صافي الربح/الخسارة"].sum() if not deals_df.empty else 0
        total_opex = expenses_df["المبلغ"].sum() if not expenses_df.empty else 0
        real_net_profit = total_sales_profit - total_opex
        
        # كروت الأرقام الذكية الملونة
        c_m1, c_m2, c_m3 = st.columns(3)
        with c_m1:
            st.markdown(f"<div class='dashboard-card card-blue'><h4>📦 أرباح مبيعات المنتجات</h4><h2>{total_sales_profit:,.2f}</h2></div>", unsafe_allow_html=True)
        with c_m2:
            st.markdown(f"<div class='dashboard-card card-red'><h4>📉 إجمالي المصاريف والنفقات</h4><h2>{total_opex:,.2f}</h2></div>", unsafe_allow_html=True)
        with c_m3:
            card_style = "card-green" if real_net_profit >= 0 else "card-red"
            st.markdown(f"<div class='dashboard-card {card_style}'><h4>🥇 صافي الربح الحقيقي والنهائي</h4><h2>{real_net_profit:,.2f}</h2></div>", unsafe_allow_html=True)
            
        st.divider()
        
        # الرسوم البيانية المتطورة
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.write("📊 سجل مبيعات الصفقات والمنتجات الحالية:")
            if deals_df.empty:
                st.info("لا توجد مبيعات مسجلة حتى الآن لرسمها بيانيًا.")
            else:
                st.dataframe(deals_df, use_container_width=True, hide_index=True)
        with col_g2:
            st.write("📈 توزيع وهيكل المصاريف العامة:")
            if expenses_df.empty:
                st.info("لا توجد مصاريف تشغيلية لعرض مخططها.")
            else:
                fig_pie = px.pie(expenses_df, values="المبلغ", names="التصنيف", hole=0.3, color_discrete_sequence=px.colors.sequential.RdBu)
                st.plotly_chart(fig_pie, use_container_width=True)

    # التبويب الثاني: حاسبة الصفقات فائقة السهولة
    with tab_calc:
        st.subheader("🛍️ إضافة صفقة بيع جديدة للعملاء")
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            p_name = st.text_input("🏷️ اسم المنتج المباع:", value="هاتف ذكي Pro")
            qty = st.number_input("📦 الكمية المباعة (قطع):", min_value=1, value=10)
            c_cost = st.number_input("💵 تكلفة شراء القطعة الواحدة الكلية:", min_value=0.0, value=150.0)
        with col_in2:
            s_price = st.number_input("💰 سعر بيع القطعة الواحدة للزبون:", min_value=0.0, value=250.0)
            tax_r = st.number_input("٪ ضريبة القيمة المضافة إن وجدت (VAT):", min_value=0.0, value=15.0)
            
        # عملية حسابية فورية مبسطة
        t_cost = qty * c_cost
        sub_rev = qty * s_price
        t_tax = sub_rev * (tax_r / 100)
        t_revenue = sub_rev + t_tax
        s_profit = sub_rev - t_cost
        
        st.markdown(f"### 📊 النتيجة التقديرية الفورية: صافي ربح البضاعة هو **{s_profit:,.2f}**")
        
        if st.button("💾 ترحيل وحفظ عملية البيع في السجل", use_container_width=True, type="primary"):
            current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            inv_num = f"INV-{datetime.now().strftime('%M%S')}"
            
            new_deal = pd.DataFrame([{"رقم الفاتورة": inv_num, "التاريخ": current_time_str, "اسم المنتج": p_name, "الكمية المباعة": qty, "إجمالي التكاليف": t_cost, "إجمالي المبيعات": t_revenue, "صافي الربح/الخسارة": s_profit}])
            deals_df = pd.concat([deals_df, new_deal], ignore_index=True)
            deals_df.to_csv(DB_FILE, index=False, encoding='utf-8-sig')
            
            st.success("✅ تم حفظ الفاتورة بنجاح في قاعدة بياناتك المعزولة!")
            st.rerun()

    # التبويب الثالث: تسجيل نفقات بلمسة واحدة
    with tab_exp:
        st.subheader("💸 تسجيل المصاريف النثرية والتشغيلية للمتجر")
        col_ex1, col_ex2 = st.columns(2)
        with col_ex1:
            exp_cat = st.selectbox("📂 بند المصروف التشغيلي:", ["إيجارات ومستودعات", "رواتب موظفين", "فواتير عامة (كهرباء/إنترنت)", "تسويق وإعلانات مأجورة", "أخرى ونثريات صيانة"])
        with col_ex2:
            exp_amt = st.number_input("💵 مبلغ المصروف المدفوع بالكامل:", min_value=0.0, value=50.0)
            
        if st.button("💾 ترحيل وحفظ المصروف الحالي", use_container_width=True):
            current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            new_exp = pd.DataFrame([{"التاريخ": current_time_str, "التصنيف": exp_cat, "المبلغ": exp_amt}])
            expenses_df = pd.concat([expenses_df, new_exp], ignore_index=True)
            expenses_df.to_csv(EXPENSES_FILE, index=False, encoding='utf-8-sig')
            
            st.success("✅ تم تسجيل وتخصيص النفقة العامة للمحل بنجاح!")
            st.rerun()