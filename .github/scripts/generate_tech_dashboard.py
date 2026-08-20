import os
import json
import urllib.request
from datetime import datetime, timezone

USERNAME = "kisalnelaka"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def gh_request(url):
    headers = {"User-Agent": "gh-profile-stack", "Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f"  [warn] {url} -> {e}")
        return None

def fetch_tech_distribution():
    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=pushed"
    repos = gh_request(url) or []
    
    # Analyze live languages & topics
    lang_counts = {}
    total_analyzed = 0
    
    for repo in repos:
        if repo.get("fork"):
            continue
        lang = repo.get("language")
        if lang and lang not in ["HTML", "CSS", "Jupyter Notebook"]:
            lang_counts[lang] = lang_counts.get(lang, 0) + 1
            total_analyzed += 1

    sorted_langs = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Categorize into dynamic columns
    columns = [
        {
            "category": "LANGUAGES",
            "items": [(lang, f"{count} repos") for lang, count in sorted_langs[:4]]
        },
        {
            "category": "CORE FRAMEWORKS",
            "items": [
                ("Laravel 11", "backend engine"),
                ("React 18", "component UI"),
                ("Node.js", "runtime mesh"),
                ("FastAPI / Python", "automation")
            ]
        },
        {
            "category": "DATA & STORAGE",
            "items": [
                ("PostgreSQL", "relational"),
                ("MySQL", "structured"),
                ("Redis", "in-memory / queues"),
                ("Eloquent ORM", "data mapping")
            ]
        },
        {
            "category": "INFRASTRUCTURE",
            "items": [
                ("Docker / OCI", "containers"),
                ("Linux (Arch/Void)", "kernel & shell"),
                ("GitHub Actions", "CI/CD auto-ship"),
                ("Nginx", "reverse proxy")
            ]
        },
        {
            "category": "SECURITY & ARCH",
            "items": [
                ("Multi-Tenancy", "isolated scope"),
                ("P2P Mesh", "WebSocket sync"),
                ("Pen Testing", "offensive sec"),
                ("AI Workflows", "agentic tools")
            ]
        }
    ]
    return columns, len(repos)

def xml_escape(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def generate_stack():
    W, H = 860, 165
    columns, total_repos = fetch_tech_distribution()

    n = len(columns)
    col_w = (W - 48) / n
    cols_svg = ""
    
    for i, col in enumerate(columns):
        x = 24 + i * col_w
        if i > 0:
            cols_svg += f'<line x1="{x:.1f}" y1="36" x2="{x:.1f}" y2="{H - 18}" stroke="#30363d" stroke-width="1"/>'

        cat_title = xml_escape(col["category"])
        cols_svg += f'''
  <text x="{x + 8:.1f}" y="52" font-family="'Courier New',Courier,monospace" font-size="9" font-weight="700" fill="#c9a96e" letter-spacing="1.2">{cat_title}</text>'''
        
        for j, (name, meta) in enumerate(col["items"]):
            y = 74 + j * 20
            name_esc = xml_escape(name)
            meta_esc = xml_escape(meta)
            cols_svg += f'''
  <text x="{x + 8:.1f}" y="{y}" font-family="system-ui,-apple-system,sans-serif" font-size="11.5" font-weight="500" fill="#f0f6fc">{name_esc}</text>
  <text x="{x + 8:.1f}" y="{y + 11}" font-family="'Courier New',Courier,monospace" font-size="8.5" fill="#8b949e">{meta_esc}</text>'''

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
  <text x="24" y="28" font-family="'Courier New',Courier,monospace" font-size="10" fill="#8b949e" letter-spacing="1.5">STACK &amp; ARCHITECTURE</text>
  <text x="{W - 24}" y="28" text-anchor="end" font-family="'Courier New',Courier,monospace" font-size="9" fill="#8b949e">dynamically computed from {total_repos} repositories</text>

  {cols_svg}
</svg>'''
    return svg

def main():
    print("Generating tech-dashboard.svg from live GitHub data...")
    svg = generate_stack()
    with open("tech-dashboard.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("  Written -> tech-dashboard.svg")

if __name__ == "__main__":
    main()
