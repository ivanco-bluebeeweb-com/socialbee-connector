# SocialBee Connector — UI Component Plan

**Status:** Blocked-state UI only; no simulated SocialBee resources.

## Layout
- Full-width form container within the left sidebar; contents stretch to its full available width.
- Every input has a visible label; any placeholder must describe the exact expected official credential or workspace value.
- Do not duplicate modal instructions in the left sidebar.

## Initial components
1. **Status card:** title `SocialBee API access not yet verified`; explains the connector is intentionally inactive rather than pretending to connect.
2. **Evidence checklist:** official API reference, auth/scopes, test account, harmless validation endpoint, write/webhook evidence.
3. **Connection form:** hidden until the authentication requirements in `AUTH_AND_CREDENTIALS.md` are verified.
4. **Audit panel:** when implemented, shows non-sensitive timestamps and validation result only; never secrets.

## Interaction safety
- No publish/delete controls in the blocked state.
- Future destructive or externally visible actions require a confirmation modal containing the specific target and effect.
- Use loading, empty and vendor-error states; do not fabricate social profiles, campaigns or analytics.

## Verification criterion
Before release, capture Webbee Eyes evidence for blocked, disconnected, connected, empty, error and confirmation states against the actual SDK components.
