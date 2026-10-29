"""omni-quilt: Visual multi-modal attention and storyboard generator for omni-modal LLMs.

Evaluates online content drafts, video storyboards, and multimodal briefs
across 4 distinct Parallax Quilt stakeholder dimensions:
  1. Audience Thumb-Stop (0-3s sensory hook, curiosity gap, drop-off risk)
  2. Technical & Tool Calling (FFmpeg clipping, kinetic captions, safe-zone framing)
  3. Proof-Led Integrity (Empirical receipts vs AI slop detection)
  4. Growth & Algorithmic Fit (Retention curve, share catalyst, platform alignment)
"""

__version__ = "0.1.0"
__all__ = [
    "__version__",
    "audit_attention",
    "detect_archetype",
    "format_markdown_quilt",
    "calculate_vision_budget",
    "QuiltReport",
    "PerspectiveEvaluation",
    "ToolAction",
    "VisionBudget",
]

from omni_quilt.engine import (
    PerspectiveEvaluation,
    QuiltReport,
    ToolAction,
    VisionBudget,
    audit_attention,
    calculate_vision_budget,
    detect_archetype,
    format_markdown_quilt,
)
