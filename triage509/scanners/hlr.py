"""Scanner HLR (Home Location Register) — À CONFIGURER.

Le HLR est LA donnée la plus utile pour un enquêteur :
- le numéro est-il actif en ce moment ?
- est-il en itinérance (roaming), et sur quel réseau ?

C'est un service PAYANT (ex. : Twilio Lookup, Veriphone, API HLR dédiées).
Aucune source gratuite et fiable n'existe. Prévoir un budget par requête
(quelques centimes d'euro/USD par numéro selon le fournisseur).

Tant qu'aucune clé API n'est configurée, le scanner reste désactivé.
"""

NOM = "HLR"
DESCRIPTION = "interrogation du registre HLR : ligne active, itinérance (service payant)"
STATUT = "a_configurer"


def scanner(info_numero):
    return {
        "statut": "a_configurer",
        "resume": "Service payant (Twilio Lookup, Veriphone…). Aucune clé API configurée.",
    }
