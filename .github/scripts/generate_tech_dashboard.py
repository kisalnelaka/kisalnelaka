import os
import json
import urllib.request
import math
from datetime import datetime, timezone

USERNAME = "kisalnelaka"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Each language gets its own accent so the chart doesn't look monochrome
LANG_COLORS = {
    "TypeScript":  "#38bdf8",  # sky blue
    "PHP":         "#a78bfa",  # violet
    "Python":      "#facc15",  # amber
    "JavaScript":  "#34d399",  # emerald
    "Rust":        "#fb923c",  # orange
    "HTML":        "#f472b6",  # pink
    "Blade":       "#60a5fa",  # blue
    "CSS":         "#c084fc",  # purple
    "Kotlin":      "#f97316",  # dark orange
    "Shell":       "#00ff9f",  # terminal green
    "C#":          "#a855f7",  # indigo
    "C++":         "#ef4444",  # red
    "Go":          "#06b6d4",  # cyan
    "Java":        "#f59e0b",  # yellow
    "Ruby":        "#e11d48",  # rose
    "Swift":       "#ff6b35",  # swift orange
    "Dart":        "#64b5f6",  # light blue
}
DEFAULT_COLOR = "#94a3b8"


def gh_request(url):
    headers = {
        "User-Agent": "tech-dashboard-generator",
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


def fetch_lang_stats():
    repos = gh_request(
        f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=pushed"
    )
    if not repos:
        return []

    lang_counts = {}
    lang_bytes = {}

    for repo in repos:
        if repo.get("fork"):
            continue  # skip forks — own work only
        lang = repo.get("language")
        if lang:
            lang_counts[lang] = lang_counts.get(lang, 0) + 1

        # Also fetch per-repo language bytes for accuracy
        langs_url = repo.get("languages_url")
        if langs_url and GITHUB_TOKEN:
            lang_data = gh_request(langs_url)
            if lang_data:
                for l, b in lang_data.items():
                    lang_bytes[l] = lang_bytes.get(l, 0) + b

    # Prefer byte-based stats if available (more accurate than repo count)
    if lang_bytes:
        sorted_langs = sorted(lang_bytes.items(), key=lambda x: x[1], reverse=True)
        # Convert bytes to percentages
        total = sum(b for _, b in sorted_langs)
        result = [(name, round(b / total * 100, 1)) for name, b in sorted_langs[:8]]
        return result

    # Fallback: repo count
    sorted_langs = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)
    total = sum(c for _, c in sorted_langs)
    result = [(name, round(c / total * 100, 1)) for name, c in sorted_langs[:8]]
    return result


def generate_svg(lang_stats):
    W, H = 860, 380
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    max_pct = lang_stats[0][1] if lang_stats else 100
    bar_area_w = 500
    row_h = 36
    start_y = 90
    label_x = 40
    bar_x = 200
    pct_x = bar_x + bar_area_w + 10

    rows_svg = ""
    for i, (lang, pct) in enumerate(lang_stats):
        y = start_y + i * row_h
        color = LANG_COLORS.get(lang, DEFAULT_COLOR)
        bar_w = round(bar_area_w * (pct / max_pct), 2)
        delay = i * 0.08

        # Row background
        bg_opacity = "0.04" if i % 2 == 0 else "0.02"
        rows_svg += f'''
  <rect x="20" y="{y - 20}" width="{W - 40}" height="{row_h}" rx="4"
        fill="#00ff9f" fill-opacity="{bg_opacity}"/>'''

        # Language name
        rows_svg += f'''
  <text x="{label_x}" y="{y}"
        font-family="'Courier New',Courier,monospace" font-size="12" font-weight="bold"
        fill="{color}">{lang}</text>'''

        # Bar track
        rows_svg += f'''
  <rect x="{bar_x}" y="{y - 12}" width="{bar_area_w}" height="8" rx="4"
        fill="#00ff9f" fill-opacity="0.06"/>'''

        # Filled bar
        rows_svg += f'''
  <rect x="{bar_x}" y="{y - 12}" width="0" height="8" rx="4" fill="{color}" opacity="0.85">
    <animate attributeName="width" from="0" to="{bar_w}" dur="0.8s"
             begin="{delay:.2f}s" fill="freeze" calcMode="spline"
             keySplines="0.4 0 0.2 1" keyTimes="0;1"/>
  </rect>'''

        # Percentage
        rows_svg += f'''
  <text x="{pct_x}" y="{y}"
        font-family="'Courier New',Courier,monospace" font-size="11"
        fill="{color}" opacity="0.7">{pct}%</text>'''

    svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}"
     fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="{W}" y2="{H}" gradientUnits="userSpaceOnUse">
      <stop stop-color="#020c02"/>
      <stop offset="1" stop-color="#041a04"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="13.5"
        stroke="#00ff9f" stroke-opacity="0.15" stroke-width="1"/>

  <!-- Top bar -->
  <rect x="0" y="0" width="{W}" height="40" rx="14" fill="#00ff9f" fill-opacity="0.04"/>
  <rect x="0" y="39" width="{W}" height="1" fill="#00ff9f" fill-opacity="0.15"/>

  <!-- Window dots -->
  <circle cx="22" cy="20" r="5" fill="#ff5f57" fill-opacity="0.7"/>
  <circle cx="38" cy="20" r="5" fill="#ffbd2e" fill-opacity="0.7"/>
  <circle cx="54" cy="20" r="5" fill="#28c840" fill-opacity="0.7"/>

  <!-- Header label -->
  <text x="72" y="25"
        font-family="'Courier New',Courier,monospace" font-size="11"
        fill="#00ff9f" opacity="0.5">sys/lang-profile --user {USERNAME} --sort bytes</text>

  <!-- Status ping -->
  <circle cx="{W - 34}" cy="20" r="4" fill="#00ff9f">
    <animate attributeName="opacity" values="1;0.3;1" dur="2.5s" repeatCount="indefinite"/>
  </circle>
  <text x="{W - 24}" y="24"
        font-family="'Courier New',Courier,monospace" font-size="9"
        fill="#00ff9f" opacity="0.5">LIVE</text>

  <!-- Section title -->
  <text x="40" y="65"
        font-family="'Courier New',Courier,monospace" font-size="14" font-weight="bold"
        fill="#00ff9f">LANGUAGE DISTRIBUTION</text>
  <text x="40" y="80"
        font-family="'Courier New',Courier,monospace" font-size="9"
        fill="#00ff9f" opacity="0.4">ranked by byte volume across non-forked repositories</text>

  <!-- Column headers -->
  <text x="{label_x}" y="{start_y - 25}"
        font-family="'Courier New',Courier,monospace" font-size="9"
        fill="#00ff9f" opacity="0.3">LANGUAGE</text>
  <text x="{bar_x}" y="{start_y - 25}"
        font-family="'Courier New',Courier,monospace" font-size="9"
        fill="#00ff9f" opacity="0.3">VOLUME</text>
  <text x="{pct_x}" y="{start_y - 25}"
        font-family="'Courier New',Courier,monospace" font-size="9"
        fill="#00ff9f" opacity="0.3">PCT</text>

  {rows_svg}

  <!-- Footer -->
  <rect x="20" y="{H - 28}" width="{W - 40}" height="1" fill="#00ff9f" fill-opacity="0.1"/>
  <text x="40" y="{H - 12}"
        font-family="'Courier New',Courier,monospace" font-size="9"
        fill="#00ff9f" opacity="0.3">updated {now} · github.com/{USERNAME}</text>
</svg>'''

    return svg


def main():
    print("Fetching language stats...")
    lang_stats = fetch_lang_stats()

    if not lang_stats:
        print("  No data. Aborting.")
        return

    print(f"  Top langs: {[n for n, _ in lang_stats[:4]]}")
    print("Generating tech-dashboard.svg...")
    svg = generate_svg(lang_stats)

    out = "tech-dashboard.svg"
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"  Written -> {out}")


if __name__ == "__main__":
    main()
