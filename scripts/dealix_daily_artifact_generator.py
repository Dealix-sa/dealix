from pathlib import Path
import json
out=Path('out/founder/daily_artifacts'); out.mkdir(parents=True, exist_ok=True)
clients=['شركة تدريب الرياض','مكتب عقار جدة']
if Path('data/preview/preview_clients.json').exists():
    try:
        data=json.loads(Path('data/preview/preview_clients.json').read_text(encoding='utf-8'))
        if isinstance(data, list): clients=[c.get('name') or c.get('client') for c in data if isinstance(c,dict)] or clients
        elif isinstance(data, dict): clients=[c.get('name') or c.get('client') for c in data.get('clients',[]) if isinstance(c,dict)] or clients
    except Exception:  # malformed JSON or missing keys — skip file
for client in clients[:3]:
    safe=client.replace(' ','_')
    (out/f'{safe}_followup_draft.md').write_text(f"""# Follow-up Draft — {client}

مرحبًا {client}،

أقترح نثبت الخطوة القادمة بشكل عملي: نحدد نطاق Pilot صغير، نطلع proof report، وبعدها نقرر هل يتحول إلى Retainer شهري.

ملاحظة داخلية: لا ترسل قبل مراجعة السياق وتخصيص الرسالة.
""", encoding='utf-8')
    (out/f'{safe}_proof_summary_draft.md').write_text(f"""# Proof Summary Draft — {client}

## ما تم
- مراجعة workflow الحالي.
- تحديد فرص التعطل.

## الدليل المطلوب
- قبل/بعد.
- عدد الفرص.
- next actions.

## القرار
متابعة Pilot أو التحويل إلى Retainer بعد proof.
""", encoding='utf-8')
print(f'Wrote founder daily artifacts to {out}')
