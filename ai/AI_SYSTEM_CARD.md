# AI System Card — SafeChat

## Description

Pipeline de modération: Discord → API FastAPI → Mistral (Ollama) → décision `delete|nothing`.

## Entrées/Sorties

- Entrée: `content` (texte du message)
- Sortie: `{ action: "delete"|"nothing", reason?: string }`

## Gouvernance et supervision

- Anonymisation du placeholder public
- Commande `/appeal submit` pour contestation et révision humaine

## Gestion des risques

- Biais et surblocage: suivi via retours de contestations et tests synthétiques
- Pas de stockage des messages

## Évaluation

- Jeux de tests synthétiques (à documenter), collecte des métriques de faux positifs/négatifs (agrégées)

## Déploiement

- Exposition locale via Docker Compose; CORS restreint et en-têtes sécurité sur l’API

## Contact

- <à compléter>
