import urllib.request
import xml.etree.ElementTree as ET
import os
from datetime import datetime, timezone

MEDIUM_USER = "kisalnelaka6"

def fetch_posts(limit=3):
    url = f"https://medium.com/feed/@{MEDIUM_USER}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            root = ET.fromstring(r.read().decode("utf-8"))
        posts = []
        for item in root.findall(".//item"):
            title   = (item.find("title").text or "").strip()
            link    = (item.find("link").text or "").split("?")[0]
            pub_date = item.find("pubDate")
            date_str = ""
            if pub_date is not None and pub_date.text:
                try:
                    # RFC 822 -> simple date
                    from email.utils import parsedate_to_datetime
                    dt = parsedate_to_datetime(pub_date.text)
                    date_str = dt.strftime("%b %Y")
                except Exception:
                    pass
            if title and link:
                posts.append({"title": title, "link": link, "date": date_str})
        return posts[:limit]
    except Exception as e:
        print(f"  [warn] Medium RSS -> {e}")
        return []

def clip(text, max_len=62):
    return text if len(text) <= max_len else text[:max_len - 1].rstrip() + "..."

def generate_writing_svg(posts):
    W, H = 860, 170
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    rows_svg = ""
    for i, post in enumerate(posts):
        y_base = 68 + i * 32
        title_clipped = clip(post["title"])
        date_label = post["date"]

        rows_svg += f'''
  <!-- Article {i+1} -->
  <line x1="24" y1="{y_base + 18}" x2="{W - 24}" y2="{y_base + 18}" stroke="#1a1a1f" stroke-width="1"/>
  <!-- Index number -->
  <text x="24" y="{y_base + 12}" font-family="'Courier New',Courier,monospace" font-size="10" fill="#374151">{str(i + 1).zfill(2)}</text>
  <!-- Title -->
  <text x="56" y="{y_base + 12}" font-family="system-ui,-apple-system,sans-serif" font-size="13" font-weight="500" fill="#d1d5db">{title_clipped}</text>
  <!-- Date, right-aligned -->
  <text x="{W - 24}" y="{y_base + 12}" text-anchor="end" font-family="'Courier New',Courier,monospace" font-size="10" fill="#374151">{date_label}</text>'''

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
  <text x="24" y="36" font-family="'Courier New',Courier,monospace" font-size="10" fill="#374151" letter-spacing="1.5">WRITING</text>
  <text x="{W - 24}" y="36" text-anchor="end" font-family="'Courier New',Courier,monospace" font-size="10" fill="#27272a">medium.com/@kisalnelaka6</text>
  <line x1="24" y1="46" x2="{W - 24}" y2="46" stroke="#1a1a1f" stroke-width="1"/>

  {rows_svg}
</svg>'''
    return svg

def main():
    print("Generating writing-card.svg...")
    posts = fetch_posts()
    if not posts:
        # Fallback with known articles so the card never disappears
        posts = [
            {"title": "AETHER: Building a PHP 8.3 Framework Without the Bloat", "link": "https://medium.com/@kisalnelaka6/aether-building-a-php-8-3-framework-without-the-bloat-f0c1a69780ed", "date": ""},
            {"title": "Building InfraFlow: A Production-Grade Multi-Tenant MSP Platform", "link": "https://medium.com/@kisalnelaka6/building-infraflow-a-production-grade-multi-tenant-msp-platform-with-laravel-11-and-filament-v3-b0070a377124", "date": ""},
            {"title": "Bunny: The Laravel Scaffolding Package That Makes Web Dev a Hop", "link": "https://medium.com/@kisalnelaka6/bunny-the-laravel-scaffolding-package-that-makes-web-development-a-hop-7276d4efdf57", "date": ""},
        ]
    for p in posts:
        print(f"  {p['title'][:60]}")
    svg = generate_writing_svg(posts)
    with open("writing-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("  Written -> writing-card.svg")

if __name__ == "__main__":
    main()
