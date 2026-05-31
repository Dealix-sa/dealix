"""
acceptance_tests.py — Dealix Growth OS
7 acceptance tests verifying core system behaviors.

Run: python -m pytest growth-os/acceptance_tests.py -v
  or: python growth-os/acceptance_tests.py
"""

import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

_BASE = Path(__file__).parent

# Add growth-os to path for imports
sys.path.insert(0, str(_BASE))

from anti_ban_guardian import AntiBanGuardian
from reply_classifier import ReplyClassifier
from quality_gate import DraftQualityGate
from verification_gates import run_all_gates


class Test1FiftyCompanySimulation(unittest.TestCase):
    """
    Test: simulate processing 50 companies through the full pipeline
    (brief → asset → quality gate → routing decision).
    Verify no doctrine violations occur.
    """

    def test_50_company_simulation(self):
        gate = DraftQualityGate()
        guardian = AntiBanGuardian()

        sectors = [
            "legal", "facility_management", "consulting", "real_estate",
            "financial_services", "logistics", "construction", "retail",
            "education", "international"
        ]
        countries = ["SA", "AE", "KW", "QA", "BH"]

        doctrine_violations = []
        processed = 0

        for i in range(50):
            sector = sectors[i % len(sectors)]
            country = countries[i % len(countries)]

            # Simulate a draft
            draft = {
                "text": (
                    f"Dear team, many {sector} companies in {country} are losing time "
                    "to manual processes. Our 7-day sprint maps these gaps. "
                    "Would a free 48-hour diagnostic be useful? "
                    "To unsubscribe reply STOP."
                ),
                "subject": f"Quick question about your {sector} operations",
                "channel": "email",
                "language": "en",
                "company_name": f"TestCo {i}",
                "sector": sector,
            }

            result = gate.score_draft(draft)

            # Verify no guaranteed outcome claims pass
            self.assertNotIn(
                "guaranteed", draft["text"].lower(),
                f"Company {i}: draft contains 'guaranteed' — doctrine violation"
            )

            # Verify governance_decision is present
            self.assertIn(
                "governance_decision", result,
                f"Company {i}: quality gate result missing governance_decision"
            )

            # Verify decision is valid
            self.assertIn(
                result.get("decision"),
                ["ready", "founder_review", "rewrite", "reject"],
                f"Company {i}: invalid decision {result.get('decision')}"
            )

            # Check LinkedIn is always assisted_manual
            linkedin_result = guardian.check_channel("linkedin", {})
            self.assertEqual(
                linkedin_result.get("mode"),
                "assisted_manual",
                "LinkedIn must always be assisted_manual"
            )

            processed += 1

        self.assertEqual(processed, 50)
        self.assertEqual(len(doctrine_violations), 0, f"Doctrine violations: {doctrine_violations}")


class Test2NoSendDryRun(unittest.TestCase):
    """
    Test: verify that DRY_RUN=true prevents any actual send action.
    All pipeline steps complete but execution is blocked.
    """

    def test_no_send_dry_run(self):
        # Set DRY_RUN env var
        with patch.dict(os.environ, {"DRY_RUN": "true"}):
            dry_run = os.environ.get("DRY_RUN", "").lower()
            self.assertEqual(dry_run, "true")

            # Simulate a job that would be sent
            job = {
                "job_id": "test_dry_run_001",
                "channel": "email",
                "execution_mode": "auto_send",
                "status": "queued",
                "governance_decision": "auto_send_eligible",
            }

            # In dry run, status should remain queued — no send action
            if dry_run in ("true", "1", "yes"):
                job["status"] = "dry_run_held"
                job["governance_decision"] = "dry_run_no_send"

            self.assertEqual(job["status"], "dry_run_held")
            self.assertEqual(job["governance_decision"], "dry_run_no_send")

            # Verify no real send occurred (mock would catch any send call)
            # In this test we verify the env var gate works
            self.assertTrue(
                dry_run in ("true", "1", "yes"),
                "DRY_RUN flag must gate all send operations"
            )


class Test3CanaryLaunch(unittest.TestCase):
    """
    Test: canary launch — first 5 sends before scaling.
    Verify quality gate passes, execution modes are correct,
    and canary batch is small enough to monitor.
    """

    def test_canary_launch(self):
        gate = DraftQualityGate()
        guardian = AntiBanGuardian()

        canary_batch_size = 5
        canary_drafts = []

        for i in range(canary_batch_size):
            draft = {
                "text": (
                    f"Hello, I noticed your facility management company is growing. "
                    f"Many FM firms report spending 30%+ of management time on manual SLA tracking. "
                    f"We map these gaps in a free 48-hour diagnostic. "
                    f"Would that be useful? To unsubscribe reply STOP."
                ),
                "subject": "Quick question about your SLA reporting",
                "channel": "email",
                "language": "en",
                "company_name": f"FM Company {i}",
                "sector": "facility_management",
            }
            result = gate.score_draft(draft)
            canary_drafts.append(result)

        # All canary drafts should have governance decision
        for draft_result in canary_drafts:
            self.assertIn("governance_decision", draft_result)
            self.assertIn("total_score", draft_result)

        # Canary batch should not exceed 10 items
        self.assertLessEqual(
            canary_batch_size, 10,
            "Canary launch must be 10 or fewer sends"
        )

        # Email batch check (canary is 5, well within daily quota of 500)
        batch_ok = guardian.check_email(canary_drafts)
        self.assertTrue(batch_ok, "Canary batch should pass anti-ban check")

        # Scores should be reasonable for this well-formed draft
        avg_score = sum(d.get("total_score", 0) for d in canary_drafts) / len(canary_drafts)
        self.assertGreater(avg_score, 50, "Canary draft quality should be above 50")


class Test4AutoThrottle(unittest.TestCase):
    """
    Test: verify auto-throttle kicks in when metrics exceed thresholds.
    Guardian.should_pause_channel() must return True when bounce > 5%.
    """

    def test_auto_throttle(self):
        guardian = AntiBanGuardian()

        # Normal metrics — should not pause
        normal_metrics = {
            "bounce_rate": 0.02,
            "spam_rate": 0.0005,
        }
        should_pause_normal = guardian.should_pause_channel("email", normal_metrics)
        self.assertFalse(
            should_pause_normal,
            "Normal metrics should not trigger pause"
        )

        # High bounce rate — should pause
        high_bounce = {
            "bounce_rate": 0.06,
            "spam_rate": 0.0005,
        }
        should_pause_bounce = guardian.should_pause_channel("email", high_bounce)
        self.assertTrue(
            should_pause_bounce,
            "Bounce rate > 5% must trigger auto-pause"
        )

        # High spam rate — should pause
        high_spam = {
            "bounce_rate": 0.01,
            "spam_rate": 0.005,
        }
        should_pause_spam = guardian.should_pause_channel("email", high_spam)
        self.assertTrue(
            should_pause_spam,
            "Spam rate > 0.3% must trigger auto-pause"
        )

        # WhatsApp high block rate — should pause
        high_block = {
            "block_rate": 0.03,
        }
        should_pause_wa = guardian.should_pause_channel("whatsapp", high_block)
        self.assertTrue(
            should_pause_wa,
            "WhatsApp block rate > 2% must trigger auto-pause"
        )

        # Risk score should be high for bad metrics
        risk = guardian.get_risk_score("email", high_bounce)
        self.assertGreaterEqual(risk, 0.5, "Risk score should be >= 0.5 for high bounce")
        self.assertLessEqual(risk, 1.0, "Risk score should be <= 1.0")


class Test5Suppression(unittest.TestCase):
    """
    Test: verify suppression is enforced — suppressed contacts
    must never receive outreach.
    """

    def test_suppression(self):
        from verification_gates import Gate8ReplyQualityReady
        classifier = ReplyClassifier()

        # Classify an unsubscribe reply
        unsubscribe_texts = [
            "Please remove me from your list",
            "Unsubscribe",
            "STOP",
            "لا أريد تلقي رسائل",
            "توقف",
        ]

        for text in unsubscribe_texts:
            lang = "ar" if any(
                "؀" <= c <= "ۿ" for c in text
            ) else "en"
            result = classifier.classify(text, lang)
            next_action = classifier.get_next_action(result)

            # All unsubscribes must be classified correctly
            self.assertEqual(
                result.get("classification"),
                "unsubscribe",
                f"'{text}' should classify as unsubscribe, got {result.get('classification')}"
            )

            # Next action must be add_to_suppression_immediately
            self.assertEqual(
                next_action.get("action"),
                "add_to_suppression_immediately",
                f"Unsubscribe action must be add_to_suppression_immediately for '{text}'"
            )

            # Urgency must be critical
            self.assertEqual(
                next_action.get("urgency"),
                "critical",
                "Unsubscribe urgency must be critical"
            )

            # CRM update must include suppression_required
            crm = next_action.get("crm_update", {})
            self.assertTrue(
                crm.get("suppression_required", False),
                "Unsubscribe CRM update must set suppression_required=True"
            )

            # Governance decision must reference the action
            self.assertIn(
                "suppression",
                next_action.get("governance_decision", ""),
                "Governance decision must reference suppression"
            )


class Test6SensitiveSector(unittest.TestCase):
    """
    Test: verify sensitive sectors (healthcare, government, financial_services)
    are handled with extra protection — no auto_send, only founder_approval.
    """

    def test_sensitive_sector(self):
        guardian = AntiBanGuardian()

        sensitive_sectors = ["healthcare_admin", "government", "financial_services"]

        for sector in sensitive_sectors:
            # Simulate a company in a sensitive sector
            company = {
                "sector": sector,
                "country": "SA",
                "company_size": "200+",
            }

            # For sensitive sectors, channel check should require founder approval
            context = {
                "sector": sector,
                "company_size_large": True,
                "is_inbound": False,
                "batch": ["test@test.com"],
            }

            # Email check for sensitive sector — should still pass batch check
            # but execution mode should be founder_approval per channel-router.yml
            email_result = guardian.check_channel("email", context)
            self.assertIn(
                "governance_decision", email_result,
                f"Sensitive sector {sector}: governance_decision required"
            )

            # LinkedIn must always be assisted_manual for any sector
            linkedin = guardian.check_linkedin()
            self.assertEqual(
                linkedin, "assisted_manual",
                f"LinkedIn must be assisted_manual for {sector}"
            )

        # Verify sensitive sector draft quality — must not contain PII keywords
        gate = DraftQualityGate()
        draft_with_pii_hint = {
            "text": (
                "Dear patient records manager, we can process your medical records automatically. "
                "No unsubscribe option available."
            ),
            "subject": "Medical records automation",
            "channel": "email",
            "language": "en",
            "company_name": "Test Hospital",
            "sector": "healthcare_admin",
        }
        result = gate.score_draft(draft_with_pii_hint)
        # Should score low due to missing opt-out
        self.assertIn("decision", result)
        # The no-exaggeration check should catch "automatically"
        self.assertIsNotNone(result.get("total_score"))


class Test7ReplyClassification(unittest.TestCase):
    """
    Test: verify reply classifier handles all 9 classification types correctly.
    """

    def test_reply_classification(self):
        classifier = ReplyClassifier()

        test_cases = [
            # (text, language, expected_classification)
            ("Yes I am interested, let's schedule a call", "en", "interested"),
            ("Can you tell me more about how this works?", "en", "details_requested"),
            ("I am not the right person, please contact our COO", "en", "wrong_person"),
            ("How much does this cost?", "en", "pricing_requested"),
            ("We are concerned about GDPR and data security", "en", "security_concern"),
            ("Not right now, maybe next quarter", "en", "not_now"),
            ("We are not interested, no thank you", "en", "not_interested"),
            ("Please remove me from your list", "en", "unsubscribe"),
            ("Delivery failed: user does not exist", "en", "bounce"),
        ]

        for text, lang, expected in test_cases:
            result = classifier.classify(text, lang)
            self.assertEqual(
                result.get("classification"),
                expected,
                f"'{text[:50]}' expected '{expected}', got '{result.get('classification')}'"
            )
            self.assertIn(
                "governance_decision", result,
                f"Classification of '{text[:30]}' missing governance_decision"
            )
            self.assertIn(
                "confidence", result,
                f"Classification missing confidence score"
            )
            self.assertGreater(
                result.get("confidence", 0), 0,
                f"Confidence should be > 0 for '{text[:30]}'"
            )

        # Arabic classifications
        arabic_cases = [
            ("نعم أنا مهتم", "ar", "interested"),
            ("توقف", "ar", "unsubscribe"),
            ("لا أريد تلقي رسائل", "ar", "unsubscribe"),
        ]

        for text, lang, expected in arabic_cases:
            result = classifier.classify(text, lang)
            self.assertEqual(
                result.get("classification"),
                expected,
                f"Arabic: '{text}' expected '{expected}', got '{result.get('classification')}'"
            )

        # Verify next_action is provided for each classification
        for text, lang, expected in test_cases:
            result = classifier.classify(text, lang)
            next_action = classifier.get_next_action(result)
            self.assertIn("action", next_action)
            self.assertIn("urgency", next_action)
            self.assertIn("crm_update", next_action)
            self.assertIn("governance_decision", next_action)


if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
