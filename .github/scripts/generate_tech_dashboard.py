import os
import json
import urllib.request
import math
from datetime import datetime

# GitHub Config
USERNAME = "kisalnelaka"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_repos():
    """Fetch all public repositories for the user."""
    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=pushed"
    headers = {"User-Agent": "Tech-Dashboard-Generator"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching repos: {e}")
        return []

def aggregate_languages(repos):
    """Aggregate language stats from repositories."""
    lang_stats = {}
    for repo in repos:
        lang = repo.get("language")
        if lang:
            lang_stats[lang] = lang_stats.get(lang, 0) + 1
    
    # Sort by count and take top 6 for the radar chart
    sorted_langs = sorted(lang_stats.items(), key=lambda x: x[1], reverse=True)
    return sorted_langs[:6]

def get_radar_points(stats, center_x, center_y, max_radius):
    """Calculate points for the radar chart polygon."""
    num_vars = len(stats)
    if num_vars == 0:
        return ""
    
    angle_step = (2 * math.pi) / num_vars
    points = []
    
    # Normalize values (0 to 1) based on the max value in stats
    max_val = max([s[1] for s in stats]) if stats else 1
    
    for i, (name, val) in enumerate(stats):
        # Scale value to at least 30% for visibility even if count is low
        scale = 0.3 + (0.7 * (val / max_val))
        radius = max_radius * scale
        angle = i * angle_step - (math.pi / 2) # Start from top
        
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        points.append(f"{x},{y}")
        
    return " ".join(points)

def generate_svg(lang_stats):
    width = 850
    height = 420
    cx, cy = 250, 220
    radius = 120
    
    # Theme Colors (Professional Dark & Vibrant)
    bg_start = "#030712"
    bg_end = "#0f172a"
    accent_primary = "#38bdf8" # Sky Blue
    accent_secondary = "#10b981" # Emerald
    accent_tertiary = "#8b5cf6" # Violet
    text_main = "#f8fafc"
    text_dim = "#94a3b8"
    grid_color = "rgba(148, 163, 184, 0.15)"
    
    # Radar Data
    points = get_radar_points(lang_stats, cx, cy, radius)
    
    svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&amp;display=swap');
        .text {{ font-family: 'Inter', system-ui, sans-serif; }}
        .label {{ font-size: 12px; font-weight: 600; fill: {text_dim}; }}
        .title {{ font-size: 24px; font-weight: 700; fill: {text_main}; }}
        .subtitle {{ font-size: 14px; fill: {accent_primary}; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; }}
    </style>
    
    <defs>
        <linearGradient id="bg_grad" x1="0" y1="0" x2="{width}" y2="{height}" gradientUnits="userSpaceOnUse">
            <stop stop-color="{bg_start}"/>
            <stop offset="1" stop-color="{bg_end}"/>
        </linearGradient>
        <linearGradient id="poly_grad" x1="{cx}" y1="{cy-radius}" x2="{cx}" y2="{cy+radius}" gradientUnits="userSpaceOnUse">
            <stop stop-color="{accent_primary}" stop-opacity="0.6"/>
            <stop offset="1" stop-color="{accent_tertiary}" stop-opacity="0.4"/>
        </linearGradient>
        <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
    </defs>
    
    <!-- Background Card -->
    <rect width="{width}" height="{height}" rx="24" fill="url(#bg_grad)" />
    <rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="23.5" stroke="rgba(255,255,255,0.05)" />
    
    <!-- Header -->
    <text x="40" y="60" class="text title">Technical Arsenal</text>
    <text x="40" y="85" class="text subtitle">Dynamic Language Distribution</text>
    <rect x="40" y="95" width="80" height="4" rx="2" fill="{accent_primary}" />
    
    <!-- Status Indicator -->
    <g transform="translate({width - 180}, 55)">
        <circle cx="0" cy="0" r="4" fill="{accent_secondary}">
            <animate attributeName="opacity" values="1;0.4;1" dur="3s" repeatCount="indefinite" />
        </circle>
        <text x="15" y="5" class="text label" fill="{accent_secondary}">Live Ecosystem Data</text>
    </g>

    <!-- Radar Chart Grid -->
    <g>
    '''
    
    # Grid circles
    for r in [0.25, 0.5, 0.75, 1.0]:
        svg += f'<circle cx="{cx}" cy="{cy}" r="{radius * r}" stroke="{grid_color}" stroke-width="1" fill="none" />'
    
    # Grid lines & Labels
    num_vars = len(lang_stats)
    if num_vars > 0:
        angle_step = (2 * math.pi) / num_vars
        for i, (name, val) in enumerate(lang_stats):
            angle = i * angle_step - (math.pi / 2)
            x2 = cx + radius * math.cos(angle)
            y2 = cy + radius * math.sin(angle)
            svg += f'<line x1="{cx}" y1="{cy}" x2="{x2}" y2="{y2}" stroke="{grid_color}" stroke-width="1" />'
            
            # Label positioning
            label_dist = radius + 30
            lx = cx + label_dist * math.cos(angle)
            ly = cy + label_dist * math.sin(angle)
            anchor = "middle" if abs(lx - cx) < 10 else "start" if lx > cx else "end"
            svg += f'<text x="{lx}" y="{ly + 5}" class="text label" text-anchor="{anchor}">{name}</text>'

    # Radar Polygon
    if points:
        svg += f'''
        <polygon points="{points}" fill="url(#poly_grad)" stroke="{accent_primary}" stroke-width="2" filter="url(#glow)">
            <animate attributeName="opacity" values="0.7;0.9;0.7" dur="4s" repeatCount="indefinite" />
        </polygon>
        '''
    
    svg += '</g>'
    
    # Right Side: Expertise Breakdown
    # We'll use the counts to show some "Power Levels"
    svg += f'<g transform="translate(500, 140)">'
    for i, (name, count) in enumerate(lang_stats):
        bar_y = i * 45
        bar_w = 250
        # Calculate percentage based on total repos or just a max
        progress = min(0.95, 0.4 + (count / max([s[1] for s in lang_stats]) * 0.55))
        
        svg += f'''
        <g transform="translate(0, {bar_y})">
            <text x="0" y="0" class="text label" fill="{text_main}">{name}</text>
            <text x="{bar_w}" y="0" class="text label" text-anchor="end" fill="{text_dim}">{count} Projects</text>
            <rect x="0" y="10" width="{bar_w}" height="6" rx="3" fill="rgba(255,255,255,0.05)" />
            <rect x="0" y="10" width="{bar_w * progress}" height="6" rx="3" fill="{accent_primary}">
                <animate attributeName="width" from="0" to="{bar_w * progress}" dur="1s" fill="freeze" />
            </rect>
        </g>
        '''
    svg += '</g>'
    
    # Footer
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    svg += f'''
    <text x="{width - 40}" y="{height - 30}" class="text label" text-anchor="end" fill="{text_dim}">Last Updated: {timestamp} • Powered by GitHub API</text>
    </svg>'''
    
    return svg

def main():
    print("Fetching repository data...")
    repos = fetch_repos()
    if not repos:
        print("No repos found or error occurred.")
        return
        
    print(f"Analyzing {len(repos)} repositories...")
    lang_stats = aggregate_languages(repos)
    
    print("Generating Dynamic SVG...")
    svg_content = generate_svg(lang_stats)
    
    output_path = "tech-dashboard.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    main()
