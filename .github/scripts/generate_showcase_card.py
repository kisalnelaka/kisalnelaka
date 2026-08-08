import os
import json
import urllib.request
from datetime import datetime, timezone

USERNAME = "kisalnelaka"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# These are the two repos you want featured.
# Edit these names to change which repos appear.
FEATURED_REPOS = ["nexusflow_erp", "thenet"]

def gh_request(url):
    headers = {"User-Agent": "gh-profile", "Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f"  [warn] {url} -> {e}")
        return None

def fetch_repo(name):
    """Fetch live repo data from GitHub API."""
    data = gh_request(f"https://api.github.com/repos/{USERNAME}/{name}")
    if not data:
        return None
    return {
        "name":        data.get("name", name),
        "description": data.get("description") or "",
        "stars":       data.get("stargazers_count", 0),
        "forks":       data.get("forks_count", 0),
        "language":    data.get("language") or "",
        "url":         data.get("html_url", f"https://github.com/{USERNAME}/{name}"),
        "updated":     data.get("pushed_at", "")[:10],
    }

# Static metadata that lives alongside the live data.
# These are the things only you know (tagline, key metrics).
FEATURED_META = {
    "nexusflow_erp": {
        "subtitle":   "multi-tenant saas infrastructure",
        "key_facts":  [("100%", "data isolation"), ("&lt;12ms", "inter-service latency"), ("N+", "horizontal tenants")],
        "stack_line": "Laravel 11 · Filament v3 · MySQL · Redis",
    },
    "thenet": {
        "subtitle":   "decentralized p2p mesh network",
        "key_facts":  [("0", "cloud dependencies"), ("P2P", "full mesh sync"), ("WS", "transport layer")],
        "stack_line": "Node.js · WebSockets · Local-First",
    },
}

def xml_escape(s):
    """Escape characters that are invalid in SVG/XML text nodes."""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def generate_showcase(repos):
    W, H = 860, 210

    def render_card(repo, meta, x_offset):
        title    = xml_escape(repo["name"].replace("_", " ").title())
        subtitle = xml_escape(meta["subtitle"])
        desc_lines = []
        desc = repo["description"]
        # Word-wrap description into two lines of ~55 chars each
        words = desc.split()
        line = ""
        for w in words:
            if len(line) + len(w) + 1 > 56:
                desc_lines.append(xml_escape(line.strip()))
                line = w + " "
                if len(desc_lines) == 2:
                    break
            else:
                line += w + " "
        if len(desc_lines) < 2 and line.strip():
            desc_lines.append(xml_escape(line.strip()))
        while len(desc_lines) < 2:
            desc_lines.append("")

        facts_svg = ""
        fact_x_positions = [0, 110, 250]
        for i, (val, label) in enumerate(meta["key_facts"]):
            fx = fact_x_positions[i]
            facts_svg += f'''
      <text x="{fx}" y="0" font-family="system-ui,-apple-system,sans-serif" font-size="20" font-weight="600" fill="#e4e4e7">{val}</text>
      <text x="{fx}" y="16" font-family="system-ui,-apple-system,sans-serif" font-size="10" fill="#4b5563">{label}</text>'''

        # Live stats (stars, language, last push)
        live_line = f"updated {repo['updated']}"
        if repo["language"]:
            live_line = f"{repo['language']}  \u00b7  {live_line}"
        live_line = xml_escape(live_line)

        return f'''
  <g transform="translate({x_offset}, 55)">
    <text x="0" y="0" font-family="system-ui,-apple-system,sans-serif" font-size="17" font-weight="600" fill="#f4f4f5">{title}</text>
    <text x="0" y="20" font-family="'Courier New',Courier,monospace" font-size="10" fill="#4b5563">{subtitle}</text>
    <line x1="0" y1="34" x2="380" y2="34" stroke="#1f1f23" stroke-width="1"/>
    <text x="0" y="55" font-family="system-ui,-apple-system,sans-serif" font-size="12" fill="#52525b">{desc_lines[0]}</text>
    <text x="0" y="71" font-family="system-ui,-apple-system,sans-serif" font-size="12" fill="#52525b">{desc_lines[1]}</text>
    <g transform="translate(0, 98)">{facts_svg}
    </g>
    <text x="0" y="138" font-family="'Courier New',Courier,monospace" font-size="10.5" fill="#374151">{meta["stack_line"]}</text>
    <text x="0" y="152" font-family="'Courier New',Courier,monospace" font-size="9" fill="#27272a">{live_line}</text>
  </g>'''

    card_svgs = ""
    positions = [24, 450]
    for i, (repo_name, pos) in enumerate(zip(FEATURED_REPOS, positions)):
        repo = repos[i]
        meta = FEATURED_META.get(repo_name, {
            "subtitle": repo_name,
            "key_facts": [],
            "stack_line": repo.get("language", ""),
        })
        card_svgs += render_card(repo, meta, pos)

    svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="{W}" y2="{H}" gradientUnits="userSpaceOnUse">
      <stop offset="0%"   stop-color="#0c0c0e"/>
      <stop offset="100%" stop-color="#101014"/>
    </linearGradient>
    <linearGradient id="rule-grad" x1="0" y1="0" x2="0" y2="{H}" gradientUnits="userSpaceOnUse">
      <stop offset="0%"   stop-color="#c9a96e" stop-opacity="0"/>
      <stop offset="35%"  stop-color="#c9a96e" stop-opacity="0.9"/>
      <stop offset="65%"  stop-color="#c9a96e" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#c9a96e" stop-opacity="0"/>
    </linearGradient>
    <filter id="noise" color-interpolation-filters="linearRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch" result="n"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.06 0" in="n"/>
    </filter>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" filter="url(#noise)" style="pointer-events:none;"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" stroke="#ffffff" stroke-opacity="0.06" stroke-width="1" fill="none"/>
  <rect x="0" y="0" width="2" height="{H}" fill="url(#rule-grad)"/>
  <text x="24" y="36" font-family="'Courier New',Courier,monospace" font-size="10" fill="#374151" letter-spacing="1.5">SYSTEMS</text>
  <line x1="430" y1="20" x2="430" y2="{H - 20}" stroke="#ffffff" stroke-opacity="0.05" stroke-width="1"/>
  {card_svgs}
</svg>'''
    return svg

def main():
    print("Generating showcase-card.svg (live data)...")
    repos = []
    for name in FEATURED_REPOS:
        r = fetch_repo(name)
        if r:
            print(f"  Fetched: {r['name']} ({r['stars']} stars, updated {r['updated']})")
            repos.append(r)
        else:
            # Fallback: minimal stub so SVG still generates
            repos.append({
                "name": name, "description": "A featured project.", "stars": 0,
                "forks": 0, "language": "", "url": f"https://github.com/{USERNAME}/{name}", "updated": ""
            })

    svg = generate_showcase(repos)
    with open("showcase-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("  Written -> showcase-card.svg")

if __name__ == "__main__":
    main()
