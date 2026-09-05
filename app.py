import plotly.express as px
import requests
import streamlit as st


def get_repos_by_language(language):
    """Get top repositories for a given language from GitHub API."""
    url = f"https://api.github.com/search/repositories?q=language:{language}&sort=stars"
    r = requests.get(url, timeout=10)
    return r


def get_single_repo(repo_name):
    """Get a single repository's info from GitHub API."""
    url = f"https://api.github.com/repos/{repo_name}"
    r = requests.get(url, timeout=10)
    return r


def render_language_tab(language, display_name):
    """Render a tab showing top 10 repos for a given language."""
    st.header(f"Top 10 {display_name} Repositories by Stars")
    if st.button("Fetch Data", key=f"fetch_{language}"):
        with st.spinner("Fetching data from GitHub..."):
            try:
                r = get_repos_by_language(language)

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
                    descriptions = [repo["description"] for repo in repo_dicts]
                    links = [repo["html_url"] for repo in repo_dicts]
                    desc_texts = [d if d else "No description" for d in descriptions]

                    fig = px.bar(
                        x=names,
                        y=stars,
                        labels={"x": "Repository", "y": "Stars"},
                        title=f"Most-Starred {display_name} Projects on GitHub",
                    )

                    fig.update_traces(
                        customdata=desc_texts,
                        hovertemplate="<b>%{x}</b><br>Stars: %{y}<br>%{customdata}<extra></extra>",
                    )

                    # Embeded the plot into page.
                    st.plotly_chart(fig)

                    # Show a list of clickable links below the chart.
                    st.subheader("Repository Links")
                    for name, desc, link in zip(names, descriptions, links):
                        st.markdown(f"**[{name}]({link})** - {desc}")

            except requests.exceptions.Timeout:
                st.error("The request took too long. Please try again.")

            except requests.exceptions.RequestException as e:
                st.error(f"Network error: could not reach GitHub. ({e})")


st.title("GitHub Explorer")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🔍 Repo Lookup", "🏆 Python", "☕ Java", "🐹 Go", "🔧 C"]
)

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
    render_language_tab("python", "Python")

with tab3:
    render_language_tab("java", "Java")

with tab4:
    render_language_tab("go", "Go")

with tab5:
    render_language_tab("c", "C")
