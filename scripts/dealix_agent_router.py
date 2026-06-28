import argparse
import json
import uuid
from datetime import UTC, datetime
from pathlib import Path

REG=Path('data/agents/agent_registry.json')
RUNS=Path('data/agents/agent_runs.jsonl')
OUT=Path('out/agents'); OUT.mkdir(parents=True, exist_ok=True)

def registry(): return json.loads(REG.read_text(encoding='utf-8'))

def produce(role, task):
    approval_required = registry().get(role, {}).get('approval_required', True)
    risk = registry().get(role, {}).get('risk','medium')
    if role=='crm_research_agent':
        return {'summary': task, 'likely_pains':['متابعة غير منظمة','فرص تضيع','غياب next action'], 'missing_information':['حجم leads الشهري','قنوات التواصل','نسبة التحويل الحالية'], 'recommended_next_action':'جهز discovery call مختصر', 'risk_level':risk, 'needs_human_review':approval_required}
    if role=='outreach_draft_agent':
        return {'channel':'whatsapp','draft':'السلام عليكم، لاحظت أن كثير من شركات التدريب تخسر فرص بعد أول تواصل. Dealix يساعدكم تبنون نظام متابعة وعروض وتقارير بدون وعود مبالغ فيها. هل يناسب نرسل تشخيص مختصر؟','send_status':'draft_only','risk_level':risk,'needs_human_review':True}
    if role=='lead_qualification_agent':
        return {'fit_score':78,'stage_recommendation':'outreach_drafted','why':'الألم مرتبط بالإيراد والمتابعة','next_action':'راجع draft يدويًا ثم سجّل interaction','approval_required':True}
    if role=='proposal_agent':
        return {'proposal_draft':'Pilot 14 يوم لبناء workflow متابعة، dashboard، وقوالب عروض. الأرقام تقديرية وليست ضمانًا.','assumptions':['توفر بيانات أولية','مراجعة بشرية للرسائل'],'risk_level':risk,'needs_human_review':True}
    if role=='ceo_briefing_agent':
        return {'briefing':['راجع أعلى 10 leads','أرسل 5 رسائل مراجعة يدويًا','حسن صفحة training solution'], 'risk_level':'low','needs_human_review':False}
    return {'output':'No specialized handler yet; produce structured draft only.', 'task':task, 'risk_level':risk, 'needs_human_review':approval_required}

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--role', required=True); ap.add_argument('--task', required=True); ap.add_argument('--task-id', default=None)
    a=ap.parse_args(); run_id='run_'+uuid.uuid4().hex[:10]
    output=produce(a.role,a.task)
    out_path=OUT/f'{run_id}_{a.role}.json'
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
    record={'run_id':run_id,'task_id':a.task_id,'role':a.role,'started_at':datetime.now(UTC).isoformat(),'finished_at':datetime.now(UTC).isoformat(),'status':'needs_approval' if output.get('needs_human_review') else 'done','output_path':str(out_path),'risk_level':output.get('risk_level'),'approval_required':output.get('needs_human_review')}
    RUNS.parent.mkdir(parents=True, exist_ok=True)
    with RUNS.open('a',encoding='utf-8') as f: f.write(json.dumps(record, ensure_ascii=False)+'\n')
    print('Wrote', out_path)
    print(json.dumps(record, ensure_ascii=False, indent=2))
