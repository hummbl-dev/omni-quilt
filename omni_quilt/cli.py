"""CLI interface for omni-quilt."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from omni_quilt import __version__
from omni_quilt.engine import audit_attention, calculate_vision_budget, format_markdown_quilt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="omni-quilt",
        description="Visual multi-modal attention and storyboard generator for omni-modal LLMs.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: audit
    audit_p = subparsers.add_parser("audit", help="Evaluate text, script, or storyboard attention score")
    audit_p.add_argument("input", help="Text string or path to markdown/txt file")
    audit_p.add_argument("--type", default="short-form-video", choices=["short-form-video", "x-thread", "blog", "carousel"])
    audit_p.add_argument("--width", type=int, default=1080)
    audit_p.add_argument("--height", type=int, default=1920)
    audit_p.add_argument("--json", action="store_true", help="Output raw JSON")

    # Subcommand: budget
    budget_p = subparsers.add_parser("budget", help="Calculate vision token budget for image/video resolutions")
    budget_p.add_argument("--width", type=int, required=True, help="Image or video width in pixels")
    budget_p.add_argument("--height", type=int, required=True, help="Image or video height in pixels")
    budget_p.add_argument("--frames", type=int, default=1, help="Number of frames (default: 1)")
    budget_p.add_argument("--json", action="store_true", help="Output JSON")

    args = parser.parse_args(argv)

    if args.command == "audit":
        content = args.input
        path_candidate = Path(args.input)
        if path_candidate.is_file():
            content = path_candidate.read_text(encoding="utf-8")

        report = audit_attention(
            content=content,
            media_type=args.type,
            resolution=(args.width, args.height),
        )

        if args.json:
            print(json.dumps(report.to_dict(), indent=2))
        else:
            print(format_markdown_quilt(report))
        return 0

    elif args.command == "budget":
        budget = calculate_vision_budget(args.width, args.height, args.frames)
        if args.json:
            print(json.dumps(budget.__dict__, indent=2))
        else:
            print(f"Vision Token Budget for {args.width}x{args.height} ({args.frames} frame{'s' if args.frames > 1 else ''}):")
            print(f"  * Gemini Vision:    {budget.gemini_tokens} tokens ({budget.num_tiles} tiles @ 258 tok)")
            print(f"  * OpenAI GPT-4o:    {budget.openai_tokens} tokens")
            print(f"  * Anthropic Claude: ~{budget.claude_tokens} tokens")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
