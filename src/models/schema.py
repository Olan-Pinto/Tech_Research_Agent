# Define the data shapes that flow through your entire system.
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class Message(BaseModel):
    # Literal ensures only allowed strings are accepted
    role: Literal["user", "assistant", "system"]
    content: str
    # Automatically generates current time if not provided
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ConversationHistory(BaseModel):
    messages: list[Message] = []
    def add_message(self, role, content):
        self.messages.append(Message(role=role, content=content))

    def to_openai_format(self):
        return [{"role": msg.role, "content": msg.content} for msg in self.messages]

class OrchestratorResponse(BaseModel):
    response: str
    model_used : str
    tokens_used: int
    error: str
