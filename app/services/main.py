import json
from os import getenv

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers.string import StrOutputParser

from schemas import ModerationResponse

llm = ChatOllama(
    model="mistral",
    base_url=getenv("OLLAMA_BASE_URL", "http://localhost:11434")
)

async def check_if_message_is_about_banned_topic(message: str, topics: list[str]) -> ModerationResponse:
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("""
            Tu es un assistant de modération strict et vigilant.
            Ta mission est de détecter si un message parle, même indirectement, d’un sujet interdit.
            Tu dois être capable de comprendre le message quelle que soit la langue utilisée (français, anglais, arabe, espagnol, etc.).
            Si c’est le cas, retourne 'delete' et une explication courte du sujet concerné en français. Sinon, retourne 'nothing' et sans explication.
        """),
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