import os
import json
from datetime import datetime, timezone

USERNAME = "kisalnelaka"

LANG_COLORS = {
    "Laravel / PHP": "#ff2d20",
    "React":         "#61dafb",
    "Node.js":       "#68a063",
    "TypeScript":    "#3178c6",
    "Python":        "#facc15",
    "SQL / DB":      "#008780",
    "Tailwind CSS":  "#38bdf8",
    "Docker / Infra": "#2496ed"
}
DEFAULT_COLOR = "#38bdf8"

def load_stack_config():
    config_path = os.path.join(".github", "scripts", "stack-config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "languages": [
            {"name": "Laravel / PHP", "pct": 95, "note": "primary stack"},
            {"name": "React", "pct": 88, "note": "frontend core"},
            {"name": "Node.js", "pct": 82, "note": "async services"},
            {"name": "TypeScript", "pct": 78, "note": "type safety"},
            {"name": "Python", "pct": 65, "note": "scripting & tooling"},
            {"name": "SQL / DB", "pct": 75, "note": "architectural scoping"}
        ]
    }

def generate_svg(stack_data):
    W, H = 860, 360
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    items = stack_data.get("languages", [])
    max_pct = 100
    bar_area_w = 460
    row_h = 38
    start_y = 95
    label_x = 40
    bar_x = 220
    pct_x = bar_x + bar_area_w + 15

    rows_svg = ""
    for i, item in enumerate(items):
        name = item["name"]
        pct = item["pct"]
        note = item.get("note", "")
        y = start_y + i * row_h
        color = LANG_COLORS.get(name, DEFAULT_COLOR)
        bar_w = round(bar_area_w * (pct / max_pct), 2)
        delay = i * 0.08

        bg_opacity = "0.03" if i % 2 == 0 else "0.015"
        rows_svg += f'''
  <rect x="20" y="{y - 22}" width="{W - 40}" height="{row_h - 4}" rx="6"
        fill="#38bdf8" fill-opacity="{bg_opacity}"/>'''

        rows_svg += f'''
  <text x="{label_x}" y="{y}"
        font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="700"
        fill="{color}">{name}</text>'''

        rows_svg += f'''
  <rect x="{bar_x}" y="{y - 12}" width="{bar_area_w}" height="8" rx="4"
        fill="#1e293b" fill-opacity="0.6"/>'''

        rows_svg += f'''
  <rect x="{bar_x}" y="{y - 12}" width="0" height="8" rx="4" fill="{color}" opacity="0.9">
    <animate attributeName="width" from="0" to="{bar_w}" dur="0.8s"
             begin="{delay:.2f}s" fill="freeze" calcMode="spline"
             keySplines="0.4 0 0.2 1" keyTimes="0;1"/>
  </rect>'''

        rows_svg += f'''
  <text x="{pct_x}" y="{y}"
        font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="600"
        fill="#f8fafc">{pct}%</text>
  <text x="{pct_x + 45}" y="{y}"
        font-family="system-ui, -apple-system, sans-serif" font-size="10"
        fill="#94a3b8" opacity="0.6">{note}</text>'''

    svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}"
     fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="{W}" y2="{H}" gradientUnits="userSpaceOnUse">
      <stop stop-color="#0b0f19"/>
      <stop offset="1" stop-color="#030712"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <rect width="{W}" height="{H}" rx="16" fill="url(#bg)"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="15.5"
        stroke="#38bdf8" stroke-opacity="0.2" stroke-width="1"/>

  <rect x="0" y="0" width="{W}" height="42" rx="16" fill="#38bdf8" fill-opacity="0.03"/>
  <rect x="0" y="41" width="{W}" height="1" fill="#38bdf8" fill-opacity="0.15"/>

  <circle cx="22" cy="21" r="5" fill="#ef4444" fill-opacity="0.8"/>
  <circle cx="38" cy="21" r="5" fill="#f59e0b" fill-opacity="0.8"/>
  <circle cx="54" cy="21" r="5" fill="#10b981" fill-opacity="0.8"/>

  <text x="72" y="25"
        font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="600"
        fill="#38bdf8">TECHNICAL ARSENAL</text>
  <text x="210" y="25"
        font-family="system-ui, -apple-system, sans-serif" font-size="10"
        fill="#94a3b8" opacity="0.7">· Core Stack Proficiency &amp; Focus Areas</text>

  <circle cx="{W - 70}" cy="21" r="4" fill="#10b981">
    <animate attributeName="opacity" values="1;0.3;1" dur="2.5s" repeatCount="indefinite"/>
  </circle>
  <text x="{W - 60}" y="24"
        font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="600"
        fill="#10b981">VERIFIED</text>

  <text x="{label_x}" y="72"
        font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="700"
        fill="#64748b" letter-spacing="1">TECHNOLOGY</text>
  <text x="{bar_x}" y="72"
        font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="700"
        fill="#64748b" letter-spacing="1">PROFICIENCY / MASTERY</text>

  {rows_svg}

  <rect x="20" y="{H - 30}" width="{W - 40}" height="1" fill="#38bdf8" fill-opacity="0.1"/>
  <text x="40" y="{H - 12}"
        font-family="system-ui, -apple-system, sans-serif" font-size="10"
        fill="#64748b">Updated {now} · Kisal Nelaka Stack Profile</text>
</svg>'''

    return svg

def main():
    stack_data = load_stack_config()
    print("Generating tech-dashboard.svg...")
    svg = generate_svg(stack_data)

    out = "tech-dashboard.svg"
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"  Written -> {out}")

if __name__ == "__main__":
    main()
