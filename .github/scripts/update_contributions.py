import urllib.request
import json
import os
import re

USERNAME = "kisalnelaka"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
README_PATH = "README.md"
START_MARKER = "<!-- CONTRIBUTIONS:START -->"
END_MARKER = "<!-- CONTRIBUTIONS:END -->"

def gh_request(url):
    headers = {
        "User-Agent": "gh-profile-contributions",
        "Accept": "application/vnd.github+json"
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f"[warn] GitHub API error for {url}: {e}")
        return None

def fetch_contributions(limit=6):
    # Search for PRs authored by user on non-owned repositories
    query = f"type:pr author:{USERNAME} -user:{USERNAME}"
    url = f"https://api.github.com/search/issues?q={urllib.parse.quote(query)}&sort=created&order=desc&per_page=20"
    
    data = gh_request(url)
    items = data.get("items", []) if data else []
    
    contributions = []
    seen_repos = set()

    for item in items:
        pr_title = item.get("title", "")
        pr_url = item.get("html_url", "")
        state = item.get("state", "open")
        # Check if merged
        pull_request = item.get("pull_request", {})
        merged_at = pull_request.get("merged_at")
        
        status_tag = "merged" if merged_at else state
        
        # repo url is like https://api.github.com/repos/owner/repo
        repo_api_url = item.get("repository_url", "")
        repo_full_name = "/".join(repo_api_url.split("/")[-2:]) if repo_api_url else ""
        repo_html_url = f"https://github.com/{repo_full_name}" if repo_full_name else pr_url

        if repo_full_name:
            contributions.append({
                "repo_name": repo_full_name,
                "repo_url": repo_html_url,
                "pr_title": pr_title,
                "pr_url": pr_url,
                "status": status_tag
            })
            if len(contributions) >= limit:
                break

    return contributions

def update_readme(contributions):
    if not os.path.exists(README_PATH):
        print(f"{README_PATH} not found.")
        return

    with open(README_PATH, "r", encoding="utf-8") as f:
        readme_content = f.read()

    if not contributions:
        # Fallback if no external PRs found or rate limited
        contributions_md = (
            "- *Actively contributing to open source ecosystems across Laravel, PHP core tooling, and decentralized networks.*"
        )
    else:
        lines = []
        for c in contributions:
            badge = "🟣 merged" if c["status"] == "merged" else "🟢 " + c["status"]
            lines.append(f"- [{c['repo_name']}]({c['repo_url']}) — [{c['pr_title']}]({c['pr_url']}) `({badge})`")
        contributions_md = "\n".join(lines)

    pattern = re.compile(rf"({re.escape(START_MARKER)}).*?({re.escape(END_MARKER)})", re.DOTALL)
    
    if pattern.search(readme_content):
        new_readme = pattern.sub(rf"\1\n{contributions_md}\n\2", readme_content)
    else:
        print("Markers not found in README.")
        return

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_readme)

    print("README updated with open source contributions.")

if __name__ == "__main__":
    contributions = fetch_contributions()
    update_readme(contributions)
