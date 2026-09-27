# 📞 Triage-509

Outil de **triage rapide** des numéros de téléphone haïtiens (+509), pensé pour les
enquêteurs disposant de peu de moyens.

## Ce que l'outil fait

- Parsing et validation d'un numéro (bibliothèque `libphonenumber` de Google)
- Détection de l'**opérateur probable** (Digicel / Natcom / fixe / VoIP) d'après le
  plan national de numérotation du CONATEL (communication du 20/01/2017, réf. ITU)
- Type de ligne (mobile, fixe, VoIP…)
- Journal d'utilisation (**audit**) : chaque analyse est horodatée et enregistrée
- Rapport en français, sauvegardé dans `rapports/`
- Interface terminal (`cli.py`) et interface web minimale (`web.py`)

## Ce que l'outil ne fait PAS (et ne fera jamais)

- ❌ Identifier le propriétaire d'un numéro
- ❌ Localiser un téléphone en temps réel
- ❌ Intercepter des communications

Ces informations ne peuvent être obtenues que par **réquisition judiciaire
auprès de l'opérateur**. Tout outil qui prétend le faire autrement est malhonnête.

## Limites connues

- L'opérateur détecté est **probable** : la portabilité des numéros et les
  réattributions de blocs depuis 2017 peuvent fausser le résultat. Le rapport
  l'indique explicitement.
- Les scanners WhatsApp / Telegram / HLR sont documentés mais **désactivés** :
  WhatsApp n'a pas d'API publique de vérification, Telegram exige des identifiants
  API officiels, le HLR est un service payant. Voir `triage509/scanners/`.

## Installation

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Utilisation

```bash
# Terminal
python cli.py +50934123456
python cli.py 34123456 --utilisateur "Agent D." --dossier "2026-118"
python cli.py +50942123456 --json

# Web
python web.py   # → http://127.0.0.1:5000
```

## Structure

```
triage-509/
├── cli.py                  # interface terminal
├── web.py                  # interface web (Flask)
├── triage509/
│   ├── core.py             # parsing / validation (libphonenumber)
│   ├── carriers.py         # détection opérateur (plan CONATEL)
│   ├── audit.py            # journal d'utilisation (JSON Lines)
│   ├── report.py           # rapport français
│   └── scanners/           # scanners complémentaires (WhatsApp, Telegram, HLR)
├── data/
│   ├── prefixes_ht.json    # blocs CONATEL 2017
│   └── audit.jsonl         # journal (généré à l'usage)
└── rapports/               # rapports générés
```

## Usage responsable

Cet outil traite des données potentiellement personnelles. Il est destiné à un
usage légitime (enquête judiciaire, vérification de ses propres numéros,
recherche avec consentement). Chaque utilisation est journalisée : c'est une
garantie, pas une option.
