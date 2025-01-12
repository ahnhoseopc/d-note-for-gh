import streamlit as st
from forms.contact import contact_form

@st.dialog("Contact Me")
def show_contact_form():
    contact_form()


# Main section Split into two
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")

with col1:
    st.image("./assets/20180310_hs_on_winter_mt.jpg", width=230)

with col2:
    st.title("Ahn Hoseop", anchor=False)
    st.write(
        "Senior Tech Engineer, assisting new business in DK Healthcare AI Section"
    )
    if st.button("✉️ Contact Me:"):
        show_contact_form()

# Experience & Qualifications
st.write("\n")
st.subheader("Experience & Qualifications", anchor=False)
st.write(
    """
    - 20 years of jard work.
    - strong on data and systems.
    """
)

# Skills
st.write("\n")
st.subheader("Hard skills", anchor=False)
st.write(
    """
    - Programming in Python, Java, C# and more
    - Databases in Oracle, MS SQLServer, Postgres.
    """
)
