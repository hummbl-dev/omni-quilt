# omni-quilt

> Visual multi-modal attention and storyboard generator for omni-modal LLMs (Gemini, GPT-4o, Claude 3.5).

[![CI](https://github.com/hummbl-dev/omni-quilt/actions/workflows/ci.yml/badge.svg)](https://github.com/hummbl-dev/omni-quilt/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

`omni-quilt` is a fast, zero-dependency library and CLI that audits and stitches video clips, storyboards, and technical content drafts into multi-dimensional attention quilts.

It bridges the gap between raw video/media assets and the native multimodal input interfaces of frontier vision models.

---

## 4-Dimensional Parallax Quilt Dimensions

Every draft is audited across four adversarial stakeholder positions:

1. **Audience / Consumer**: Thumb-stop score in first 0–3 seconds, opening word velocity, curiosity gap.
2. **Technical Systems Architect**: Viewport safe zones, automated FFmpeg transforms, kinetic captions.
3. **Auditor & Trust Governance**: Quantitative verification vs AI slop/buzzword penalty.
4. **Growth & Algorithmic Optimization**: Completion rates, retention curve, and viral loop design.

---

## Installation

```bash
pip install git+https://github.com/hummbl-dev/omni-quilt.git
```

Or run directly:
```bash
python -m omni_quilt.cli --help
```

---

## Quickstart

### 1. Audit Text or Video Storyboard
```bash
omni-quilt audit "Analyzed 1,200 production outages: 2 bugs caused 80% of downtime."
```

Output:
```markdown
# Parallax Quilt Review — Multimodal Attention Audit

**Headline Hook**: *"Analyzed 1,200 production outages: 2 bugs caused 80% of downtime."*
**Primary Archetype**: `Proof Led` | **Slop Penalty**: `-0`
**Thumb-Stop Score**: `85/100` | **Proof Integrity**: `70/100`

## 4-Dimensional Quilt Perspectives

| Perspective | Dimension | Score | Stance | Priority Remedy |
|---|---|---|---|---|
| **Audience / Consumer** | Thumb-Stop Sensory Hook (0-3s) | `85/100` | `Engaged` | Maintain immediate visual cut within 1.5 seconds. |
| **Technical Systems Architect** | Multimodal Formatting & Execution Bounds | `85/100` | `Feasible` | Render kinetic captions strictly above lower 25% UI elements. |
| **Auditor & Trust Governance** | Empirical Grounding vs Slop Detection | `70/100` | `Verified` | Receipt integrity verified. |
| **Growth & Algorithmic Optimization** | Loop Completion & Retention Curve | `79/100` | `Viral Contender` | Add an open curiosity loop in beat 1 that resolves in the final 2 seconds. |
```

### 2. Calculate Vision Token Budgets
Calculate patch tokenization costs before feeding high-res images or video frames to vision models:

```bash
omni-quilt budget --width 1080 --height 1920 --frames 5
```

Output:
```text
Vision Token Budget for 1080x1920 (5 frames):
  * Gemini Vision:    7740 tokens (30 tiles @ 258 tok)
  * OpenAI GPT-4o:    2635 tokens
  * Anthropic Claude: ~13824 tokens
```

---

## Python API

```python
from omni_quilt import audit_attention, calculate_vision_budget, format_markdown_quilt

report = audit_attention("Stop deploying to production without this 5-second check.", media_type="short-form-video")
print(format_markdown_quilt(report))

budget = calculate_vision_budget(1920, 1080, num_frames=1)
print(f"Gemini tokens: {budget.gemini_tokens}")
```

---

## License

Licensed under the [Apache License, Version 2.0](LICENSE).
