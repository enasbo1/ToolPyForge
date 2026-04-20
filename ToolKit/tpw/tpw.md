# ToolPyWorkshop — TPW

Kit interne de TPF. Regroupe les tools de gestion du framework lui-même.

---

## Tools

### `new` — Créer un tool ou un kit

```
tpf tpw new
tpf tpw new -g
```

| Option | Effet |
|--------|-------|
| *(aucune)* | Crée un kit (si nécessaire) et un tool |
| `-g` | Crée uniquement un kit vide |

#### Comportement

- Affiche la liste des kits existants (nom ou numéro acceptés)
- Si le kit n'existe pas, le crée avec son `knot.py` et met à jour `ToolKit/knot.py`
- Crée `ToolKit/<kit>/<tool>.py` avec la structure `@tool_def` + `run()` + `man()`
- Met à jour `ToolKit/<kit>/knot.py` avec l'import du tool
- Ne crée jamais de doublon

#### Fichier généré

```python
from Core.Worker import tool_def

@tool_def("<kit>", "<tool>")
class <Tool>:
    @staticmethod
    def run(opt: str):
        pass

    @staticmethod
    def man():
        print("<kit>.<tool> : (no documentation yet)")
```

---

### `init` — Initialiser ou mettre à jour l'installation

```
tpf tpw init
tpf tpw init -f
```

| Option | Effet |
|--------|-------|
| *(aucune)* | Install ou mise à jour silencieuse |
| `-f` | Force la question du scope user/système |

#### Comportement

- Détecte le dossier racine de TPF via `__file__` (fiable peu importe le CWD)
- Écrit `tpf.cmd` avec le chemin absolu vers `tpf.py`
- Modifie le PATH Windows via PowerShell `[Environment]::SetEnvironmentVariable`
- Nettoie les anciennes entrées TPF si le projet a été déplacé

**Première installation :** demande le scope `user` ou `system`.

**Relancement :** détecte le scope existant et met à jour silencieusement.
Utiliser `-f` pour changer de scope.

> Le PATH système nécessite des droits administrateur.
> En cas d'échec, relancer TPF en tant qu'administrateur ou choisir `user`.

> Un redémarrage du terminal est nécessaire pour que le nouveau PATH soit pris en compte.

---

## Fichiers

```
ToolKit/tpw/
├── knot.py   # Agrégateur : importe New et Init
├── new.py    # Tool tpw.new
├── init.py   # Tool tpw.init
└── tpw.md    # Ce fichier
```