
from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime


class Message(BaseModel):
    id: Optional[int] = None
    content: str
    timestamp: datetime
    is_from_user: bool


class CharacterConversation(BaseModel):
    id: Optional[int] = None
    character_name: str
    messages: List[Message] = Field(default_factory=list)


class UserConversations(BaseModel):
    id: Optional[int] = None
    user_id: int
    conversations: Dict[str, CharacterConversation] = Field(default_factory=dict)