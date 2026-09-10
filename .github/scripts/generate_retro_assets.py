import os

def generate_construction_stripe():
    # Authentic 90s yellow (#FFFF00) & black (#000000) 45-degree hazard stripe
    svg = '''<svg width="100%" height="14" viewBox="0 0 880 14" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="hazard" width="28.28" height="28.28" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="0" y2="28.28" stroke="#FFFF00" stroke-width="14.14" />
      <line x1="14.14" y1="0" x2="14.14" y2="28.28" stroke="#000000" stroke-width="14.14" />
    </pattern>
  </defs>
  <!-- 3D outer bevel -->
  <rect x="0" y="0" width="880" height="14" fill="url(#hazard)" stroke="#808080" stroke-width="1"/>
  <line x1="0" y1="0" x2="880" y2="0" stroke="#FFFFFF" stroke-width="1.5"/>
  <line x1="0" y1="13.5" x2="880" y2="13.5" stroke="#404040" stroke-width="1.5"/>
</svg>'''
    with open("construction-stripe.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("  Written -> construction-stripe.svg")

def generate_groove_rule():
    # Authentic Windows 95 etched 3D groove horizontal divider
    svg = '''<svg width="100%" height="4" viewBox="0 0 880 4" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="880" height="2" fill="#808080"/>
  <rect x="0" y="2" width="880" height="2" fill="#FFFFFF"/>
</svg>'''
    with open("groove-rule.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("  Written -> groove-rule.svg")

def main():
    print("Generating retro decorative SVG assets...")
    generate_construction_stripe()
    generate_groove_rule()

if __name__ == "__main__":
    main()
