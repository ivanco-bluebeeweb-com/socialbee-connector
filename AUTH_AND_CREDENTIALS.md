# SocialBee Connector — Authentication & Credentials

**Status:** Blocked — no verified supported third-party credential model.

## Current credential policy
Do **not** request, save, test, or transmit SocialBee usernames, passwords, browser cookies, session tokens, or guessed API keys. The repository has no verified official API authentication contract to justify accepting any of them.

## Required future authentication evidence
Before enabling a connection form, record from an official source:
- grant type (for example OAuth 2.0 or vendor-issued API token);
- exact token issuance and revocation path;
- necessary least-privilege scopes;
- account/workspace selection semantics;
- expiry, refresh and rotation behaviour;
- harmless identity/read endpoint used by connection validation;
- rate limits and vendor error mappings.

## Non-negotiable implementation rules
- BYOC only; encrypt secrets using Imperal secret storage.
- Never return a secret after save; mask connection metadata.
- Validate once with the documented harmless endpoint, not with a write/publish action.
- Support disconnect and deletion of locally stored credentials.
- Keep secrets out of manifests, Git, tests, logs, UI state and error text.

No credential schema is approved while this document remains blocked.
