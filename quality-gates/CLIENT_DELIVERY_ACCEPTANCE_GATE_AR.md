# بوابة قبول العميل

قبول العميل لا يعني الإعجاب العام. يعني أن العميل وافق على مخرج محدد.

## أنواع القبول
- accepted
- accepted_with_notes
- needs_revision
- rejected

## مطلوب لكل قبول
- اسم العميل.
- اسم المخرج.
- التاريخ.
- الملاحظات.
- next action.

## الاستخدام
شغل:

```bash
python scripts/dealix_preview_acceptance_gate.py --client "شركة تدريب الرياض" --deliverable "Workflow map" --status accepted
```
