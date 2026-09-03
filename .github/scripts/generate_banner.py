import os
import json
import urllib.request
from datetime import datetime, timezone

USERNAME = "kisalnelaka"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

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

def fetch_stats():
    stats = {"repos": 71, "stars": 5, "followers": 10, "age": 9.3, "commits": 1149}
    user = gh_request(f"https://api.github.com/users/{USERNAME}")
    if user:
        stats["repos"] = user.get("public_repos", stats["repos"])
        stats["followers"] = user.get("followers", stats["followers"])
        created = user.get("created_at", "")
        if created:
            created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            delta = datetime.now(timezone.utc) - created_dt
            stats["age"] = round(delta.days / 365.25, 1)
    repos = gh_request(f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=pushed")
    if repos:
        stats["stars"] = sum(r.get("stargazers_count", 0) for r in repos)
    if GITHUB_TOKEN:
        q = '{"query":"{ user(login:\\"%s\\") { contributionsCollection { contributionCalendar { totalContributions } } } }"}' % USERNAME
        gql_headers = {"User-Agent": "gh-profile", "Authorization": f"Bearer {GITHUB_TOKEN}", "Content-Type": "application/json"}
        req = urllib.request.Request("https://api.github.com/graphql", data=q.encode(), headers=gql_headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                d = json.loads(r.read().decode())
                c = d.get("data", {}).get("user", {}).get("contributionsCollection", {}).get("contributionCalendar", {}).get("totalContributions")
                if c: stats["commits"] = c
        except Exception as e:
            print(f"  [warn] GraphQL -> {e}")
    return stats

def generate_banner(stats):
    W, H = 860, 240
    now = datetime.now(timezone.utc).strftime("%B %Y")

    age     = stats["age"]
    commits = stats["commits"]
    repos   = stats["repos"]

    # A single, elegant, typographic composition
    # Palette: near-black bg, off-white primary, slate secondary, one muted warm accent (#c9a96e)
    svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="{W}" y2="{H}" gradientUnits="userSpaceOnUse">
      <stop offset="0%"   stop-color="#0c0c0e"/>
      <stop offset="100%" stop-color="#101014"/>
    </linearGradient>
    <!-- The ONE accent: a warm, muted amber/gold -->
    <!-- Used ONLY on the thin left rule and the availability dot -->
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

  <!-- Outer border: subtle rounded border matching GitHub dark theme -->
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="8" stroke="#30363d" stroke-width="1" fill="none"/>

  <!-- The accent rule: thin vertical bar inside left edge -->
  <rect x="1" y="8" width="2.5" height="{H - 16}" rx="1" fill="url(#rule-grad)"/>

  <!-- =============================== -->
  <!-- LEFT: Identity                  -->
  <!-- =============================== -->

  <!-- Availability signal -->
  <circle cx="26" cy="26" r="3" fill="#c9a96e">
    <animate attributeName="opacity" values="0.9;0.3;0.9" dur="4s" repeatCount="indefinite"/>
  </circle>
  <text x="36" y="30" font-family="system-ui,-apple-system,sans-serif" font-size="10.5" font-weight="500" fill="#6b7280" letter-spacing="0.5">available for senior engineering roles</text>

  <!-- Name: large, weight 300, generous letter spacing -->
  <text x="24" y="98" font-family="system-ui,-apple-system,sans-serif" font-size="44" font-weight="300" fill="#f0f6fc" letter-spacing="-1">Kisal Nelaka</text>

  <!-- Role: monospace, muted -->
  <text x="26" y="124" font-family="'Courier New',Courier,monospace" font-size="12" font-weight="400" fill="#8b949e" letter-spacing="0.5">senior full-stack engineer &amp; systems architect</text>

  <!-- Thin horizontal rule -->
  <line x1="24" y1="144" x2="460" y2="144" stroke="#30363d" stroke-width="1"/>

  <!-- Tagline: max 2 lines, human voice -->
  <text x="26" y="165" font-family="system-ui,-apple-system,sans-serif" font-size="13" font-weight="400" fill="#c9d1d9">
    9+ years shipping high-throughput multi-tenant SaaS, distributed
  </text>
  <text x="26" y="183" font-family="system-ui,-apple-system,sans-serif" font-size="13" font-weight="400" fill="#c9d1d9">
    architectures, zero-dependency engines, and security tooling.
  </text>

  <!-- Stack line: compact, grey -->
  <text x="26" y="208" font-family="'Courier New',Courier,monospace" font-size="11" fill="#8b949e" letter-spacing="0.3">
    PHP 8.3 / Laravel · React / Vite · Node.js · TypeScript · Python · Swift
  </text>

  <!-- =============================== -->
  <!-- RIGHT: Stats (clean, restrained) -->
  <!-- =============================== -->

  <!-- Vertical separator -->
  <line x1="520" y1="30" x2="520" y2="{H - 30}" stroke="#30363d" stroke-width="1"/>

  <!-- Stat 1: y=70 value, y=90 label -->
  <text x="564" y="70" font-family="system-ui,-apple-system,sans-serif" font-size="32" font-weight="600" fill="#f0f6fc">{age}</text>
  <text x="564" y="86" font-family="system-ui,-apple-system,sans-serif" font-size="11" font-weight="400" fill="#8b949e" letter-spacing="0.4">years building</text>

  <!-- Stat 2: y=130 value, y=148 label -->
  <text x="564" y="132" font-family="system-ui,-apple-system,sans-serif" font-size="32" font-weight="600" fill="#f0f6fc">{commits:,}</text>
  <text x="564" y="148" font-family="system-ui,-apple-system,sans-serif" font-size="11" font-weight="400" fill="#8b949e" letter-spacing="0.4">contributions this year</text>

  <!-- Stat 3: y=194 value, y=212 label -->
  <text x="564" y="194" font-family="system-ui,-apple-system,sans-serif" font-size="32" font-weight="600" fill="#f0f6fc">{repos}</text>
  <text x="564" y="210" font-family="system-ui,-apple-system,sans-serif" font-size="11" font-weight="400" fill="#8b949e" letter-spacing="0.4">public repositories</text>

  <!-- Date: far right, quiet -->
  <text x="{W - 24}" y="30" text-anchor="end" font-family="'Courier New',Courier,monospace" font-size="10" fill="#8b949e">{now}</text>

</svg>'''
    return svg

def main():
    print("Generating banner.svg...")
    stats = fetch_stats()
    svg = generate_banner(stats)
    with open("banner.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("  Written -> banner.svg")

if __name__ == "__main__":
    main()
