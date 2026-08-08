import os
import math

def generate_showcase_svg():
    W, H = 860, 260

    svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="{W}" y2="{H}" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>
    <!-- Left card top accent -->
    <linearGradient id="card-l-top" x1="0" y1="0" x2="400" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0"/>
    </linearGradient>
    <!-- Right card top accent -->
    <linearGradient id="card-r-top" x1="0" y1="0" x2="400" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#a78bfa" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#a78bfa" stop-opacity="0"/>
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

  <!-- Base -->
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" filter="url(#noise)" style="pointer-events:none;"/>
  <rect x="0" y="0" width="3" height="{H}" fill="url(#accent-strip)"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" stroke="#ffffff" stroke-opacity="0.05" stroke-width="1" fill="none"/>

  <!-- Section header -->
  <text x="26" y="38" font-family="'Courier New', monospace" font-size="10" font-weight="700" fill="#64748b" letter-spacing="1.5">FEATURED SYSTEMS</text>
  <line x1="26" y1="50" x2="{W - 26}" y2="50" stroke="#1e293b" stroke-width="1"/>

  <!-- ============ LEFT CARD: NexusFlow ERP ============ -->
  <g transform="translate(20, 58)">
    <!-- Card Background -->
    <rect x="0" y="0" width="400" height="190" rx="8" fill="#0a1628" stroke="#1e293b" stroke-width="1"/>
    <!-- Top Accent Line (animated) -->
    <rect x="0" y="0" width="400" height="2" rx="1" fill="url(#card-l-top)"/>

    <!-- Title area -->
    <text x="20" y="30" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="700" fill="#f1f5f9">NexusFlow ERP</text>
    <rect x="280" y="14" width="100" height="18" rx="9" fill="#22c55e" fill-opacity="0.1"/>
    <circle cx="294" cy="23" r="3" fill="#22c55e"><animate attributeName="opacity" values="1;0.3;1" dur="2.5s" repeatCount="indefinite"/></circle>
    <text x="302" y="27" font-family="system-ui, -apple-system, sans-serif" font-size="9" font-weight="600" fill="#86efac">100% Isolated</text>
    
    <text x="20" y="48" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#64748b">Multi-tenant SaaS. Automated scoping, zero data bleed.</text>

    <!-- Minimal Architecture Diagram -->
    <g transform="translate(20, 65)">
      <!-- Tenant Nodes -->
      <rect x="0" y="10" width="70" height="22" rx="4" fill="#1e293b" stroke="#334155"/>
      <text x="35" y="25" text-anchor="middle" font-family="'Courier New', monospace" font-size="9" fill="#94a3b8">Tenant A</text>

      <rect x="0" y="42" width="70" height="22" rx="4" fill="#1e293b" stroke="#334155"/>
      <text x="35" y="57" text-anchor="middle" font-family="'Courier New', monospace" font-size="9" fill="#94a3b8">Tenant B</text>

      <!-- Data packet animations from tenants to router -->
      <line x1="70" y1="21" x2="115" y2="33" stroke="#334155" stroke-width="1"/>
      <line x1="70" y1="53" x2="115" y2="41" stroke="#334155" stroke-width="1"/>
      <circle r="2.5" fill="#38bdf8" opacity="0.9">
        <animateMotion dur="1.8s" repeatCount="indefinite" path="M70,21 L115,33"/>
        <animate attributeName="opacity" values="0;1;0" dur="1.8s" repeatCount="indefinite"/>
      </circle>
      <circle r="2.5" fill="#38bdf8" opacity="0.9">
        <animateMotion dur="2.2s" repeatCount="indefinite" begin="0.8s" path="M70,53 L115,41"/>
        <animate attributeName="opacity" values="0;1;0" dur="2.2s" repeatCount="indefinite" begin="0.8s"/>
      </circle>

      <!-- Router -->
      <rect x="115" y="22" width="90" height="30" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-opacity="0.4"/>
      <text x="160" y="41" text-anchor="middle" font-family="'Courier New', monospace" font-size="9" fill="#7dd3fc">SCOPE ROUTER</text>

      <!-- Router to DB -->
      <line x1="205" y1="37" x2="250" y2="37" stroke="#334155" stroke-width="1"/>
      <circle r="2.5" fill="#38bdf8" opacity="0.9">
        <animateMotion dur="1.4s" repeatCount="indefinite" begin="0.4s" path="M205,37 L250,37"/>
        <animate attributeName="opacity" values="0;1;0" dur="1.4s" repeatCount="indefinite" begin="0.4s"/>
      </circle>

      <!-- DB -->
      <rect x="250" y="22" width="70" height="30" rx="4" fill="#1e293b" stroke="#334155"/>
      <text x="285" y="41" text-anchor="middle" font-family="'Courier New', monospace" font-size="9" fill="#94a3b8">SECURE DB</text>
    </g>

    <!-- Tech Pills -->
    <g transform="translate(20, 150)">
      <rect x="0" y="0" width="64" height="18" rx="3" fill="#1e293b"/>
      <text x="32" y="13" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="#94a3b8">Laravel 11</text>
      <rect x="70" y="0" width="68" height="18" rx="3" fill="#1e293b"/>
      <text x="104" y="13" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="#94a3b8">Filament v3</text>
      <rect x="144" y="0" width="48" height="18" rx="3" fill="#1e293b"/>
      <text x="168" y="13" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="#94a3b8">MySQL</text>
      <rect x="198" y="0" width="40" height="18" rx="3" fill="#1e293b"/>
      <text x="218" y="13" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="#94a3b8">Redis</text>
    </g>
  </g>

  <!-- ============ RIGHT CARD: TheNet ============ -->
  <g transform="translate(440, 58)">
    <!-- Card Background -->
    <rect x="0" y="0" width="400" height="190" rx="8" fill="#0d0a1e" stroke="#1e293b" stroke-width="1"/>
    <!-- Top Accent Line -->
    <rect x="0" y="0" width="400" height="2" rx="1" fill="url(#card-r-top)"/>

    <!-- Title area -->
    <text x="20" y="30" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="700" fill="#f1f5f9">TheNet</text>
    <rect x="265" y="14" width="115" height="18" rx="9" fill="#38bdf8" fill-opacity="0.08"/>
    <circle cx="279" cy="23" r="3" fill="#38bdf8"><animate attributeName="opacity" values="1;0.3;1" dur="3s" repeatCount="indefinite"/></circle>
    <text x="287" y="27" font-family="system-ui, -apple-system, sans-serif" font-size="9" font-weight="600" fill="#7dd3fc">Zero Cloud Dep.</text>

    <text x="20" y="48" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#64748b">Decentralized P2P mesh. Real-time sync, no middleman.</text>

    <!-- Minimal P2P Diagram -->
    <g transform="translate(40, 70)">
      <!-- Nodes -->
      <circle cx="0" cy="40" r="16" fill="#1e293b" stroke="#a78bfa" stroke-opacity="0.5"/>
      <text x="0" y="44" text-anchor="middle" font-family="'Courier New', monospace" font-size="9" fill="#c4b5fd">P1</text>

      <circle cx="100" cy="10" r="16" fill="#1e293b" stroke="#334155"/>
      <text x="100" y="14" text-anchor="middle" font-family="'Courier New', monospace" font-size="9" fill="#94a3b8">P2</text>

      <circle cx="100" cy="70" r="16" fill="#1e293b" stroke="#334155"/>
      <text x="100" y="74" text-anchor="middle" font-family="'Courier New', monospace" font-size="9" fill="#94a3b8">P3</text>

      <circle cx="200" cy="40" r="16" fill="#1e293b" stroke="#22c55e" stroke-opacity="0.5"/>
      <text x="200" y="44" text-anchor="middle" font-family="'Courier New', monospace" font-size="9" fill="#86efac">P4</text>

      <!-- Connection lines -->
      <line x1="16" y1="35" x2="85" y2="17" stroke="#334155" stroke-dasharray="3 3"/>
      <line x1="16" y1="45" x2="85" y2="63" stroke="#334155" stroke-dasharray="3 3"/>
      <line x1="100" y1="26" x2="100" y2="54" stroke="#334155" stroke-dasharray="3 3"/>
      <line x1="116" y1="17" x2="185" y2="35" stroke="#334155" stroke-dasharray="3 3"/>
      <line x1="116" y1="63" x2="185" y2="45" stroke="#334155" stroke-dasharray="3 3"/>

      <!-- Animated packets -->
      <circle r="2" fill="#a78bfa">
        <animateMotion dur="1.5s" repeatCount="indefinite" path="M16,35 L85,17"/>
        <animate attributeName="opacity" values="0;1;0" dur="1.5s" repeatCount="indefinite"/>
      </circle>
      <circle r="2" fill="#a78bfa">
        <animateMotion dur="2s" repeatCount="indefinite" begin="0.5s" path="M16,45 L85,63"/>
        <animate attributeName="opacity" values="0;1;0" dur="2s" repeatCount="indefinite" begin="0.5s"/>
      </circle>
      <circle r="2" fill="#22c55e">
        <animateMotion dur="1.2s" repeatCount="indefinite" begin="0.2s" path="M116,17 L185,35"/>
        <animate attributeName="opacity" values="0;1;0" dur="1.2s" repeatCount="indefinite" begin="0.2s"/>
      </circle>
      <circle r="2" fill="#22c55e">
        <animateMotion dur="1.6s" repeatCount="indefinite" begin="0.9s" path="M116,63 L185,45"/>
        <animate attributeName="opacity" values="0;1;0" dur="1.6s" repeatCount="indefinite" begin="0.9s"/>
      </circle>
    </g>

    <!-- Tech Pills -->
    <g transform="translate(20, 150)">
      <rect x="0" y="0" width="52" height="18" rx="3" fill="#1e293b"/>
      <text x="26" y="13" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="#94a3b8">Node.js</text>
      <rect x="58" y="0" width="74" height="18" rx="3" fill="#1e293b"/>
      <text x="95" y="13" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="#94a3b8">WebSockets</text>
      <rect x="138" y="0" width="60" height="18" rx="3" fill="#1e293b"/>
      <text x="168" y="13" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="#94a3b8">Local-First</text>
    </g>
  </g>

</svg>'''

    return svg

def main():
    print("Generating showcase-card.svg...")
    svg = generate_showcase_svg()
    out = "showcase-card.svg"
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"  Written -> {out}")

if __name__ == "__main__":
    main()
