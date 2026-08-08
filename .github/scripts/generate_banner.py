import os
import json
import urllib.request
import urllib.error
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
        "repos": 0,
        "stars": 0,
        "followers": 0,
        "account_age_years": 0,
        "stack_summary": "PHP / React / Node",
        "total_contributions": 1149
    }

    user = gh_request(f"https://api.github.com/users/{USERNAME}")
    if user:
        stats["repos"] = user.get("public_repos", 0)
        stats["followers"] = user.get("followers", 0)
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

def generate_banner(stats):
    W, H = 860, 200
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    repos     = stats.get("repos", 0)
    stars     = stats.get("stars", 0)
    followers = stats.get("followers", 0)
    age       = stats.get("account_age_years", 0)
    stack_sum = stats.get("stack_summary", "PHP / React / Node")
    contribs  = stats.get("total_contributions", 1149)

    metrics = [
        ("ACTIVE",       f"{age}y",       "years building"),
        ("COMMITS",      f"{contribs:,}", "total contributions"),
        ("REPOSITORIES", str(repos),      "public repos"),
        ("STARS",        str(stars),      "stars earned"),
        ("FOLLOWERS",    str(followers),  "community"),
        ("FOCUS",        stack_sum,       "primary stack"),
    ]

    cell_w = (W - 80) / len(metrics)

    cells_svg = ""
    for i, (key, val, desc) in enumerate(metrics):
        x = 40 + i * cell_w
        sep_x = x + cell_w - 1
        if i < len(metrics) - 1:
            cells_svg += f'<line x1="{sep_x:.1f}" y1="105" x2="{sep_x:.1f}" y2="175" stroke="#38bdf8" stroke-opacity="0.15" stroke-width="1"/>'

        cells_svg += f'''
    <text x="{x + cell_w/2:.1f}" y="126" text-anchor="middle"
          font-family="system-ui, -apple-system, sans-serif" font-size="9" font-weight="600"
          fill="#38bdf8" opacity="0.6" letter-spacing="1">{key}</text>
    <text x="{x + cell_w/2:.1f}" y="152" text-anchor="middle"
          font-family="system-ui, -apple-system, sans-serif" font-size="16"
          font-weight="700" fill="#f8fafc">{val}</text>
    <text x="{x + cell_w/2:.1f}" y="170" text-anchor="middle"
          font-family="system-ui, -apple-system, sans-serif" font-size="9"
          fill="#94a3b8" opacity="0.7">{desc}</text>'''

    svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}"
     fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="{W}" y2="{H}" gradientUnits="userSpaceOnUse">
      <stop stop-color="#0b0f19"/>
      <stop offset="1" stop-color="#030712"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <rect width="{W}" height="{H}" rx="16" fill="url(#bg)"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="15.5"
        stroke="#38bdf8" stroke-opacity="0.2" stroke-width="1"/>

  <rect x="0" y="0" width="{W}" height="40" rx="16" fill="#38bdf8" fill-opacity="0.03"/>
  <rect x="0" y="39" width="{W}" height="1" fill="#38bdf8" fill-opacity="0.15"/>

  <circle cx="22" cy="20" r="5" fill="#ef4444" fill-opacity="0.8"/>
  <circle cx="38" cy="20" r="5" fill="#f59e0b" fill-opacity="0.8"/>
  <circle cx="54" cy="20" r="5" fill="#10b981" fill-opacity="0.8"/>

  <text x="72" y="24"
        font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="500"
        fill="#94a3b8">kisalnelaka / system summary</text>

  <text x="{W - 20}" y="24" text-anchor="end"
        font-family="system-ui, -apple-system, sans-serif" font-size="10"
        fill="#64748b">updated {now}</text>

  <text x="40" y="78"
        font-family="system-ui, -apple-system, sans-serif" font-size="26"
        font-weight="800" fill="#38bdf8" filter="url(#glow)">KISAL NELAKA</text>

  <text x="40" y="96"
        font-family="system-ui, -apple-system, sans-serif" font-size="12"
        fill="#94a3b8" font-weight="500">Systems Architect · Full-Stack Engineer (Laravel / React / Node) · Security</text>

  <rect x="40" y="104" width="{W - 80}" height="1" fill="#38bdf8" fill-opacity="0.15"/>

  {cells_svg}

  <rect x="40" y="186" width="{W - 80}" height="1" fill="#38bdf8" fill-opacity="0.1"/>
</svg>'''

    return svg

def main():
    print("Fetching GitHub stats...")
    stats = fetch_stats()
    svg = generate_banner(stats)

    out = "banner.svg"
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"  Written -> {out}")

if __name__ == "__main__":
    main()
