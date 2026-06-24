# Multi-Tenant Architecture

## Core objects

- Organization: paying company or client account.
- Workspace: operational space under an organization.
- Member: user with role and permissions.
- Plan: commercial package.
- Subscription: status and limits, not live payment capture.
- Usage event: auditable consumption metric.
- Audit log: immutable record of sensitive actions.

## Security principle

Never trust a client-provided `organization_id` or `workspace_id` unless server-side membership validation has passed.

## Access model

- owner: all organization settings.
- admin: team, workspace, operations.
- operator: run workflows and generate reports.
- viewer: read-only.
- billing_admin: manual invoice and subscription review.

## Tenant boundary rule

Every SaaS API must resolve tenant context from authentication, API key, or server session. Direct request body values are treated as hints only and must be validated.

## Commercial state

This architecture supports paid beta now, not unmanaged public signup.
