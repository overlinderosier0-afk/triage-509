"""Scanner WhatsApp — À CONFIGURER.

Ce qu'il faut savoir honnêtement :
- Il n'existe PAS d'API publique WhatsApp pour vérifier si un numéro
  possède un compte. Les méthodes existantes (vérification via l'écran
  d'inscription, bibliothèques non officielles) violent les conditions
  d'utilisation et font bannir les comptes utilisés.
- La méthode manuelle légitime : ouvrir https://wa.me/<numéro> dans un
  navigateur et voir si une conversation peut être initiée.

Piste d'implémentation propre : utiliser l'API WhatsApp Business officielle
(compte vérifié requis) — coûteuse et réservée aux entreprises.

Tant que ce scanner n'est pas configuré proprement, il reste désactivé :
mieux vaut un outil honnête qu'un outil qui triche et se fait bannir.
"""

NOM = "WhatsApp"
DESCRIPTION = "vérification de l'existence d'un compte WhatsApp lié au numéro"
STATUT = "a_configurer"


def scanner(info_numero):
    return {
        "statut": "a_configurer",
        "resume": "Vérification manuelle : ouvrir https://wa.me/{} dans un navigateur.".format(
            info_numero["e164"].replace("+", "")
        ),
    }
