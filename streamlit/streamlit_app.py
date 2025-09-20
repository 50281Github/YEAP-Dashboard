import streamlit as st
import st_general_dashboard
import st_q345_dashboard
import st_q6q7q10q11_dashboard

st.set_page_config(layout="wide")

# 添加自定义CSS样式，将标题设置为浅灰色
st.markdown("""
<style>
.main-title {
    color: #9E9E9E !important;
    font-size: 2.5rem !important;
    font-weight: 600 !important;
    margin-bottom: 1rem !important;
}
</style>
""", unsafe_allow_html=True)

# 使用自定义样式的标题
st.markdown('<h1 class="main-title">Data Analysis Dashboard</h1>', unsafe_allow_html=True)

PAGES = {
    "General Dashboard": st_general_dashboard,
    "Q3, Q4, Q5 Analysis": st_q345_dashboard,
    "Q6, Q7, Q10, Q11 Analysis": st_q6q7q10q11_dashboard,
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]

# Check if the selected page has a create_layout function
if hasattr(page, 'create_layout'):
    page.create_layout()
else:
    st.error("The selected page does not have a create_layout function.")