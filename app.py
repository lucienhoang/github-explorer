import streamlit as st

st.title("GitHub Explorer")

tab1, tab2 = st.tabs(["🔍 Find a repo", "🏆 Top 10 Python Repos"])

with tab1:
    st.header("Search for a Repository")
    repo_name = st.text_input("Enter repository name (e.g., pytorch/pytorch)")
    if repo_name:
        st.write(f"You entered: {repo_name}")

with tab2:
    st.header("Top 10 Python Repositories by Stars")
    if st.button("Fetch Data"):
        st.write("The API will be called here...")
