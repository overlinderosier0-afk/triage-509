"""Scanner Telegram — OPTIONNEL (via API officielle).

Activation : remplir la section "telegram" de config.json avec api_id / api_hash
(obtenus sur https://my.telegram.org). Utilisez un compte Telegram DÉDIÉ à
l'outil, jamais un compte personnel.

Première utilisation : connexion interactive dans le terminal (numéro + code
reçu sur Telegram). La session est ensuite réutilisée sans redemander le code.

Limites : vérifie seulement si le numéro est inscrit sur Telegram (+ pseudo
public éventuel). Débit limité par Telegram : usage modéré uniquement.
"""

NOM = "Telegram"
DESCRIPTION = "vérification de l'inscription du numéro sur Telegram (via API officielle)"


def scanner(info_numero):
    from triage509 import config as cfg

    conf = cfg.charger().get("telegram", {})
    api_id, api_hash = conf.get("api_id"), conf.get("api_hash")
    if not api_id or not api_hash:
        return {
            "statut": "non_configuré",
            "resume": "Optionnel — ajouter api_id/api_hash dans config.json (voir config.example.json).",
        }
    try:
        import telethon  # noqa: F401
    except ImportError:
        return {"statut": "erreur", "resume": "telethon non installé : pip install telethon"}

    import asyncio

    try:
        return asyncio.run(_verifier(info_numero["e164"], api_id, api_hash,
                                     conf.get("session", "triage509")))
    except Exception as exc:
        return {"statut": "erreur", "resume": f"Échec Telegram : {exc}"}


async def _verifier(e164, api_id, api_hash, session):
    import random
    from telethon import TelegramClient
    from telethon.tl.functions.contacts import DeleteContactsRequest, ImportContactsRequest
    from telethon.tl.types import InputPhoneContact

    async with TelegramClient(session, api_id, api_hash) as client:
        contact = InputPhoneContact(
            client_id=random.randrange(1_000_000_000),
            phone=e164, first_name="Triage", last_name="509",
        )
        resultat = await client(ImportContactsRequest([contact]))
        if resultat.users:
            utilisateur = resultat.users[0]
            # Nettoyage : on supprime le contact importé pour le test.
            await client(DeleteContactsRequest(id=[utilisateur.id]))
            pseudo = f" (@{utilisateur.username})" if utilisateur.username else ""
            return {"statut": "trouvé",
                    "resume": f"Compte Telegram inscrit{pseudo}."}
        return {"statut": "absent",
                "resume": "Aucun compte Telegram lié à ce numéro."}
