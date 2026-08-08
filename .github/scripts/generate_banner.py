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
    W, H = 860, 250
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    repos     = stats.get("repos", 71)
    stars     = stats.get("stars", 5)
    followers = stats.get("followers", 10)
    age       = stats.get("account_age_years", 9.3)
    contribs  = stats.get("total_contributions", 1149)

    metrics = [
        ("EXPERIENCE", f"{age} Yrs", "Systems & Full-Stack", "#00f0ff"),
        ("CONTRIBUTIONS", f"{contribs:,}", "Verified Commits", "#00ff9f"),
        ("REPOSITORIES", f"{repos}", "Public Architectures", "#a855f7"),
        ("COMMUNITY", f"{followers} Devs", "Network Followers", "#38bdf8"),
    ]

    metric_boxes = ""
    box_w = 180
    gap = 15
    start_x = 40

    for i, (label, val, sub, col) in enumerate(metrics):
        x = start_x + i * (box_w + gap)
        metric_boxes += f'''
    <!-- Metric Card {i+1} -->
    <g transform="translate({x}, 145)">
      <rect width="{box_w}" height="75" rx="12" fill="#0d1527" fill-opacity="0.7" stroke="{col}" stroke-opacity="0.3" stroke-width="1"/>
      <rect width="{box_w}" height="75" rx="12" fill="url(#card-glow-{i})" opacity="0.15"/>
      <text x="16" y="24" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="700" fill="{col}" letter-spacing="1.2">{label}</text>
      <text x="16" y="48" font-family="system-ui, -apple-system, sans-serif" font-size="20" font-weight="800" fill="#f8fafc">{val}</text>
      <text x="16" y="64" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="500" fill="#94a3b8">{sub}</text>
    </g>'''

    svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#070c18"/>
      <stop offset="50%" stop-color="#030712"/>
      <stop offset="100%" stop-color="#0b1120"/>
    </linearGradient>

    <!-- Neon Border Gradient -->
    <linearGradient id="border-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f0ff" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#a855f7" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#00ff9f" stop-opacity="0.8"/>
    </linearGradient>

    <!-- Ambient Glows -->
    <radialGradient id="glow-cyan" cx="10%" cy="10%" r="60%">
      <stop offset="0%" stop-color="#00f0ff" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#00f0ff" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="glow-purple" cx="90%" cy="80%" r="60%">
      <stop offset="0%" stop-color="#a855f7" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#a855f7" stop-opacity="0"/>
    </radialGradient>

    <!-- Card Inner Glows -->
    <radialGradient id="card-glow-0" cx="0%" cy="0%" r="100%"><stop offset="0%" stop-color="#00f0ff"/><stop offset="100%" stop-color="transparent"/></radialGradient>
    <radialGradient id="card-glow-1" cx="0%" cy="0%" r="100%"><stop offset="0%" stop-color="#00ff9f"/><stop offset="100%" stop-color="transparent"/></radialGradient>
    <radialGradient id="card-glow-2" cx="0%" cy="0%" r="100%"><stop offset="0%" stop-color="#a855f7"/><stop offset="100%" stop-color="transparent"/></radialGradient>
    <radialGradient id="card-glow-3" cx="0%" cy="0%" r="100%"><stop offset="0%" stop-color="#38bdf8"/><stop offset="100%" stop-color="transparent"/></radialGradient>

    <!-- Filter Drop Shadows -->
    <filter id="neon-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <!-- Container Box -->
  <rect width="{W}" height="{H}" rx="18" fill="url(#bg-grad)"/>
  <rect width="{W}" height="{H}" rx="18" fill="url(#glow-cyan)"/>
  <rect width="{W}" height="{H}" rx="18" fill="url(#glow-purple)"/>

  <!-- Glassmorphism Outline -->
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="17" stroke="url(#border-grad)" stroke-width="1.5" fill="none"/>

  <!-- Top Glass Header Bar -->
  <rect x="1" y="1" width="{W-2}" height="42" rx="17" fill="#ffffff" fill-opacity="0.02"/>
  <line x1="1" y1="43" x2="{W-1}" y2="43" stroke="#ffffff" stroke-opacity="0.08" stroke-width="1"/>

  <!-- OS Dots -->
  <circle cx="24" cy="22" r="5" fill="#ff5f57"/>
  <circle cx="40" cy="22" r="5" fill="#febc2e"/>
  <circle cx="56" cy="22" r="5" fill="#28c840"/>

  <!-- Status Indicator -->
  <g transform="translate(76, 22)">
    <text font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="600" fill="#94a3b8">
      SYSTEM STATUS: <tspan fill="#00ff9f">ONLINE</tspan>
    </text>
  </g>

  <!-- Live Pulse Dot -->
  <circle cx="710" cy="22" r="4" fill="#00ff9f">
    <animate attributeName="opacity" values="1;0.2;1" dur="2s" repeatCount="indefinite"/>
  </circle>
  <text x="722" y="25" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="600" fill="#00ff9f" letter-spacing="1">LIVE HUD</text>
  <text x="{W - 24}" y="25" text-anchor="end" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#64748b">{now}</text>

  <!-- Main Hero Title -->
  <text x="40" y="86" font-family="system-ui, -apple-system, sans-serif" font-size="30" font-weight="900" fill="#f8fafc" letter-spacing="-0.5">
    KISAL NELAKA
  </text>
  <text x="245" y="86" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#00f0ff" filter="url(#neon-glow)">
    // SYSTEMS ARCHITECT &amp; FULL-STACK ENGINEER
  </text>

  <!-- Sub-header Stack Tags -->
  <g transform="translate(40, 102)">
    <!-- Pill 1 -->
    <rect x="0" y="0" width="100" height="22" rx="6" fill="#ff2d20" fill-opacity="0.15" stroke="#ff2d20" stroke-opacity="0.4"/>
    <text x="50" y="14" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="700" fill="#ff4d40">Laravel 11</text>

    <!-- Pill 2 -->
    <rect x="108" y="0" width="80" height="22" rx="6" fill="#61dafb" fill-opacity="0.15" stroke="#61dafb" stroke-opacity="0.4"/>
    <text x="148" y="14" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="700" fill="#61dafb">React.js</text>

    <!-- Pill 3 -->
    <rect x="196" y="0" width="80" height="22" rx="6" fill="#68a063" fill-opacity="0.15" stroke="#68a063" stroke-opacity="0.4"/>
    <text x="236" y="14" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="700" fill="#68a063">Node.js</text>

    <!-- Pill 4 -->
    <rect x="284" y="0" width="100" height="22" rx="6" fill="#3178c6" fill-opacity="0.15" stroke="#3178c6" stroke-opacity="0.4"/>
    <text x="334" y="14" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="700" fill="#38bdf8">TypeScript</text>

    <!-- Pill 5 -->
    <rect x="392" y="0" width="130" height="22" rx="6" fill="#a855f7" fill-opacity="0.15" stroke="#a855f7" stroke-opacity="0.4"/>
    <text x="457" y="14" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="700" fill="#c084fc">Offensive Security</text>

    <!-- Pill 6 -->
    <rect x="530" y="0" width="140" height="22" rx="6" fill="#00ff9f" fill-opacity="0.15" stroke="#00ff9f" stroke-opacity="0.4"/>
    <text x="600" y="14" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="700" fill="#00ff9f">Multi-Tenant SaaS</text>
  </g>

  <!-- Metric Cards Row -->
  {metric_boxes}
</svg>'''

    return svg

def main():
    print("Generating high-end banner.svg...")
    stats = fetch_stats()
    svg = generate_banner_svg(stats)

    out = "banner.svg"
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"  Successfully written -> {out}")

if __name__ == "__main__":
    main()
