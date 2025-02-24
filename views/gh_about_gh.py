import streamlit as st

def main():
    st.header("좋은병원들 네트워크", anchor="network", divider=True)

    cols = st.columns(5)
    with cols[2]:
        st.image("assets/gh/gh_logo.png", width=200)

    cols = st.columns(5)
    with cols[0]: st.image("assets/gh/network_1.jpg", width=200)
    with cols[1]: st.image("assets/gh/network_2.jpg", width=200)
    with cols[2]: st.image("assets/gh/network_3.jpg", width=200)
    with cols[3]: st.image("assets/gh/network_4.jpg", width=200)
    with cols[4]: st.image("assets/gh/network_5.jpg", width=200)

    cols = st.columns(6)
    with cols[0]: st.image("assets/gh/network_6.jpg", width=200)
    with cols[1]: st.image("assets/gh/network_7.jpg", width=200)
    with cols[2]: st.image("assets/gh/network_8.jpg", width=200)
    with cols[3]: st.image("assets/gh/network_9.jpg", width=200)
    with cols[4]: st.image("assets/gh/network_10.jpg", width=200)
    with cols[5]: st.image("assets/gh/network_11.jpg", width=200)

    cols = st.columns(2)
    with cols[0]: st.image("https://www.moonhwa.or.kr/moonhwa/board/image.do?mId=68&id=gLIPvyTqKyW+zoW9e3tGypgPir8mJPqFvO0/L3mUun8=", width=500)
    with cols[1]: st.image("https://www.moonhwa.or.kr/moonhwa/board/image.do?mId=68&id=Bs40RWz9R+Hh8//twWklygJ3bggWUiqg5oAQxj4QmgY=", width=500)


import forms.sidebar as sidebar

if __name__ == "__page__":
    main()
    sidebar.display()
