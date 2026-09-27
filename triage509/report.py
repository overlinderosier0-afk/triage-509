"""Génération du rapport d'analyse en français (texte et HTML)."""

from datetime import datetime
from pathlib import Path

_RAPPORTS_DIR = Path(__file__).resolve().parent.parent / "rapports"


def _lignes(analyse):
    info = analyse["base"]
    op = analyse.get("operateur")
    lignes = [
        "TRIAGE-509 — RAPPORT D'ANALYSE",
        f"Généré le : {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        "",
        f"Numéro saisi   : {info['saisie']}",
        f"Format E.164   : {info['e164']}",
        f"Format national: {info['national']}",
        f"Valide         : {'Oui' if info['valide'] else 'Non'}",
        f"Type de ligne  : {info['type_ligne']}",
    ]
    if op:
        lignes += [
            f"Opérateur      : {op['operateur']} (probable, préfixe {op['prefixe']})",
            f"Service        : {op['service']}",
            f"Réserve        : {op['reserve']}",
        ]
    else:
        lignes.append("Opérateur      : Inconnu (préfixe hors plan CONATEL 2017)")
    lignes += [
        "",
        "Scanners complémentaires :",
    ]
    for nom, res in analyse.get("scanners", {}).items():
        lignes.append(f"  - {nom} : {res.get('resume', res.get('statut', '?'))}")
    lignes += [
        "",
        "LIMITES : ce rapport n'identifie pas le propriétaire du numéro et",
        "ne fournit aucune localisation. Seule une réquisition judiciaire",
        "auprès de l'opérateur permet d'obtenir ces informations.",
    ]
    return "\n".join(lignes)


def generer(analyse, utilisateur="", dossier=""):
    texte = _lignes(analyse)
    _RAPPORTS_DIR.mkdir(parents=True, exist_ok=True)
    nom = f"rapport_{analyse['base']['e164'].replace('+', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    chemin = _RAPPORTS_DIR / nom
    chemin.write_text(texte, encoding="utf-8")
    return texte, str(chemin)
