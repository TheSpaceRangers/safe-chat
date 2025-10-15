# DPIA — SafeChat (aperçu)

## Portée

Modération de messages en transit, sans persistance applicative. Utilisation d’un LLM (Mistral via Ollama local) pour classer.

## Risques principaux

- Faux positifs (blocage injustifié)
- Biais de classification
- Divulgation d’identifiants si affichés publiquement (mitigée: anonymisation)

## Mesures

- Anonymisation du placeholder public
- Droit de contestation avec escalade humaine
- Journalisation sobre (sans PII), rétention courte
- En-têtes de sécurité et CORS restreint

## Résidu

Risque résiduel faible compte tenu de l’absence de stockage et des garde-fous.
