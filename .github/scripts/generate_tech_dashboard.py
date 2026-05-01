import urllib.request
import json
import os
import re

def main():
    # Tech stack requirements (Explicitly defined based on your expertise and job needs)
    tech_categories = {
        "Frontend": [
            {"name": "React", "level": "Expert"},
            {"name": "Flutter", "level": "Expert"},
            {"name": "Redux", "level": "Expert"},
            {"name": "TypeScript", "level": "Expert"}
        ],
        "Backend": [
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
        "Engineering": [
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
    
    # Tokyo Night / GitHub Dark Theme
    bg_color = "#0d1117"
    card_bg = "#161b22"
    border_color = "#30363d"
    text_main = "#c9d1d9"
    text_dim = "#8b949e"
    accent_green = "#3fb950"
    
    svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
    <style>
        .title {{ font: 700 20px 'Segoe UI', Ubuntu, Sans-Serif; fill: {text_main}; }}
        .cat-label {{ font: 600 13px 'Segoe UI', Sans-Serif; fill: {accent_green}; text-transform: uppercase; letter-spacing: 1.5px; }}
        .tech-name {{ font: 600 15px 'Segoe UI', Sans-Serif; fill: {text_main}; }}
        .tech-level {{ font: 400 12px 'Segoe UI', Sans-Serif; fill: {text_dim}; }}
        .indicator {{ fill: {accent_green}; }}
        .status-text {{ font: 600 12px 'Segoe UI', Sans-Serif; fill: {accent_green}; }}
    </style>
    
    <rect width="{width}" height="{height}" rx="12" fill="{bg_color}" stroke="{border_color}" stroke-width="1"/>
    
    <!-- Header -->
    <text x="30" y="45" class="title">Technical Arsenal &amp; Ecosystem</text>
    <circle cx="335" cy="39" r="4" fill="{accent_green}" />
    <text x="345" y="44" class="status-text">Active in Production</text>
    '''
    
    x_start = 30
    y_start = 85
    card_w = 180
    card_h = 240
    gap = 15
    
    for i, (cat_name, techs) in enumerate(categories.items()):
        curr_x = x_start + (i * (card_w + gap))
        
        # Category Card
        svg += f'<rect x="{curr_x}" y="{y_start}" width="{card_w}" height="{card_h}" rx="10" fill="{card_bg}" stroke="{border_color}"/>'
        svg += f'<text x="{curr_x + 20}" y="{y_start + 30}" class="cat-label">{cat_name.split()[0]}</text>'
        
        for j, tech in enumerate(techs):
            item_y = y_start + 70 + (j * 42)
            
            # Tech Item with clean alignment
            svg += f'<circle cx="{curr_x + 20}" cy="{item_y - 5}" r="3" class="indicator"/>'
            svg += f'<text x="{curr_x + 35}" y="{item_y}" class="tech-name">{tech["name"]}</text>'
            svg += f'<text x="{curr_x + 35}" y="{item_y + 18}" class="tech-level">{tech["level"]}</text>'
            
    svg += f'''
    <text x="{width - 30}" y="{height - 20}" font-family="Segoe UI, Sans-Serif" font-size="11" fill="{text_dim}" text-anchor="end">Verified Full-Stack Architecture</text>
    </svg>'''
    
    with open("tech-dashboard.svg", "w", encoding="utf-8") as f:
        f.write(svg)

if __name__ == "__main__":
    main()
