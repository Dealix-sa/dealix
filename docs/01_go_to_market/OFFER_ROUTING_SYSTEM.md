# Offer Routing System

> Company → Weakness → Dealix OS Angle → Offer → Draft

Once the primary weakness is known, the router picks the right first commercial
offer. Engine: `scripts/targeting_offer_router.py`.

---

## Offer catalog (entry points)

| Offer id | Name | Price | Includes |
|----------|------|-------|----------|
| `command_sprint` | Dealix Command Sprint (7 days) | 499 SAR | Revenue Map · Proof Register · Executive Command Brief · Next Action Board |
| `business_os_setup` | Business OS Setup | 1,500 SAR | Delivery visibility · Client memory · Data consolidation |
| `delivery_os_lite` | Delivery OS Lite | 1,500 SAR | Delivery board · Acceptance criteria · Status visibility |
| `partner_diagnostic` | Partner Diagnostic | 0 SAR | Partner fit map · Co-sell angle · Referral mechanics |

The **Command Sprint** is the universal default first offer:
**Revenue + Proof + Command + Governance Lite**.

---

## Routing rules

| Primary weakness | Routed offer |
|------------------|--------------|
| `partner_potential` | `partner_diagnostic` |
| `delivery_blindness` | `delivery_os_lite` |
| `data_fragmentation` | `business_os_setup` |
| `client_memory_gap` | `business_os_setup` |
| everything else | `command_sprint` |

---

## Worked examples

| Company | Weakness | Offer |
|---------|----------|-------|
| Marketing agency | proof gap + revenue leakage | Command Sprint |
| Training company | proof gap | Command Sprint (+ Academy OS later) |
| Tech company | delivery + client memory | Business OS Setup |
| Consultancy | command fog + proof gap | Executive Command Sprint |
| Operations firm | delivery visibility | Delivery OS Lite |
| Potential partner | partner potential | Partner Diagnostic |

---

## Output

```python
{
  "company_name": "...",
  "primary_weakness": "proof_gap",
  "primary_os_angle": "proof_os",
  "offer_id": "command_sprint",
  "offer": { name_en, name_ar, price_sar, includes, draft },
  "draft_type": "command_sprint_offer"
}
```

`draft_type` tells the Draft Lab which template to compose.
