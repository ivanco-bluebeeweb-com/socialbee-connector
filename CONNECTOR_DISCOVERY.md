# SocialBee Connector — Connector Discovery

**Discovery status:** Blocked / no verified public API surface  
**Last reviewed:** 2026-09-06

## Evidence-led finding
The official SocialBee materials reviewed during the C31 audit did not establish a public developer API or official REST reference that supports third-party CRUD for workspace content, profiles, posting queues, analytics, or webhooks. Therefore no endpoint, HTTP method, request schema, authentication header, scope, quota, or webhook contract is asserted in this repository.

## What must be proven before code begins
1. An official SocialBee developer/API reference and applicable integration terms.
2. Supported authentication method, grant lifecycle, scopes, token revocation and rotation behaviour.
3. Exact read endpoints for accounts/profiles/content and pagination/rate-limit contracts.
4. Exact write endpoints and whether publishing requires an interactive approval or additional channel permissions.
5. Webhook availability, signature-verification contract and retry semantics.
6. An authorised sandbox or production test account for harmless connection validation.

## Rejected approaches
- Calling undocumented browser endpoints.
- Imitating the SocialBee web UI.
- Taking usernames/passwords or browser cookies as an integration credential.
- Reusing the C30 email-marketing resource model.

## Engineering implication
The prior email-marketing scaffold is not a valid SocialBee implementation. It must remain unsubmitted and be replaced only after the above evidence is attached to this document. Until then, the only valid product output is an honest blocked-state onboarding experience.
