import urllib.request
import json
import os
import re

def main():
    url = "https://api.github.com/users/kisalnelaka/repos?sort=pushed&per_page=20"
    token = os.getenv("GITHUB_TOKEN")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    if token:
        headers['Authorization'] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching repos: {e}")
        return

    markdown_lines = []
    count = 0
    EXCLUDED_REPOS = {'kisalnelaka', 'kisalnelaka.github.io', 'Eldertale', 'curd'}
    for repo in data:
        name = repo.get('name')
        if name in EXCLUDED_REPOS:
            continue
        # Exclude forks unless it's a recognized contribution repo
        if repo.get('fork') and name != 'ani-cli':
            continue
            
        url = repo.get('html_url')
        description = repo.get('description')
        if not description:
            description = 'Production repository.'
            
        markdown_lines.append(f"- ⚡ **[{name}]({url})** — {description}")
        count += 1
        
        # Only show the top 5
        if count >= 5:
            break

    repo_list = "\n".join(markdown_lines)
    
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        print(f"{readme_path} not found.")
        return
        
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()

    start_marker = "<!-- RECENT-REPOS:START -->"
    end_marker = "<!-- RECENT-REPOS:END -->"
    
    pattern = re.compile(f"({start_marker}).*?({end_marker})", re.DOTALL)
    
    # \1 matches the start marker, \2 matches the end marker
    new_readme = pattern.sub(rf"\1\n{repo_list}\n\2", readme_content)
    
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_readme)
        
    print("README.md updated successfully with recent repos.")

if __name__ == "__main__":
    main()
