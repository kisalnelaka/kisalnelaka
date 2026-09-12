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
    W, H = 880, 240
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    age     = stats["age"]
    commits = stats["commits"]
    repos   = stats["repos"]
    stars   = stats.get("stars", 0)

    # Sleek, minimalist Dark Obsidian HUD Banner
    svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Radial ambient glow -->
    <radialGradient id="ambient-glow" cx="80%" cy="20%" r="60%">
      <stop offset="0%" stop-color="#00f0ff" stop-opacity="0.08"/>
      <stop offset="50%" stop-color="#a855f7" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>

    <!-- Card Background Gradient -->
    <linearGradient id="hud-card-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#161b22" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#0d1117" stop-opacity="0.95"/>
    </linearGradient>

    <!-- Accent Line Gradient -->
    <linearGradient id="accent-line" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00f0ff"/>
      <stop offset="50%" stop-color="#a855f7"/>
      <stop offset="100%" stop-color="#10b981"/>
    </linearGradient>

    <style>
      .mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace; }}
      .sans {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
      .cursor-blink {{ animation: blink 1.2s step-end infinite; }}
      .pulse-dot {{ animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }}
      @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
      @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} }}
    </style>
  </defs>

  <!-- Background Base -->
  <rect width="{W}" height="{H}" rx="10" fill="#080a0f"/>
  <rect width="{W}" height="{H}" rx="10" fill="url(#ambient-glow)"/>

  <!-- Border -->
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="9" stroke="#1f2937" stroke-width="1.2"/>
  
  <!-- Top Laser Accent Line -->
  <path d="M10 1 H{W - 10}" stroke="url(#accent-line)" stroke-width="2"/>

  <!-- ============================================== -->
  <!-- TOP TELEMETRY BAR                              -->
  <!-- ============================================== -->
  <!-- Status Indicator Dot -->
  <circle cx="28" cy="24" r="4" fill="#10b981" class="pulse-dot"/>
  <text x="40" y="28" class="mono" font-size="11" font-weight="600" fill="#10b981" letter-spacing="1">
    AUDHD_HYPERFOCUS // THREAD_PINNED
  </text>

  <text x="{W - 28}" y="28" text-anchor="end" class="mono" font-size="10.5" fill="#64748b" letter-spacing="0.5">
    LATENCY: &lt;0.1ms · ZERO_BLOAT_DIRECTIVE · KERNEL_NATIVE
  </text>

  <line x1="20" y1="42" x2="{W - 20}" y2="42" stroke="#1e293b" stroke-width="1"/>

  <!-- ============================================== -->
  <!-- HERO IDENTITY AREA                             -->
  <!-- ============================================== -->
  <text x="28" y="80" class="sans" font-size="30" font-weight="900" fill="#f8fafc" letter-spacing="-0.5">
    KISAL NELAKA
  </text>

  <rect x="238" y="63" width="168" height="22" rx="4" fill="#1e1e38" stroke="#6366f1" stroke-width="0.8"/>
  <text x="246" y="78" class="mono" font-size="10" font-weight="700" fill="#818cf8" letter-spacing="0.5">
    SYSTEMS ARCHITECT
  </text>

  <!-- Arrogant / Sociopathic ADHD Manifesto Quote -->
  <text x="28" y="107" class="mono" font-size="12" fill="#94a3b8">
    &quot;I don't write software to collaborate. I write software because your architecture offended my central nervous system.&quot;
  </text>

  <!-- ============================================== -->
  <!-- TELEMETRY METRICS GRID (4 CARDS)               -->
  <!-- ============================================== -->
  <!-- Card 1: Production Uptime -->
  <g transform="translate(28, 126)">
    <rect width="192" height="58" rx="6" fill="url(#hud-card-grad)" stroke="#1e293b" stroke-width="1"/>
    <text x="14" y="22" class="mono" font-size="9.5" font-weight="600" fill="#64748b" letter-spacing="1">PROD UPTIME</text>
    <text x="14" y="44" class="sans" font-size="19" font-weight="800" fill="#38bdf8">{age} YRS</text>
    <text x="178" y="44" text-anchor="end" class="mono" font-size="10" fill="#0284c7">ACTIVE</text>
  </g>

  <!-- Card 2: Annual Commits -->
  <g transform="translate(234, 126)">
    <rect width="192" height="58" rx="6" fill="url(#hud-card-grad)" stroke="#1e293b" stroke-width="1"/>
    <text x="14" y="22" class="mono" font-size="9.5" font-weight="600" fill="#64748b" letter-spacing="1">LIFETIME COMMITS</text>
    <text x="14" y="44" class="sans" font-size="19" font-weight="800" fill="#10b981">{commits:,}+</text>
    <text x="178" y="44" text-anchor="end" class="mono" font-size="10" fill="#059669">SYNCED</text>
  </g>

  <!-- Card 3: Public Repos -->
  <g transform="translate(440, 126)">
    <rect width="192" height="58" rx="6" fill="url(#hud-card-grad)" stroke="#1e293b" stroke-width="1"/>
    <text x="14" y="22" class="mono" font-size="9.5" font-weight="600" fill="#64748b" letter-spacing="1">SHIPPED CODEBASES</text>
    <text x="14" y="44" class="sans" font-size="19" font-weight="800" fill="#a855f7">{repos}</text>
    <text x="178" y="44" text-anchor="end" class="mono" font-size="10" fill="#7c3aed">PUBLIC</text>
  </g>

  <!-- Card 4: Executive Directive -->
  <g transform="translate(646, 126)">
    <rect width="206" height="58" rx="6" fill="url(#hud-card-grad)" stroke="#1e293b" stroke-width="1"/>
    <text x="14" y="22" class="mono" font-size="9.5" font-weight="600" fill="#64748b" letter-spacing="1">DOPAMINE ENGINE</text>
    <text x="14" y="44" class="sans" font-size="18" font-weight="800" fill="#f43f5e">PURE SPITE</text>
    <text x="192" y="44" text-anchor="end" class="mono" font-size="10" fill="#e11d48">100%</text>
  </g>

  <!-- ============================================== -->
  <!-- BOTTOM TERMINAL PROMPT                         -->
  <!-- ============================================== -->
  <line x1="20" y1="198" x2="{W - 20}" y2="198" stroke="#1e293b" stroke-width="1"/>

  <text x="28" y="222" class="mono" font-size="11" fill="#475569">
    root@kisalnelaka:~$ <tspan fill="#38bdf8">./execute_superiority.sh</tspan> <tspan fill="#64748b">--bypass-bloat --compile-native --no-human-error</tspan><tspan class="cursor-blink" fill="#38bdf8">_</tspan>
  </text>

  <text x="{W - 28}" y="222" text-anchor="end" class="mono" font-size="10" fill="#475569">
    UPSTREAM_TARGET: ALL // {now}
  </text>
</svg>'''
    return svg

def main():
    print("Generating lethal dark HUD banner.svg...")
    stats = fetch_stats()
    svg = generate_banner(stats)
    with open("banner.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("  Written -> banner.svg")

if __name__ == "__main__":
    main()
