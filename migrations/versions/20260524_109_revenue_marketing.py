"""Revenue Marketing Engine — campaign / touch / attribution / experiment tables."""

DDL = """
CREATE TABLE IF NOT EXISTS hermes_marketing_campaigns (
  id UUID PRIMARY KEY,
  campaign_name TEXT NOT NULL,
  target_segment TEXT NOT NULL,
  offer_id UUID,
  channel TEXT NOT NULL,
  message_angle TEXT NOT NULL,
  budget_sar NUMERIC NOT NULL DEFAULT 0,
  success_metric TEXT NOT NULL,
  scale_kill_rule TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS hermes_marketing_touches (
  id UUID PRIMARY KEY,
  campaign_id UUID REFERENCES hermes_marketing_campaigns(id) ON DELETE SET NULL,
  lead_id TEXT,
  touch_type TEXT,
  channel TEXT,
  content_id TEXT,
  message_variant TEXT,
  occurred_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_hermes_marketing_touches_campaign_id
  ON hermes_marketing_touches(campaign_id);
CREATE INDEX IF NOT EXISTS idx_hermes_marketing_touches_lead_id
  ON hermes_marketing_touches(lead_id);

CREATE TABLE IF NOT EXISTS hermes_revenue_attribution (
  id UUID PRIMARY KEY,
  revenue_sar NUMERIC NOT NULL,
  deal_id TEXT NOT NULL,
  campaign_id UUID,
  offer_id UUID,
  channel TEXT,
  asset_id UUID,
  agent_id TEXT,
  attribution_type TEXT NOT NULL,
  payment_received BOOLEAN NOT NULL DEFAULT FALSE,
  signed_agreement BOOLEAN NOT NULL DEFAULT FALSE,
  is_real_revenue BOOLEAN GENERATED ALWAYS AS (
    payment_received OR signed_agreement
  ) STORED,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CHECK (
    payment_received OR signed_agreement OR attribution_type = 'pipeline_only'
  )
);
CREATE INDEX IF NOT EXISTS idx_hermes_revenue_attribution_deal_id
  ON hermes_revenue_attribution(deal_id);
CREATE INDEX IF NOT EXISTS idx_hermes_revenue_attribution_campaign_id
  ON hermes_revenue_attribution(campaign_id);
CREATE INDEX IF NOT EXISTS idx_hermes_revenue_attribution_offer_id
  ON hermes_revenue_attribution(offer_id);

CREATE TABLE IF NOT EXISTS hermes_marketing_experiments (
  id UUID PRIMARY KEY,
  experiment_name TEXT NOT NULL,
  target_segment TEXT NOT NULL,
  offer_id UUID,
  variable_tested TEXT NOT NULL,
  variant_a TEXT NOT NULL,
  variant_b TEXT NOT NULL,
  success_metric TEXT NOT NULL,
  result JSONB NOT NULL DEFAULT '{}',
  decision TEXT,
  status TEXT NOT NULL DEFAULT 'draft',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""
