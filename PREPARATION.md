# SocialBee Connector — Preparation

**Category:** C31 — Social Media Management  
**Preparation status:** Blocked pending an officially supported integration surface  
**Scope decision:** No invented SocialBee REST CRUD or credential collection.

## 1. Product passport
SocialBee helps teams plan, approve, publish and analyse social content. The intended Imperal connector would give an owner a single operational view of social profiles, planned posts and publishing outcomes where SocialBee officially authorises programmatic access.

## 2. Human problem
When a social-media manager needs to audit scheduled content or coordinate publication, she currently moves between SocialBee and other systems, manually checks queues, and copies status into team workflows. This costs time and makes approval/accountability hard to trace.

## 3. Users, roles and permissions
- **Social-media manager:** reads calendars and delivery outcomes; drafts permitted content actions.
- **Marketing approver:** reviews publishing-impacting actions before they run.
- **Workspace owner/admin:** owns vendor access, connection lifecycle and least-privilege decisions.
- **Imperal operator:** may view only data exposed by the authorised vendor integration.

## 4. Primary scenario and human decision
`manager identifies a campaign need → connector reads authorised vendor data → manager reviews a proposed action → explicit approval → vendor executes action → connector records returned status`.

Current state is **blocked before the read step**: no public, supported SocialBee API documentation was established during discovery. No action may claim to read, create, publish, edit, or delete SocialBee content until that evidence exists.

## 5. Value and measurable outcome
If a supported API becomes available, success means: fewer manual status checks, traceable approvals for publishing actions, and clear vendor-returned delivery state. Failure means unsupported calls, scraped/browser automation, or uncertain account permissions.

## 6. Boundaries
### P0 if vendor access becomes available
- Connection validation using a documented harmless read endpoint.
- Read-only profile/content calendar visibility.
- Explicit, review-gated publication actions only where vendor documentation permits them.

### Explicitly excluded now
- Scraping SocialBee UI, browser automation, reverse-engineered endpoints, and fabricated API routes.
- Storage of passwords or unrestricted session cookies.
- Automatic posting without a documented API and human approval.

## 7. Data, privacy and integrations
Any later integration must use BYOC, encrypted secret storage, masked connection metadata, explicit disconnect, bounded pagination, vendor rate-limit handling and tenant isolation. Secret values, message bodies and unverified response payloads must not enter Git, logs, analytics or task comments.

**Integration status:** `blocked` — official public API/access model needs primary-source evidence and an authorised test account.

## 8. Release gate
Do not implement or submit for Marketplace Review until discovery is updated with: official API terms/docs, auth grant type and scopes, endpoint-by-endpoint evidence, authorised harmless live test, secrets review, UI evidence, and post-audit/PST requirements from the Master Playbook.
