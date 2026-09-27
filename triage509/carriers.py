"""Détection de l'opérateur haïtien d'après le plan de numérotation CONATEL.

Méthode : plus long préfixe correspondant dans data/prefixes_ht.json.
Résultat indicatif — la portabilité des numéros peut fausser l'opérateur réel.
"""

import json
from pathlib import Path

_PREFIXES_PATH = Path(__file__).resolve().parent.parent / "data" / "prefixes_ht.json"


def _charger():
    with open(_PREFIXES_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def detecter(numero_national):
    """Retourne {'operateur', 'service', 'prefixe'} ou None si aucun bloc ne correspond."""
    donnees = _charger()
    meilleur = None
    for bloc in donnees["blocs"]:
        if numero_national.startswith(bloc["prefixe"]):
            if meilleur is None or len(bloc["prefixe"]) > len(meilleur["prefixe"]):
                meilleur = bloc
    if meilleur is None:
        return None
    return {
        "operateur": meilleur["operateur"],
        "service": meilleur["service"],
        "prefixe": meilleur["prefixe"],
        "source": donnees["source"],
        "reserve": "Opérateur probable — la portabilité des numéros peut fausser ce résultat.",
    }
