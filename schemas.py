"""Pydantic schemas for SocialBee Connector (C31. Social Media Management)."""
from __future__ import annotations
from typing import Any, Optional, List, Dict
from pydantic import BaseModel, Field

class NoParams(BaseModel):
    """Empty parameters model."""
    pass

class ConnectParams(BaseModel):
    label: str = Field(default="", description="Friendly connection label, e.g. Primary SocialBee.")
    api_key: str = Field(description="SocialBee API Key or Workspace Bearer Token.")
    base_url: str = Field(default="https://api.socialbee.io/v1", description="SocialBee API base URL.")

class ConnectionIdParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier (empty uses active connection).")

class ConnectionRecord(BaseModel):
    id: str
    label: str
    masked_key: str
    base_url: str
    is_active: bool

class ConnectionList(BaseModel):
    connections: list[ConnectionRecord]
    total: int

class DeleteResult(BaseModel):
    success: bool
    message: str

class ProfileRecord(BaseModel):
    id: str
    name: str
    platform: str
    status: str
    raw: Dict[str, Any] = Field(default_factory=dict)

class ProfileList(BaseModel):
    profiles: list[ProfileRecord]
    total: int

class ListProfilesParams(BaseModel):
    connection_id: str = Field(default="", description="Optional connection ID.")

class CategoryRecord(BaseModel):
    id: str
    name: str
    color: Optional[str] = None
    post_count: int = 0
    raw: Dict[str, Any] = Field(default_factory=dict)

class CategoryList(BaseModel):
    categories: list[CategoryRecord]
    total: int

class ListCategoriesParams(BaseModel):
    connection_id: str = Field(default="", description="Optional connection ID.")

class PostRecord(BaseModel):
    id: str
    category_id: Optional[str] = None
    text: str
    status: str
    scheduled_at: Optional[str] = None
    raw: Dict[str, Any] = Field(default_factory=dict)

class PostList(BaseModel):
    posts: list[PostRecord]
    total: int

class ListPostsParams(BaseModel):
    connection_id: str = Field(default="", description="Optional connection ID.")
    category_id: Optional[str] = Field(default=None, description="Filter by category ID.")
    limit: int = Field(default=20, ge=1, le=100, description="Max posts to return.")

class CreatePostParams(BaseModel):
    connection_id: str = Field(default="", description="Optional connection ID.")
    category_id: str = Field(description="SocialBee content category ID.")
    text: str = Field(description="Post content text.")
    profile_ids: List[str] = Field(default_factory=list, description="Target social profile IDs.")

class DeletePostParams(BaseModel):
    connection_id: str = Field(default="", description="Optional connection ID.")
    post_id: str = Field(description="SocialBee post ID to delete.")

class AuditSocialHealthParams(BaseModel):
    connection_id: str = Field(default="", description="Optional connection ID.")

class HealthAuditReport(BaseModel):
    connection_status: str
    profiles_count: int
    categories_count: int
    health_score: int
    details: Dict[str, Any]
