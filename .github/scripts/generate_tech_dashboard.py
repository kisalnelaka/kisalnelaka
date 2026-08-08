import os
import json
from datetime import datetime, timezone

def generate_tech_dashboard_svg():
    W, H = 860, 360
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Left Column: Core Web Engineering Stack
    web_stack = [
        ("Laravel 11 / PHP 8.3", 95, "Primary Framework · Core SaaS Engine", "#ff2d20"),
        ("React.js & Frontend",   88, "Interactive UI · SPA Architecture", "#61dafb"),
        ("Node.js & Async I/O",  85, "Microservices · Event Loop Ops", "#68a063"),
        ("TypeScript",           82, "Strict Static Typing · Full Stack", "#38bdf8"),
        ("Database Architecture", 88, "PostgreSQL · MySQL · Redis Scoping", "#f59e0b"),
        ("Tailwind CSS",         90, "Custom Design Systems & Styling", "#38bdf8"),
    ]

    # Right Column: Systems, Security & DevOps
    systems_stack = [
        ("Multi-Tenant Isolation", 96, "Automated Tenant Scoping & Auth", "#00ff9f"),
        ("Decentralized P2P Mesh", 90, "WebSockets · Cloud-Free Sync", "#a855f7"),
        ("Offensive Security",    85, "OSCP-Standard Pen Testing", "#ef4444"),
        ("SIEM & Log Analytics",   80, "Splunk · Threat Detection", "#f97316"),
        ("Docker & Infra Automation", 85, "CI/CD · Container Orchestration", "#2496ed"),
        ("Non-Blocking Fibers",   82, "High-Concurrency Async PHP", "#c084fc"),
    ]

    def render_column(items, x_offset):
        rows = ""
        bar_w = 200
        for i, (name, pct, note, col) in enumerate(items):
            y = 110 + i * 39
            fill_w = round(bar_w * (pct / 100), 1)
            delay = i * 0.06

            rows += f'''
      <!-- Item {i} -->
      <g transform="translate({x_offset}, {y})">
        <text x="0" y="0" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="700" fill="#f8fafc">{name}</text>
        <text x="380" y="0" text-anchor="end" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="800" fill="{col}">{pct}%</text>
        
        <!-- Track Background -->
        <rect x="0" y="8" width="380" height="6" rx="3" fill="#1e293b" fill-opacity="0.6"/>
        <!-- Active Bar -->
        <rect x="0" y="8" width="0" height="6" rx="3" fill="{col}">
          <animate attributeName="width" from="0" to="{fill_w * 1.9}" dur="0.8s" begin="{delay}s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1" keyTimes="0;1"/>
        </rect>
        <text x="0" y="26" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="#94a3b8">{note}</text>
      </g>'''
        return rows

    left_rows = render_column(web_stack, 30)
    right_rows = render_column(systems_stack, 450)

    svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="dash-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#080d1a"/>
      <stop offset="100%" stop-color="#030712"/>
    </linearGradient>

    <!-- Border Gradient -->
    <linearGradient id="dash-border" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f0ff" stop-opacity="0.6"/>
      <stop offset="50%" stop-color="#38bdf8" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#00ff9f" stop-opacity="0.6"/>
    </linearGradient>

    <radialGradient id="glow-ambient" cx="50%" cy="0%" r="50%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.1"/>
      <stop offset="100%" stop-color="transparent"/>
    </radialGradient>
  </defs>

  <!-- Container Base -->
  <rect width="{W}" height="{H}" rx="18" fill="url(#dash-bg)"/>
  <rect width="{W}" height="{H}" rx="18" fill="url(#glow-ambient)"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="17.5" stroke="url(#dash-border)" stroke-width="1.2" fill="none"/>

  <!-- Top Glass Bar -->
  <rect x="1" y="1" width="{W-2}" height="42" rx="17" fill="#ffffff" fill-opacity="0.02"/>
  <line x1="1" y1="43" x2="{W-1}" y2="43" stroke="#ffffff" stroke-opacity="0.08" stroke-width="1"/>

  <!-- Window OS Dots -->
  <circle cx="24" cy="22" r="5" fill="#ff5f57"/>
  <circle cx="40" cy="22" r="5" fill="#febc2e"/>
  <circle cx="56" cy="22" r="5" fill="#28c840"/>

  <text x="76" y="26" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="800" fill="#00f0ff" letter-spacing="1">TECHNICAL ARSENAL</text>
  <text x="235" y="25" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="500" fill="#64748b">// Verified Production Competencies &amp; System Mastery</text>

  <rect x="730" y="13" width="110" height="18" rx="9" fill="#00ff9f" fill-opacity="0.12"/>
  <circle cx="742" cy="22" r="3" fill="#00ff9f"/>
  <text x="750" y="25" font-family="system-ui, -apple-system, sans-serif" font-size="9" font-weight="700" fill="#00ff9f">SYSTEM VERIFIED</text>

  <!-- Column Headers -->
  <text x="30" y="78" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="800" fill="#38bdf8" letter-spacing="1.2">01 / CORE WEB STACK</text>
  <line x1="30" y1="86" x2="410" y2="86" stroke="#38bdf8" stroke-opacity="0.2" stroke-width="1"/>

  <text x="450" y="78" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="800" fill="#00ff9f" letter-spacing="1.2">02 / ARCHITECTURE &amp; SECURITY</text>
  <line x1="450" y1="86" x2="830" y2="86" stroke="#00ff9f" stroke-opacity="0.2" stroke-width="1"/>

  <!-- Render Columns -->
  {left_rows}
  {right_rows}

  <!-- Footer -->
  <line x1="30" y1="332" x2="{W-30}" y2="332" stroke="#ffffff" stroke-opacity="0.08" stroke-width="1"/>
  <text x="30" y="348" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="#64748b">Verified Stack Benchmark · Updated {now}</text>
  <text x="{W-30}" y="348" text-anchor="end" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="#00f0ff">Kisal Nelaka Engineering Hub</text>
</svg>'''

    return svg

def main():
    print("Generating updated high-end tech-dashboard.svg...")
    svg = generate_tech_dashboard_svg()
    out = "tech-dashboard.svg"
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"  Successfully written -> {out}")

if __name__ == "__main__":
    main()
