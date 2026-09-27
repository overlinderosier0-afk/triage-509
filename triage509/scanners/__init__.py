"""Registre des scanners complémentaires.

Chaque scanner est un module exposant :
  NOM, DESCRIPTION, STATUT ("actif" ou "a_configurer") et scanner(info_numero) -> dict.
"""

from . import whatsapp, telegram, hlr

SCANNERS = {
    "whatsapp": whatsapp,
    "telegram": telegram,
    "hlr": hlr,
}


def executer(info_numero):
    """Exécute les scanners actifs et retourne {nom: resultat}."""
    resultats = {}
    for nom, module in SCANNERS.items():
        if module.STATUT == "actif":
            try:
                resultats[nom] = module.scanner(info_numero)
            except Exception as exc:  # un scanner ne doit jamais faire planter l'analyse
                resultats[nom] = {"statut": "erreur", "resume": f"Échec du scanner : {exc}"}
        else:
            resultats[nom] = {
                "statut": module.STATUT,
                "resume": f"Non configuré — {module.DESCRIPTION}",
            }
    return resultats
