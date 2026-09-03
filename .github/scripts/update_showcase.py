import json
import os
import re

def update_readme():
    projects_path = os.path.join(".github", "scripts", "projects.json")
    if not os.path.exists(projects_path):
        print("projects.json not found.")
        return

    with open(projects_path, "r", encoding="utf-8") as f:
        projects = json.load(f)

    rows = [
        "| System | Architecture & Focus | Impact / Key Metrics | Stack |",
        "| :--- | :--- | :--- | :--- |"
    ]
    for p in projects:
        stack_badges = " · ".join([f"`{s.strip()}`" for s in p["stack"].split(",")])
        rows.append(f"| **[{p['title']}]({p['url']})** | {p['architecture']} | {p['impact']} | {stack_badges} |")

    table_markdown = "\n".join(rows) + "\n"

    readme_path = "README.md"
    if not os.path.exists(readme_path):
        print("README.md not found.")
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<!-- SHOWCASE:START -->"
    end_marker = "<!-- SHOWCASE:END -->"
    
    pattern = re.compile(f"({start_marker}).*?({end_marker})", re.DOTALL)
    if pattern.search(content):
        new_content = pattern.sub(rf"\1\n{table_markdown}\2", content)
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("README.md updated with flagship systems showcase.")
    else:
        print("Showcase markers not found in README.md.")

if __name__ == "__main__":
    update_readme()
