from pydantic import BaseModel

class ModerationRequest(BaseModel):
    content: str
    author_id: str

class ModerationResponse(BaseModel):
    action: str
    reason: str | None = None
