import urllib.request
import xml.etree.ElementTree as ET
import re
import os

MEDIUM_USER = "kisalnelaka6"

def fetch_posts(limit=4):
    url = f"https://medium.com/feed/@{MEDIUM_USER}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            root = ET.fromstring(r.read().decode("utf-8"))
        posts = []
        for item in root.findall(".//item"):
            title = item.find("title").text or ""
            link  = (item.find("link").text or "").split("?")[0]
            if title and link:
                posts.append({"title": title, "link": link})
        return posts[:limit]
    except Exception as e:
        print(f"  [warn] Medium RSS -> {e}")
        return []

def update_readme(posts):
    if not posts:
        print("  No posts fetched, skipping README update.")
        return
    lines = "\n".join(f"- [{p['title']}]({p['link']})" for p in posts)
    readme = "README.md"
    with open(readme, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = re.compile(r"(<!-- BLOG-POST-LIST:START -->).*?(<!-- BLOG-POST-LIST:END -->)", re.DOTALL)
    new = pattern.sub(rf"\1\n{lines}\n\2", content)
    with open(readme, "w", encoding="utf-8") as f:
        f.write(new)
    print(f"  Updated README with {len(posts)} posts.")

if __name__ == "__main__":
    posts = fetch_posts()
    update_readme(posts)
