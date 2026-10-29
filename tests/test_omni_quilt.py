"""Unit tests for omni-quilt."""

import unittest
from omni_quilt.engine import audit_attention, calculate_vision_budget, detect_archetype, format_markdown_quilt


class TestOmniQuilt(unittest.TestCase):
    def test_detect_archetype_proof_led(self):
        text = "Here is the terminal log that fixed 42 failed tests in 0.5s."
        archetype, count = detect_archetype(text)
        self.assertEqual(archetype, "Proof Led")
        self.assertGreater(count, 0)

    def test_detect_archetype_counter_intuitive(self):
        text = "Unpopular opinion: stop optimizing your code for performance."
        archetype, count = detect_archetype(text)
        self.assertEqual(archetype, "Counter Intuitive")
        self.assertGreater(count, 0)

    def test_slop_penalty_applied(self):
        clean_text = "42 tests verified in production postmortem with zero downtime."
        sloppy_text = "Hey guys, welcome back to my channel! In today's fast-paced world, this game-changer will revolutionize and seamlessly unleash synergy."

        clean_report = audit_attention(clean_text)
        sloppy_report = audit_attention(sloppy_text)

        self.assertEqual(clean_report.slop_penalty, 0)
        self.assertGreater(sloppy_report.slop_penalty, 0)
        self.assertGreater(clean_report.thumb_stop_score, sloppy_report.thumb_stop_score)
        self.assertGreater(clean_report.proof_integrity_score, sloppy_report.proof_integrity_score)

    def test_tool_actions_generated_for_video(self):
        report = audit_attention("Stop deploying to production without this 5-second check.", media_type="short-form-video")
        tool_names = [t.tool for t in report.tool_actions]
        self.assertIn("ffmpeg", tool_names)
        self.assertIn("subtitles", tool_names)

    def test_format_markdown_quilt(self):
        report = audit_attention("Analyzed 1,200 production outages: 2 bugs caused 80% of downtime.")
        md = format_markdown_quilt(report)
        self.assertIn("# Parallax Quilt Review", md)
        self.assertIn("Audience / Consumer", md)
        self.assertIn("Technical Systems Architect", md)
        self.assertIn("Auditor & Trust Governance", md)
        self.assertIn("Growth & Algorithmic Optimization", md)

    def test_vision_budget_calculation(self):
        # 1080x1920 portrait:
        # width 1080 / 768 = 2 tiles; height 1920 / 768 = 3 tiles -> 6 tiles
        budget = calculate_vision_budget(1080, 1920, num_frames=1)
        self.assertEqual(budget.num_tiles, 6)
        self.assertEqual(budget.gemini_tokens, 6 * 258)
        self.assertGreater(budget.openai_tokens, 0)
        self.assertGreater(budget.claude_tokens, 0)


if __name__ == "__main__":
    unittest.main()
