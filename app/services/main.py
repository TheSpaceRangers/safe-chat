import json
from os import getenv

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers.string import StrOutputParser

from schemas import ModerationResponse

llm = ChatOllama(
    model="mistral",
    base_url=getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    temperature=0.0
)

async def check_if_message_is_about_banned_topic(message: str, topics: list[str]) -> ModerationResponse:
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            "Tu es un assistant de modération **zéro tolérance**. "
            "Ta mission est de détecter **tout contenu inapproprié**, y compris :\n"
            "  • insulte directe ou déguisée (ex. «fdp», «salaud», «enculé»)\n"
            "  • discours haineux (racisme, sexisme, homophobie…)\n"
            "  • apologie de la violence ou de la drogue\n"
            "  • tout propos violant les règles de civilité\n\n"
            "Tu dois comprendre **toutes les langues**. Si le message contient **la moindre infraction**, même implicite:\n"
            "- **retourne** exactement la chaîne:  \n"
            "  `delete|<raison courte en français>`\n\n"
            "Sinon:\n"
            "- **retourne** exactement:  \n"
            "  `nothing`\n\n"
            "🔹 **Exemples**:\n"
            "  • message = «fdp» → `delete|insulte «fdp»`\n"
            "  • message = «Bonjour tout le monde» → `nothing`\n"
        ),
        HumanMessagePromptTemplate.from_template(
            "Message à analyser : {message}\n"
            "Sujets interdits : {topics}\n\n"
            "Le message fait-il référence à l’un de ces sujets, de manière directe ou indirecte ? "
            "Réponds uniquement au format JSON comme ceci :\n"
            "{{ \"action\": delete, \"reason\": \"Votre message contient un sujet interdit (le sujet interdit)\" }}"
        ),
    ])

    chain = prompt | llm | StrOutputParser()

    response = await chain.ainvoke({"message": message, "topics": topics})

    try:
        data = json.loads(response)
        return ModerationResponse(**data)
    except Exception:
        return ModerationResponse(action="nothing", reason="Réponse invalide ou mal formée")