# Revenue KPI Tree | شجرة مؤشرات الإيرادات

## Purpose | الغرض
A single hierarchical view of every metric that drives Dealix's revenue. Each leaf
metric is owned by a machine; every parent metric is a deterministic function of
its children. This is the navigation map for performance work.

## Inputs | المدخلات
- Telemetry from every machine
- Ultimate Finance OS ledger
- AI Unit Economics System snapshots
- Performance Improvement OS experiment results

## Outputs | المخرجات
- `performance.kpi_tree`: hierarchical tree with current value, trend, owner, target
- Daily snapshot
- Weekly trend report
- Per-node drill-down links

## Tree structure | بنية الشجرة

### Top: Cash collected (monthly)
- = MRR + one-time revenue
- = Paid clients × average revenue per client
- = (Pipeline × win rate) realized as cash

### Sub-tree 1: Paid clients
- = Proposals sent × proposal win rate
- Proposal win rate
- Proposals sent (count, period)

### Sub-tree 2: Proposals sent
- = Meetings × meeting → proposal rate
- Meetings booked
- Meeting → proposal rate

### Sub-tree 3: Meetings booked
- = Sends approved × reply rate × reply → meeting rate
- Sends approved
- Reply rate
- Reply → meeting rate

### Sub-tree 4: Sends approved
- = Drafts produced × draft approval rate
- Drafts produced (LinkedIn / email / form / ABM / follow-up / nurture)
- Draft approval rate (per channel)

### Sub-tree 5: Drafts produced
- = A-bucket accounts × ABM coverage + B-bucket × outbound coverage
- A-bucket accounts (count)
- B-bucket accounts (count)

### Sub-tree 6: Pipeline value (parallel)
- = Open opportunities × stated value
- Weighted pipeline = sum(opportunity_value × stage_probability)

### Sub-tree 7: Retention (parallel)
- Logo retention rate
- Net revenue retention
- Referrals received per active client

### Sub-tree 8: Unit economics (parallel)
- AI cost per paid client
- Founder hours per paid client
- Gross margin per client

## Node fields | حقول العقدة
- name
- current_value
- target_value
- trend (7d, 30d, 90d)
- owner_worker
- diagnostic_link (to Conversion Diagnostics)
- experiment_link (to Experiment Backlog)

## Decision rules | قواعد القرار
- Any node falling > 20% below target for 14d triggers Conversion Diagnostics
- Any node trending favorable for 30d → capture pattern in Learning Loop
- Founder-set targets quarterly; worker computes daily

## Data source | مصدر البيانات
`performance.kpi_tree`, `finance.ledger`, machine-level telemetry.

## Approval class | فئة الموافقة
- A1: tree computation and snapshots
- A2: target setting; any externally published version
- A3: any benchmark publication referencing real client counts/values

## Trust gate | بوابة الثقة
- Every node traceable to source telemetry
- No node value presented without timestamp
- No external publication without founder approval and anonymization where needed
- Policy snapshot + audit row per snapshot

## Owner | المالك
Founder sets targets. Workers own their leaf metrics.

## Worker name
`performance.kpi_tree`

## KPI | المؤشرات (meta)
- Tree completeness (% nodes with current value)
- Freshness (median age of leaf values, target < 24h)
- Forecast accuracy at the top node (rolling 90d)

## Failure mode | حالات الفشل
- Leaf metric stops reporting; parent silently averages over missing data
- Target staleness (last set > 1 quarter ago)
- Node attribution drift (e.g., a metric counted in two sub-trees)

## Recovery path | مسار الاسترداد
- Missing-leaf alarm; parents pause aggregation until leaf reports
- Quarterly target-setting ritual enforced
- Annual tree audit to catch double-counting
