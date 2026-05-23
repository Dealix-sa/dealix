# Copywriting Rules

The Dealix voice in five rules. Verified by `scripts/verify_brand_system.py`.

## 1. Concrete over generic
- ✅ "Eight accounts scored ≥ 80. Top three below."
- ❌ "Boost your sales."

## 2. Drafts, not sends
- ✅ "Drafted for your approval."
- ❌ "Sent automatically on your behalf."

## 3. No multipliers
- ❌ "10x your pipeline."
- ❌ "Triple your reply rate."
- ✅ "Approval-to-meeting rate visible weekly."

## 4. No guarantees
- ❌ "Guaranteed revenue lift."
- ❌ "Guaranteed leads."
- ✅ "Founder-approved machinery; outcomes depend on use."

## 5. Bilingual, not translated
- The Arabic version is an idiomatic re-write, not a literal translation.

## Forbidden phrases (regex)

```
(?i)\bguarantee[d]?\b\s+(revenue|sales|leads|results|pipeline|roi)
(?i)\b\d+x\b\s+(your|in)\s+(sales|revenue|pipeline|leads|growth)
(?i)\bfully\s+autonomous\b\s+(outbound|sales|sending|posting)
(?i)\bunlimited\b\s+(sends|outreach|automation|leads|messages)
(?i)\bset\s+(it|and)\s+forget\s*(it)?\b
(?i)\brevolutioniz(e|es|ed|ing)\b
(?i)\bnext-generation\b
```
