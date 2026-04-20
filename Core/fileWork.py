import os


def read(filepath: str) -> str:
    """Lit un fichier texte et retourne son contenu."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def write(filepath: str, content: str) -> None:
    """Écrit un fichier texte (écrase le contenu existant)."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def append_line(filepath: str, line: str) -> None:
    """Ajoute une ligne au fichier si elle n'y est pas déjà."""
    if os.path.exists(filepath):
        if line.strip() in read(filepath):
            return
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(line)


def exists(filepath: str) -> bool:
    """Retourne True si le fichier existe."""
    return os.path.exists(filepath)


def make_dir(dirpath: str) -> None:
    """Crée un dossier et ses parents si nécessaire."""
    os.makedirs(dirpath, exist_ok=True)


def list_dirs(dirpath: str, exclude: set[str] = None) -> list[str]:
    """Liste les sous-dossiers d'un dossier, en excluant ceux listés dans exclude."""
    if exclude is None:
        exclude = {"__pycache__"}
    return [
        d for d in os.listdir(dirpath)
        if os.path.isdir(os.path.join(dirpath, d))
           and d not in exclude
    ]


def list_files(dirpath: str, ext: str = None, exclude: set[str] = None) -> list[str]:
    """Liste les fichiers d'un dossier, filtrables par extension et exclusions."""
    if exclude is None:
        exclude = set()
    return [
        f for f in os.listdir(dirpath)
        if os.path.isfile(os.path.join(dirpath, f))
           and f not in exclude
           and (ext is None or f.endswith(ext))
    ]


def join(*parts: str) -> str:
    """Raccourci pour os.path.join."""
    return os.path.join(*parts)