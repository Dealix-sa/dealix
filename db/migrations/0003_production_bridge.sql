-- Dealix V10 Production Implementation Bridge

create table if not exists health_checks (
  id text primary key,
  service text not null,
  status text not null check (status in ('ok','warn','fail')),
  checked_at timestamptz not null default now(),
  details jsonb not null default '{}'::jsonb
);

create table if not exists deployment_events (
  id text primary key,
  environment text not null,
  git_sha text,
  status text not null check (status in ('planned','started','succeeded','failed','rolled_back')),
  actor text,
  created_at timestamptz not null default now(),
  notes text
);

create table if not exists tenant_seed_runs (
  id text primary key,
  tenant_id text not null,
  workspace_id text,
  status text not null default 'created',
  created_at timestamptz not null default now(),
  manifest jsonb not null default '{}'::jsonb
);

create index if not exists idx_deployment_events_environment on deployment_events(environment);
create index if not exists idx_tenant_seed_runs_tenant_id on tenant_seed_runs(tenant_id);
