from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import deal_conversation_intelligence as dci

REPORT_DIR = Path('reports/commercial/deal_strategy_brain')

CLOSE_PROBABILITY_BANDS = ('low', 'medium', 'high', 'very_high')

OFFER_LADDER = {
    'free_diagnostic': {'price': '0 SAR', 'duration': '30 min'},
    'micro_sprint_499_sar': {'price': '499 SAR', 'duration': '1 week'},
    'data_pack_1500_sar': {'price': '1500 SAR', 'duration': 'one-time'},
    'managed_ops_2999_4999_sar_monthly': {'price': '2999-4999 SAR/mo', 'duration': 'monthly'},
    'transformation_diagnostic_sprint_7500_25000_sar': {'price': '7500-25000 SAR', 'duration': '3-7 days'},
    'custom_enterprise_system': {'price': '25000-100000+ SAR', 'duration': 'custom'},
}

FORBIDDEN_COMMITMENTS = [
    'guaranteed_revenue',
    'final_price_without_scope',
    'fake_case_studies',
    'legal_commitments',
    'uncontrolled_outreach',
]


def _score_deal(
    stage: str,
    sentiment: str,
    urgency: str,
    objection: str,
    missing_info: list[str],
) -> int:
    score = 0
    stage_scores = {
        'cold': 5, 'aware': 15, 'interested': 35, 'discovery': 45,
        'proposal': 60, 'negotiation': 70, 'procurement': 80,
        'closed_won': 100, 'closed_lost': 0, 'renewal': 85, 'expansion': 90,
    }
    score += stage_scores.get(stage, 10)
    if sentiment == 'positive':
        score += 10
    elif sentiment == 'negative':
        score -= 10
    urgency_bonus = {'high': 10, 'medium': 5, 'low': 0}
    score += urgency_bonus.get(urgency, 0)
    objection_penalty = {'price': -10, 'timing': -8, 'trust': -12, 'authority': -15,
                         'details': -5, 'competition': -10, 'scope': -5, 'legal': -10, 'none': 0}
    score += objection_penalty.get(objection, 0)
    score -= len(missing_info) * 3
    return max(0, min(100, score))


def _close_probability_band(score: int) -> str:
    if score >= 75:
        return 'very_high'
    if score >= 50:
        return 'high'
    if score >= 25:
        return 'medium'
    return 'low'


def _discount_policy(stage: str, score: int) -> dict[str, Any]:
    return {
        'max_discount_pct': 0 if score < 50 else (5 if score < 75 else 10),
        'discount_requires_approval': True,
        'never_discount_below_floor': True,
        'floor_rule': 'no discount without confirmed scope and owner',
        'auto_commit': False,
    }


def _negotiation_position(stage: str, objection: str, score: int) -> dict[str, Any]:
    if objection == 'price':
        return {
            'stance': 'anchor_value_first',
            'message': 'Present ROI calculation before discussing price adjustment.',
            'concession_order': ['scope_reduction', 'payment_terms', 'minor_discount'],
            'never_do': ['immediate_discount', 'guaranteed_roi', 'price_without_scope'],
        }
    if objection == 'trust':
        return {
            'stance': 'proof_first',
            'message': 'Offer pilot or proof pack before any price concession.',
            'concession_order': ['free_pilot', 'case_study', 'reference_call'],
            'never_do': ['fake_testimonials', 'guaranteed_results', 'unverified_claims'],
        }
    if objection == 'timing':
        return {
            'stance': 'discover_trigger',
            'message': 'Find what must happen before they can move. Set a future touchpoint.',
            'concession_order': ['future_date_commit', 'low_commitment_next_step'],
            'never_do': ['pressure_tactics', 'fake_urgency', 'spam_follow_up'],
        }
    return {
        'stance': 'discovery_mode',
        'message': 'Ask one focused question to uncover the real blocker.',
        'concession_order': ['information_sharing', 'free_diagnostic', 'pilot'],
        'never_do': ['mass_outreach', 'unqualified_proposal', 'final_commitment'],
    }


def _proof_to_show(stage: str, sector: str, objection: str) -> list[str]:
    base = ['daily_command_report', 'opportunity_count', 'owner_map_sample']
    if objection == 'trust':
        base += ['sector_case_highlight', 'pilot_scope_proposal']
    if stage in ('proposal', 'negotiation'):
        base += ['roi_model_draft', 'sample_proof_pack']
    return base


def _must_ask_questions(intent: str, stage: str, missing: list[str]) -> list[str]:
    questions = dci.DISCOVERY_QUESTIONS.get(intent, dci.DISCOVERY_QUESTIONS['default'])
    if 'decision_maker_unknown' in missing:
        questions = ['من يملك قرار الموافقة النهائية على هذا؟'] + questions
    if 'budget_unknown' in missing:
        questions = ['ما هي الميزانية المتاحة تقريباً لهذا النوع من الحلول؟'] + questions
    return questions[:4]


def _do_not_do(objection: str, stage: str, risk_flags: list[str]) -> list[str]:
    base = list(FORBIDDEN_COMMITMENTS)
    if 'no_final_price_without_scope' in risk_flags:
        base.append('commit_final_price_before_scope')
    if objection == 'legal':
        base.append('accept_custom_legal_terms_without_review')
    if stage in ('cold', 'aware'):
        base.append('send_full_proposal_before_discovery')
    return base


def build_strategy(
    account: str = 'Demo Account',
    sector: str = 'Real Estate',
    message: str = 'كم السعر؟',
) -> dict[str, Any]:
    intel = dci.classify(message)
    intent = intel['intent']
    stage = intel['deal_stage']
    sentiment = intel['sentiment']
    urgency = intel['urgency']
    objection = intel['objection_type']
    missing = intel['missing_info']
    risk_flags = intel['risk_flags']
    offered = intel['suggested_offer']

    score = _score_deal(stage, sentiment, urgency, objection, missing)
    band = _close_probability_band(score)
    discount = _discount_policy(stage, score)
    negotiation = _negotiation_position(stage, objection, score)
    proof = _proof_to_show(stage, sector, objection)
    questions = _must_ask_questions(intent, stage, missing)
    do_not = _do_not_do(objection, stage, risk_flags)

    offer_detail = OFFER_LADDER.get(offered, OFFER_LADDER['free_diagnostic'])
    pricing_range = offer_detail['price']

    approval_gates = []
    if intel['approval_required']:
        approval_gates.append('external_send_requires_approval')
    if discount['discount_requires_approval']:
        approval_gates.append('discount_requires_founder_approval')
    if stage in ('proposal', 'negotiation', 'procurement'):
        approval_gates.append('proposal_send_requires_review')

    return {
        'account': account,
        'sector': sector,
        'message': message,
        'conversation_intel': intel,
        'deal_score': score,
        'close_probability_band': band,
        'best_offer': offered,
        'pricing_range': pricing_range,
        'recommended_discount_policy': discount,
        'negotiation_position': negotiation,
        'must_ask_questions': questions,
        'next_best_action': intel['next_best_action'],
        'do_not_do': do_not,
        'approval_gates': approval_gates,
        'proof_to_show': proof,
        'live_sends': 0,
        'final_commitments': 0,
    }


def build_payload() -> dict[str, Any]:
    demo_cases = [
        ('Alpha Trading', 'Retail', 'كم السعر؟'),
        ('Beta Logistics', 'Logistics', 'ارسل العرض'),
        ('Gamma Real Estate', 'Real Estate', 'ما نحتاج'),
        ('Delta Healthcare', 'Healthcare', 'we need more proof before deciding'),
        ('Epsilon Tech', 'Technology', 'can you give us a discount?'),
    ]
    strategies = [build_strategy(a, s, m) for a, s, m in demo_cases]
    summary = {
        'strategies_built': len(strategies),
        'live_sends': 0,
        'final_commitments': 0,
        'probability_bands': [s['close_probability_band'] for s in strategies],
        'offers_suggested': [s['best_offer'] for s in strategies],
    }
    return {
        'summary': summary,
        'strategies': strategies,
    }


def write_reports(payload: dict[str, Any]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / 'latest.json').write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')
    lines = ['# Deal Strategy Brain', '']
    for key, value in payload['summary'].items():
        lines.append(f'- {key}: `{value}`')
    lines.append('\n## Strategies')
    for s in payload['strategies']:
        lines.append(
            f"- {s['account']} [{s['close_probability_band']}] → {s['next_best_action']}"
        )
    (REPORT_DIR / 'latest.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def verify(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload['summary']['live_sends'] != 0:
        errors.append('live_sends must be zero')
    if payload['summary']['final_commitments'] != 0:
        errors.append('final_commitments must be zero')
    for s in payload['strategies']:
        if s['close_probability_band'] not in CLOSE_PROBABILITY_BANDS:
            errors.append(f"invalid probability band: {s['close_probability_band']}")
        if not s['must_ask_questions']:
            errors.append(f"missing discovery questions for {s['account']}")
        if not s['next_best_action']:
            errors.append(f"missing next_best_action for {s['account']}")
        if not s['approval_gates'] and s['conversation_intel']['approval_required']:
            errors.append(f"approval_gates empty but required for {s['account']}")
    return errors


def main() -> int:
    payload = build_payload()
    write_reports(payload)
    errors = verify(payload)
    print('DEAL_STRATEGY_READY=' + ('0' if errors else '1'))
    print(payload['summary'])
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
