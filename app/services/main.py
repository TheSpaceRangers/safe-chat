from os import getenv

from langchain_ollama import ChatOllama

from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers.string import StrOutputParser

llm = ChatOllama(
    model="llama3.2:1b",
    base_url=getenv("OLLAMA_BASE_URL", "http://localhost:11434")
)

async def check_if_message_is_about_banned_topic(message: str, topics: list[str]) -> str:
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("Tu es un assistant de modération. Ta tâche est de dire si un message parle d'un sujet interdit."),
        HumanMessagePromptTemplate.from_template("Voici un message : \"{message}\"\n\nVoici les sujets interdits : {topics}\n\nEst-ce que le message traite d’un de ces sujets (même indirectement) ?"),
    ])

    chain = prompt | llm | StrOutputParser()

    response = await chain.ainvoke({"message": message, "topics": topics})

    return response