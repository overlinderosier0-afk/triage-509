#!/usr/bin/env python3
"""Triage-509 — analyse d'un numéro haïtien depuis le terminal.

Exemple :
    python cli.py +50934123456
    python cli.py 34123456 --utilisateur "Agent D." --dossier "2026-118"
"""

import argparse
import json
import sys

from triage509 import core, carriers, audit, report
from triage509.scanners import executer as executer_scanners


def analyser_numero(saisie):
    base = core.analyser(saisie)
    if not base["ok"]:
        return {"ok": False, "erreur": base["erreur"]}
    analyse = {"ok": True, "base": base}
    if base["pays_appelant"] == "+509":
        analyse["operateur"] = carriers.detecter(base["numero_national"])
    else:
        analyse["operateur"] = None
    analyse["scanners"] = executer_scanners(base)
    return analyse


def main():
    ap = argparse.ArgumentParser(description="Triage-509 : triage rapide des numéros +509")
    ap.add_argument("numero", help="Numéro à analyser (ex. +50934123456)")
    ap.add_argument("--utilisateur", default="", help="Nom/pseudonyme de l'utilisateur (audit)")
    ap.add_argument("--dossier", default="", help="Référence du dossier (audit)")
    ap.add_argument("--json", action="store_true", help="Sortie JSON au lieu du rapport texte")
    args = ap.parse_args()

    analyse = analyser_numero(args.numero)
    if not analyse["ok"]:
        print(f"Erreur : {analyse['erreur']}", file=sys.stderr)
        sys.exit(1)

    base = analyse["base"]
    audit.enregistrer(
        numero_e164=base["e164"],
        operateur=(analyse["operateur"] or {}).get("operateur", "Inconnu"),
        type_ligne=base["type_ligne"],
        valide=base["valide"],
        utilisateur=args.utilisateur,
        dossier=args.dossier,
    )

    if args.json:
        print(json.dumps(analyse, ensure_ascii=False, indent=2))
    else:
        texte, chemin = report.generer(analyse, args.utilisateur, args.dossier)
        print(texte)
        print(f"\nRapport enregistré : {chemin}")


if __name__ == "__main__":
    main()
