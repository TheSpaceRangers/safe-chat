from pydantic import BaseModel

class RuleRequest(BaseModel):
    topic: str

class RuleResponse(BaseModel):
    topics: list[str]
