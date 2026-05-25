"""Revenue Marketing Engine schema reference.

Source of truth migration: db/migrations/versions/20260525_014_revenue_marketing_engine.py
"""

DDL = """
CREATE TABLE rm_offers (
  id TEXT PRIMARY KEY,
  name_ar TEXT NOT NULL,
  name_en TEXT NOT NULL,
  tier TEXT NOT NULL,
  price_min_sar NUMERIC(12,2) NOT NULL DEFAULT 0,
  price_max_sar NUMERIC(12,2) NOT NULL DEFAULT 0,
  promise_ar TEXT NOT NULL DEFAULT '',
  deliverables JSONB NOT NULL DEFAULT '[]',
  target_segments JSONB NOT NULL DEFAULT '[]',
  primary_pain TEXT NOT NULL DEFAULT '',
  success_metric TEXT NOT NULL DEFAULT '',
  money_quality NUMERIC(5,3) NOT NULL DEFAULT 0.5,
  active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE rm_signals (
  id TEXT PRIMARY KEY,
  source TEXT NOT NULL,
  summary_ar TEXT NOT NULL,
  summary_en TEXT NOT NULL DEFAULT '',
  segment TEXT NOT NULL,
  pain TEXT NOT NULL,
  suggested_offer_id TEXT NOT NULL DEFAULT '',
  why_now TEXT NOT NULL DEFAULT '',
  proof_target TEXT NOT NULL DEFAULT '',
  confidence NUMERIC(4,3) NOT NULL DEFAULT 0.5,
  captured_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE rm_campaigns (
  id TEXT PRIMARY KEY,
  campaign_name TEXT NOT NULL,
  target_segment TEXT NOT NULL,
  offer_id TEXT NOT NULL,
  channel TEXT NOT NULL,
  message_angle TEXT NOT NULL DEFAULT '',
  cta_label_ar TEXT NOT NULL DEFAULT '',
  cta_path TEXT NOT NULL DEFAULT '',
  success_metric TEXT NOT NULL DEFAULT '',
  scale_kill_rule TEXT NOT NULL DEFAULT '',
  budget_sar NUMERIC(12,2) NOT NULL DEFAULT 0,
  status TEXT NOT NULL DEFAULT 'draft',
  signal_id TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE rm_marketing_touches (
  id TEXT PRIMARY KEY,
  campaign_id TEXT,
  lead_id TEXT,
  touch_type TEXT NOT NULL,
  channel TEXT,
  content_id TEXT,
  asset_id TEXT,
  agent_id TEXT,
  message_variant TEXT NOT NULL DEFAULT '',
  occurred_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE rm_revenue_attribution (
  id TEXT PRIMARY KEY,
  revenue_sar NUMERIC(14,2) NOT NULL CHECK (revenue_sar >= 0),
  deal_id TEXT NOT NULL,
  primary_source TEXT NOT NULL,
  secondary_source TEXT NOT NULL DEFAULT '',
  campaign_id TEXT,
  offer_id TEXT,
  channel TEXT,
  asset_ids JSONB NOT NULL DEFAULT '[]',
  agent_ids JSONB NOT NULL DEFAULT '[]',
  influenced_by JSONB NOT NULL DEFAULT '[]',
  attribution_type TEXT NOT NULL DEFAULT 'multi_touch',
  payment_confirmed BOOLEAN NOT NULL DEFAULT TRUE,
  money_quality NUMERIC(5,3) NOT NULL DEFAULT 0.5,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE rm_marketing_experiments (
  id TEXT PRIMARY KEY,
  experiment_name TEXT NOT NULL,
  target_segment TEXT NOT NULL,
  offer_id TEXT NOT NULL,
  variable_tested TEXT NOT NULL,
  variant_a TEXT NOT NULL,
  variant_b TEXT NOT NULL,
  success_metric TEXT NOT NULL,
  minimum_sample INTEGER NOT NULL DEFAULT 50,
  decision_rule TEXT NOT NULL,
  samples_a INTEGER NOT NULL DEFAULT 0,
  samples_b INTEGER NOT NULL DEFAULT 0,
  wins_a INTEGER NOT NULL DEFAULT 0,
  wins_b INTEGER NOT NULL DEFAULT 0,
  status TEXT NOT NULL DEFAULT 'draft',
  result JSONB NOT NULL DEFAULT '{}',
  decision TEXT NOT NULL DEFAULT '',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE rm_content_cards (
  id TEXT PRIMARY KEY,
  topic_ar TEXT NOT NULL,
  target_segment TEXT NOT NULL,
  pain TEXT NOT NULL,
  offer_id TEXT NOT NULL,
  cta_ar TEXT NOT NULL,
  channel TEXT NOT NULL,
  success_metric TEXT NOT NULL DEFAULT 'leads_booked',
  pillar TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL DEFAULT 'idea',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE rm_funnel_snapshots (
  id TEXT PRIMARY KEY,
  captured_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  visitors INTEGER NOT NULL DEFAULT 0,
  leads INTEGER NOT NULL DEFAULT 0,
  qualified_leads INTEGER NOT NULL DEFAULT 0,
  calls_booked INTEGER NOT NULL DEFAULT 0,
  proposals_sent INTEGER NOT NULL DEFAULT 0,
  won INTEGER NOT NULL DEFAULT 0,
  lost INTEGER NOT NULL DEFAULT 0,
  paid INTEGER NOT NULL DEFAULT 0,
  retainers INTEGER NOT NULL DEFAULT 0,
  period_label TEXT NOT NULL DEFAULT ''
);
"""
