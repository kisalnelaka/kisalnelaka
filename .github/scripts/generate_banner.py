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
        query = '{ user(login: "%s") { contributionsCollection { contributionCalendar { totalContributions } } } }' % USERNAME
        payload = json.dumps({"query": query}).encode()
        gql_headers = {
            "User-Agent": "profile-banner-generator",
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Content-Type": "application/json",
        }
        req = urllib.request.Request("https://api.github.com/graphql", data=payload, headers=gql_headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                gql_data = json.loads(r.read().decode())
                contrib = gql_data.get("data", {}).get("user", {}).get("contributionsCollection", {}).get("contributionCalendar", {}).get("totalContributions", None)
                if contrib is not None:
                    stats["total_contributions"] = contrib
        except Exception as e:
            print(f"  [warn] GraphQL -> {e}")
    return stats

def generate_banner_svg(stats):
    W, H = 860, 280
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    repos     = stats.get("repos", 71)
    followers = stats.get("followers", 10)
    age       = stats.get("account_age_years", 9.3)
    contribs  = stats.get("total_contributions", 1149)

    # Build animated contour lines (topographic map aesthetic)
    contour_lines = ""
    for i in range(8):
        # Bezier curves that look like topo contour lines
        offset_y = 160 + i * 18
        ctrl1_y = offset_y - 30 + (i % 3) * 15
        ctrl2_y = offset_y + 20 - (i % 2) * 25
        opacity = 0.04 + i * 0.012
        stroke_w = 0.8
        # Second animation offset creates parallax
        anim_offset_a = i * 1.5
        anim_offset_b = i * -1.8

        contour_lines += f'''
  <path d="M -20 {offset_y} C 200 {ctrl1_y}, 400 {ctrl2_y}, 860 {offset_y - 10}" 
        fill="none" stroke="#38bdf8" stroke-width="{stroke_w}" stroke-opacity="{opacity:.3f}">
    <animateTransform attributeName="transform" type="translate" 
                      values="0,0; 0,{anim_offset_a}; 0,0" 
                      dur="{12 + i * 2.1}s" repeatCount="indefinite" calcMode="spline"
                      keySplines="0.45 0 0.55 1; 0.45 0 0.55 1" keyTimes="0;0.5;1"/>
  </path>'''

    metrics = [
        (f"{age}", "YRS", "experience"),
        (f"{contribs:,}", "CMT", "yearly commits"),
        (f"{repos}", "REP", "public repos"),
        (f"{followers}", "FOL", "following"),
    ]

    metric_svg = ""
    for i, (val, label, desc) in enumerate(metrics):
        x = 520 + i * 88
        metric_svg += f'''
  <g transform="translate({x}, 100)">
    <text x="0" y="0" font-family="system-ui, -apple-system, sans-serif" font-size="22" font-weight="800" fill="#f1f5f9">{val}</text>
    <text x="0" y="16" font-family="'Courier New', monospace" font-size="9" font-weight="700" fill="#38bdf8" letter-spacing="1">{label}</text>
    <text x="0" y="30" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="#475569">{desc}</text>
    <line x1="0" y1="38" x2="68" y2="38" stroke="#1e293b" stroke-width="1"/>
  </g>'''

    svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="{W}" y2="{H}" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>
    <!-- The glowing accent strip left side -->
    <linearGradient id="accent-strip" x1="0" y1="0" x2="0" y2="{H}" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0"/>
      <stop offset="40%" stop-color="#38bdf8" stop-opacity="0.7"/>
      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0"/>
    </linearGradient>
    <!-- Right panel separator -->
    <linearGradient id="sep-grad" x1="0" y1="0" x2="0" y2="{H}" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="50%" stop-color="#ffffff" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
    <filter id="soft-glow">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="noise">
      <feTurbulence type="fractalNoise" baseFrequency="0.75" numOctaves="4" stitchTiles="stitch"/>
      <feColorMatrix type="matrix" values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0.045 0"/>
    </filter>
  </defs>

  <!-- Base -->
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  
  <!-- Contour Map (Topographic Animation) -->
  <g clip-path="url(#clip-main)">
    {contour_lines}
  </g>
  <clipPath id="clip-main">
    <rect width="{W}" height="{H}"/>
  </clipPath>
  
  <!-- Noise Grain -->
  <rect width="{W}" height="{H}" filter="url(#noise)" style="pointer-events:none;"/>
  
  <!-- Left accent bar -->
  <rect x="0" y="0" width="3" height="{H}" fill="url(#accent-strip)"/>
  
  <!-- Outer border -->
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" stroke="#ffffff" stroke-opacity="0.05" stroke-width="1" fill="none"/>

  <!-- Right panel divider -->
  <rect x="505" y="0" width="1" height="{H}" fill="url(#sep-grad)"/>
  <!-- Right panel dark overlay -->
  <rect x="506" y="0" width="{W - 506}" height="{H}" fill="#000000" fill-opacity="0.12"/>

  <!-- == LEFT PANEL: Identity == -->
  <!-- Status dot -->
  <circle cx="26" cy="34" r="3.5" fill="#22c55e" filter="url(#soft-glow)">
    <animate attributeName="opacity" values="1;0.4;1" dur="3s" repeatCount="indefinite"/>
  </circle>
  <text x="40" y="38" font-family="'Courier New', monospace" font-size="10" fill="#64748b" letter-spacing="1.5">AVAILABLE TO COLLABORATE</text>
  <text x="{W - 20}" y="22" text-anchor="end" font-family="'Courier New', monospace" font-size="9" fill="#334155">{now}</text>

  <!-- Name -->
  <text x="26" y="105" font-family="system-ui, -apple-system, sans-serif" font-size="46" font-weight="900" fill="#f8fafc" letter-spacing="-2">Kisal Nelaka</text>

  <!-- Title and tagline -->
  <text x="28" y="132" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="400" fill="#64748b">Senior Software Engineer</text>

  <!-- Stack tags row -->
  <g transform="translate(26, 155)">
    <!-- PHP/Laravel -->
    <rect x="0" y="0" width="88" height="20" rx="4" fill="#ff2d20" fill-opacity="0.1"/>
    <text x="44" y="14" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="600" fill="#ff6b5b">PHP / Laravel</text>
    <!-- React -->
    <rect x="95" y="0" width="60" height="20" rx="4" fill="#38bdf8" fill-opacity="0.1"/>
    <text x="125" y="14" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="600" fill="#7dd3fc">React</text>
    <!-- Node -->
    <rect x="162" y="0" width="60" height="20" rx="4" fill="#22c55e" fill-opacity="0.1"/>
    <text x="192" y="14" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="600" fill="#86efac">Node.js</text>
    <!-- Security -->
    <rect x="229" y="0" width="80" height="20" rx="4" fill="#a78bfa" fill-opacity="0.1"/>
    <text x="269" y="14" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="600" fill="#c4b5fd">Pen Testing</text>
  </g>

  <!-- Divider -->
  <line x1="26" y1="195" x2="490" y2="195" stroke="#ffffff" stroke-opacity="0.05" stroke-width="1"/>

  <!-- Tagline -->
  <text x="26" y="218" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="400" fill="#475569">Building systems that don't need babysitting.</text>
  <text x="26" y="236" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="400" fill="#334155">Multi-tenant SaaS, distributed mesh, and the occasional late-night hotfix.</text>

  <!-- == RIGHT PANEL: Stats == -->
  <text x="526" y="56" font-family="'Courier New', monospace" font-size="9" fill="#334155" letter-spacing="2">RUNTIME STATS</text>
  <line x1="526" y1="64" x2="{W - 20}" y2="64" stroke="#1e293b" stroke-width="1"/>

  {metric_svg}

  <!-- Small decorative element: clock arc -->
  <g transform="translate(670, 185)">
    <circle cx="0" cy="0" r="45" stroke="#1e293b" stroke-width="1" fill="none"/>
    <circle cx="0" cy="0" r="38" stroke="#0f172a" stroke-width="8" fill="none"/>
    <!-- Thin progress ring - years active / 10 -->
    <circle cx="0" cy="0" r="38" stroke="#38bdf8" stroke-opacity="0.4" stroke-width="2"
            stroke-dasharray="{2 * math.pi * 38:.1f}" 
            stroke-dashoffset="{2 * math.pi * 38 * (1 - min(age / 12.0, 1.0)):.1f}"
            stroke-linecap="round"
            transform="rotate(-90)" fill="none"/>
    <text x="0" y="-4" text-anchor="middle" font-family="'Courier New', monospace" font-size="10" fill="#64748b">ACTIVE</text>
    <text x="0" y="10" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#f1f5f9">{age}y</text>
  </g>

</svg>'''
    return svg

def main():
    print("Generating banner.svg...")
    stats = fetch_stats()
    svg = generate_banner_svg(stats)
    out = "banner.svg"
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"  Written -> {out}")

if __name__ == "__main__":
    main()
