import sys

stdin = input

def input(prompt: str = "") -> str:
    value = stdin(prompt)
    if value.strip().lower() in {"exit", "q"}:
        print("Fermeture de TPF.")
        sys.exit(0)
    return value


def choice(label: str, choices: list[str], back:bool = False, sentence:str = "\n --- \nChoose between (q to exit):") -> str | None:
    """Demande à l'utilisateur de choisir parmi une liste.
    Accepte le nom ou le numéro correspondant.
    Si la réponse est vide, affiche la liste et redemande."""
    short_label = (label if len(label)<2 else label[:2]).title()
    short_label = f"[{short_label}]> " if short_label!="" else ">> "

    while True:
        print(sentence)
        for i, c in enumerate(choices):
            print(f"    [{i}] {c}")


        value = input(short_label).strip()

        if back & (value.lower() in {"b","back"}):
            return None

        if value.isdigit():
            idx = int(value)
            if 0 <= idx < len(choices):
                return choices[idx]
            else:
                print(f"  Numéro invalide, choisir entre 0 et {len(choices) - 1}.")
                continue
        if value in choices:
            return value
        print(f"  '{value}' introuvable. Valeurs possibles :")
        for i, c in enumerate(choices):
            print(f"    [{i}] {c}")