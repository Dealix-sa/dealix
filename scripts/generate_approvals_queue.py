#!/usr/bin/env python3
"""Generate founder approvals queue (/decisions.html)."""

import json
from datetime import datetime
from pathlib import Path

def generate_approvals_html() -> str:
    """Generate HTML approvals queue for founder review."""
    html = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dealix Founder Approvals Queue</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f7fa; color: #1a1a1a; padding: 20px; }
        .container { max-width: 1000px; margin: 0 auto; }
        h1 { font-size: 2em; margin-bottom: 10px; color: #0066cc; }
        .subtitle { color: #666; margin-bottom: 30px; }
        .queue-item { background: white; border-left: 4px solid #ff9800; padding: 20px; margin-bottom: 15px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .queue-item.approved { border-left-color: #4caf50; background: #f1f8e9; }
        .queue-item.rejected { border-left-color: #f44336; background: #ffebee; }
        .item-type { display: inline-block; padding: 4px 8px; border-radius: 3px; font-size: 0.75em; font-weight: bold; margin-bottom: 10px; }
        .type-outreach { background: #e3f2fd; color: #0066cc; }
        .type-diagnostic { background: #fff3e0; color: #ff9800; }
        .type-followup { background: #e8f5e9; color: #4caf50; }
        .item-title { font-size: 1.2em; font-weight: bold; margin-bottom: 10px; }
        .item-content { background: #f8f9fa; padding: 15px; border-radius: 3px; margin: 10px 0; font-family: 'Courier New', monospace; white-space: pre-wrap; word-wrap: break-word; }
        .item-meta { color: #999; font-size: 0.85em; margin-top: 10px; }
        .button-group { margin-top: 15px; }
        .button { padding: 8px 16px; margin-right: 10px; border: none; border-radius: 3px; cursor: pointer; font-size: 0.9em; }
        .btn-approve { background: #4caf50; color: white; }
        .btn-approve:hover { background: #45a049; }
        .btn-reject { background: #f44336; color: white; }
        .btn-reject:hover { background: #da190b; }
        .btn-edit { background: #2196F3; color: white; }
        .btn-edit:hover { background: #0b7dda; }
        .status-badge { display: inline-block; padding: 4px 8px; border-radius: 3px; font-size: 0.75em; font-weight: bold; }
        .status-pending { background: #fff3e0; color: #ff9800; }
        .status-approved { background: #e8f5e9; color: #4caf50; }
        .status-rejected { background: #ffebee; color: #f44336; }
        .footer { text-align: center; color: #999; margin-top: 40px; font-size: 0.85em; }
        .empty { text-align: center; color: #999; padding: 40px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Founder Approvals Queue</h1>
        <div class="subtitle">Items waiting for your review and approval</div>

        <div style="margin-bottom: 20px;">
            <strong>Queue Status:</strong> 3 pending | 0 approved | 0 rejected
        </div>

        <!-- Sample Approval Items (in production, these come from AI agents) -->

        <div class="queue-item">
            <span class="item-type type-outreach">OUTREACH</span>
            <span class="status-badge status-pending">PENDING</span>
            <div class="item-title">WhatsApp to محمد (عقارات الحمد) — Objection Handling</div>
            <div class="item-meta">AI Agent: Sales Objection Handler | Created: 2026-06-17 09:30</div>
            <div class="item-content">السلام عليكم محمد 👋

شكراً لك على الوقت امس; فهمت إن القلق على الـ implementation بدون رقم فريقك

الحقيقة نحنا نشتغل بدون فريقك الأول
نحمل عملاءك بدايةً، نشتغل معهم يومياً
بعدين; بعد 14 يوم, تعرف الفريق إن العملاء مين اللي محتاج متابعة

ودك نبدأ الجمعة بـ499 ريال?</div>
            <div class="button-group">
                <button class="button btn-approve">✓ Approve & Send</button>
                <button class="button btn-edit">✏️ Edit</button>
                <button class="button btn-reject">✗ Reject</button>
            </div>
        </div>

        <div class="queue-item">
            <span class="item-type type-diagnostic">DIAGNOSTIC SUMMARY</span>
            <span class="status-badge status-pending">PENDING</span>
            <div class="item-title">Auto-generated Diagnostic Summary: سارة (SaaS رياض)</div>
            <div class="item-meta">AI Agent: Intake Engine | Created: 2026-06-17 08:15</div>
            <div class="item-content">Diagnostic Summary - Ready to Send

Company: SaaS رياض
Founder: سارة
Current Pain: "We're losing 30% of deals because sales doesn't follow up"

Key Insight:
سارة تبحث عن نظام يوقف الفرص المنسية
Proof: في 14 يوم, سنرفع الـ follow-up rate من 40% إلى 80%+

Next Step:
اتفقنا على pilot 499 SAR, الجمعة 9 AM
ستبدأ مع البيانات الحالية، نشتغل 14 يوم

Approval Needed:
هل الـ summary صحيح? أضف تفاصيل إن لزم الأمر</div>
            <div class="button-group">
                <button class="button btn-approve">✓ Approve</button>
                <button class="button btn-edit">✏️ Edit</button>
                <button class="button btn-reject">✗ Reject</button>
            </div>
        </div>

        <div class="queue-item">
            <span class="item-type type-followup">FOLLOW-UP REMINDER</span>
            <span class="status-badge status-pending">PENDING</span>
            <div class="item-title">Day 3 Follow-up: محمد (عقارات الحمد) — Pilot in Progress</div>
            <div class="item-meta">Scheduled: 2026-06-20 08:00 | AI Agent: Customer Success Orchestrator</div>
            <div class="item-content">Follow-up WhatsApp — Day 3 of Pilot

Send to: محمد, عقارات الحمد

السلام عليكم محمد 👋

يوم 3 من التجربة; كيف الحال?
عندك فيه 2-3 دقايق لتفقد أول عميل ادخلناه في النظام?

(الرابط تحت لتشف اللوحة بنفسك)
https://dealix.app/pilot/...

أي أسئلة أو مشاكل?</div>
            <div class="button-group">
                <button class="button btn-approve">✓ Schedule for Friday</button>
                <button class="button btn-edit">✏️ Adjust Time</button>
                <button class="button btn-reject">✗ Cancel</button>
            </div>
        </div>

        <div class="empty" style="display: none;">
            <p>🎉 No pending approvals! You're all caught up.</p>
        </div>

        <div class="footer">
            <p>Approvals Queue — Items created by AI agents, awaiting founder review</p>
            <p>Refresh every 30 minutes for new items</p>
        </div>
    </div>
    <script>
        // In production, this would:
        // 1. Fetch from Redis queue
        // 2. Show/hide items based on approval status
        // 3. Send approval back to system
        // 4. Log decision for analytics
    </script>
</body>
</html>
"""
    return html

def main():
    """Generate and save approvals queue."""
    html = generate_approvals_html()

    output_path = Path(__file__).parents[1] / "company" / "runtime" / "decisions.html"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Approvals queue generated: {output_path}")
    print("Items ready for founder review (3 pending, 0 approved, 0 rejected)")

    return 0

if __name__ == '__main__':
    exit(main())
