import os
import math
from datetime import datetime, timezone

def generate_tech_dashboard_svg():
    W, H = 860, 200
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Core stack items - two rows
    stack = [
        # Row 1
        {"name": "Laravel",    "sub": "PHP 8.3+",       "pct": 95, "col": "#ef4444"},
        {"name": "React",      "sub": "TypeScript",     "pct": 88, "col": "#38bdf8"},
        {"name": "Node.js",    "sub": "Async I/O",      "pct": 85, "col": "#22c55e"},
        {"name": "MySQL/Redis","sub": "Data Layer",     "pct": 90, "col": "#f59e0b"},
        {"name": "Security",   "sub": "Pen Testing",    "pct": 85, "col": "#a78bfa"},
        {"name": "Docker",     "sub": "CI/CD",          "pct": 82, "col": "#64748b"},
    ]

    col_w = (W - 60) / len(stack)
    BAR_H = 80   # height of the bar drawing area
    bar_top = 100

    bars_svg = ""
    for i, item in enumerate(stack):
        x = 30 + i * col_w + col_w / 2
        pct = item["pct"]
        col = item["col"]
        bar_h = BAR_H * (pct / 100)
        bar_y = bar_top + BAR_H - bar_h
        delay = i * 0.1

        bars_svg += f'''
  <!-- Column {i}: {item["name"]} -->
  <!-- Track -->
  <rect x="{x - 14:.1f}" y="{bar_top}" width="28" height="{BAR_H}" rx="4" fill="#0f172a"/>
  
  <!-- Animated Fill -->
  <rect x="{x - 14:.1f}" y="{bar_top + BAR_H}" width="28" height="0" rx="4" fill="{col}" opacity="0.85">
    <animate attributeName="height" from="0" to="{bar_h:.1f}" dur="0.9s" begin="{delay:.2f}s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1" keyTimes="0;1"/>
    <animate attributeName="y" from="{bar_top + BAR_H:.1f}" to="{bar_y:.1f}" dur="0.9s" begin="{delay:.2f}s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1" keyTimes="0;1"/>
  </rect>

  <!-- Top cap glow -->
  <rect x="{x - 14:.1f}" y="{bar_y:.1f}" width="28" height="3" rx="1.5" fill="{col}" opacity="0.6">
    <animate attributeName="y" from="{bar_top + BAR_H:.1f}" to="{bar_y:.1f}" dur="0.9s" begin="{delay:.2f}s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1" keyTimes="0;1"/>
  </rect>

  <!-- Pct Label -->
  <text x="{x:.1f}" y="{bar_top - 8}" text-anchor="middle" font-family="'Courier New', monospace" font-size="11" font-weight="700" fill="{col}">{pct}</text>

  <!-- Name -->
  <text x="{x:.1f}" y="{bar_top + BAR_H + 18}" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="600" fill="#e2e8f0">{item["name"]}</text>
  <text x="{x:.1f}" y="{bar_top + BAR_H + 32}" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="#475569">{item["sub"]}</text>
'''

    svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="{W}" y2="{H}" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>
    <linearGradient id="accent-strip" x1="0" y1="0" x2="0" y2="{H}" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0"/>
      <stop offset="40%" stop-color="#38bdf8" stop-opacity="0.7"/>
      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0"/>
    </linearGradient>
    <filter id="noise">
      <feTurbulence type="fractalNoise" baseFrequency="0.75" numOctaves="4" stitchTiles="stitch"/>
      <feColorMatrix type="matrix" values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0.04 0"/>
    </filter>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" filter="url(#noise)" style="pointer-events:none;"/>
  <rect x="0" y="0" width="3" height="{H}" fill="url(#accent-strip)"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" stroke="#ffffff" stroke-opacity="0.05" stroke-width="1" fill="none"/>

  <!-- Header -->
  <text x="26" y="38" font-family="'Courier New', monospace" font-size="10" font-weight="700" fill="#64748b" letter-spacing="1.5">STACK PROFICIENCY</text>
  <line x1="26" y1="50" x2="{W - 26}" y2="50" stroke="#1e293b" stroke-width="1"/>
  <text x="{W - 26}" y="38" text-anchor="end" font-family="'Courier New', monospace" font-size="9" fill="#334155">{now}</text>
  
  <!-- Baseline -->
  <line x1="26" y1="{bar_top + BAR_H}" x2="{W - 26}" y2="{bar_top + BAR_H}" stroke="#1e293b" stroke-width="1"/>

  {bars_svg}
</svg>'''

    return svg

def main():
    print("Generating tech-dashboard.svg...")
    svg = generate_tech_dashboard_svg()
    out = "tech-dashboard.svg"
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"  Written -> {out}")

if __name__ == "__main__":
    main()
