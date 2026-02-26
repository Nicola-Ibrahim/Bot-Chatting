import re
from pathlib import Path

files_to_update = [
    "src/modules/accounts/infrastructure/accounts_module.py",
    "src/modules/chats/infrastructure/chat_module.py",
    "src/api/routers/chats/v1/conversations/endpoints.py",
]

backend_dir = Path("/Users/nicolaibrahim/Desktop/proj/Bot-Chating/backend")

for f in files_to_update:
    path = backend_dir / f
    if path.exists():
        content = path.read_text()
        # Replace .command import -> _command import
        content = re.sub(r"\.command import", r"_command import", content)
        # Replace .query import -> _query import
        content = re.sub(r"\.query import", r"_query import", content)
        # Replace .dto import -> _dto import
        content = re.sub(r"\.dto import", r"_dto import", content)

        path.write_text(content)
        print(f"Updated {f}")
