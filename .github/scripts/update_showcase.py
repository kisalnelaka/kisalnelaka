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

    markdown = ""
    for project in projects:
        markdown += f"#### [{project['title']}]({project['url']}) | *{project['subtitle']}*\n"
        markdown += f"*   **Challenge:** {project['challenge']}\n"
        markdown += f"*   **Solution:** {project['solution']}\n"
        markdown += f"*   **Impact:** {project['impact']}\n\n"

    readme_path = "README.md"
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<!-- SHOWCASE:START -->"
    end_marker = "<!-- SHOWCASE:END -->"
    
    pattern = re.compile(f"({start_marker}).*?({end_marker})", re.DOTALL)
    new_content = pattern.sub(rf"\1\n{markdown}\2", content)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("README.md updated with featured showcase.")

if __name__ == "__main__":
    update_readme()
