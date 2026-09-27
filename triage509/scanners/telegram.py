"""Scanner Telegram — À CONFIGURER.

Méthode propre possible : l'import de contacts via l'API Telegram officielle
(api_id / api_hash sur https://my.telegram.org) permet de vérifier si un
numéro est inscrit sur Telegram. Points d'attention :
- Nécessite un compte Telegram dédié à l'outil (jamais un compte personnel).
- Fortement limité en débit (rate limits) ; un usage massif fait bannir le compte.
- Ne révèle que : compte existant ou non (+ éventuellement photo/nom publics).

Tant que les identifiants API ne sont pas configurés, le scanner reste désactivé.
"""

NOM = "Telegram"
DESCRIPTION = "vérification de l'inscription du numéro sur Telegram (via API officielle)"
STATUT = "a_configurer"


def scanner(info_numero):
    return {
        "statut": "a_configurer",
        "resume": "Nécessite api_id/api_hash Telegram (https://my.telegram.org). Non configuré.",
    }
