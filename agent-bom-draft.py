#!/usr/bin/env python3
"""
Forkable Factory – Week 7: Agent BOM Draft

Given a product spec, ask Claude to generate a bill of materials.
Then compare the agent-generated BOM against the human-crafted one.

Usage:
    python agent-bom-draft.py [--compare]

    Without --compare: generates BOM from spec, saves to agent-bom.yaml
    With --compare:    also loads bom.yaml and prints a comparison report

Requires: ANTHROPIC_API_KEY environment variable
"""

import os
import sys
import json
import yaml
from pathlib import Path
from datetime import date

try:
    import anthropic
except ImportError:
    print("Error: pip install anthropic")
    sys.exit(1)

SCRIPT_DIR = Path(__file__).parent
SPEC_PATH = SCRIPT_DIR / "spec.md"
SCHEMA_PATH = SCRIPT_DIR / "bom-schema.yaml"
HUMAN_BOM_PATH = SCRIPT_DIR / "bom.yaml"
OUTPUT_PATH = SCRIPT_DIR / "agent-bom.yaml"
REPORT_PATH = SCRIPT_DIR / "agent-bom-comparison.md"


def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def generate_bom(spec: str, schema: str) -> str:
    """Ask Claude to generate a BOM from the product spec."""
    client = anthropic.Anthropic()

    prompt = f"""You are a product engineer creating a bill of materials (BOM) for a new consumer electronics product.

You have been given:
1. A product specification (spec.md)
2. A BOM schema (bom-schema.yaml) that defines the output format

Your task: Generate a complete BOM in YAML format that follows the schema.

Rules:
- Include EVERY component needed to build and ship this product
- Group components into logical assemblies
- Estimate realistic unit costs at the MOQ specified in the spec
- Identify real supplier types (manufacturer, distributor, contract manufacturer)
- List applicable compliance requirements per component
- Suggest alternatives where relevant
- Include fasteners, packaging, labels, and documentation — not just the "interesting" parts
- Be specific about materials, dimensions, and electrical specs
- Output valid YAML only — no markdown fences, no commentary before or after

PRODUCT SPECIFICATION:
{spec}

BOM SCHEMA:
{schema}

Generate the BOM now. Output YAML only."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text


def parse_bom_yaml(text: str) -> dict:
    """Parse YAML from agent output, handling potential markdown fences."""
    # Strip markdown code fences if present
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        # Remove first line (```yaml) and last line (```)
        lines = [l for l in lines[1:] if not l.strip() == "```"]
        cleaned = "\n".join(lines)
    return yaml.safe_load(cleaned)


def extract_components(bom: dict) -> dict:
    """Extract a flat dict of component_id → component from a BOM."""
    components = {}
    for assembly in bom.get("assemblies", []):
        for comp in assembly.get("components", []):
            components[comp["id"]] = comp
    return components


def compare_boms(human_bom: dict, agent_bom: dict) -> str:
    """Compare human-crafted and agent-generated BOMs, return markdown report."""
    human_comps = extract_components(human_bom)
    agent_comps = extract_components(agent_bom)

    human_ids = set(human_comps.keys())
    agent_ids = set(agent_comps.keys())

    # Matching, missing, extra
    matched = human_ids & agent_ids
    missing_from_agent = human_ids - agent_ids
    extra_in_agent = agent_ids - human_ids

    lines = []
    lines.append("# Agent BOM Draft — Comparison Report")
    lines.append(f"\n**Date:** {date.today()}")
    lines.append(f"**Human BOM components:** {len(human_ids)}")
    lines.append(f"**Agent BOM components:** {len(agent_ids)}")
    lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append(f"| Metric | Count |")
    lines.append(f"|---|---|")
    lines.append(f"| Matched (same ID) | {len(matched)} |")
    lines.append(f"| Missing from agent | {len(missing_from_agent)} |")
    lines.append(f"| Extra in agent | {len(extra_in_agent)} |")
    lines.append("")

    # Cost comparison
    human_total = sum(
        c.get("unit_cost", 0) * c.get("quantity", 1) for c in human_comps.values()
    )
    agent_total = sum(
        c.get("unit_cost", 0) * c.get("quantity", 1) for c in agent_comps.values()
    )
    lines.append("## Cost Comparison")
    lines.append("")
    lines.append(f"| | Human BOM | Agent BOM | Delta |")
    lines.append(f"|---|---|---|---|")
    lines.append(
        f"| Total COGS | €{human_total:.2f} | €{agent_total:.2f} | €{agent_total - human_total:+.2f} |"
    )
    lines.append("")

    # Matched components — cost deltas
    if matched:
        lines.append("## Matched Components — Cost Comparison")
        lines.append("")
        lines.append("| ID | Name | Human Cost | Agent Cost | Delta |")
        lines.append("|---|---|---|---|---|")
        for cid in sorted(matched):
            h = human_comps[cid]
            a = agent_comps[cid]
            h_cost = h.get("unit_cost", 0) * h.get("quantity", 1)
            a_cost = a.get("unit_cost", 0) * a.get("quantity", 1)
            delta = a_cost - h_cost
            name = h.get("name", a.get("name", "?"))
            lines.append(
                f"| {cid} | {name} | €{h_cost:.2f} | €{a_cost:.2f} | €{delta:+.2f} |"
            )
        lines.append("")

    # Missing from agent
    if missing_from_agent:
        lines.append("## Missing from Agent BOM")
        lines.append("")
        lines.append(
            "*Components in the human BOM that the agent did not generate.*"
        )
        lines.append("")
        lines.append("| ID | Name | Category | Cost |")
        lines.append("|---|---|---|---|")
        for cid in sorted(missing_from_agent):
            c = human_comps[cid]
            cost = c.get("unit_cost", 0) * c.get("quantity", 1)
            lines.append(
                f"| {cid} | {c.get('name', '?')} | {c.get('category', '?')} | €{cost:.2f} |"
            )
        lines.append("")

    # Extra in agent
    if extra_in_agent:
        lines.append("## Extra in Agent BOM")
        lines.append("")
        lines.append(
            "*Components the agent added that are not in the human BOM.*"
        )
        lines.append("")
        lines.append("| ID | Name | Category | Cost | Notes |")
        lines.append("|---|---|---|---|---|")
        for cid in sorted(extra_in_agent):
            c = agent_comps[cid]
            cost = c.get("unit_cost", 0) * c.get("quantity", 1)
            lines.append(
                f"| {cid} | {c.get('name', '?')} | {c.get('category', '?')} | €{cost:.2f} | {c.get('notes', '')} |"
            )
        lines.append("")

    # Qualitative notes
    lines.append("## Observations")
    lines.append("")
    lines.append(
        "*(Filled in after reviewing the comparison — what did the agent get right, "
        "wrong, and what does it tell us about AI-generated BOMs?)*"
    )
    lines.append("")

    return "\n".join(lines)


def main():
    compare_mode = "--compare" in sys.argv

    # Check API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not set")
        sys.exit(1)

    # Read inputs
    print("Reading spec.md...")
    spec = read_file(SPEC_PATH)

    print("Reading bom-schema.yaml...")
    schema = read_file(SCHEMA_PATH)

    # Generate BOM
    print("Asking Claude to generate a BOM from the spec...")
    print("(This takes 15–30 seconds)")
    raw_output = generate_bom(spec, schema)

    # Parse and validate
    print("Parsing agent output...")
    try:
        agent_bom = parse_bom_yaml(raw_output)
    except yaml.YAMLError as e:
        print(f"Error: Agent output is not valid YAML: {e}")
        print("\n--- Raw output ---")
        print(raw_output)
        # Save raw output for debugging
        OUTPUT_PATH.with_suffix(".raw.txt").write_text(raw_output, encoding="utf-8")
        print(f"\nRaw output saved to {OUTPUT_PATH.with_suffix('.raw.txt')}")
        sys.exit(1)

    # Save agent BOM
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("# Agent-Generated BOM\n")
        f.write(f"# Generated: {date.today()}\n")
        f.write("# Input: spec.md (no access to human bom.yaml)\n")
        f.write(f"# Model: claude-sonnet-4-20250514\n\n")
        yaml.dump(agent_bom, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    print(f"Agent BOM saved to {OUTPUT_PATH}")

    # Count components
    agent_comps = extract_components(agent_bom)
    print(f"Agent generated {len(agent_comps)} components across {len(agent_bom.get('assemblies', []))} assemblies")

    # Compare if requested
    if compare_mode:
        print("\nComparing against human BOM...")
        human_text = read_file(HUMAN_BOM_PATH)
        # Strip YAML comments for parsing
        human_bom = yaml.safe_load(human_text)
        report = compare_boms(human_bom, agent_bom)
        REPORT_PATH.write_text(report, encoding="utf-8")
        print(f"Comparison report saved to {REPORT_PATH}")
        print("\n" + report)
    else:
        print("\nRun with --compare to compare against human bom.yaml")


if __name__ == "__main__":
    main()
