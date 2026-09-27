"""Registre des scanners complémentaires (tous optionnels).

Chaque module expose NOM, DESCRIPTION et scanner(info_numero) -> dict.
Le module décide lui-même s'il est configuré : s'il ne l'est pas, il
retourne un statut 'non_configuré' avec la marche à suivre. Rien n'est
obligatoire — un scanner non configuré n'empêche jamais l'analyse.
"""

from . import hlr, telegram, whatsapp

SCANNERS = {
    "whatsapp": whatsapp,
    "telegram": telegram,
    "hlr": hlr,
}


def executer(info_numero):
    """Exécute chaque scanner et retourne {nom: resultat}."""
    resultats = {}
    for nom, module in SCANNERS.items():
        try:
            resultats[nom] = module.scanner(info_numero)
        except Exception as exc:  # un scanner ne doit jamais faire planter l'analyse
            resultats[nom] = {"statut": "erreur", "resume": f"Échec du scanner : {exc}"}
    return resultats
