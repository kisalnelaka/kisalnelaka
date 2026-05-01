import urllib.request
import json
import os
import re

def main():
    # Tech stack requirements (Explicitly defined based on your expertise and job needs)
    tech_categories = {
        "Frontend Ecosystem": [
            {"name": "React", "level": "Expert"},
            {"name": "Flutter", "level": "Expert"},
            {"name": "Redux", "level": "Expert"},
            {"name": "TypeScript", "level": "Expert"}
        ],
        "Backend Architecture": [
            {"name": "Node.js", "level": "Expert"},
            {"name": "Laravel", "level": "Expert"},
            {"name": "Python", "level": "Advanced"},
            {"name": "gRPC", "level": "Advanced"}
        ],
        "Cloud & Data": [
            {"name": "GCP", "level": "Expert"},
            {"name": "PostgreSQL", "level": "Expert"},
            {"name": "MongoDB", "level": "Advanced"},
            {"name": "Firestore", "level": "Expert"}
        ],
        "Engineering Ops": [
            {"name": "Docker", "level": "Expert"},
            {"name": "CI/CD", "level": "Expert"},
            {"name": "REST APIs", "level": "Expert"},
            {"name": "Git", "level": "Expert"}
        ]
    }

    generate_svg(tech_categories)
    print("Technical Arsenal SVG generated.")

def generate_svg(categories):
    width = 820
    height = 360
    
    # Premium Dark Theme
    bg_color = "#08090a"
    border_color = "#1f2124"
    text_main = "#f0f6fc"
    text_dim = "#8b949e"
    accent = "#58a6ff"
    
    svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="card_grad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#161b22;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#0d1117;stop-opacity:1" />
        </linearGradient>
    </defs>
    <style>
        .title {{ font: 700 18px 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; fill: {text_main}; }}
        .cat-label {{ font: 600 13px 'Inter', sans-serif; fill: {accent}; text-transform: uppercase; letter-spacing: 1px; }}
        .tech-name {{ font: 500 14px 'Inter', sans-serif; fill: {text_main}; }}
        .tech-level {{ font: 400 11px 'Inter', sans-serif; fill: {text_dim}; }}
        .indicator {{ fill: {accent}; filter: drop-shadow(0 0 3px {accent}); }}
    </style>
    
    <rect width="{width}" height="{height}" rx="16" fill="{bg_color}" stroke="{border_color}" stroke-width="1"/>
    
    <text x="30" y="45" class="title">Technical Arsenal &amp; Ecosystem</text>
    <circle cx="280" cy="40" r="4" fill="#3fb950" />
    <text x="290" y="44" font-family="Inter" font-size="11" fill="#3fb950">Active in Production</text>
    '''
    
    x_start = 30
    y_start = 85
    card_w = 180
    card_h = 240
    gap = 15
    
    for i, (cat_name, techs) in enumerate(categories.items()):
        curr_x = x_start + (i * (card_w + gap))
        
        # Category Section
        svg += f'<rect x="{curr_x}" y="{y_start}" width="{card_w}" height="{card_h}" rx="12" fill="url(#card_grad)" stroke="{border_color}"/>'
        svg += f'<text x="{curr_x + 15}" y="{y_start + 30}" class="cat-label">{cat_name.split()[0]}</text>'
        
        for j, tech in enumerate(techs):
            item_y = y_start + 65 + (j * 42)
            
            # Tech Item
            svg += f'<circle cx="{curr_x + 20}" cy="{item_y - 4}" r="3" class="indicator"/>'
            svg += f'<text x="{curr_x + 35}" y="{item_y}" class="tech-name">{tech["name"]}</text>'
            svg += f'<text x="{curr_x + 35}" y="{item_y + 16}" class="tech-level">{tech["level"]}</text>'
            
    svg += f'''
    <text x="{width - 30}" y="{height - 20}" font-family="Inter" font-size="10" fill="{text_dim}" text-anchor="end">Engineered for Scalability &amp; Performance</text>
    </svg>'''
    
    with open("tech-dashboard.svg", "w", encoding="utf-8") as f:
        f.write(svg)

if __name__ == "__main__":
    main()
