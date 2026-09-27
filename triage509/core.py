"""Parsing et validation des numéros via libphonenumber (bibliothèque de Google)."""

import phonenumbers
from phonenumbers import PhoneNumberFormat, PhoneNumberType, number_type

TYPES_FR = {
    PhoneNumberType.MOBILE: "Mobile",
    PhoneNumberType.FIXED_LINE: "Fixe",
    PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixe ou mobile",
    PhoneNumberType.TOLL_FREE: "Numéro vert",
    PhoneNumberType.PREMIUM_RATE: "Numéro surtaxé",
    PhoneNumberType.SHARED_COST: "Coût partagé",
    PhoneNumberType.VOIP: "VoIP",
    PhoneNumberType.PERSONAL_NUMBER: "Numéro personnel",
    PhoneNumberType.PAGER: "Pager",
    PhoneNumberType.UAN: "UAN",
    PhoneNumberType.VOICEMAIL: "Messagerie vocale",
    PhoneNumberType.UNKNOWN: "Inconnu",
}


def analyser(saisie):
    """Analyse un numéro. Retourne un dict ; 'ok' vaut False si le numéro est illisible."""
    saisie = saisie.strip().replace(" ", "").replace("-", "").replace(".", "")
    resultat = {"saisie": saisie, "ok": False}
    try:
        # Région par défaut : HT — un numéro sans indicatif est supposé haïtien.
        numero = phonenumbers.parse(saisie, "HT")
    except phonenumbers.NumberParseException as exc:
        resultat["erreur"] = f"Numéro illisible ({exc})"
        return resultat

    resultat["ok"] = True
    resultat["e164"] = phonenumbers.format_number(numero, PhoneNumberFormat.E164)
    resultat["international"] = phonenumbers.format_number(numero, PhoneNumberFormat.INTERNATIONAL)
    resultat["national"] = phonenumbers.format_number(numero, PhoneNumberFormat.NATIONAL)
    resultat["pays_appelant"] = f"+{numero.country_code}"
    resultat["numero_national"] = str(numero.national_number)
    resultat["valide"] = phonenumbers.is_valid_number(numero)
    resultat["possible"] = phonenumbers.is_possible_number(numero)
    resultat["type_ligne"] = TYPES_FR.get(number_type(numero), "Inconnu")
    return resultat
