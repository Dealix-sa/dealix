# Nurture Sequences — تسلسلات الرعاية

> Owned-channel nurture (email +, where consented, WhatsApp **inbound-initiated only**).
> **NO auto-send. NO cold outreach. NO scraping.** Every message is a **draft queued for founder
> approval** and sent manually after approval. Status: `DOCS_ONLY`. Voice from `CONTENT_FACTORY.md`.

## القواعد (Rules)

- Only contacts who **opted in** (free-tool capture, diagnostic booking, prior buyer) enter a sequence.
- Cold lists are forbidden. No purchased/scraped contacts. PDPL consent required + easy unsubscribe.
- Sequences are **draft templates**; the founder/operator reviews and sends each step manually,
  or approves a manual batch. No background auto-sender in any environment.
- Every email has exactly one CTA, matching the contact's funnel stage.

## التسلسل ١: عميل أداة مجّانية (Free-tool lead)

Trigger: opted-in after Business OS Score / calculator. Goal: → Diagnostic.

| Step | When | Message gist | CTA |
|------|------|--------------|-----|
| 1 | T+0 | "Your result + what it means" (full breakdown) | Get Business OS Score (if not done) |
| 2 | T+2d | One sector pattern (anonymized/hypothesis-framed) | Book Diagnostic |
| 3 | T+5d | "What a Diagnostic actually delivers" (free, rung 0) | Book Diagnostic |
| 4 | T+9d | Founder note + soft opt-down ("less often / pause") | Book Diagnostic |

## التسلسل ٢: تشخيص لم يحضر (Diagnostic no-show)

Trigger: booked Diagnostic, did not attend. Goal: re-book. Tone: helpful, no guilt.

| Step | When | Message gist | CTA |
|------|------|--------------|-----|
| 1 | T+1h | "We missed you — here's a 1-click re-book" | Re-book Diagnostic |
| 2 | T+1d | "Async option: send us 3 numbers, we'll pre-fill it" | Re-book Diagnostic |
| 3 | T+4d | Proof Pack preview as the reason it's worth 20 min | Re-book Diagnostic |
| 4 | T+8d | Final, respectful close ("we'll stop here unless you reply") | Re-book Diagnostic |

## التسلسل ٣: متابعة السبرنت (Sprint follow-up)

Trigger: completed a 499 Command Sprint. Goal: proof → next rung + referral seed.

| Step | When | Message gist | CTA |
|------|------|--------------|-----|
| 1 | T+0 | Deliver Proof Pack + ask approval to anonymize | Approve Proof Pack |
| 2 | T+3d | "What the Sprint surfaced → Data-to-Revenue Pack (1,500)" | Start Data Pack |
| 3 | T+10d | Outcome check-in (honest, no guaranteed-revenue claims) | Book follow-up |
| 4 | T+21d | Referral ask tied to delivered proof (see `REFERRAL_ENGINE.md`) | Refer a peer |

## حواجز المحتوى (Content guardrails)

- No fake scarcity ("only 2 spots") unless a real capacity limit exists and is true.
- No guaranteed revenue. Outcomes framed as what was *delivered*, not what is *promised*.
- No fabricated testimonials in any step.

## خطة 30 يوم (30-day plan)

1. Draft all three sequences as approval-ready templates (Arabic-first + English mirror).
2. Confirm opt-in source + PDPL consent + unsubscribe on every entry point.
3. Wire triggers to the **draft queue** (no live auto-sender) for founder review.
4. Run a small manual-send pilot of Sequence 1; measure reply/Diagnostic rate (`GROWTH_METRICS.md`).
5. Have `proof-governance-reviewer` clear every template before any send.
