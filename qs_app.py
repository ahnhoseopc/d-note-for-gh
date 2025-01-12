import streamlit as st

# page setup
zs_about_page = st.Page(
    page="views/about_me.py",
    title="About Me",
    icon=":material/account_circle:",
    default=True
)

zs_project_1_page = st.Page(
    page="views/sales_dashboard.py",
    title="Sales Dashboard",
    icon=":material/bar_chart:",
    default=False
)

zs_project_2_page = st.Page(
    page="views/chatbot.py",
    title="Chat Bot",
    icon=":material/smart_toy:",
    default=False
)

#pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

pg = st.navigation(
    {
        "Info": [zs_about_page],
        "Projects": [zs_project_1_page, zs_project_2_page],
    }
)
# shared on all pages
st.logo("assets/dk_logo.png")
st.sidebar.text("Made with ❤️❤️ by Hoseop")

# Run Navigation
pg.run()
