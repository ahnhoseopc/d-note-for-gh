import streamlit as st

def main():
    st.header("DK Medical Agents", anchor="network", divider=True)

    cols = st.columns(5)
    with cols[2]:
        st.image("assets/dk_logo.png", width=200)

    cols = st.columns(5)
    with cols[0]: st.image("assets/march_hs.jpg", width=200)
    with cols[1]: st.image("assets/square_hs.jpg", width=200)

import forms.sidebar as sidebar

if __name__ == "__page__":
    main()
    sidebar.display()
