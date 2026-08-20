import os
import json
import urllib.request
from datetime import datetime, timezone

USERNAME = "kisalnelaka"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Target top priority projects (falls back to latest pushed if any not found)
TARGET_PROJECTS = ["TenancyOS", "aether"]

def gh_request(url):
    headers = {"User-Agent": "gh-profile-showcase", "Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f"  [warn] {url} -> {e}")
        return None

def fetch_showcase_repos():
    repos_data = []
    
    # Try fetching specified top projects
    for name in TARGET_PROJECTS:
        data = gh_request(f"https://api.github.com/repos/{USERNAME}/{name}")
        if data and not data.get("message"):
            repos_data.append(data)
            
    # If we need more, fetch latest non-fork public repositories
    if len(repos_data) < 2:
        all_repos = gh_request(f"https://api.github.com/users/{USERNAME}/repos?sort=pushed&per_page=10") or []
        for r in all_repos:
            if r["name"] not in [x["name"] for x in repos_data] and not r.get("fork") and r["name"] not in [USERNAME, f"{USERNAME}.github.io"]:
                repos_data.append(r)
                if len(repos_data) >= 2:
                    break
                    
    formatted = []
    for r in repos_data[:2]:
        name = r.get("name", "")
        desc = r.get("description") or "Production-ready open source system."
        lang = r.get("language") or "Full-Stack"
        stars = r.get("stargazers_count", 0)
        forks = r.get("forks_count", 0)
        issues = r.get("open_issues_count", 0)
        size_kb = r.get("size", 0)
        updated = (r.get("pushed_at") or "")[:10]
        license_name = r.get("license", {}).get("spdx_id") if r.get("license") else "MIT"
        
        formatted.append({
            "name": name,
            "description": desc,
            "language": lang,
            "stars": stars,
            "forks": forks,
            "issues": issues,
            "size": f"{size_kb} KB" if size_kb < 1024 else f"{round(size_kb/1024, 1)} MB",
            "updated": updated,
            "license": license_name or "MIT",
            "url": r.get("html_url", f"https://github.com/{USERNAME}/{name}")
        })
        
    return formatted

def xml_escape(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def generate_showcase():
    W, H = 860, 210
    repos = fetch_showcase_repos()

    def render_card(repo, x_offset):
        title = xml_escape(repo["name"].replace("-", " ").replace("_", " ").title())
        desc = repo["description"]
        
        # Word wrap description into 2 lines of max 56 chars
        words = desc.split()
        desc_lines = []
        cur = ""
        for w in words:
            if len(cur) + len(w) + 1 > 56:
                desc_lines.append(xml_escape(cur.strip()))
                cur = w + " "
                if len(desc_lines) == 2:
                    break
            else:
                cur += w + " "
        if len(desc_lines) < 2 and cur.strip():
            desc_lines.append(xml_escape(cur.strip()))
        while len(desc_lines) < 2:
            desc_lines.append("")

        lang = xml_escape(repo["language"])
        stars = repo["stars"]
        forks = repo["forks"]
        size = xml_escape(repo["size"])
        license_id = xml_escape(repo["license"])
        updated = xml_escape(repo["updated"])

        return f'''
  <g transform="translate({x_offset}, 55)">
    <text x="0" y="0" font-family="system-ui,-apple-system,sans-serif" font-size="17" font-weight="600" fill="#f0f6fc">{title}</text>
    <text x="0" y="20" font-family="'Courier New',Courier,monospace" font-size="10" fill="#c9a96e">{lang} · {license_id}</text>
    <line x1="0" y1="34" x2="380" y2="34" stroke="#30363d" stroke-width="1"/>
    
    <text x="0" y="55" font-family="system-ui,-apple-system,sans-serif" font-size="12" fill="#c9d1d9">{desc_lines[0]}</text>
    <text x="0" y="71" font-family="system-ui,-apple-system,sans-serif" font-size="12" fill="#c9d1d9">{desc_lines[1]}</text>
    
    <g transform="translate(0, 98)">
      <text x="0"   y="0" font-family="system-ui,-apple-system,sans-serif" font-size="20" font-weight="600" fill="#f0f6fc">{stars}</text>
      <text x="0"   y="16" font-family="system-ui,-apple-system,sans-serif" font-size="10" fill="#8b949e">stars</text>

      <text x="95"  y="0" font-family="system-ui,-apple-system,sans-serif" font-size="20" font-weight="600" fill="#f0f6fc">{forks}</text>
      <text x="95"  y="16" font-family="system-ui,-apple-system,sans-serif" font-size="10" fill="#8b949e">forks</text>

      <text x="190" y="0" font-family="system-ui,-apple-system,sans-serif" font-size="20" font-weight="600" fill="#f0f6fc">{size}</text>
      <text x="190" y="16" font-family="system-ui,-apple-system,sans-serif" font-size="10" fill="#8b949e">codebase size</text>
    </g>
    
    <text x="0" y="145" font-family="'Courier New',Courier,monospace" font-size="9" fill="#8b949e">last active: {updated}</text>
  </g>'''

    card_svgs = ""
    positions = [24, 450]
    for i, pos in enumerate(positions):
        if i < len(repos):
            card_svgs += render_card(repos[i], pos)

    svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="rule-grad" x1="0" y1="0" x2="0" y2="{H}" gradientUnits="userSpaceOnUse">
      <stop offset="0%"   stop-color="#c9a96e" stop-opacity="0"/>
      <stop offset="35%"  stop-color="#c9a96e" stop-opacity="0.9"/>
      <stop offset="65%"  stop-color="#c9a96e" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#c9a96e" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="8" stroke="#30363d" stroke-width="1" fill="none"/>
  <rect x="1" y="8" width="2.5" height="{H - 16}" rx="1" fill="url(#rule-grad)"/>

  <!-- Section label -->
  <text x="24" y="36" font-family="'Courier New',Courier,monospace" font-size="10" fill="#8b949e" letter-spacing="1.5">FEATURED REPOSITORIES</text>
  <text x="{W - 24}" y="36" text-anchor="end" font-family="'Courier New',Courier,monospace" font-size="9" fill="#8b949e">live metrics from GitHub API</text>
  <line x1="430" y1="20" x2="430" y2="{H - 20}" stroke="#30363d" stroke-width="1"/>

  {card_svgs}
</svg>'''
    return svg

def main():
    print("Generating showcase-card.svg from live GitHub data...")
    svg = generate_showcase()
    with open("showcase-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("  Written -> showcase-card.svg")

if __name__ == "__main__":
    main()
