# ToolPyForge — TPF

Framework Python modulaire pour créer, organiser et exécuter des outils en ligne de commande.

---

## Structure

```
ToolPyForge/
├── tpf.py              # Point d'entrée principal
├── tpf.cmd             # Raccourci Windows (généré par tpw init)
├── Core/
│   ├── knot.py         # Agrégateur d'imports du Core
│   ├── Worker.py       # Moteur de dispatch (Worker, ToolClassRoot, tool_def)
│   ├── inface.py       # Interface utilisateur (input, choice)
│   └── fileWork.py     # Utilitaires fichiers/dossiers
└── ToolKit/
    ├── knot.py         # Agrégateur d'imports de tous les kits
    └── <kit>/
        ├── knot.py     # Agrégateur d'imports du kit
        └── <tool>.py   # Définition d'un tool
```

---

## Installation

Depuis le dossier du projet, au premier lancement :

```
python tpf.py tpw init
```

Puis depuis n'importe quel terminal :

```
tpf tpw init
```

---

## Utilisation

### Lancement interactif

```
tpf
```

TPF demande successivement le kit, le tool et les options.
À chaque étape on peut entrer le nom ou son numéro dans la liste affichée.

### Lancement direct

```
tpf <kit> <tool> -<options>
```

Exemples :

```
tpf tpw new
tpf tpw new -g
tpf tpw init -f
tpf tpw new -h
```

### Mots-clés réservés

| Entrée | Contexte | Effet |
|--------|----------|-------|
| `q` / `exit` | partout | Quitte TPF |
| `b` / `back` | choix du tool | Remonte au choix du kit |
| `back` | choix des options | Remonte au choix du tool |
| `-` | options | Appelle `run("")` sans prompt |
| `h` / `help` / `man` | options | Affiche la doc du tool (`man()`) |
| `-h` / `-help` / `-man` | argument direct | Affiche la doc du tool (`man()`) |

---

## Architecture

### `Worker`

Registre central de tous les tools, indexés par `kit → tool`.
Dispatch en trois étapes : `kit_pick → tool_pick → option_pick`.

### `ToolClassRoot`

Classe de base de tous les tools. Interface minimale :

```python
@tool_def("mon_kit", "mon_tool")
class MonTool:
    @staticmethod
    def run(opt: str) -> None: ...

    @staticmethod
    def man() -> None: ...
```

### `tool_def`

Décorateur qui enregistre un tool dans `Worker.tools` au moment de l'import.

### `knot.py`

Chaque niveau expose un `knot.py` qui agrège les imports de son niveau.
Le chaînage `tpf.py → Core/knot.py + ToolKit/knot.py → kit/knot.py`
garantit que tous les tools sont enregistrés au démarrage.

### `inface`

Surcouche à `input()` qui intercepte `q` / `exit`.
Expose `choice()` pour les menus numérotés avec option `back`.

### `fileWork`

Utilitaires fichiers centralisés. À importer via `from Core import fileWork as fw`.

---

## Créer un tool

La façon recommandée est d'utiliser `tpw new`.

Pour le faire manuellement :

1. Créer `ToolKit/<kit>/<tool>.py` :

```python
from Core.Worker import tool_def

@tool_def("<kit>", "<tool>")
class MonTool:
    @staticmethod
    def run(opt: str) -> None:
        pass

    @staticmethod
    def man() -> None:
        print("Documentation du tool.")
```

2. Ajouter dans `ToolKit/<kit>/knot.py` :

```python
from ToolKit.<kit>.<tool> import MonTool
```

3. Si le kit est nouveau, ajouter dans `ToolKit/knot.py` :

```python
from ToolKit.<kit>.knot import *
```