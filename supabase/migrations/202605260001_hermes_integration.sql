-- Dealix-Hermes Strategic Integration Schema Migration
-- Apply via Supabase SQL editor or `supabase db push` after linking.
-- RLS: enabled by default. Backend uses service role or strict policies.

-- 1. Signals & Opportunities ────────────────────────────────
CREATE TABLE IF NOT EXISTS public.hermes_signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source TEXT NOT NULL, -- e.g., 'Founder Insight', 'CRM', 'SPL API', 'BorderGuru'
    payload JSONB NOT NULL DEFAULT '{}'::jsonb, -- البيانات الخام الواردة
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.hermes_opportunities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    signal_id UUID REFERENCES public.hermes_signals(id) ON DELETE SET NULL,
    title TEXT NOT NULL,
    sector TEXT, -- e.g., 'E-commerce', 'Luxury Goods', 'B2B Services'
    buyer_persona TEXT,
    strategic_score NUMERIC(5,2), -- Strategic Priority Score (0-100)
    status TEXT DEFAULT 'Draft', -- Draft, Scored, In_Progress, Closed_Won, Closed_Lost
    estimated_revenue NUMERIC(12,2) DEFAULT 0.00,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 2. Agent & Tool Governance ────────────────────────────────
CREATE TABLE IF NOT EXISTS public.hermes_agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT UNIQUE NOT NULL,
    purpose TEXT NOT NULL,
    autonomy_level TEXT DEFAULT 'Draft-Only', -- Draft-Only, Gated, Autonomous
    trust_score NUMERIC(5,2) DEFAULT 100.00,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.hermes_tools (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID REFERENCES public.hermes_agents(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    permission_required TEXT DEFAULT 'High', -- Low, Medium, High
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.hermes_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID REFERENCES public.hermes_agents(id) ON DELETE CASCADE,
    action_type TEXT NOT NULL, -- e.g., 'Send Message', 'Create Booking', 'Calculate Duty'
    status TEXT NOT NULL DEFAULT 'Pending_Approval', -- Pending_Approval, Executed, Failed, Blocked
    evidence_payload JSONB DEFAULT '{}'::jsonb, -- تفاصيل توثيق الحوكمة (Evidence Pack)
    approved_by TEXT, -- توثيق موافقة سامي في الحالات الحساسة
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 3. Hermes Shipments & Last-Mile Verification ────────────────
CREATE TABLE IF NOT EXISTS public.hermes_shipments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tracking_number TEXT UNIQUE NOT NULL,
    client_name TEXT NOT NULL,
    delivery_address TEXT NOT NULL,
    national_address_valid BOOLEAN DEFAULT FALSE,
    cargo_value NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    is_luxury BOOLEAN DEFAULT FALSE,
    evidence_pack_url TEXT,
    status TEXT DEFAULT 'Intake', -- Intake, Customs_Clearance, Last_Mile, Delivered, Returned
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 4. Sami Personal Wealth & Deals ──────────────────────────────
CREATE TABLE IF NOT EXISTS public.sami_deals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    opportunity_id UUID REFERENCES public.hermes_opportunities(id) ON DELETE SET NULL,
    deal_type TEXT NOT NULL, -- 'Consulting', 'White-Label License', 'Revenue Share', 'SaaS Retainer'
    target_value NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    my_share_percentage NUMERIC(5,2) DEFAULT 100.00,
    expected_cash_date DATE,
    pipeline_stage TEXT DEFAULT 'Lead', -- Lead, Diagnostic, Pitch, Negotiation, Closed_Won, Lost
    negotiation_notes TEXT,
    walkaway_conditions TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 5. Enable Row Level Security (RLS) ───────────────────────────
ALTER TABLE public.hermes_signals ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.hermes_opportunities ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.hermes_agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.hermes_tools ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.hermes_executions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.hermes_shipments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sami_deals ENABLE ROW LEVEL SECURITY;

-- 6. Indexes for optimized querying ────────────────────────────
CREATE INDEX IF NOT EXISTS hermes_opportunities_strategic_score_idx ON public.hermes_opportunities (strategic_score DESC);
CREATE INDEX IF NOT EXISTS hermes_shipments_tracking_idx ON public.hermes_shipments (tracking_number);
CREATE INDEX IF NOT EXISTS sami_deals_stage_idx ON public.sami_deals (pipeline_stage);

-- Comments ───────────────────────────────────────────────────
COMMENT ON TABLE public.hermes_signals IS 'Raw signals captured from Saudi market, SPL APIs, or Hermes logistics.';
COMMENT ON TABLE public.hermes_opportunities IS 'Processed opportunities categorized by sector, with strategic viability scores.';
COMMENT ON TABLE public.hermes_agents IS 'Agent Registry for governing autonomous executing entities.';
COMMENT ON TABLE public.hermes_tools IS 'Registered tools accessible by agents, subject to governance approvals.';
COMMENT ON TABLE public.hermes_executions IS 'Execution log representing actions taken by agents and approvals by Sami.';
COMMENT ON TABLE public.hermes_shipments IS 'Tracking for shipments using Saudi national address validation and luxury White-Glove standards.';
COMMENT ON TABLE public.sami_deals IS 'Deals tracker mapped directly to Sami Personal Wealth Engine metrics.';
