import sys
from pathlib import Path

# Agrega la raíz del proyecto al PATH para poder importar app.utils
ROOT = Path(__file__).resolve().parents[1]   # sube un nivel (Avatars_VS_Rooks)
sys.path.append(str(ROOT))

from app.utils import auth  # noqa: E402

def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print("Uso: python tools/add_user.py <usuario> <password> [rol]")
        return

    user = args[0]
    pwd = args[1]
    role = args[2] if len(args) > 2 else "user"

    ok = auth.create_user(user, pwd, role)
    print("✅ Usuario creado correctamente." if ok else "⚠️ El usuario ya existe.")

if __name__ == "__main__":
    main()
