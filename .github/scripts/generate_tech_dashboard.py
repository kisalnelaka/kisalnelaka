import os
import math
from datetime import datetime, timezone

def generate_tech_dashboard_svg():
    W, H = 860, 400
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Define the core technologies for the radial HUD
    tech_nodes = [
        {"name": "LARAVEL", "pct": 95, "col": "#ff2d20", "desc": "SaaS Engine", "angle": 0},
        {"name": "REACT", "pct": 88, "col": "#61dafb", "desc": "UI Core", "angle": 60},
        {"name": "NODE.JS", "pct": 85, "col": "#68a063", "desc": "Mesh Sync", "angle": 120},
        {"name": "SEC / OSCP", "pct": 85, "col": "#ef4444", "desc": "Offensive", "angle": 180},
        {"name": "DB ARCH", "pct": 88, "col": "#f59e0b", "desc": "Isolation", "angle": 240},
        {"name": "TYPESCRIPT", "pct": 82, "col": "#3178c6", "desc": "Strict Auth", "angle": 300},
    ]

    center_x, center_y = W / 2, H / 2
    radius = 130 # Distance of satellite nodes from center

    # Generate connection lines
    connection_lines = ""
    for node in tech_nodes:
        rad = math.radians(node["angle"])
        nx = center_x + radius * math.cos(rad)
        ny = center_y + radius * math.sin(rad)
        
        connection_lines += f'''
    <line x1="{center_x}" y1="{center_y}" x2="{nx}" y2="{ny}" stroke="{node['col']}" stroke-width="2" stroke-opacity="0.3" stroke-dasharray="4 4">
        <animate attributeName="stroke-dashoffset" from="8" to="0" dur="2s" repeatCount="indefinite" />
    </line>
    '''

    # Generate satellite nodes
    nodes_svg = ""
    for i, node in enumerate(tech_nodes):
        rad = math.radians(node["angle"])
        nx = center_x + radius * math.cos(rad)
        ny = center_y + radius * math.sin(rad)
        
        col = node['col']
        pct = node['pct']
        
        # Calculate SVG stroke-dasharray for circular progress
        circumference = 2 * math.pi * 35
        dash_len = (pct / 100) * circumference
        
        nodes_svg += f'''
    <g transform="translate({nx}, {ny})">
        <!-- Outer Glow Ring -->
        <circle cx="0" cy="0" r="40" fill="none" stroke="{col}" stroke-width="1" opacity="0.1"/>
        
        <!-- Background Track -->
        <circle cx="0" cy="0" r="35" fill="none" stroke="#1a1a2e" stroke-width="4"/>
        
        <!-- Animated Progress Ring -->
        <circle cx="0" cy="0" r="35" fill="none" stroke="{col}" stroke-width="4" stroke-dasharray="{circumference}" stroke-dashoffset="{circumference}" stroke-linecap="round" transform="rotate(-90)">
            <animate attributeName="stroke-dashoffset" from="{circumference}" to="{circumference - dash_len}" dur="1.5s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1" keyTimes="0;1"/>
        </circle>
        
        <!-- Center Dot -->
        <circle cx="0" cy="0" r="3" fill="{col}" opacity="0.8"/>
        
        <!-- Labels -->
        <text x="0" y="4" text-anchor="middle" font-family="monospace" font-size="14" font-weight="bold" fill="#ffffff">{pct}%</text>
        <text x="0" y="55" text-anchor="middle" font-family="monospace" font-size="10" font-weight="bold" fill="{col}">{node['name']}</text>
        <text x="0" y="68" text-anchor="middle" font-family="monospace" font-size="8" fill="#888888">{node['desc']}</text>
    </g>
    '''

    svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Dark Tech Background -->
    <radialGradient id="bg" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#0a0f18"/>
      <stop offset="100%" stop-color="#02040a"/>
    </radialGradient>
    
    <filter id="core-glow">
        <feGaussianBlur stdDeviation="8" result="blur" />
        <feMerge>
            <feMergeNode in="blur" />
            <feMergeNode in="SourceGraphic" />
        </feMerge>
    </filter>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  
  <!-- Subtle Grid -->
  <pattern id="hex-bg" width="60" height="103.923" patternUnits="userSpaceOnUse" patternTransform="scale(0.5)">
     <path d="M30 0L60 17.32V51.96L30 69.28L0 51.96V17.32Z" fill="none" stroke="#333344" stroke-width="1" stroke-opacity="0.3"/>
     <path d="M30 103.92L60 86.6V51.96L30 69.28L0 51.96V86.6Z" fill="none" stroke="#333344" stroke-width="1" stroke-opacity="0.3"/>
  </pattern>
  <rect width="{W}" height="{H}" fill="url(#hex-bg)"/>

  {connection_lines}

  <!-- Central Hub -->
  <g transform="translate({center_x}, {center_y})">
      <!-- Pulsing Core -->
      <circle cx="0" cy="0" r="50" fill="#0a0f18" stroke="#00f0ff" stroke-width="2" filter="url(#core-glow)">
         <animate attributeName="r" values="48;52;48" dur="3s" repeatCount="indefinite" />
      </circle>
      
      <!-- Inner Ring -->
      <circle cx="0" cy="0" r="40" fill="none" stroke="#a855f7" stroke-width="1" stroke-dasharray="10 5">
          <animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="10s" repeatCount="indefinite"/>
      </circle>
      
      <text x="0" y="-5" text-anchor="middle" font-family="monospace" font-size="12" font-weight="bold" fill="#00f0ff">SYSTEM</text>
      <text x="0" y="10" text-anchor="middle" font-family="monospace" font-size="12" font-weight="bold" fill="#a855f7">CORE</text>
  </g>

  {nodes_svg}

  <!-- Corner Brackets -->
  <path d="M 10 30 L 10 10 L 30 10" fill="none" stroke="#00f0ff" stroke-width="2" opacity="0.5"/>
  <path d="M {W-30} 10 L {W-10} 10 L {W-10} 30" fill="none" stroke="#00f0ff" stroke-width="2" opacity="0.5"/>
  <path d="M 10 {H-30} L 10 {H-10} L 30 {H-10}" fill="none" stroke="#00f0ff" stroke-width="2" opacity="0.5"/>
  <path d="M {W-30} {H-10} L {W-10} {H-10} L {W-10} {H-30}" fill="none" stroke="#00f0ff" stroke-width="2" opacity="0.5"/>

  <!-- Footer Info -->
  <text x="20" y="{H-20}" font-family="monospace" font-size="10" fill="#666666">RADIAL.HUD.V2 // IMPERIAL SYSTEMS</text>
  <text x="{W-20}" y="{H-20}" text-anchor="end" font-family="monospace" font-size="10" fill="#666666">SYNC_TIME: {now}</text>

</svg>'''

    return svg

def main():
    print("Generating God-Tier tech-dashboard.svg...")
    svg = generate_tech_dashboard_svg()
    out = "tech-dashboard.svg"
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"  Successfully written -> {out}")

if __name__ == "__main__":
    main()
