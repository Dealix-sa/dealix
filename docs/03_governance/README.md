# Governance — حوكمة Targeting OS

حدود الثقة والأمان التي تحوّل البحث المكثّف إلى عمل آمن. لا scraping خلف login،
لا spam، لا overclaim، لا إرسال بدون موافقة — تُفرض بالكود لا بالنية فقط.

## الوثائق

| الوثيقة | الموضوع |
|---|---|
| [RESEARCH_SOURCE_POLICY.md](RESEARCH_SOURCE_POLICY.md) | المصادر المسموحة/الممنوعة |
| [ROBOTS_AND_TERMS_POLICY.md](ROBOTS_AND_TERMS_POLICY.md) | احترام robots.txt (RFC 9309) وشروط المواقع |
| [OUTREACH_APPROVAL_POLICY.md](OUTREACH_APPROVAL_POLICY.md) | بوابة موافقة المؤسس قبل أي إرسال |
| [NO_SPAM_POLICY.md](NO_SPAM_POLICY.md) | منع الإزعاج وسقوف الإرسال |

## يفرضها الكود

- [`scripts/targeting_compliance_gate.py`](../../scripts/targeting_compliance_gate.py) + [`data/targeting/blocked_sources.yml`](../../data/targeting/blocked_sources.yml)
- `targeting_draft_lab.validate_draft()` — رفض العبارات المحظورة
- لا قناة إرسال في أي script ضمن المنظومة

## المرجعية الدستورية

[docs/00_constitution/NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md) ·
[docs/00_constitution/WHAT_DEALIX_REFUSES.md](../00_constitution/WHAT_DEALIX_REFUSES.md)
