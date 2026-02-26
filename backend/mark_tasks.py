import re
from pathlib import Path

tasks_file = Path("/Users/nicolaibrahim/Desktop/proj/Bot-Chating/specs/002-flatten-app-layer/tasks.md")
content = tasks_file.read_text()

# Replace all incomplete tasks with completed tasks
content = re.sub(r"- \[ \]", r"- [X]", content)

tasks_file.write_text(content)
print("Marked all tasks as [X]")
