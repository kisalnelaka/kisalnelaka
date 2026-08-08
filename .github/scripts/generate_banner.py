import os
import json
import urllib.request
import math
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
    W, H = 860, 320
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    repos     = stats.get("repos", 71)
    stars     = stats.get("stars", 5)
    followers = stats.get("followers", 10)
    age       = stats.get("account_age_years", 9.3)
    contribs  = stats.get("total_contributions", 1149)

    svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Void Background -->
    <radialGradient id="void-bg" cx="50%" cy="50%" r="70%">
      <stop offset="0%" stop-color="#0a0a1a"/>
      <stop offset="60%" stop-color="#020205"/>
      <stop offset="100%" stop-color="#000000"/>
    </radialGradient>

    <!-- Holographic Glows -->
    <radialGradient id="core-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00ffff" stop-opacity="0.4"/>
      <stop offset="50%" stop-color="#8a2be2" stop-opacity="0.1"/>
      <stop offset="100%" stop-color="transparent"/>
    </radialGradient>
    
    <linearGradient id="neon-cyan" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00ffff" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#00ffff" stop-opacity="0.2"/>
    </linearGradient>

    <!-- Displacement for Glitch -->
    <filter id="hologram">
      <feTurbulence type="fractalNoise" baseFrequency="0.05 0.95" numOctaves="1" result="noise"/>
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="3" xChannelSelector="R" yChannelSelector="G"/>
      <feGaussianBlur stdDeviation="0.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow-heavy">
      <feGaussianBlur stdDeviation="6" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Base -->
  <rect width="{W}" height="{H}" fill="url(#void-bg)"/>
  
  <!-- Ambient Grid -->
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#ffffff" stroke-width="0.5" stroke-opacity="0.03"/>
  </pattern>
  <rect width="{W}" height="{H}" fill="url(#grid)"/>

  <!-- Center Core Glow -->
  <circle cx="{W/2}" cy="{H/2}" r="150" fill="url(#core-glow)"/>

  <!-- Rotating Rings (Center) -->
  <g transform="translate({W/2}, {H/2})">
    <!-- Outer Ring -->
    <circle cx="0" cy="0" r="120" stroke="#00ffff" stroke-width="1" stroke-opacity="0.3" fill="none" stroke-dasharray="4 12">
      <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="20s" repeatCount="indefinite"/>
    </circle>
    <!-- Middle Ring -->
    <circle cx="0" cy="0" r="100" stroke="#8a2be2" stroke-width="2" stroke-opacity="0.5" fill="none" stroke-dasharray="40 20 5 10">
      <animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="15s" repeatCount="indefinite"/>
    </circle>
    <!-- Inner Ring -->
    <circle cx="0" cy="0" r="80" stroke="#00ffff" stroke-width="1" stroke-opacity="0.8" fill="none" stroke-dasharray="2 4">
      <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="10s" repeatCount="indefinite"/>
    </circle>
    
    <!-- Central Data Node -->
    <polygon points="0,-15 13,8 -13,8" fill="#00ffff" opacity="0.8" filter="url(#glow-heavy)">
       <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="5s" repeatCount="indefinite"/>
    </polygon>
  </g>

  <!-- High-Tech Brackets -->
  <path d="M 40 60 L 20 60 L 20 {H-60} L 40 {H-60}" fill="none" stroke="#00ffff" stroke-width="2" stroke-opacity="0.5"/>
  <path d="M {W-40} 60 L {W-20} 60 L {W-20} {H-60} L {W-40} {H-60}" fill="none" stroke="#00ffff" stroke-width="2" stroke-opacity="0.5"/>

  <!-- HUD Data Lines (Left) -->
  <g transform="translate(40, 90)" font-family="monospace" font-size="10" fill="#00ffff" opacity="0.7">
    <text y="0">SYS.INIT.SEQ // 0x4F2A</text>
    <text y="20">AURA.LINK // ACTIVE</text>
    <text y="40">LATENCY // 12ms</text>
    <text y="60">TENANT.ISO // SECURE</text>
    <line x1="0" y1="70" x2="100" y2="70" stroke="#00ffff" stroke-width="1" stroke-opacity="0.4"/>
  </g>

  <!-- HUD Data Lines (Right) -->
  <g transform="translate({W-160}, 90)" font-family="monospace" font-size="10" fill="#8a2be2" opacity="0.7" text-anchor="end">
    <text x="120" y="0">NODE.JS // v20.x</text>
    <text x="120" y="20">LARAVEL // v11.x</text>
    <text x="120" y="40">REACT // v18.x</text>
    <text x="120" y="60">OSCP // VERIFIED</text>
    <line x1="20" y1="70" x2="120" y2="70" stroke="#8a2be2" stroke-width="1" stroke-opacity="0.4"/>
  </g>

  <!-- Main Identity (Holographic Text) -->
  <g transform="translate({W/2}, 70)" text-anchor="middle" filter="url(#hologram)">
    <text font-family="'Courier New', Courier, monospace" font-size="48" font-weight="900" fill="#ffffff" letter-spacing="8">KISAL NELAKA</text>
    <text y="30" font-family="'Courier New', Courier, monospace" font-size="14" font-weight="700" fill="#00ffff" letter-spacing="4">IMPERIAL SYSTEMS ARCHITECT</text>
  </g>

  <!-- Floating Stats Modules -->
  <!-- Stat 1 -->
  <g transform="translate(80, {H-90})">
    <rect x="0" y="0" width="120" height="40" fill="#00ffff" fill-opacity="0.05" stroke="#00ffff" stroke-opacity="0.3"/>
    <text x="60" y="15" text-anchor="middle" font-family="monospace" font-size="9" fill="#00ffff">COMBAT EXPERIENCE</text>
    <text x="60" y="32" text-anchor="middle" font-family="monospace" font-size="16" font-weight="bold" fill="#ffffff">{age} YRS</text>
  </g>

  <!-- Stat 2 -->
  <g transform="translate(240, {H-90})">
    <rect x="0" y="0" width="120" height="40" fill="#8a2be2" fill-opacity="0.05" stroke="#8a2be2" stroke-opacity="0.3"/>
    <text x="60" y="15" text-anchor="middle" font-family="monospace" font-size="9" fill="#8a2be2">VERIFIED COMMITS</text>
    <text x="60" y="32" text-anchor="middle" font-family="monospace" font-size="16" font-weight="bold" fill="#ffffff">{contribs:,}</text>
  </g>
  
  <!-- Stat 3 -->
  <g transform="translate(400, {H-90})">
    <rect x="0" y="0" width="120" height="40" fill="#00ffff" fill-opacity="0.05" stroke="#00ffff" stroke-opacity="0.3"/>
    <text x="60" y="15" text-anchor="middle" font-family="monospace" font-size="9" fill="#00ffff">ARCHITECTURES</text>
    <text x="60" y="32" text-anchor="middle" font-family="monospace" font-size="16" font-weight="bold" fill="#ffffff">{repos}</text>
  </g>

  <!-- Stat 4 -->
  <g transform="translate(560, {H-90})">
    <rect x="0" y="0" width="120" height="40" fill="#8a2be2" fill-opacity="0.05" stroke="#8a2be2" stroke-opacity="0.3"/>
    <text x="60" y="15" text-anchor="middle" font-family="monospace" font-size="9" fill="#8a2be2">NETWORK FOLLOWERS</text>
    <text x="60" y="32" text-anchor="middle" font-family="monospace" font-size="16" font-weight="bold" fill="#ffffff">{followers}</text>
  </g>

  <!-- System Status Footer -->
  <text x="{W/2}" y="{H-20}" text-anchor="middle" font-family="monospace" font-size="10" fill="#555555" letter-spacing="2">SYS.UPDATE :: {now} // ALL SYSTEMS NOMINAL</text>

  <!-- Glitch overlay animation -->
  <rect width="{W}" height="{H}" fill="none">
    <animate attributeName="opacity" values="0;0;0.1;0;0" keyTimes="0;0.9;0.92;0.94;1" dur="4s" repeatCount="indefinite"/>
  </rect>

</svg>'''

    return svg

def main():
    print("Generating God-Tier banner.svg...")
    stats = fetch_stats()
    svg = generate_banner_svg(stats)
    out = "banner.svg"
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"  Successfully written -> {out}")

if __name__ == "__main__":
    main()
