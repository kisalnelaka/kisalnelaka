import os

def generate_showcase():
    W, H = 860, 210

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
  <text x="24" y="36" font-family="'Courier New',Courier,monospace" font-size="10" fill="#374151" letter-spacing="1.5">SYSTEMS</text>

  <!-- Vertical card divider -->
  <line x1="430" y1="20" x2="430" y2="{H - 20}" stroke="#ffffff" stroke-opacity="0.05" stroke-width="1"/>

  <!-- ============================== -->
  <!-- LEFT: NexusFlow ERP            -->
  <!-- ============================== -->
  <g transform="translate(24, 55)">
    <!-- Project name -->
    <text x="0" y="0" font-family="system-ui,-apple-system,sans-serif" font-size="18" font-weight="600" fill="#f4f4f5">NexusFlow ERP</text>
    <text x="0" y="20" font-family="'Courier New',Courier,monospace" font-size="10" fill="#4b5563">multi-tenant saas infrastructure</text>

    <line x1="0" y1="34" x2="380" y2="34" stroke="#1f1f23" stroke-width="1"/>

    <!-- Description -->
    <text x="0" y="56" font-family="system-ui,-apple-system,sans-serif" font-size="12.5" fill="#52525b">Automated tenant scoping with guaranteed data isolation.</text>
    <text x="0" y="73" font-family="system-ui,-apple-system,sans-serif" font-size="12.5" fill="#52525b">Zero bleed between tenants, async inter-service comms.</text>

    <!-- Key numbers: no fluff, just facts -->
    <g transform="translate(0, 100)">
      <text x="0"   y="0" font-family="system-ui,-apple-system,sans-serif" font-size="20" font-weight="600" fill="#e4e4e7">100%</text>
      <text x="0"   y="16" font-family="system-ui,-apple-system,sans-serif" font-size="10" fill="#4b5563">data isolation</text>

      <text x="110" y="0" font-family="system-ui,-apple-system,sans-serif" font-size="20" font-weight="600" fill="#e4e4e7">&lt;12ms</text>
      <text x="110" y="16" font-family="system-ui,-apple-system,sans-serif" font-size="10" fill="#4b5563">inter-service latency</text>

      <text x="250" y="0" font-family="system-ui,-apple-system,sans-serif" font-size="20" font-weight="600" fill="#e4e4e7">N</text>
      <text x="265" y="0" font-family="system-ui,-apple-system,sans-serif" font-size="20" font-weight="300" fill="#4b5563">tenants</text>
      <text x="250" y="16" font-family="system-ui,-apple-system,sans-serif" font-size="10" fill="#4b5563">horizontal scale</text>
    </g>

    <!-- Stack -->
    <text x="0" y="140" font-family="'Courier New',Courier,monospace" font-size="10.5" fill="#374151">Laravel 11 · Filament v3 · MySQL · Redis</text>
  </g>

  <!-- ============================== -->
  <!-- RIGHT: TheNet                  -->
  <!-- ============================== -->
  <g transform="translate(450, 55)">
    <text x="0" y="0" font-family="system-ui,-apple-system,sans-serif" font-size="18" font-weight="600" fill="#f4f4f5">TheNet</text>
    <text x="0" y="20" font-family="'Courier New',Courier,monospace" font-size="10" fill="#4b5563">decentralized p2p mesh network</text>

    <line x1="0" y1="34" x2="380" y2="34" stroke="#1f1f23" stroke-width="1"/>

    <text x="0" y="56" font-family="system-ui,-apple-system,sans-serif" font-size="12.5" fill="#52525b">Real-time peer synchronization with no cloud dependency.</text>
    <text x="0" y="73" font-family="system-ui,-apple-system,sans-serif" font-size="12.5" fill="#52525b">WebSocket mesh, file orchestration, offline-first design.</text>

    <g transform="translate(0, 100)">
      <text x="0"   y="0" font-family="system-ui,-apple-system,sans-serif" font-size="20" font-weight="600" fill="#e4e4e7">0</text>
      <text x="0"   y="16" font-family="system-ui,-apple-system,sans-serif" font-size="10" fill="#4b5563">cloud dependencies</text>

      <text x="110" y="0" font-family="system-ui,-apple-system,sans-serif" font-size="20" font-weight="600" fill="#e4e4e7">P2P</text>
      <text x="110" y="16" font-family="system-ui,-apple-system,sans-serif" font-size="10" fill="#4b5563">full mesh sync</text>

      <text x="250" y="0" font-family="system-ui,-apple-system,sans-serif" font-size="20" font-weight="600" fill="#e4e4e7">WS</text>
      <text x="250" y="16" font-family="system-ui,-apple-system,sans-serif" font-size="10" fill="#4b5563">transport layer</text>
    </g>

    <text x="0" y="140" font-family="'Courier New',Courier,monospace" font-size="10.5" fill="#374151">Node.js · WebSockets · Local-First</text>
  </g>

</svg>'''
    return svg

def main():
    print("Generating showcase-card.svg...")
    svg = generate_showcase()
    with open("showcase-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("  Written -> showcase-card.svg")

if __name__ == "__main__":
    main()
