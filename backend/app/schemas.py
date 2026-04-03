from pydantic import BaseModel

class AICommand(BaseModel):
    message: str