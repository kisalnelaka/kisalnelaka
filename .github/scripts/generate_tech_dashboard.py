import os

def main():
    # Tech stack requirements (Refined for a senior/architect profile)
    tech_categories = {
        "Systems & Backend": [
            {"name": "Laravel Internals", "level": "Expert"},
            {"name": "Node.js / Bun", "level": "Expert"},
            {"name": "Python / gRPC", "level": "Advanced"},
            {"name": "Rust / C++", "level": "Proficient"}
        ],
        "Frontend & UI": [
            {"name": "React / Next.js", "level": "Expert"},
            {"name": "TypeScript", "level": "Expert"},
            {"name": "Flutter / Dart", "level": "Expert"},
            {"name": "Tailwind / CSS", "level": "Expert"}
        ],
        "Cloud & DevOps": [
            {"name": "Docker / K8s", "level": "Expert"},
            {"name": "GCP / AWS", "level": "Advanced"},
            {"name": "CI/CD Pipelines", "level": "Expert"},
            {"name": "PostgreSQL / Redis", "level": "Expert"}
        ],
        "Security & Research": [
            {"name": "Pentesting / OSCP", "level": "Expert"},
            {"name": "Malware Analysis", "level": "Advanced"},
            {"name": "SIEM / Splunk", "level": "Advanced"},
            {"name": "Network Security", "level": "Expert"}
        ]
    }

    generate_svg(tech_categories)
    print("Premium Technical Arsenal SVG generated.")

def generate_svg(categories):
    width = 850
    height = 380
    
    # Premium Dark Theme
    bg_gradient_start = "#0f172a"
    bg_gradient_end = "#020617"
    card_bg = "rgba(30, 41, 59, 0.5)"
    border_color = "rgba(148, 163, 184, 0.2)"
    text_main = "#f8fafc"
    text_dim = "#94a3b8"
    accent_color = "#38bdf8" # Sky Blue
    accent_success = "#4ade80" # Green
    
    svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="bg_grad" x1="0" y1="0" x2="{width}" y2="{height}" gradientUnits="userSpaceOnUse">
            <stop stop-color="{bg_gradient_start}"/>
            <stop offset="1" stop-color="{bg_gradient_end}"/>
        </linearGradient>
        <filter id="blur" x="0" y="0">
            <feGaussianBlur in="SourceGraphic" stdDeviation="5" />
        </filter>
    </defs>
    
    <!-- Background -->
    <rect width="{width}" height="{height}" rx="16" fill="url(#bg_grad)" />
    <rect width="{width}" height="{height}" rx="16" stroke="{border_color}" stroke-width="1"/>
    
    <!-- Header -->
    <text x="40" y="50" font-family="Inter, system-ui, sans-serif" font-weight="700" font-size="22" fill="{text_main}">Technical Core &amp; Specializations</text>
    <rect x="40" y="65" width="60" height="4" rx="2" fill="{accent_color}" />
    
    <g transform="translate({width - 200}, 45)">
        <circle cx="0" cy="-5" r="4" fill="{accent_success}">
            <animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite" />
        </circle>
        <text x="12" y="0" font-family="Inter, sans-serif" font-weight="600" font-size="12" fill="{accent_success}">Production Ready</text>
    </g>
    '''
    
    x_start = 40
    y_start = 100
    card_w = 185
    card_h = 240
    gap = 15
    
    for i, (cat_name, techs) in enumerate(categories.items()):
        curr_x = x_start + (i * (card_w + gap))
        
        # Category Group
        svg += f'<g transform="translate({curr_x}, {y_start})">'
        
        # Card Background (Simulated Glassmorphism)
        svg += f'<rect width="{card_w}" height="{card_h}" rx="12" fill="{card_bg}" stroke="{border_color}" stroke-width="1"/>'
        
        # Category Title
        svg += f'<text x="15" y="30" font-family="Inter, sans-serif" font-weight="700" font-size="11" fill="{accent_color}" text-transform="uppercase" letter-spacing="1">{cat_name}</text>'
        
        for j, tech in enumerate(techs):
            item_y = 70 + (j * 42)
            
            # Tech Name
            svg += f'<text x="15" y="{item_y}" font-family="Inter, sans-serif" font-weight="600" font-size="14" fill="{text_main}">{tech["name"]}</text>'
            
            # Level Indicator
            level_color = accent_success if tech["level"] == "Expert" else text_dim
            svg += f'<text x="15" y="{item_y + 18}" font-family="Inter, sans-serif" font-weight="400" font-size="11" fill="{level_color}">{tech["level"]}</text>'
            
            # Simple progress line
            line_w = card_w - 30
            level_pct = 1.0 if tech["level"] == "Expert" else 0.8 if tech["level"] == "Advanced" else 0.6
            svg += f'<rect x="15" y="{item_y + 25}" width="{line_w}" height="2" rx="1" fill="{border_color}"/>'
            svg += f'<rect x="15" y="{item_y + 25}" width="{line_w * level_pct}" height="2" rx="1" fill="{accent_color}"/>'
        
        svg += '</g>'
            
    svg += f'''
    <text x="{width - 40}" y="{height - 25}" font-family="Inter, sans-serif" font-weight="500" font-size="11" fill="{text_dim}" text-anchor="end">Architecting Scalable Solutions @ 2024</text>
    </svg>'''
    
    with open("tech-dashboard.svg", "w", encoding="utf-8") as f:
        f.write(svg)

if __name__ == "__main__":
    main()

