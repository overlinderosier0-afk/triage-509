"""Scanner HLR / Lookup — OPTIONNEL (service payant).

Utilise Twilio Lookup v2 : type de ligne, nom de l'opérateur, validité.
Activation : remplir la section "twilio" de config.json (account_sid + auth_token,
console sur https://console.twilio.com). Coût : quelques centimes par requête.

C'est la donnée la plus proche d'un vrai HLR accessible sans partenariat opérateur.
"""

NOM = "HLR / Lookup"
DESCRIPTION = "Twilio Lookup v2 : type de ligne, opérateur, validité (service payant)"


def scanner(info_numero):
    from triage509 import config as cfg

    conf = cfg.charger().get("twilio", {})
    sid, token = conf.get("account_sid"), conf.get("auth_token")
    if not sid or not token:
        return {
            "statut": "non_configuré",
            "resume": "Optionnel — ajouter account_sid/auth_token Twilio dans config.json (service payant).",
        }
    try:
        return _lookup(info_numero["e164"], sid, token)
    except Exception as exc:
        return {"statut": "erreur", "resume": f"Échec Lookup : {exc}"}


def _lookup(e164, sid, token):
    import base64
    import json
    import urllib.request

    url = (f"https://lookups.twilio.com/v2/PhoneNumbers/{e164}"
           "?Fields=line_type_intelligence")
    identifiants = base64.b64encode(f"{sid}:{token}".encode()).decode()
    requete = urllib.request.Request(url, headers={
        "Authorization": f"Basic {identifiants}",
        "User-Agent": "triage-509",
    })
    try:
        with urllib.request.urlopen(requete, timeout=20) as reponse:
            donnees = json.loads(reponse.read().decode())
    except Exception as exc:
        if hasattr(exc, "code") and exc.code == 401:
            return {"statut": "erreur", "resume": "Clés Twilio rejetées (401) — vérifiez config.json."}
        raise

    lti = donnees.get("line_type_intelligence", {}) or {}
    morceaux = []
    if donnees.get("valid") is not None:
        morceaux.append("valide" if donnees["valid"] else "invalide")
    if lti.get("type"):
        morceaux.append(f"ligne {lti['type']}")
    if lti.get("carrier_name"):
        morceaux.append(f"opérateur {lti['carrier_name']}")
    resume = "Twilio Lookup : " + (", ".join(morceaux) if morceaux else "réponse vide")
    return {"statut": "ok", "resume": resume + "."}
