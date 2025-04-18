from pydantic import BaseModel

class RuleRequest(BaseModel):
    topic: str

class RuleResponse(BaseModel):
    topics: list[str]

class ModerationRequest(BaseModel):
    content: str
    author_id: str

class ModerationResponse(BaseModel):
    action: str
    reason: str | None = None
