import streamlit as st
import requests
import plotly.express as px


def get_python_repos():
    """Get repositories from GitHub API."""
    url = "https://api.github.com/search/repositories?q=language:python&sort=stars"
    r = requests.get(url)
    return r


st.title("GitHub Explorer")

tab1, tab2 = st.tabs(["🔍 Repo Lookup", "🏆 Top 10 Python Repos"])

with tab1:
    st.header("Repository Search")
    repo_name = st.text_input("Enter a repo name (e.g., pytorch/pytorch)")
    if repo_name:
        st.write(f"You entered: {repo_name}")

with tab2:
    st.header("Top 10 Python Repositories by Stars")
    if st.button("Fetch Data"):
        r = get_python_repos()
        # Convert the JSON response into a Python dict.
        response_dict = r.json()
        # Store the list of repo dictionaries.
        repo_dicts = response_dict["items"][:10]

        # Prepare information for plot.
        names = [repo["name"] for repo in repo_dicts]
        stars = [repo["stargazers_count"] for repo in repo_dicts]

        fig = px.bar(
            x=names,
            y=stars,
            labels={"x": "Repository", "y": "Stars"},
            title="Most-Starred Python Projects on GitHub",
        )

        # Embeded the plot into page.
        st.plotly_chart(fig)
