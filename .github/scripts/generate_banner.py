import os
import json
import urllib.request
from datetime import datetime, timezone

USERNAME = "kisalnelaka"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def gh_request(url):
    headers = {
        "User-Agent": "profile-banner-generator",
        "Accept": "application/vnd.github+json",
    }
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
    stats = {
        "repos": 71,
        "stars": 5,
        "followers": 10,
        "account_age_years": 9.3,
        "total_contributions": 1149
    }

    user = gh_request(f"https://api.github.com/users/{USERNAME}")
    if user:
        stats["repos"] = user.get("public_repos", stats["repos"])
        stats["followers"] = user.get("followers", stats["followers"])
        created = user.get("created_at", "")
        if created:
            created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            delta = datetime.now(timezone.utc) - created_dt
            stats["account_age_years"] = round(delta.days / 365.25, 1)

    repos = gh_request(f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=pushed")
    if repos:
        total_stars = sum(r.get("stargazers_count", 0) for r in repos)
        stats["stars"] = total_stars

    if GITHUB_TOKEN:
        query = """
        {
          user(login: "%s") {
            contributionsCollection {
              contributionCalendar {
                totalContributions
              }
            }
          }
        }
        """ % USERNAME
        payload = json.dumps({"query": query}).encode()
        gql_headers = {
            "User-Agent": "profile-banner-generator",
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Content-Type": "application/json",
        }
        req = urllib.request.Request(
            "https://api.github.com/graphql",
            data=payload,
            headers=gql_headers,
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                gql_data = json.loads(r.read().decode())
                contrib = (
                    gql_data
                    .get("data", {})
                    .get("user", {})
                    .get("contributionsCollection", {})
                    .get("contributionCalendar", {})
                    .get("totalContributions", None)
                )
                if contrib is not None:
                    stats["total_contributions"] = contrib
        except Exception as e:
            print(f"  [warn] GraphQL -> {e}")

    return stats

def generate_banner_svg(stats):
    W, H = 860, 240
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    repos     = stats.get("repos", 71)
    stars     = stats.get("stars", 5)
    followers = stats.get("followers", 10)
    age       = stats.get("account_age_years", 9.3)
    contribs  = stats.get("total_contributions", 1149)

    svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Muted Slate Background -->
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>

    <!-- Subtle Wave Gradient -->
    <linearGradient id="wave-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.0"/>
      <stop offset="50%" stop-color="#38bdf8" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.0"/>
    </linearGradient>

    <!-- Noise Filter -->
    <filter id="noise">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" stitchTiles="stitch"/>
      <feColorMatrix type="matrix" values="1 0 0 0 0, 0 1 0 0 0, 0 0 1 0 0, 0 0 0 0.04 0"/>
    </filter>
  </defs>

  <!-- Base -->
  <rect width="{W}" height="{H}" rx="12" fill="url(#bg-grad)"/>
  
  <!-- Subtle Ambient Animation (Slow moving wave) -->
  <g opacity="0.6">
    <path d="M 0 120 Q 215 80 430 120 T 860 120 L 860 240 L 0 240 Z" fill="url(#wave-grad)">
      <animate attributeName="d" 
               values="M 0 120 Q 215 80 430 120 T 860 120 L 860 240 L 0 240 Z;
                       M 0 120 Q 215 160 430 120 T 860 120 L 860 240 L 0 240 Z;
                       M 0 120 Q 215 80 430 120 T 860 120 L 860 240 L 0 240 Z" 
               dur="15s" repeatCount="indefinite"/>
    </path>
    <path d="M 0 150 Q 215 190 430 150 T 860 150 L 860 240 L 0 240 Z" fill="url(#wave-grad)" opacity="0.5">
       <animate attributeName="d" 
               values="M 0 150 Q 215 190 430 150 T 860 150 L 860 240 L 0 240 Z;
                       M 0 150 Q 215 110 430 150 T 860 150 L 860 240 L 0 240 Z;
                       M 0 150 Q 215 190 430 150 T 860 150 L 860 240 L 0 240 Z" 
               dur="20s" repeatCount="indefinite"/>
    </path>
  </g>

  <!-- Grain Overlay -->
  <rect width="{W}" height="{H}" rx="12" style="pointer-events:none;" filter="url(#noise)"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="11.5" stroke="#ffffff" stroke-opacity="0.05" stroke-width="1" fill="none"/>

  <!-- Minimal Header -->
  <g transform="translate(40, 40)">
      <circle cx="6" cy="6" r="4" fill="#38bdf8" opacity="0.8"/>
      <text x="18" y="10" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="600" fill="#94a3b8" letter-spacing="1">SYSTEMS READY</text>
  </g>
  <text x="{W-40}" y="50" text-anchor="end" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="500" fill="#64748b">{now}</text>

  <!-- Main Identity -->
  <text x="40" y="100" font-family="system-ui, -apple-system, sans-serif" font-size="36" font-weight="800" fill="#f8fafc" letter-spacing="-0.5">Kisal Nelaka</text>
  <text x="40" y="125" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="500" fill="#94a3b8">Senior Software Engineer</text>
  <text x="40" y="145" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="400" fill="#64748b">Building resilient infrastructure. Deleting legacy code.</text>

  <!-- Clean Metric Row -->
  <g transform="translate(40, 185)">
      <!-- Metric 1 -->
      <text x="0" y="0" font-family="system-ui, -apple-system, sans-serif" font-size="18" font-weight="700" fill="#f8fafc">{age}</text>
      <text x="0" y="14" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="600" fill="#64748b" letter-spacing="0.5">YEARS EXPERIENCE</text>
      
      <!-- Divider -->
      <line x1="120" y1="-10" x2="120" y2="15" stroke="#ffffff" stroke-opacity="0.1" stroke-width="1"/>

      <!-- Metric 2 -->
      <text x="150" y="0" font-family="system-ui, -apple-system, sans-serif" font-size="18" font-weight="700" fill="#f8fafc">{contribs:,}</text>
      <text x="150" y="14" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="600" fill="#64748b" letter-spacing="0.5">YEARLY COMMITS</text>
      
      <!-- Divider -->
      <line x1="260" y1="-10" x2="260" y2="15" stroke="#ffffff" stroke-opacity="0.1" stroke-width="1"/>

      <!-- Metric 3 -->
      <text x="290" y="0" font-family="system-ui, -apple-system, sans-serif" font-size="18" font-weight="700" fill="#f8fafc">{repos}</text>
      <text x="290" y="14" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="600" fill="#64748b" letter-spacing="0.5">REPOSITORIES</text>
  </g>
  
</svg>'''

    return svg

def main():
    print("Generating minimalist banner.svg...")
    stats = fetch_stats()
    svg = generate_banner_svg(stats)
    out = "banner.svg"
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"  Successfully written -> {out}")

if __name__ == "__main__":
    main()
