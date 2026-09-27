#!/usr/bin/env python3
"""Triage-509 — interface web minimale (Flask).

Lancement :  python web.py   →  http://127.0.0.1:5000
"""

from flask import Flask, request, render_template_string

from cli import analyser_numero
from triage509 import audit, report

app = Flask(__name__)

PAGE = """<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Triage-509</title>
<style>
body{font-family:system-ui,sans-serif;max-width:640px;margin:2em auto;padding:0 1em;background:#0f172a;color:#e2e8f0}
h1{color:#7dd3fc}input,button{font-size:1.1em;padding:.5em;border-radius:8px;border:1px solid #334155}
input{background:#1e293b;color:#e2e8f0;width:70%}button{background:#0284c7;color:#fff;cursor:pointer}
pre{background:#1e293b;padding:1em;border-radius:8px;white-space:pre-wrap}
.limite{color:#fbbf24;font-size:.9em}
</style></head><body>
<h1>📞 Triage-509</h1>
<p>Triage rapide des numéros haïtiens (+509).</p>
<form method="post" action="/analyser">
<input name="numero" placeholder="+509…" required>
<input name="utilisateur" placeholder="Utilisateur (audit)" style="width:40%;margin-top:.5em">
<input name="dossier" placeholder="Dossier (audit)" style="width:40%;margin-top:.5em"><br><br>
<button type="submit">Analyser</button></form>
{% if rapport %}<h2>Résultat</h2><pre>{{ rapport }}</pre>{% endif %}
{% if erreur %}<p style="color:#f87171">{{ erreur }}</p>{% endif %}
<p class="limite">⚠️ Cet outil n'identifie pas le propriétaire d'un numéro et ne le localise pas.</p>
</body></html>"""


@app.route("/", methods=["GET"])
def index():
    return render_template_string(PAGE)


@app.route("/analyser", methods=["POST"])
def analyser():
    numero = request.form.get("numero", "")
    utilisateur = request.form.get("utilisateur", "")
    dossier = request.form.get("dossier", "")
    analyse = analyser_numero(numero)
    if not analyse["ok"]:
        return render_template_string(PAGE, erreur=f"Erreur : {analyse['erreur']}")
    base = analyse["base"]
    audit.enregistrer(base["e164"], (analyse["operateur"] or {}).get("operateur", "Inconnu"),
                      base["type_ligne"], base["valide"], utilisateur, dossier)
    texte, _ = report.generer(analyse, utilisateur, dossier)
    return render_template_string(PAGE, rapport=texte)


if __name__ == "__main__":
    app.run(debug=True)
