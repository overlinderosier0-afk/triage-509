"""Scanner WhatsApp — vérification MANUELLE (pas d'API publique).

Il n'existe pas d'API WhatsApp permettant de vérifier proprement si un numéro
possède un compte ; les méthodes automatisées violent les conditions
d'utilisation et font bannir les comptes. Ce scanner fournit donc le lien
de vérification manuelle : si https://wa.me/<numéro> ouvre une conversation,
le numéro est inscrit sur WhatsApp.
"""

NOM = "WhatsApp"
DESCRIPTION = "vérification manuelle de l'existence d'un compte WhatsApp"


def scanner(info_numero):
    numero = info_numero["e164"].replace("+", "")
    return {
        "statut": "manuel",
        "resume": (f"Ouvrir https://wa.me/{numero} : si une conversation peut "
                   "être initiée, le numéro a WhatsApp. (Pas d'automatisation "
                   "possible sans violer les CGU.)"),
    }
