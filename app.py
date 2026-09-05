import streamlit as st

st.title("GitHub Explorer")
st.write("Xin chào. Đây là app đầu tiên của Lucien.")

name = st.text_input("Nhập tên của bạn:")
if name:
    st.write(f"Chào {name}! 👋")
