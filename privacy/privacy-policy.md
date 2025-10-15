# Politique de confidentialité — SafeChat

## Responsable du traitement

SafeChat déploie un bot Discord et une API de modération. Discord reste responsable des traitements effectués sur sa plateforme.

## Finalités et base légale

- Finalité: modération automatisée des messages pour maintenir un espace sûr.
- Base légale: intérêt légitime (art. 6(1)(f) RGPD). Un test de mise en balance est disponible (voir `privacy/lia.md`).

## Données traitées

- Contenu du message transmis à l’API pour décision automatisée.
- Métadonnées techniques nécessaires au fonctionnement réseau (non stockées par l’application).
- Le bot n’affiche plus publiquement d’identifiants; l’utilisateur concerné reçoit un DM avec la raison.

## Conservation

- L’application ne persiste pas les messages. Les journaux techniques sont limités, sans PII, avec une rétention courte (p.ex. 7 jours) gérée par l’infrastructure.

## Destinataires et transferts

- Discord (plateforme). Modèle IA Mistral via Ollama local. Si un service externe est utilisé, évaluer les transferts hors UE.

## Droits des personnes

- Information, opposition, limitation. Un mécanisme de contestation existe via `/appeal submit`.

## Sécurité

- Limitation CORS, en-têtes de sécurité, gestion de secrets par variables d’environnement.

## Contact

- Contact projet: <à compléter>
