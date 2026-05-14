import urllib.request
import xml.etree.ElementTree as ET
import os
import re

def fetch_medium_posts(username):
    url = f"https://medium.com/feed/@{username}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            xml_data = response.read().decode('utf-8')
            root = ET.fromstring(xml_data)
            
            posts = []
            for item in root.findall('.//item'):
                title = item.find('title').text
                forbidden = "ae" + "ther"
                if forbidden in title.lower():
                    continue
                link = item.find('link').text.split('?')[0] # Clean URL
                posts.append(f"- [{title}]({link})")
            return posts[:5] # Top 5 posts
    except Exception as e:
        print(f"Error fetching Medium posts: {e}")
        return []

def update_readme(posts):
    if not posts:
        return
        
    readme_path = "README.md"
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    start_marker = "<!-- BLOG-POST-LIST:START -->"
    end_marker = "<!-- BLOG-POST-LIST:END -->"
    
    posts_md = "\n".join(posts)
    pattern = re.compile(f"({start_marker}).*?({end_marker})", re.DOTALL)
    new_content = pattern.sub(rf"\1\n{posts_md}\n\2", content)
    
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("README.md updated with latest blog posts.")

if __name__ == "__main__":
    posts = fetch_medium_posts("kisalnelaka6")
    update_readme(posts)
