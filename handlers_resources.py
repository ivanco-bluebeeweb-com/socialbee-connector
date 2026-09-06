"""Resource handlers for SocialBee Connector."""
from __future__ import annotations
from imperal_sdk import ActionResult
from app import chat
from schemas import (
    NoParams,
    ListProfilesParams, ProfileList, ProfileRecord,
    ListCategoriesParams, CategoryList, CategoryRecord,
    ListPostsParams, PostList, PostRecord,
    CreatePostParams, DeletePostParams, DeleteResult,
    AuditSocialHealthParams, HealthAuditReport
)
from handlers_connection import resolve_client

@chat.function(
    "list_profiles",
    "List social media profiles managed in SocialBee.",
    action_type="read",
    chain_callable=True,
    event="socialbee-connector.list_profiles",
    effects=["read:profiles"],
    data_model=ProfileList
)
async def list_profiles(params: ListProfilesParams, ctx) -> ActionResult:
    """List social profiles."""
    try:
        client = await resolve_client(ctx, params.connection_id)
        raw = await client.list_profiles()
        items = [
            ProfileRecord(
                id=str(p.get("id", "")),
                name=p.get("name", "Unknown Profile"),
                platform=p.get("platform", p.get("type", "unknown")),
                status=p.get("status", "active"),
                raw=p
            )
            for p in raw
        ]
        return ActionResult.ok(ProfileList(profiles=items, total=len(items)), summary=f"Retrieved {len(items)} social profiles.")
    except Exception as e:
        return ActionResult.error(f"Error listing profiles: {e}")

@chat.function(
    "list_categories",
    "List content categories in SocialBee workspace.",
    action_type="read",
    chain_callable=True,
    event="socialbee-connector.list_categories",
    effects=["read:categories"],
    data_model=CategoryList
)
async def list_categories(params: ListCategoriesParams, ctx) -> ActionResult:
    """List categories."""
    try:
        client = await resolve_client(ctx, params.connection_id)
        raw = await client.list_categories()
        items = [
            CategoryRecord(
                id=str(c.get("id", "")),
                name=c.get("name", "General"),
                color=c.get("color"),
                post_count=c.get("post_count", 0),
                raw=c
            )
            for c in raw
        ]
        return ActionResult.ok(CategoryList(categories=items, total=len(items)), summary=f"Retrieved {len(items)} categories.")
    except Exception as e:
        return ActionResult.error(f"Error listing categories: {e}")

@chat.function(
    "list_posts",
    "List scheduled or published posts in SocialBee.",
    action_type="read",
    chain_callable=True,
    event="socialbee-connector.list_posts",
    effects=["read:posts"],
    data_model=PostList
)
async def list_posts(params: ListPostsParams, ctx) -> ActionResult:
    """List posts."""
    try:
        client = await resolve_client(ctx, params.connection_id)
        raw = await client.list_posts(category_id=params.category_id, limit=params.limit)
        items = [
            PostRecord(
                id=str(p.get("id", "")),
                category_id=str(p.get("category_id", "")),
                text=p.get("text", p.get("content", "")),
                status=p.get("status", "queued"),
                scheduled_at=p.get("scheduled_at"),
                raw=p
            )
            for p in raw
        ]
        return ActionResult.ok(PostList(posts=items, total=len(items)), summary=f"Retrieved {len(items)} posts.")
    except Exception as e:
        return ActionResult.error(f"Error listing posts: {e}")

@chat.function(
    "create_post",
    "Create or schedule a post in SocialBee.",
    action_type="write",
    chain_callable=True,
    event="socialbee-connector.create_post",
    effects=["create:post"],
    data_model=PostRecord
)
async def create_post(params: CreatePostParams, ctx) -> ActionResult:
    """Create a post."""
    try:
        client = await resolve_client(ctx, params.connection_id)
        res = await client.create_post(category_id=params.category_id, text=params.text, profile_ids=params.profile_ids)
        if "error" in res:
            return ActionResult.error(f"Failed to create post: {res.get('error')}")
        rec = PostRecord(
            id=str(res.get("id", "temp_id")),
            category_id=params.category_id,
            text=params.text,
            status=res.get("status", "scheduled"),
            scheduled_at=res.get("scheduled_at"),
            raw=res
        )
        return ActionResult.ok(rec, summary=f"Created post {rec.id} in SocialBee.")
    except Exception as e:
        return ActionResult.error(f"Error creating post: {e}")

@chat.function(
    "delete_post",
    "Delete a post from SocialBee calendar or queue.",
    action_type="write",
    chain_callable=True,
    event="socialbee-connector.delete_post",
    effects=["delete:post"],
    data_model=DeleteResult
)
async def delete_post(params: DeletePostParams, ctx) -> ActionResult:
    """Delete a post."""
    try:
        client = await resolve_client(ctx, params.connection_id)
        success = await client.delete_post(post_id=params.post_id)
        if success:
            return ActionResult.ok(DeleteResult(success=True, message=f"Deleted post {params.post_id}."), summary=f"Deleted post {params.post_id}.")
        return ActionResult.error("Failed to delete post.")
    except Exception as e:
        return ActionResult.error(f"Error deleting post: {e}")

@chat.function(
    "audit_social_health",
    "Audit SocialBee profiles, categories, and content health.",
    action_type="read",
    chain_callable=True,
    event="socialbee-connector.audit_social_health",
    effects=["read:social_health"],
    data_model=HealthAuditReport
)
async def audit_social_health(params: AuditSocialHealthParams, ctx) -> ActionResult:
    """Audit social health."""
    try:
        client = await resolve_client(ctx, params.connection_id)
        profiles = await client.list_profiles()
        categories = await client.list_categories()
        score = 100 if profiles and categories else 50
        rep = HealthAuditReport(
            connection_status="healthy" if profiles is not None else "degraded",
            profiles_count=len(profiles),
            categories_count=len(categories),
            health_score=score,
            details={"profiles_active": len(profiles), "categories_active": len(categories)}
        )
        return ActionResult.ok(rep, summary=f"SocialBee health score: {score}/100 with {len(profiles)} profiles.")
    except Exception as e:
        return ActionResult.error(f"Error auditing health: {e}")
