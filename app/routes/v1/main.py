from os import getenv

from fastapi import APIRouter

from schemas import GetVersionOutput, RuleRequest, RuleResponse, ModerationRequest, ModerationResponse
from storage import banned_topics
from services import check_if_message_is_about_banned_topic

api_v1 = APIRouter(prefix="/api/v1")

@api_v1.get('/version')
def get_version() -> GetVersionOutput:
    return GetVersionOutput(version=getenv("VERSION", "0.0.0"))

@api_v1.post("/rule")
def add_rule(rule: RuleRequest) -> RuleResponse:
    if rule.topic.lower() not in banned_topics:
        banned_topics.add(rule.topic.lower())
    return RuleResponse(topics=list(banned_topics))

@api_v1.delete('/rule')
def delete_rule(rule: RuleRequest) -> RuleResponse:
    if rule.topic.lower() in banned_topics:
        banned_topics.remove(rule.topic.lower())
    return RuleResponse(topics=list(banned_topics))

@api_v1.get('/rule')
def get_rules() -> RuleResponse:
    return RuleResponse(topics=list(banned_topics))

@api_v1.post('/moderate')
async def moderate(request: ModerationRequest) -> ModerationResponse:
    is_about_banned_topic: ModerationResponse = await check_if_message_is_about_banned_topic(request.content, list(banned_topics))
    return is_about_banned_topic