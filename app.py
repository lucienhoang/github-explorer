import plotly.express as px
import requests
import streamlit as st


def get_python_repos():
    """Get repositories from GitHub API."""
    url = "https://api.github.com/search/repositories?q=language:python&sort=stars"
    r = requests.get(url)
    return r


def get_single_repo(repo_name):
    """Get a single repository's info from GitHub API."""
    url = f"https://api.github.com/repos/{repo_name}"
    r = requests.get(url, timeout=10)
    return r


st.title("GitHub Explorer")

tab1, tab2 = st.tabs(["🔍 Repo Lookup", "🏆 Top 10 Python Repos"])

with tab1:
    st.header("Repository Search")
    repo_name = st.text_input("Enter a repo name (e.g., pytorch/pytorch)")

    if repo_name:
        with st.spinner("Fetching data from GitHub..."):
            try:
                r = get_single_repo(repo_name)

                if r.status_code == 404:
                    st.error(
                        f"Repository '{repo_name}' not found. Check the spelling (e.g., owner/repo)."
                    )
                elif r.status_code == 403:
                    st.error("GitHub API rate limit exceeded. Please try again later.")
                elif r.status_code != 200:
                    st.error(
                        f"GitHub API returned an error (status code {r.status_code})."
                    )
                else:
                    repo = r.json()
                    st.subheader(repo["full_name"])
                    st.write(repo["description"])

                    col1, col2, col3 = st.columns(3)
                    col1.metric("⭐ Stars", repo["stargazers_count"])
                    col2.metric("🍴 Forks", repo["forks_count"])
                    col3.metric("🐛 Open Issues", repo["open_issues_count"])

                    st.write(f"**Language:** {repo['language']}")
                    st.write(f"[View on GitHub]({repo['html_url']})")

            except requests.exceptions.Timeout:
                st.error("The request took too long. Please try again.")
            except requests.exceptions.RequestException as e:
                st.error(f"Network error: could not reach GitHub. ({e})")

with tab2:
    st.header("Top 10 Python Repositories by Stars")
    if st.button("Fetch Data"):
        with st.spinner("Fetching data from GitHub..."):
            try:
                r = get_python_repos()

                if r.status_code == 403:
                    st.error("GitHub API rate limit exceeded. Please try again later.")
                elif r.status_code != 200:
                    st.error(
                        f"GitHub API returned an error (status code {r.status_code})."
                    )
                else:
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
            except requests.exceptions.RequestException as e:
                st.error(f"Network error: could not reach GitHub. ({e})")
