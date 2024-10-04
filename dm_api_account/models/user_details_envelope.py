from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, Field, ConfigDict


class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int


    
    
class BbParseMode(str, Enum):
    Common = "Common"
    Info = "Info"
    Post = "Post"
    Chat = "Chat"


class PagingSettings(BaseModel):
    posts_per_page: int = Field(..., alias='postsPerPage')
    comments_per_page: int = Field(..., alias='commentsPerPage')
    topics_per_page: int = Field(..., alias='topicsPerPage')
    messages_per_page: int = Field(..., alias='messagesPerPage')
    entities_per_page: int = Field(..., alias='entitiesPerPage')


class UserSettings(BaseModel):
    color_schema: ColorSchema = Field(..., alias='colorSchema')
    nanny_greetings_message: str = Field(None, alias='nannyGreetingsMessage')
    paging: PagingSettings


class ColorSchema(str, Enum):
    Modern = "Modern"
    Pale = "Pale"
    Classic = "Classic"
    ClassicPale = "ClassicPale"
    Night = "Night"


class UserRole(str, Enum):
    Guest = "Guest"
    Player = "Player"
    Administrator = "Administrator"
    NannyModerator = "NannyModerator"
    RegularModerator = "RegularModerator"
    SeniorModerator = "SeniorModerator"

class Resource(BaseModel):
    login: str
    roles: List[UserRole]
    medium_picture_url: str = Field(None, alias='mediumPictureUrl')
    small_picture_url: str = Field(None, alias='smallPictureUrl')
    status: str = Field(None)
    rating: Rating
    online: datetime = Field(None)
    name: str = Field(None)
    location: str = Field(None)
    registration: datetime 
    icq: str = Field(None)
    skype: str = Field(None)
    original_picture_url: str = Field(None, alias='originalPictureUrl')
    info: str = Field(None)
    settings: UserSettings


class UserDetailsEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resource: Resource
    metadata: str = Field(None)
