from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional

class TokenModel(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    jti: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}