-- Dealix V9 multi-tenant SaaS schema
create table if not exists tenants (
  id text primary key,
  name text not null,
  plan text not null default 'starter',
  status text not null default 'active',
  created_at timestamptz not null default now()
);

create table if not exists workspaces (
  id text primary key,
  tenant_id text not null references tenants(id),
  name text not null,
  region text default 'saudi',
  created_at timestamptz not null default now()
);

create table if not exists users (
  id text primary key,
  email text not null unique,
  display_name text,
  created_at timestamptz not null default now()
);

create table if not exists memberships (
  tenant_id text not null references tenants(id),
  workspace_id text references workspaces(id),
  user_id text not null references users(id),
  role text not null,
  created_at timestamptz not null default now(),
  primary key (tenant_id, user_id, workspace_id)
);

create table if not exists usage_events (
  id text primary key,
  tenant_id text not null references tenants(id),
  workspace_id text references workspaces(id),
  event_type text not null,
  quantity numeric not null default 1,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists audit_events (
  id text primary key,
  tenant_id text references tenants(id),
  workspace_id text references workspaces(id),
  actor_user_id text,
  action text not null,
  resource_type text,
  resource_id text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index if not exists idx_usage_events_tenant_created on usage_events(tenant_id, created_at);
create index if not exists idx_audit_events_tenant_created on audit_events(tenant_id, created_at);
