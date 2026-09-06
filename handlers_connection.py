"""Connection management for SocialBee Connector."""
from __future__ import annotations
import uuid
from typing import Any
from imperal_sdk import ActionResult
from app import chat
from schemas import NoParams, ConnectParams, ConnectionIdParams, ConnectionRecord, ConnectionList, DeleteResult
from socialbee_client import SocialBeeClient

async def resolve_client(ctx, connection_id: str = "") -> SocialBeeClient:
    connections = await ctx.store.get("connections", [])
    if not connections:
        raise ValueError("No SocialBee connections configured. Use connect_socialbee first.")
    conn = None
    if connection_id:
        for c in connections:
            if c.get("id") == connection_id:
                conn = c
                break
        if not conn:
            raise ValueError(f"Connection {connection_id} not found.")
    else:
        conn = connections[0]
    return SocialBeeClient(api_key=conn["api_key"], base_url=conn.get("base_url", ""))

@chat.function(
    "connect_socialbee",
    "Connect SocialBee account via API Key or Bearer Token.",
    action_type="write",
    chain_callable=True,
    event="socialbee-connector.connect_socialbee",
    effects=["create:connection"],
    data_model=ConnectionRecord
)
async def connect_socialbee(params: ConnectParams, ctx) -> ActionResult:
    """Connect a SocialBee account."""
    client = SocialBeeClient(api_key=params.api_key, base_url=params.base_url)
    res = await client.verify_auth()
    if res.get("status") == "error":
        return ActionResult.error(f"Failed to authenticate with SocialBee: {res.get('error')}")

    connections = await ctx.store.get("connections", [])
    masked = params.api_key[:6] + "..." if len(params.api_key) > 6 else "***"
    record = {
        "id": f"conn_{uuid.uuid4().hex[:8]}",
        "label": params.label or "Primary SocialBee",
        "api_key": params.api_key,
        "masked_key": masked,
        "base_url": params.base_url,
        "is_active": True
    }
    connections.append(record)
    await ctx.store.set("connections", connections)
    return ActionResult.ok(
        ConnectionRecord(
            id=record["id"],
            label=record["label"],
            masked_key=record["masked_key"],
            base_url=record["base_url"],
            is_active=record["is_active"]
        ),
        summary=f"Successfully connected SocialBee account '{record['label']}'."
    )

@chat.function(
    "list_connections",
    "List configured SocialBee connections.",
    action_type="read",
    chain_callable=True,
    event="socialbee-connector.list_connections",
    effects=["read:connections"],
    data_model=ConnectionList
)
async def list_connections(params: NoParams, ctx) -> ActionResult:
    """List connections."""
    conns = await ctx.store.get("connections", [])
    records = [
        ConnectionRecord(
            id=c["id"],
            label=c.get("label", ""),
            masked_key=c.get("masked_key", "***"),
            base_url=c.get("base_url", ""),
            is_active=c.get("is_active", True)
        )
        for c in conns
    ]
    return ActionResult.ok(ConnectionList(connections=records, total=len(records)), summary=f"Found {len(records)} connections.")

@chat.function(
    "disconnect_socialbee",
    "Disconnect SocialBee account and remove stored credentials.",
    action_type="destructive",
    chain_callable=True,
    event="socialbee-connector.disconnect_socialbee",
    effects=["delete:connection"],
    data_model=DeleteResult
)
async def disconnect_socialbee(params: ConnectionIdParams, ctx) -> ActionResult:
    """Disconnect connection."""
    connections = await ctx.store.get("connections", [])
    if not connections:
        return ActionResult.error("No active connection found.")
    target_id = params.connection_id or connections[0].get("id")
    rem = [c for c in connections if c.get("id") != target_id]
    await ctx.store.set("connections", rem)
    return ActionResult.ok(DeleteResult(success=True, message=f"Disconnected {target_id}."), summary=f"Disconnected {target_id}.")
