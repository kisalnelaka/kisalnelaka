import os
from datetime import datetime, timezone

def generate_stack():
    W, H = 860, 160

    # Clean, categorical typography grid. No percentages. No bars.
    # The reader knows what these technologies mean. Trust them.
    cols = [
        {
            "label": "BACKEND",
            "items": ["Laravel 11", "PHP 8.3", "Node.js", "REST / GraphQL"],
        },
        {
            "label": "FRONTEND",
            "items": ["React 18", "TypeScript", "Tailwind CSS", "Vite"],
        },
        {
            "label": "DATA",
            "items": ["MySQL", "PostgreSQL", "Redis", "Eloquent ORM"],
        },
        {
            "label": "INFRASTRUCTURE",
            "items": ["Docker", "GitHub Actions", "Nginx", "Linux"],
        },
        {
            "label": "SECURITY",
            "items": ["Pen Testing", "SIEM / Splunk", "Threat Analysis", "OSCP Standard"],
        },
    ]

    n = len(cols)
    col_w = (W - 48) / n
    cols_svg = ""
    for i, col in enumerate(cols):
        x = 24 + i * col_w
        # Vertical separator (between cols, not after last)
        if i > 0:
            cols_svg += f'<line x1="{x:.1f}" y1="40" x2="{x:.1f}" y2="{H - 20}" stroke="#ffffff" stroke-opacity="0.04" stroke-width="1"/>'

        cols_svg += f'''
  <text x="{x + 8:.1f}" y="56" font-family="\'Courier New\',Courier,monospace" font-size="9" font-weight="700" fill="#374151" letter-spacing="1.2">{col["label"]}</text>'''
        for j, item in enumerate(col["items"]):
            y = 76 + j * 19
            # First item slightly brighter
            fill = "#9ca3af" if j == 0 else "#52525b"
            cols_svg += f'''
  <text x="{x + 8:.1f}" y="{y}" font-family="system-ui,-apple-system,sans-serif" font-size="12" font-weight="{600 if j == 0 else 400}" fill="{fill}">{item}</text>'''

    svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="{W}" y2="{H}" gradientUnits="userSpaceOnUse">
      <stop offset="0%"   stop-color="#0c0c0e"/>
      <stop offset="100%" stop-color="#101014"/>
    </linearGradient>
    <linearGradient id="rule-grad" x1="0" y1="0" x2="0" y2="{H}" gradientUnits="userSpaceOnUse">
      <stop offset="0%"   stop-color="#c9a96e" stop-opacity="0"/>
      <stop offset="35%"  stop-color="#c9a96e" stop-opacity="0.9"/>
      <stop offset="65%"  stop-color="#c9a96e" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#c9a96e" stop-opacity="0"/>
    </linearGradient>
    <filter id="noise" color-interpolation-filters="linearRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch" result="n"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.06 0" in="n"/>
    </filter>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" filter="url(#noise)" style="pointer-events:none;"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" stroke="#ffffff" stroke-opacity="0.06" stroke-width="1" fill="none"/>
  <rect x="0" y="0" width="2" height="{H}" fill="url(#rule-grad)"/>

  <!-- Section label -->
  <text x="24" y="30" font-family="'Courier New',Courier,monospace" font-size="10" fill="#374151" letter-spacing="1.5">STACK</text>

  {cols_svg}
</svg>'''
    return svg

def main():
    print("Generating tech-dashboard.svg...")
    svg = generate_stack()
    with open("tech-dashboard.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("  Written -> tech-dashboard.svg")

if __name__ == "__main__":
    main()
