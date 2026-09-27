"""Journal d'utilisation (audit) — indispensable pour un usage policier.

Chaque analyse est enregistrée avec horodatage, numéro, résultat et,
si fournis, l'utilisateur et la référence du dossier. Format JSON Lines.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

_AUDIT_PATH = Path(__file__).resolve().parent.parent / "data" / "audit.jsonl"


def enregistrer(numero_e164, operateur, type_ligne, valide, utilisateur="", dossier=""):
    entree = {
        "horodatage": datetime.now(timezone.utc).isoformat(),
        "numero": numero_e164,
        "operateur_detecte": operateur,
        "type_ligne": type_ligne,
        "valide": valide,
        "utilisateur": utilisateur,
        "dossier": dossier,
    }
    _AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(_AUDIT_PATH, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entree, ensure_ascii=False) + "\n")
    return entree
