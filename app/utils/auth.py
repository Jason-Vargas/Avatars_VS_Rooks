# auth.py — Usuarios en JSON con contraseñas hasheadas (PBKDF2-HMAC-SHA256)
from __future__ import annotations
import json, secrets, hashlib, base64
from pathlib import Path
from typing import Dict, Any, List

ROOT = Path(__file__).resolve().parents[2]     # .../Avatars_VS_Rooks
DATA_PATH = ROOT / "data"
USERS_FILE = DATA_PATH / "users.json"

ALGO = "sha256"
ITERATIONS = 130_000
SALT_BYTES = 16

def _ensure_store() -> None:
    DATA_PATH.mkdir(parents=True, exist_ok=True)
    if not USERS_FILE.exists():
        USERS_FILE.write_text('{"users": []}\n', encoding="utf-8")

def _load() -> Dict[str, Any]:
    _ensure_store()
    raw = USERS_FILE.read_text(encoding="utf-8") or '{"users": []}'
    return json.loads(raw)

def _save(data: Dict[str, Any]) -> None:
    _ensure_store()
    tmp = USERS_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    tmp.replace(USERS_FILE)

def _b64e(b: bytes) -> str: return base64.b64encode(b).decode("ascii")
def _b64d(s: str) -> bytes: return base64.b64decode(s.encode("ascii"))

def _hash_password(password: str, salt_b: bytes, iterations: int) -> str:
    dk = hashlib.pbkdf2_hmac(ALGO, password.encode("utf-8"), salt_b, iterations)
    return _b64e(dk)

def create_user(username: str, password: str, role: str = "user") -> bool:
    if not username or not password: return False
    data = _load()
    if any(u.get("username") == username for u in data.get("users", [])): return False
    salt_b = secrets.token_bytes(SALT_BYTES)
    user = {
        "username": username,
        "salt": _b64e(salt_b),
        "hash": _hash_password(password, salt_b, ITERATIONS),
        "iterations": ITERATIONS,
        "role": role,
        "active": True,
    }
    data.setdefault("users", []).append(user); _save(data); return True

def verify_user(username: str, password: str) -> bool:
    if not username or not password: return False
    data = _load()
    user = next((u for u in data.get("users", []) if u.get("username")==username and u.get("active", True)), None)
    if not user: return False
    return _hash_password(password, _b64d(user["salt"]), int(user.get("iterations", ITERATIONS))) == user["hash"]

def set_active(username: str, active: bool) -> bool:
    data = _load()
    for u in data.get("users", []):
        if u.get("username")==username:
            u["active"] = bool(active); _save(data); return True
    return False

def list_users() -> List[Dict[str, Any]]:
    data = _load()
    return [{"username": u.get("username"),
             "role": u.get("role","user"),
             "active": bool(u.get("active", True)),
             "iterations": int(u.get("iterations", ITERATIONS))} for u in data.get("users", [])]
