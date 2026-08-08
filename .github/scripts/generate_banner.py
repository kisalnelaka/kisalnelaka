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
        print(f"  [warn] {url} → {e}")
        return None

def fetch_stats():
    stats = {
        "repos": 0,
        "stars": 0,
        "followers": 0,
        "account_age_years": 0,
        "top_lang": "TypeScript",
        "streak_days": 89,  # fallback — updated by streak-stats workflow if available
    }

    # User profile
    user = gh_request(f"https://api.github.com/users/{USERNAME}")
    if user:
        stats["repos"] = user.get("public_repos", 0)
        stats["followers"] = user.get("followers", 0)
        created = user.get("created_at", "")
        if created:
            created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            delta = datetime.now(timezone.utc) - created_dt
            stats["account_age_years"] = round(delta.days / 365.25, 1)

    # Stars + top language
    repos = gh_request(f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=pushed")
    if repos:
        total_stars = sum(r.get("stargazers_count", 0) for r in repos)
        stats["stars"] = total_stars

        lang_counts = {}
        for r in repos:
            lang = r.get("language")
            if lang:
                lang_counts[lang] = lang_counts.get(lang, 0) + 1
        if lang_counts:
            stats["top_lang"] = max(lang_counts, key=lang_counts.get)

    # Contribution count via GitHub GraphQL
    if GITHUB_TOKEN:
        query = """
        {
          user(login: "%s") {
            contributionsCollection {
              contributionCalendar {
                totalContributions
              }
            }
            repositoriesContributedTo(first: 1, contributionTypes: [COMMIT, PULL_REQUEST, REPOSITORY]) {
              totalCount
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
            print(f"  [warn] GraphQL → {e}")

    return stats

def generate_banner(stats):
    W, H = 860, 200
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    repos     = stats.get("repos", 0)
    stars     = stats.get("stars", 0)
    followers = stats.get("followers", 0)
    age       = stats.get("account_age_years", 0)
    top_lang  = stats.get("top_lang", "TypeScript")
    contribs  = stats.get("total_contributions", 1149)

    # Build metric cells
    metrics = [
        ("UPTIME",       f"{age}y",      "years active"),
        ("COMMITS_TOT",  f"{contribs:,}", "total contributions"),
        ("PUBLIC_REPOS", str(repos),     "public repos"),
        ("STARS",        str(stars),     "stars earned"),
        ("FOLLOWERS",    str(followers), "followers"),
        ("CORE_LANG",    top_lang,       "primary language"),
    ]

    cell_w = (W - 80) / len(metrics)

    cells_svg = ""
    for i, (key, val, desc) in enumerate(metrics):
        x = 40 + i * cell_w
        sep_x = x + cell_w - 1
        # separator line (skip last)
        if i < len(metrics) - 1:
            cells_svg += f'<line x1="{sep_x:.1f}" y1="105" x2="{sep_x:.1f}" y2="175" stroke="#00ff9f" stroke-opacity="0.15" stroke-width="1"/>'

        cells_svg += f'''
    <text x="{x + cell_w/2:.1f}" y="126" text-anchor="middle"
          font-family="'Courier New',Courier,monospace" font-size="9"
          fill="#00ff9f" opacity="0.5" letter-spacing="1">{key}</text>
    <text x="{x + cell_w/2:.1f}" y="152" text-anchor="middle"
          font-family="'Courier New',Courier,monospace" font-size="20"
          font-weight="bold" fill="#00ff9f">{val}</text>
    <text x="{x + cell_w/2:.1f}" y="170" text-anchor="middle"
          font-family="'Courier New',Courier,monospace" font-size="9"
          fill="#00ff9f" opacity="0.4">{desc}</text>'''

    svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}"
     fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="{W}" y2="{H}" gradientUnits="userSpaceOnUse">
      <stop stop-color="#020c02"/>
      <stop offset="1" stop-color="#041a04"/>
    </linearGradient>
    <filter id="scan">
      <feTurbulence type="fractalNoise" baseFrequency="0 0.15" numOctaves="1" result="noise"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.04 0" result="noiseAlpha"/>
      <feComposite in="SourceGraphic" in2="noiseAlpha" operator="over"/>
    </filter>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="13.5"
        stroke="#00ff9f" stroke-opacity="0.18" stroke-width="1"/>

  <!-- Scan lines overlay -->
  <rect width="{W}" height="{H}" rx="14" fill="transparent" filter="url(#scan)"/>

  <!-- Top bar -->
  <rect x="0" y="0" width="{W}" height="40" rx="14" fill="#00ff9f" fill-opacity="0.04"/>
  <rect x="0" y="39" width="{W}" height="1" fill="#00ff9f" fill-opacity="0.2"/>

  <!-- Window dots -->
  <circle cx="22" cy="20" r="5" fill="#ff5f57" fill-opacity="0.8"/>
  <circle cx="38" cy="20" r="5" fill="#ffbd2e" fill-opacity="0.8"/>
  <circle cx="54" cy="20" r="5" fill="#28c840" fill-opacity="0.8"/>

  <!-- Terminal path -->
  <text x="72" y="25"
        font-family="'Courier New',Courier,monospace" font-size="11"
        fill="#00ff9f" opacity="0.5">~/kisalnelaka/profile</text>

  <!-- Timestamp right -->
  <text x="{W - 20}" y="25" text-anchor="end"
        font-family="'Courier New',Courier,monospace" font-size="10"
        fill="#00ff9f" opacity="0.35">updated {now}</text>

  <!-- Name -->
  <text x="40" y="78"
        font-family="'Courier New',Courier,monospace" font-size="28"
        font-weight="bold" fill="#00ff9f" filter="url(#glow)">KISAL NELAKA</text>

  <!-- Blinking cursor -->
  <rect x="238" y="58" width="16" height="24" rx="2" fill="#00ff9f" opacity="0.8">
    <animate attributeName="opacity" values="0.8;0;0.8" dur="1.1s" repeatCount="indefinite"/>
  </rect>

  <!-- Role tag -->
  <text x="40" y="96"
        font-family="'Courier New',Courier,monospace" font-size="11"
        fill="#00ff9f" opacity="0.55">// systems architect · full-stack engineer · offensive security</text>

  <!-- Divider -->
  <rect x="40" y="102" width="{W - 80}" height="1" fill="#00ff9f" fill-opacity="0.15"/>

  <!-- Metric cells -->
  {cells_svg}

  <!-- Bottom border -->
  <rect x="40" y="186" width="{W - 80}" height="1" fill="#00ff9f" fill-opacity="0.1"/>
</svg>'''

    return svg

def main():
    print("Fetching GitHub stats...")
    stats = fetch_stats()
    print(f"  repos={stats.get('repos')}, stars={stats.get('stars')}, contribs={stats.get('total_contributions', '?')}")

    print("Generating banner.svg...")
    svg = generate_banner(stats)

    out = "banner.svg"
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"  Written -> {out}")

if __name__ == "__main__":
    main()
