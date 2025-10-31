from pathlib import Path
from app.utils import auth

print("USERS_FILE =", auth.USERS_FILE)
ok = auth.create_user("admin","1234","admin")
print("create_user ->", ok)

p = Path(auth.USERS_FILE)
print("exists ->", p.exists())
if p.exists():
    print("content ->")
    print(p.read_text(encoding="utf-8"))