"""Chargement de la configuration optionnelle (config.json).

config.json est personnel et ne doit JAMAIS être commité (voir .gitignore).
Copier config.example.json vers config.json et remplir les sections voulues.
Chaque scanner désactivé reste simplement inactif : tout est optionnel.
"""

import json
from pathlib import Path

_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.json"


def charger():
    """Retourne le dict de config, ou {} si absent/illisible."""
    if not _CONFIG_PATH.exists():
        return {}
    try:
        return json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}
