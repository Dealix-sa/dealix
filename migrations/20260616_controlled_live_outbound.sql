-- Dealix Controlled Live Outbound — initial schema
-- Run via: psql $DATABASE_URL -f migrations/20260616_controlled_live_outbound.sql
-- Or via Alembic: db/migrations/versions/20260616_014_controlled_live_outbound.py

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS outbound_contacts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_name TEXT NOT NULL,
  contact_name TEXT,
  email TEXT,
  phone TEXT,
  whatsapp TEXT,
  sector TEXT,
  city TEXT,
  website TEXT,
  source_url TEXT NOT NULL,
  verification_status TEXT NOT NULL DEFAULT 'unverified',
  confidence TEXT DEFAULT 'low',
  pain_hypothesis TEXT,
  dealix_angle TEXT,
  email_opt_out BOOLEAN NOT NULL DEFAULT FALSE,
  whatsapp_opt_in BOOLEAN NOT NULL DEFAULT FALSE,
  whatsapp_opt_out BOOLEAN NOT NULL DEFAULT FALSE,
  consent_source TEXT,
  consent_timestamp TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_outbound_contacts_email ON outbound_contacts(email);
CREATE INDEX IF NOT EXISTS ix_outbound_contacts_company_name ON outbound_contacts(company_name);

CREATE TABLE IF NOT EXISTS outbound_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contact_id UUID REFERENCES outbound_contacts(id),
  channel TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  subject TEXT,
  body TEXT NOT NULL,
  template_name TEXT,
  provider_message_id TEXT,
  error_message TEXT,
  approved_by TEXT,
  approved_at TIMESTAMPTZ,
  queued_at TIMESTAMPTZ,
  sent_at TIMESTAMPTZ,
  replied_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_outbound_messages_status ON outbound_messages(status);
CREATE INDEX IF NOT EXISTS ix_outbound_messages_channel ON outbound_messages(channel);
CREATE INDEX IF NOT EXISTS ix_outbound_messages_contact_id ON outbound_messages(contact_id);

CREATE TABLE IF NOT EXISTS outbound_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  message_id UUID REFERENCES outbound_messages(id),
  event_type TEXT NOT NULL,
  payload JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_outbound_events_message_id ON outbound_events(message_id);
CREATE INDEX IF NOT EXISTS ix_outbound_events_event_type ON outbound_events(event_type);

CREATE TABLE IF NOT EXISTS suppression_list (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  channel TEXT NOT NULL,
  value TEXT NOT NULL,
  reason TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(channel, value)
);

CREATE TABLE IF NOT EXISTS deals_pipeline (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contact_id UUID REFERENCES outbound_contacts(id),
  stage TEXT NOT NULL DEFAULT 'new',
  value_sar NUMERIC DEFAULT 0,
  next_action TEXT,
  next_action_at TIMESTAMPTZ,
  owner TEXT DEFAULT 'sami',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_deals_pipeline_stage ON deals_pipeline(stage);
CREATE INDEX IF NOT EXISTS ix_deals_pipeline_owner ON deals_pipeline(owner);
