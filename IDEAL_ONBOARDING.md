# SocialBee Connector — Ideal Onboarding

**Status:** Honest blocked state until official API access is verified.

## First launch
1. State plainly that a supported SocialBee API connection is not yet verified.
2. Explain that no SocialBee password, cookie, or unverified key is requested.
3. Offer a concise status: discovery required, no store data accessed, no publishing enabled.
4. Direct the workspace owner to obtain official API/integration documentation and authorised credentials if SocialBee grants access.
5. Once evidence is complete, expose a labelled BYOC form with only the officially required fields and a `Validate connection` action.

## Failure and recovery
- **No supported API:** retain blocked state; do not provide a false connection success.
- **Insufficient permission:** surface only the vendor-returned permission message and identify the required documented scope.
- **Expired/revoked credential:** mark connection disconnected; require reauthorisation, never retry a write action.

## Success state (future)
Show connected workspace label, masked credential metadata, confirmed scopes, last successful validation, and controls for disconnect. Publishing controls must be clearly separated from read-only operational visibility and require explicit confirmation.
