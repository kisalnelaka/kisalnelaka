import os
import math
from datetime import datetime, timezone

def generate_tech_dashboard_svg():
    W, H = 860, 240
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    tech_nodes = [
        {"name": "Laravel", "pct": 95, "desc": "PHP 8.3+"},
        {"name": "React", "pct": 88, "desc": "TypeScript"},
        {"name": "Node.js", "pct": 85, "desc": "Express/Koa"},
        {"name": "Database", "pct": 88, "desc": "SQL/Redis"},
        {"name": "Security", "pct": 85, "desc": "Pen Testing"},
        {"name": "Docker", "pct": 82, "desc": "CI/CD"},
    ]

    # Grid layout: 2 rows, 3 cols
    cols = 3
    col_w = W / cols
    row_h = 100
    start_y = 60

    nodes_svg = ""
    for i, node in enumerate(tech_nodes):
        row = i // cols
        col = i % cols
        
        # Center the arc in its cell
        cx = (col * col_w) + (col_w / 2)
        cy = start_y + (row * row_h) + (row_h / 2)
        
        pct = node['pct']
        r = 30
        circumference = 2 * math.pi * r
        dash_len = (pct / 100) * circumference
        
        nodes_svg += f'''
    <g transform="translate({cx}, {cy})">
        <!-- Background Arc -->
        <circle cx="0" cy="0" r="{r}" fill="none" stroke="#1e293b" stroke-width="4"/>
        
        <!-- Progress Arc -->
        <circle cx="0" cy="0" r="{r}" fill="none" stroke="#38bdf8" stroke-opacity="0.8" stroke-width="4" stroke-dasharray="{circumference}" stroke-dashoffset="{circumference}" stroke-linecap="round" transform="rotate(-90)">
            <animate attributeName="stroke-dashoffset" from="{circumference}" to="{circumference - dash_len}" dur="1.5s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1" keyTimes="0;1"/>
        </circle>
        
        <!-- Center Text -->
        <text x="0" y="4" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="700" fill="#f8fafc">{pct}%</text>
        
        <!-- Labels -->
        <text x="45" y="-5" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="600" fill="#e2e8f0">{node['name']}</text>
        <text x="45" y="12" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#64748b">{node['desc']}</text>
    </g>
    '''

    svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>
    <filter id="noise">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" stitchTiles="stitch"/>
      <feColorMatrix type="matrix" values="1 0 0 0 0, 0 1 0 0 0, 0 0 1 0 0, 0 0 0 0.04 0"/>
    </filter>
  </defs>

  <!-- Base -->
  <rect width="{W}" height="{H}" rx="12" fill="url(#bg-grad)"/>
  <rect width="{W}" height="{H}" rx="12" style="pointer-events:none;" filter="url(#noise)"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="11.5" stroke="#ffffff" stroke-opacity="0.05" stroke-width="1" fill="none"/>

  <text x="30" y="35" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="600" fill="#94a3b8" letter-spacing="1">CORE ARSENAL</text>
  <line x1="30" y1="45" x2="{W-30}" y2="45" stroke="#ffffff" stroke-opacity="0.05" stroke-width="1"/>

  {nodes_svg}

</svg>'''

    return svg

def main():
    print("Generating minimalist tech-dashboard.svg...")
    svg = generate_tech_dashboard_svg()
    out = "tech-dashboard.svg"
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"  Successfully written -> {out}")

if __name__ == "__main__":
    main()
