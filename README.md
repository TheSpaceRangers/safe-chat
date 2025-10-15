# SafeChat

Un système complet de modération de contenu, composé :

1. d’une **API REST** FastAPI pour gérer les règles et modérer les messages
2. d’un **bot Discord** basé sur `discord.py` pour appliquer la modération en temps réel
3. d’un **serv‌‌ice Ollama/Mistral** pour l’analyse sémantique via LangChain

---

## 🔍 Fonctionnalités

- **Gestion dynamique des règles**
  - Ajouter (`POST /api/v1/rule`) et supprimer (`DELETE /api/v1/rule`) des topics interdits
  - Lister les topics (`GET /api/v1/rule`)
- **Modération automatisée**
  - Endpoint `POST /api/v1/moderate` qui renvoie `{ action: "delete"|"nothing", reason?: string }`
- **Bot Discord**
  - Surveille chaque message, appelle l’API et, si nécessaire, remplace le message supprimé par un placeholder stylé
  - Commandes slash `/topics list` et `/topics add` pour gérer les règles depuis Discord

---

## 🏗️ Architecture

```text
┌──────────────────┐       ┌─────────────────────┐      ┌───────────────────┐
│   Discord Bot    │◄──────│  SafeChat API       │◄─────│  Mistral via      │
│  (discord.py)    │ HTTP  │ (FastAPI + Pydantic)│ HTTP │  Ollama Server    │
└──────────────────┘       └─────────────────────┘      └───────────────────┘
```

---

## SafeChat API

- **Code dans** [`app/`](https://github.com/TheSpaceRangers/safe-chat/tree/master/app/)
- **Points d’entrée** dans [`app/routes/v1/main.py`](https://github.com/TheSpaceRangers/safe-chat/blob/master/app/routes/v1/main.py)
- **Stockage en mémoire** dans [`app/storage/main.py`](https://github.com/TheSpaceRangers/safe-chat/blob/master/app/storage/main.py) avec une liste initiale de topics

---

## Bot Discord

- **Code dans** [`bot/main.py`](https://github.com/TheSpaceRangers/safe-chat/blob/master/bot/main.py)
- **Déployé via** [`bot/Dockerfile`](https://github.com/TheSpaceRangers/safe-chat/blob/master/bot/Dockerfile)

---

## ⚙️ Prérequis

- Docker + Docker Compose
- Une clé d’API Discord avec les intents `message_content` activés
- (Optionnel) Serveur Ollama local pour Mistral

---

## 🚀 Installation & Lancement

1. **Cloner le dépôt**

```bash
git clone https://github.com/TheSpaceRangers/safe-chat.git
cd safe-chat
```

2. **Configurer les variables d’environnement**

   - Copier `app/.env.sample` → `app/.env` puis remplir :
     ```ini
     VERSION=1.0.0
     ```
   - Copier `bot/.env.sample` → `bot/.env` puis remplir :
     ```ini
     DISCORD_TOKEN=TON_TOKEN_DISCORD_ICI
     DISCORD_COMMAND_CHANNEL_ID=ID_DU_CHANNEL_AUTORISE
     DISCORD_CHANNEL_ID=ID_DU_CHANNEL_DE_LOG_BOT
     DISCORD_APPEALS_CHANNEL_ID=ID_DU_CHANNEL_POUR_LES_CONTESTATIONS
     ```
   - (Optionnel) Si Ollama n’est pas sur `http://localhost:11434`, ajouter dans `bot/.env` :
     ```ini
     OLLAMA_BASE_URL=http://MON_OLLAMA:11434
     ```

3. **Lancer avec Docker Compose**

```bash
docker compose up --build
```

- L’API sera disponible sur `http://localhost:8000`
- Le bot se connectera automatiquement à Discord
- Ollama sert Mistral sur le port `11434`

---

## 📡 API SafeChat

| Méthode | Chemin             | Description                                                |
| ------- | ------------------ | ---------------------------------------------------------- |
| GET     | `/api/v1/version`  | Version de l’API                                           |
| GET     | `/api/v1/rule`     | Lister les topics interdits                                |
| POST    | `/api/v1/rule`     | Ajouter un topic: `{ "topic": "drogue" }`                  |
| DELETE  | `/api/v1/rule`     | Supprimer un topic: `{ "topic": "politics" }`              |
| POST    | `/api/v1/moderate` | Modérer un message: `{ "content": "…", "author_id": "…" }` |

**Exemple de réponse pour modération:**

```json
{ "action": "delete", "reason": "insulte « fdp »" }
```

### 🔐 Conformité (RGPD/GPAI/AI Act)

- Placeholder public anonymisé (pas d'affichage nom/avatar). Identité communiquée uniquement en DM.
- Commande `/appeal submit` pour contester; supervision humaine requise.
- API avec CORS restreint et en-têtes de sécurité.
- Pas de stockage applicatif des contenus; logs sobres, sans PII.

---

## 🤖 Bot Discord

- **Surveillance**: chaque message est envoyé à `/api/v1/moderate`.
- **Suppression stylée**:
  1. Le message original est supprimé
  2. Un placeholder est reposté via webhook avec embed
  3. L’utilisateur reçoit un DM avec la raison
- **Slash commands**:
  - `/topics list` → liste les topics interdits
  - `/topics add <topic>` → ajoute un topic
  - `/topics remove <topic>` → supprime un topic

## 💡 Développement & Tests

- **API**: tests rapides avec Swagger UI sur `http://localhost:8000/docs`
- **Bot**: invitez le bot sur un serveur de test et utilisez `/api version`
