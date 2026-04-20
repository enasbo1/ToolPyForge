import os
import subprocess

from Core.Worker import tool_def
from Core import inface
from Core import fileWork as fw


TOOLKIT_DIR = "ToolKit"


def _get_tpf_dir() -> str:
    """Retourne le dossier racine de TPF via __file__ (fiable peu importe le CWD)."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _get_cmd_path(tpf_dir: str) -> str:
    return fw.join(tpf_dir, "tpf.cmd")


def _write_cmd(tpf_dir: str) -> None:
    cmd_path = _get_cmd_path(tpf_dir)
    content = f"@echo off\npython \"{fw.join(tpf_dir, 'tpf.py')}\" %*\n"
    fw.write(cmd_path, content)
    print(f"  [+] tpf.cmd écrit : {cmd_path}")


def _path_add(tpf_dir: str, scope: str) -> None:
    """Ajoute tpf_dir au PATH via PowerShell [Environment]::SetEnvironmentVariable."""
    ps_scope = "Machine" if scope == "system" else "User"

    # Récupère le PATH actuel du bon scope via PowerShell
    get_cmd = (
        f'[Environment]::GetEnvironmentVariable("PATH", "{ps_scope}")'
    )
    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", get_cmd],
        capture_output=True, text=True
    )
    current = result.stdout.strip()
    entries = [e for e in current.split(";") if e.strip()]

    if tpf_dir in entries:
        print(f"  [~] '{tpf_dir}' déjà présent dans le PATH {scope}.")
        return

    # Nettoie les anciennes entrées TPF (dossier contenant tpf.py)
    cleaned = [e for e in entries if not fw.exists(fw.join(e, "tpf.py"))]
    cleaned.append(tpf_dir)
    new_path = ";".join(cleaned)

    set_cmd = (
        f'[Environment]::SetEnvironmentVariable("PATH", "{new_path}", "{ps_scope}")'
    )
    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", set_cmd],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"  [+] '{tpf_dir}' ajouté au PATH {scope}.")
        print(f"  [!] Redémarre ton terminal pour que le PATH soit pris en compte.")
    else:
        print(f"  [!] Échec de la mise à jour du PATH :")
        print(f"      {result.stderr.strip()}")
        if scope == "system":
            print(f"      Le PATH système nécessite des droits administrateur.")
            print(f"      Relance TPF en tant qu'administrateur ou choisis 'user'.")


def _detect_scope(tpf_dir: str) -> str:
    """Détecte si tpf_dir est dans le PATH user ou système via PowerShell."""
    for scope, ps_scope in [("user", "User"), ("system", "Machine")]:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             f'[Environment]::GetEnvironmentVariable("PATH", "{ps_scope}")'],
            capture_output=True, text=True
        )
        if tpf_dir in result.stdout.split(";"):
            return scope
    return "user"  # fallback


@tool_def("tpw", "init")
class Init:
    @staticmethod
    def run(opt: str):
        tpf_dir = _get_tpf_dir()
        cmd_path = _get_cmd_path(tpf_dir)
        already_installed = fw.exists(cmd_path)

        print(f"\n  Dossier TPF détecté : {tpf_dir}")

        if already_installed:
            print("  [~] Installation existante détectée — mise à jour des liens.\n")
        else:
            print("  [~] Première installation.\n")

        # --- Écriture du .cmd ---
        _write_cmd(tpf_dir)

        # --- Choix du scope PATH ---
        force_ask = "f" in opt
        if not already_installed or force_ask:
            scope = inface.choice(
                "Sc",
                ["user", "system"],
                sentence="Ajouter TPF au PATH :"
            )
        else:
            scope = _detect_scope(tpf_dir)
            print(f"  [~] Scope détecté : {scope}. Utilise -f pour changer.")

        _path_add(tpf_dir, scope)

        print(f"\n  {'Installation' if not already_installed else 'Mise à jour'} terminée.")
        print(f"  Lance 'tpf' depuis n'importe quel terminal pour démarrer.")

    @staticmethod
    def man():
        print(
            "\n  tpw.init — Initialise ou met à jour l'installation de TPF.\n"
            "\n"
            "  Usage : tpf tpw init [-f]\n"
            "\n"
            "  (aucune option)\n"
            "    - Crée tpf.cmd dans le dossier racine de TPF.\n"
            "    - Ajoute le dossier au PATH (user ou système).\n"
            "    - Demande le scope uniquement à la première installation.\n"
            "    - Au relancement, met à jour les liens sans redemander.\n"
            "\n"
            "  -f  (force)\n"
            "    - Force la question du scope même si déjà installé.\n"
            "    - Utile pour basculer de user à system ou inversement.\n"
        )