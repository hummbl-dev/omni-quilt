"""Core attention evaluation, storyboard quilting, and vision budget engine."""

from __future__ import annotations

import json
import math
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# Hook archetype regex patterns
PATTERNS = {
    "proof_led": re.compile(
        r"\b(\$?\d+[\d,]*(\.\d+)?(%|k|m|b|x)?|\d+\s*(tests|outages|lines|nodes|ms|sec|hours|days|repos|vms))\b|"
        r"\b(analyzed|measured|receipts|benchmark|verified|terminal log|postmortem|diff|production)\b",
        re.IGNORECASE,
    ),
    "counter_intuitive": re.compile(
        r"\b(stop\s+\w+ing|unpopular opinion|backwards|never\s+use|ruining|opposite|myth|contrary|worst advice)\b",
        re.IGNORECASE,
    ),
    "loss_aversion": re.compile(
        r"\b(mistake|waste|losing|leaking|danger|risk|killed|destroy|costing you|failing|broken)\b",
        re.IGNORECASE,
    ),
    "open_loop": re.compile(
        r"\b(here is what happened|nobody is talking about|secret|what happened next|wasn't what|real reason)\b",
        re.IGNORECASE,
    ),
    "romo": re.compile(
        r"\b(you don't need|permission to|ignore|stop chasing|simplify|instead of|anti-hustle)\b",
        re.IGNORECASE,
    ),
    "slop_fluff": re.compile(
        r"\b(in today's fast-paced world|game-changer|revolutionize|supercharge|delve into|testament|"
        r"tapestry|synergy|seamlessly|unleash|empower|welcome back to my channel|hey guys)\b",
        re.IGNORECASE,
    ),
}


@dataclass
class PerspectiveEvaluation:
    name: str
    dimension: str
    score: int  # 0 to 100
    position: str
    findings: List[str] = field(default_factory=list)
    actionable_remedy: str = ""


@dataclass
class ToolAction:
    tool: str
    command_or_spec: str
    intent: str


@dataclass
class VisionBudget:
    width: int
    height: int
    num_tiles: int
    gemini_tokens: int
    openai_tokens: int
    claude_tokens: int


@dataclass
class QuiltReport:
    headline_hook: str
    primary_archetype: str
    thumb_stop_score: int
    proof_integrity_score: int
    slop_penalty: int
    perspectives: List[PerspectiveEvaluation] = field(default_factory=list)
    tool_actions: List[ToolAction] = field(default_factory=list)
    vision_budget: Optional[VisionBudget] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def calculate_vision_budget(width: int, height: int, num_frames: int = 1) -> VisionBudget:
    """Calculate token costs across frontier vision model tokenizers."""
    # Gemini: 258 tokens per 768x768 tile + base tokens
    gemini_tiles_w = math.ceil(width / 768)
    gemini_tiles_h = math.ceil(height / 768)
    gemini_tiles = max(1, gemini_tiles_w * gemini_tiles_h) * num_frames
    gemini_tokens = gemini_tiles * 258

    # OpenAI: 85 tokens per 512x512 tile + 85 base
    openai_tiles_w = math.ceil(width / 512)
    openai_tiles_h = math.ceil(height / 512)
    openai_tiles = max(1, openai_tiles_w * openai_tiles_h) * num_frames
    openai_tokens = (openai_tiles * 170) + 85

    # Claude: approx 1600 tokens per 1000x1000 image
    claude_tokens = int((width * height / 750) * num_frames)

    return VisionBudget(
        width=width,
        height=height,
        num_tiles=gemini_tiles,
        gemini_tokens=gemini_tokens,
        openai_tokens=openai_tokens,
        claude_tokens=claude_tokens,
    )


def detect_archetype(text: str) -> Tuple[str, int]:
    """Detect dominant psychological hook archetype."""
    scores = {}
    for key in ["proof_led", "counter_intuitive", "loss_aversion", "open_loop", "romo"]:
        matches = len(PATTERNS[key].findall(text))
        scores[key] = matches

    best_key = max(scores, key=lambda k: scores[k])
    best_count = scores[best_key]

    name_map = {
        "proof_led": "Proof Led",
        "counter_intuitive": "Counter Intuitive",
        "loss_aversion": "Loss Aversion",
        "open_loop": "Open Loop",
        "romo": "ROMO (Relief from FOMO)",
    }
    return (name_map[best_key] if best_count > 0 else "Unstructured / Neutral"), best_count


def audit_attention(
    content: str,
    media_type: str = "short-form-video",
    resolution: Tuple[int, int] = (1080, 1920),
) -> QuiltReport:
    """Run Parallax Quilt attention analysis on input content."""
    lines = [l.strip() for l in content.splitlines() if l.strip()]
    first_3_seconds = " ".join(lines[:2]) if lines else content

    archetype, count = detect_archetype(first_3_seconds)
    slop_matches = PATTERNS["slop_fluff"].findall(content)
    slop_penalty = min(len(slop_matches) * 20, 60)

    # 1. Perspective: Audience Thumb-Stop
    base_thumb = 45
    if count > 0:
        base_thumb += 25
    if len(first_3_seconds.split()) <= 15:
        base_thumb += 15
    thumb_score = max(0, min(100, base_thumb - slop_penalty))

    p1 = PerspectiveEvaluation(
        name="Audience / Consumer",
        dimension="Thumb-Stop Sensory Hook (0-3s)",
        score=thumb_score,
        position="Engaged" if thumb_score >= 70 else ("Bored / Scrolled" if thumb_score < 40 else "Neutral"),
        findings=[
            f"Archetype identified: {archetype} ({count} signal matches).",
            f"Opening length: {len(first_3_seconds.split())} words in first 2 beats.",
        ],
        actionable_remedy=(
            "Keep first sentence strictly under 12 words with a sharp sensory or quantitative trigger."
            if thumb_score < 70
            else "Maintain immediate visual cut within 1.5 seconds."
        ),
    )

    # 2. Perspective: Technical Systems & Multimodal Tool Calling
    tool_actions: List[ToolAction] = []
    if "video" in media_type:
        tool_actions.append(
            ToolAction(
                tool="ffmpeg",
                command_or_spec="ffmpeg -ss 00:00:00 -to 00:00:03 -i input.mp4 -vf 'crop=ih*9/16:ih' -c:v libx264 hook.mp4",
                intent="Isolate exact 3-second vertical hook crop without letterboxing.",
            )
        )
        tool_actions.append(
            ToolAction(
                tool="subtitles",
                command_or_spec="auto-subs --highlight-current-word --font Montserrat-Black --color '#FACC15'",
                intent="High-contrast kinetic yellow captions in upper-middle viewport safe zone.",
            )
        )
    p2 = PerspectiveEvaluation(
        name="Technical Systems Architect",
        dimension="Multimodal Formatting & Execution Bounds",
        score=85,
        position="Feasible",
        findings=[
            f"Target container: {media_type} ({resolution[0]}x{resolution[1]}).",
            f"Tool pipeline generated {len(tool_actions)} automated media transforms.",
        ],
        actionable_remedy="Render kinetic captions strictly above lower 25% UI elements.",
    )

    # 3. Perspective: Proof & Epistemic Integrity
    proof_matches = len(PATTERNS["proof_led"].findall(content))
    proof_score = max(0, min(100, (proof_matches * 25) + (20 if not slop_matches else 0) - slop_penalty))
    p3 = PerspectiveEvaluation(
        name="Auditor & Trust Governance",
        dimension="Empirical Grounding vs Slop Detection",
        score=proof_score,
        position="Verified" if proof_score >= 60 else "Unsubstantiated",
        findings=[
            f"Concrete verification signals found: {proof_matches}.",
            f"AI slop markers detected: {len(slop_matches)}.",
        ],
        actionable_remedy=(
            "Replace vague superlatives with empirical measurements, diff lines, or reproducible links."
            if proof_score < 60
            else "Receipt integrity verified."
        ),
    )

    # 4. Perspective: Growth & Algorithmic Fit
    growth_score = int((thumb_score * 0.6) + (proof_score * 0.4))
    p4 = PerspectiveEvaluation(
        name="Growth & Algorithmic Optimization",
        dimension="Loop Completion & Retention Curve",
        score=growth_score,
        position="Viral Contender" if growth_score >= 70 else "Flatline Risk",
        findings=[
            f"Blended engagement potential: {growth_score}/100.",
            "Algorithm reward vector: completion rate and re-watch probability.",
        ],
        actionable_remedy="Add an open curiosity loop in beat 1 that resolves in the final 2 seconds.",
    )

    budget = calculate_vision_budget(resolution[0], resolution[1])

    return QuiltReport(
        headline_hook=first_3_seconds,
        primary_archetype=archetype,
        thumb_stop_score=thumb_score,
        proof_integrity_score=proof_score,
        slop_penalty=slop_penalty,
        perspectives=[p1, p2, p3, p4],
        tool_actions=tool_actions,
        vision_budget=budget,
    )


def format_markdown_quilt(report: QuiltReport) -> str:
    """Format QuiltReport into clean Markdown report."""
    md = [
        "# Parallax Quilt Review — Multimodal Attention Audit",
        "",
        f"**Headline Hook**: *\"{report.headline_hook}\"*",
        f"**Primary Archetype**: `{report.primary_archetype}` | **Slop Penalty**: `-{report.slop_penalty}`",
        f"**Thumb-Stop Score**: `{report.thumb_stop_score}/100` | **Proof Integrity**: `{report.proof_integrity_score}/100`",
        "",
        "## 4-Dimensional Quilt Perspectives",
        "",
        "| Perspective | Dimension | Score | Stance | Priority Remedy |",
        "|---|---|---|---|---|",
    ]

    for p in report.perspectives:
        md.append(f"| **{p.name}** | {p.dimension} | `{p.score}/100` | `{p.position}` | {p.actionable_remedy} |")

    if report.tool_actions:
        md.extend([
            "",
            "## Automated Tool Actions",
            "",
            "| Tool | Intent | Command / Spec |",
            "|---|---|---|",
        ])
        for t in report.tool_actions:
            md.append(f"| `{t.tool}` | {t.intent} | `{t.command_or_spec}` |")

    if report.vision_budget:
        b = report.vision_budget
        md.extend([
            "",
            "## Vision Token Budget Estimates",
            "",
            f"- Resolution: `{b.width}x{b.height}`",
            f"- Gemini 1.5/2.0 Vision: **{b.gemini_tokens} tokens** ({b.num_tiles} tiles @ 258)",
            f"- OpenAI GPT-4o: **{b.openai_tokens} tokens**",
            f"- Anthropic Claude 3.5: **~{b.claude_tokens} tokens**",
        ])

    return "\n".join(md)
