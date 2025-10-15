# Model Card — Mistral via Ollama (SafeChat)

## Identité

- Modèle: Mistral (servi localement via Ollama)
- Version: cf. images/poids du système Ollama

## Usage prévu

- Classification/modération de messages courts pour détecter sujets interdits et propos injurieux.

## Limitations connues

- Faux positifs/négatifs possibles, sensibilité au contexte, biais linguistiques.

## Paramètres utilisés

- temperature: 0.0
- prompt de modération strict (voir `app/services/main.py`)

## Données

- Pas d’entraînement réalisé par SafeChat; inférence uniquement sur contenus en transit non persistés.

## Sécurité/Éthique

- Anonymisation publique, droit de contestation, supervision humaine.

## Contact

- <à compléter>
