import os

def generate_showcase_svg():
    W, H = 860, 240

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

  <!-- Top Title Bar -->
  <text x="30" y="35" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="600" fill="#94a3b8" letter-spacing="1">SYSTEMS SHOWCASE</text>
  <line x1="30" y1="45" x2="{W-30}" y2="45" stroke="#ffffff" stroke-opacity="0.05" stroke-width="1"/>
  
  <!-- ==================== NEXUSFLOW ERP ==================== -->
  <g transform="translate(30, 60)">
    <text x="0" y="20" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="700" fill="#f8fafc">NexusFlow ERP</text>
    <text x="0" y="40" font-family="system-ui, -apple-system, sans-serif" font-size="12" fill="#64748b">Multi-tenant SaaS with 100% data isolation.</text>
    
    <!-- Minimal Diagram -->
    <g transform="translate(0, 70)">
        <rect x="0" y="0" width="60" height="24" rx="4" fill="#1e293b" stroke="#334155" stroke-width="1"/>
        <text x="30" y="16" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#94a3b8">Tenant A</text>

        <rect x="0" y="36" width="60" height="24" rx="4" fill="#1e293b" stroke="#334155" stroke-width="1"/>
        <text x="30" y="52" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#94a3b8">Tenant B</text>
        
        <!-- Connection Lines -->
        <path d="M 60 12 L 100 30" fill="none" stroke="#475569" stroke-width="1"/>
        <path d="M 60 48 L 100 30" fill="none" stroke="#475569" stroke-width="1"/>
        
        <!-- Router -->
        <rect x="100" y="18" width="80" height="24" rx="4" fill="#0f172a" stroke="#38bdf8" stroke-opacity="0.5" stroke-width="1"/>
        <text x="140" y="34" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#38bdf8">Scoped Router</text>
        
        <path d="M 180 30 L 220 30" fill="none" stroke="#475569" stroke-width="1"/>

        <!-- DB -->
        <rect x="220" y="18" width="60" height="24" rx="12" fill="#1e293b" stroke="#334155" stroke-width="1"/>
        <text x="250" y="34" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#94a3b8">Secure DB</text>
    </g>
  </g>

  <!-- ==================== THENET ==================== -->
  <g transform="translate(440, 60)">
    <text x="0" y="20" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="700" fill="#f8fafc">TheNet</text>
    <text x="0" y="40" font-family="system-ui, -apple-system, sans-serif" font-size="12" fill="#64748b">Decentralized P2P mesh network architecture.</text>
    
    <!-- Minimal Diagram -->
    <g transform="translate(0, 70)">
        <circle cx="20" cy="30" r="14" fill="#1e293b" stroke="#334155" stroke-width="1"/>
        <text x="20" y="34" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="#94a3b8">N1</text>

        <circle cx="90" cy="10" r="14" fill="#1e293b" stroke="#334155" stroke-width="1"/>
        <text x="90" y="14" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="#94a3b8">N2</text>
        
        <circle cx="90" cy="50" r="14" fill="#1e293b" stroke="#334155" stroke-width="1"/>
        <text x="90" y="54" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="#94a3b8">N3</text>
        
        <circle cx="160" cy="30" r="14" fill="#1e293b" stroke="#38bdf8" stroke-opacity="0.5" stroke-width="1"/>
        <text x="160" y="34" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="#38bdf8">N4</text>
        
        <!-- Connection Lines -->
        <path d="M 32 24 L 78 16" fill="none" stroke="#475569" stroke-width="1" stroke-dasharray="2 2"/>
        <path d="M 32 36 L 78 44" fill="none" stroke="#475569" stroke-width="1" stroke-dasharray="2 2"/>
        <path d="M 90 24 L 90 36" fill="none" stroke="#475569" stroke-width="1" stroke-dasharray="2 2"/>
        <path d="M 102 16 L 148 24" fill="none" stroke="#475569" stroke-width="1" stroke-dasharray="2 2"/>
        <path d="M 102 44 L 148 36" fill="none" stroke="#475569" stroke-width="1" stroke-dasharray="2 2"/>
    </g>
  </g>

</svg>'''

    return svg

def main():
    print("Generating minimalist showcase-card.svg...")
    svg = generate_showcase_svg()
    out = "showcase-card.svg"
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"  Successfully written -> {out}")

if __name__ == "__main__":
    main()
