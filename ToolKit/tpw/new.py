from Core.Worker import tool_def
from Core import inface
from Core import fileWork as fw


TOOLKIT_DIR = "ToolKit"


def _tool_file_content(kit_name: str, tool_name: str) -> str:
    return (
        f"from Core.Worker import tool_def\n"
        f"\n"
        f"\n"
        f"@tool_def(\"{kit_name}\", \"{tool_name}\")\n"
        f"class {tool_name.capitalize()}:\n"
        f"    @staticmethod\n"
        f"    def run(opt: str):\n"
        f"        pass\n"
        f"\n"
        f"    @staticmethod\n"
        f"    def man():\n"
        f"        print(\"{kit_name}.{tool_name} : (no documentation yet)\\n\")\n"
    )


def _kit_knot_line(kit_name: str) -> str:
    return f"from ToolKit.{kit_name}.knot import *\n"


def _tool_knot_line(kit_name: str, tool_name: str) -> str:
    return f"from ToolKit.{kit_name}.{tool_name} import {tool_name.capitalize()}\n"


@tool_def("tpw", "new")
class New:
    @staticmethod
    def run(opt: str):
        group_only = "g" in opt

        existing_kits = fw.list_dirs(TOOLKIT_DIR)

        # --- Saisie du kit ---
        print("\nKits existants :")
        for i, k in enumerate(existing_kits):
            print(f"  [{i}] {k}")
        kit_name = inface.input("\nNom du kit (existant ou nouveau) :\n>> ").strip().lower()
        if kit_name.isdigit():
            idx = int(kit_name)
            if 0 <= idx < len(existing_kits):
                kit_name = existing_kits[idx]
            else:
                print("Numéro invalide.")
                return

        kit_dir  = fw.join(TOOLKIT_DIR, kit_name)
        kit_knot = fw.join(kit_dir, "knot.py")
        tk_knot  = fw.join(TOOLKIT_DIR, "knot.py")

        # --- Création du kit si nécessaire ---
        kit_is_new = not fw.exists(kit_dir)
        if kit_is_new:
            fw.make_dir(kit_dir)
            print(f"  [+] Dossier kit créé : {kit_dir}")
            fw.write(kit_knot, "")
            print(f"  [+] Fichier créé : {kit_knot}")
            fw.append_line(tk_knot, _kit_knot_line(kit_name))
            print(f"  [~] Lien ajouté dans : {tk_knot}")
        elif group_only:
            print(f"  [!] Le kit '{kit_name}' existe déjà.")
            return

        if group_only:
            print(f"\n  Kit '{kit_name}' créé avec succès.")
            return

        # --- Saisie du tool ---
        tool_name = inface.input("Nom du tool :\n>> ").strip().lower()
        if not tool_name:
            print("Nom de tool invalide.")
            return

        tool_file = fw.join(kit_dir, f"{tool_name}.py")

        # --- Création du fichier tool ---
        if fw.exists(tool_file):
            print(f"  [!] Le tool '{tool_name}' existe déjà dans le kit '{kit_name}'.")
            return
        fw.write(tool_file, _tool_file_content(kit_name, tool_name))
        print(f"  [+] Fichier créé : {tool_file}")

        # --- Mise à jour du knot.py du kit ---
        fw.append_line(kit_knot, _tool_knot_line(kit_name, tool_name))
        print(f"  [~] Lien ajouté dans : {kit_knot}")

        print(f"\n  Tool '{kit_name}.{tool_name}' créé avec succès.")

    @staticmethod
    def man():
        print(
            "\n  tpw.new — Crée un nouveau tool ou un nouveau kit.\n"
            "\n"
            "  Usage : tpf tpw new [-g]\n"
            "\n"
            "  (aucune option)\n"
            "    - Demande le nom du kit (existant ou nouveau).\n"
            "    - Demande le nom du tool.\n"
            "    - Crée le fichier <tool>.py avec la structure de base.\n"
            "    - Crée le kit (dossier + knot.py) si nécessaire.\n"
            "    - Met à jour les knot.py du kit et de ToolKit.\n"
            "\n"
            "  -g  (group only)\n"
            "    - Crée uniquement un kit vide (dossier + knot.py).\n"
            "    - Met à jour ToolKit/knot.py.\n"
            "    - Ne demande pas de nom de tool.\n"
        )