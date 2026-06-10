# Revenue Playbook v2

**Version**: 2.0 | **Last updated**: 2026-06-10

---

## Sales Motion: Founder-Led, Warm-First

Sami handles all external communications personally. No automated sending.
No bots. No cold mass outreach.

---

## The Daily Sales Cycle

```
Morning: Run dealix_revenue_day.sh
       → Review CEO_REVENUE_REPORT.md
       → Pick top 5 targets from TOP20_TARGETS.csv
       → Review WHATSAPP_DRAFTS.md
       → Send manually (WhatsApp / LinkedIn / email)

Afternoon: Log any replies in CRM
         → Move hot leads to "discovery_call_scheduled"
         → Update next_followup_date

Evening: Review pipeline
       → Confirm tomorrow's top targets
```

---

## Qualification Criteria

A lead is qualified if ALL of the following are true:

- [ ] Saudi-based company
- [ ] 10+ employees OR 500K+ SAR annual revenue
- [ ] Has a clear operational pain (not just "curious about AI")
- [ ] Decision maker reachable (WhatsApp / LinkedIn / email)
- [ ] Not currently in a long-term contract with a competitor

---

## Offer Selection Guide

| Lead Profile | Recommended Offer | Rationale |
|-------------|-------------------|-----------|
| Large company, complex ops | Transformation Diagnostic Sprint | Right-size for real change |
| Skeptical, first time | Micro Sprint 499 SAR | Low-risk proof |
| Has data, no insights | Data Intelligence Pack 1,500 SAR | Immediate value |
| Wants ongoing support | Managed Ops 2,999–4,999/month | Recurring relationship |
| Enterprise, budget confirmed | Custom System 25,000+ SAR | Full engagement |

---

## Conversation Templates

### Opening (WhatsApp — warm intro)
```
السلام عليكم [الاسم]،
أنا سامي من Dealix — نبني أنظمة تشغيل AI للشركات السعودية.
سمعت عن عملكم في [القطاع] وأحسست أن [pain].
هل عندك 10 دقائق هذا الأسبوع؟
```

### After Interest Shown
```
ممتاز! Dealix يبدأ بتشخيص مدفوع (3-7 أيام) يطلع لكم:
• خارطة العمليات الحالية
• أين يتسرب الإيراد
• أول نظام يستحق التركيب
• خطة تنفيذ 14 يوم

السعر: [7,500–25,000 SAR] حسب الحجم.
هل نحدد موعد Zoom لأشرح أكثر؟
```

### Handling "غالي" Objection
```
فاهم. الكثير من عملاءنا كانت عندهم نفس الملاحظة.
لكن فكر فيها هكذا: التشخيص يطلع لكم أين تخسرون — وعادة ما نكتشف أن الخسارة أكبر بكثير من سعر التشخيص.
ولو ما اقتنعتم بالنتائج، ما في التزام للتنفيذ.
```

---

## CRM Status Definitions

| Status | Meaning | Next Action |
|--------|---------|-------------|
| `needs_review` | Lead identified, not contacted | Review and decide if qualified |
| `outreach_sent` | First message sent | Follow up in 3–5 days |
| `interested` | Replied with interest | Book discovery call |
| `discovery_call_scheduled` | Call booked | Prepare diagnostic pitch |
| `proposal_sent` | Proposal/quote delivered | Follow up in 2–3 days |
| `negotiating` | Back and forth on scope/price | Move to decision |
| `won` | Sprint/project confirmed | Start delivery |
| `lost` | Declined | Log reason, stay in touch |
| `dormant` | No response after 3 tries | Revisit in 30 days |

---

## Revenue Targets

| Period | Target | Minimum |
|--------|--------|---------|
| Week 1 | 1 discovery call | 1 outreach batch |
| Month 1 | 1 paid sprint | 5 active conversations |
| Month 3 | 3 sprint clients | 1 Managed Ops retainer |
| Month 6 | 2 Managed Ops + 1 Custom | 500K SAR pipeline |

---

## Rules

- Never send before reviewing the draft
- Never promise outcomes — only deliverables
- Never issue invoice without founder sign-off
- CRM update within 24h of every interaction
- Discovery call notes saved in `clients/` immediately after call
