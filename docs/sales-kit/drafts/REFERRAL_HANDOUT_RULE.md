<!-- DRAFT — FOUNDER APPROVAL REQUIRED. -->

# Referral Code Hand-Out Rule — قاعدة توزيع رموز الإحالة

> Source of truth: `data/seeded_referrals.json` (generated 2026-05-14).

---

## 1. The 5 seeded codes — confirmed

The file contains exactly **5** referral codes, each worth **5,000 SAR credit per closed deal** and a **50% discount for the referred customer**:

| # | Referrer ID | Code | Credit (SAR) | Referred discount | Status |
|---|---|---|---|---|---|
| 1 | dealix_seed_001 | `REF-242B8799` | 5,000 | 50% | seeded_now |
| 2 | dealix_seed_002 | `REF-588AD579` | 5,000 | 50% | seeded_now |
| 3 | dealix_seed_003 | `REF-4BFA98AE` | 5,000 | 50% | seeded_now |
| 4 | dealix_seed_004 | `REF-4BB6EA62` | 5,000 | 50% | seeded_now |
| 5 | dealix_seed_005 | `REF-B559FC42` | 5,000 | 50% | seeded_now |

All 5 are `seeded_now` and unassigned — none has been handed out yet.

---

## 2. The hand-out rule — قاعدة التوزيع

1. **Eligibility:** A referral code is given **only to one of the first 5 paying customers** — a customer who has completed at least the first 50% Sprint payment. No code goes to a prospect, a free-diagnostic lead, or a warm contact.
2. **One code per customer:** Each of the 5 codes is assigned to exactly one paying customer. When customer #1 pays, they receive code #1; customer #2 receives code #2; and so on through customer #5.
3. **Reward:** When a customer's code produces a **closed (paid) deal**, the referrer earns **5,000 SAR**. The referred company gets a **50% discount** on their first engagement.
4. **Single-use per referred customer:** A code cannot be reused for the same referred company twice.
5. **Auto-rejected:** Self-referrals and same-email-domain referrals are rejected automatically (Partner Covenant).
6. **No unsafe automation, no guaranteed claims:** Referrals are shared by the customer through their own consent-based channels. Dealix does not bulk-distribute codes and does not pair them with any outcome promise.
7. **Beyond the first 5:** Once all 5 seeded codes are assigned, any further referral codes require a new founder approval and a fresh generation run — they are not minted automatically.

---

## 3. Hand-out script (founder, on first payment) — نص التسليم

**English draft:**
> Thank you for being one of our first customers. As a founding customer you get one referral code: `[CODE]`. Any B2B company you introduce gets 50% off their first engagement, and you earn 5,000 SAR for each one that becomes a paying customer. Share it only with companies you genuinely think it fits.

**العربية:**
> شكراً لكونك من أوائل عملائنا. كعميل مؤسِّس تحصل على رمز إحالة واحد: `[CODE]`. أي شركة B2B تقدّمها لنا تحصل على خصم 50% على أول مشروع، وتكسب أنت 5,000 ريال عن كل شركة تتحوّل إلى عميل مدفوع. شاركه فقط مع شركات تراها مناسبة فعلاً.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
