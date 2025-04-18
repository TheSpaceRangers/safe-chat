from pydantic import BaseModel, Field

from typing import Annotated

class GetVersionOutput(BaseModel):
    version: Annotated[str, Field(min_length=5), Field(max_length=8)]