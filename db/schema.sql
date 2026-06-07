-- Dealix CRM/Revenue Machine minimal schema
create table if not exists leads (
  id text primary key,
  created_at timestamptz default now(),
  company text not null,
  contact_name text,
  email text,
  phone text,
  sector text,
  pain text,
  source text,
  utm_source text,
  utm_campaign text,
  score integer default 0,
  status text default 'new'
);

create table if not exists accounts (
  id text primary key,
  created_at timestamptz default now(),
  name text not null,
  sector text,
  website text,
  city text,
  notes text
);

create table if not exists opportunities (
  id text primary key,
  created_at timestamptz default now(),
  account_id text,
  lead_id text,
  stage text default 'new',
  package text,
  value_sar numeric default 0,
  probability numeric default 0,
  next_action text,
  next_action_date date
);

create table if not exists interactions (
  id text primary key,
  created_at timestamptz default now(),
  lead_id text,
  opportunity_id text,
  channel text,
  direction text,
  summary text,
  next_action text
);
