#!/usr/bin/env python3
"""
Forkable Factory – Supplier Lookup Demo

Reads bom.yaml and attempts programmatic supplier lookups for each component.
Demonstrates what's API-accessible today and what isn't.

Usage:
    python supplier-lookup.py                    # Dry run (no API calls)
    python supplier-lookup.py --live             # Live API calls (requires keys)
    JLCPCB_API_KEY=xxx python supplier-lookup.py --live

The point: this script IS the thesis. Some components return instant quotes.
Most return "manual RFQ required." That gap is the opportunity.
"""

import yaml
import json
import sys
import os
from pathlib import Path
from datetime import datetime

# ─── Configuration ───────────────────────────────────────────

BOM_PATH = Path(__file__).parent.parent / "bom.yaml"
OUTPUT_PATH = Path(__file__).parent.parent / "reports" / f"supplier-lookup-{datetime.now().strftime('%Y-%m-%d')}.md"

# API availability map — which component categories have programmatic quoting?
API_AVAILABILITY = {
    # Component ID patterns → API status
    "BASE-011": {  # PCB
        "api": "JLCPCB PCB API",
        "endpoint": "https://api.jlcpcb.com/pcb/quote",
        "method": "POST (Gerber upload + parameters)",
        "status": "available",
        "notes": "Requires Gerber files. Can quote by board parameters for estimation.",
    },
    "BASE-022": {  # SMT assembly
        "api": "JLCPCB SMT API",
        "endpoint": "https://api.jlcpcb.com/smt/quote",
        "method": "POST (BOM + pick-and-place file)",
        "status": "available",
        "notes": "Requires BOM CSV + CPL file. Integrated with PCB order.",
    },
    "BASE-012": {  # MCU
        "api": "JLCPCB Components API / LCSC",
        "endpoint": "https://api.jlcpcb.com/components/search",
        "method": "GET (part number search)",
        "status": "available",
        "notes": "Real-time pricing and stock. Can verify BOM costs.",
    },
    "BASE-013": {  # PD controller
        "api": "JLCPCB Components API / LCSC",
        "endpoint": "https://api.jlcpcb.com/components/search",
        "method": "GET (part number search)",
        "status": "available",
        "notes": "Real-time pricing and stock.",
    },
    "BASE-001": {  # Housing — could prototype via 3DP
        "api": "Shapeways API (prototype only)",
        "endpoint": "https://api.shapeways.com/models/v1",
        "method": "POST (STL upload → printability + price)",
        "status": "available_prototype",
        "notes": "3D-printed prototype only. Production injection moulding has no API.",
    },
    "BASE-002": {  # Housing bottom — same as above
        "api": "Shapeways API (prototype only)",
        "endpoint": "https://api.shapeways.com/models/v1",
        "method": "POST (STL upload)",
        "status": "available_prototype",
        "notes": "Prototype only. Production requires manual RFQ.",
    },
}

# Components with no API path
NO_API_REASON = {
    "MUG-001": "Ceramic manufacturing — no digital quoting platform exists",
    "MUG-002": "CNC/stamping — Xometry API is supplier-facing only, not buyer-facing",
    "MUG-003": "Specialty chemical — direct supplier contact required",
    "BASE-003": "CNC machining — no buyer-side API (Xometry/Protolabs are web-only)",
    "BASE-004": "Custom silicone part — manual RFQ",
    "BASE-005": "Commodity — bulk order via Alibaba/distributor",
    "BASE-010": "Specialty PTC heater — direct supplier (DBK/Heatron)",
    "BASE-014": "Available on LCSC but not via JLCPCB Components API tier",
    "BASE-015": "Available on LCSC",
    "BASE-016": "Available on LCSC",
    "BASE-017": "Safety component — sourcing requires datasheet verification",
    "BASE-018": "Available on LCSC",
    "BASE-019": "Available on LCSC",
    "BASE-020": "Passives bundle — priced as set, individual lookup at PCB design phase",
    "BASE-021": "Custom cable assembly — manual RFQ",
    "BASE-030": "Commodity fasteners — bulk order",
    "PKG-001": "Custom packaging — manual RFQ",
    "PKG-002": "Custom moulded pulp — manual RFQ",
    "PKG-003": "Print job — manual RFQ",
    "PKG-004": "Label printing — manual RFQ",
}


def load_bom(path: Path) -> dict:
    """Load and parse bom.yaml."""
    with open(path) as f:
        return yaml.safe_load(f)


def lookup_component(component: dict, live: bool = False) -> dict:
    """
    Attempt supplier lookup for a single component.
    Returns a result dict with API status and quote info.
    """
    cid = component["id"]
    name = component["name"]
    bom_cost = component.get("unit_cost", 0)
    quantity = component.get("quantity", 1)

    result = {
        "id": cid,
        "name": name,
        "bom_unit_cost": bom_cost,
        "quantity": quantity,
        "bom_line_cost": round(bom_cost * quantity, 2),
    }

    if cid in API_AVAILABILITY:
        api_info = API_AVAILABILITY[cid]
        result["api_status"] = api_info["status"]
        result["api_name"] = api_info["api"]
        result["endpoint"] = api_info["endpoint"]
        result["method"] = api_info["method"]
        result["notes"] = api_info["notes"]

        if live and api_info["status"] == "available":
            # Live API call would go here
            # For now, return a simulated response structure
            result["live_quote"] = None
            result["live_note"] = "Live API call requires authentication. Set JLCPCB_API_KEY."
        else:
            result["live_quote"] = None

    else:
        result["api_status"] = "no_api"
        result["api_name"] = None
        result["reason"] = NO_API_REASON.get(cid, "No known API for this component type")

    return result


def generate_report(bom: dict, results: list[dict], live: bool) -> str:
    """Generate a markdown report from lookup results."""
    lines = []
    lines.append("# Supplier Lookup Report")
    lines.append(f"\n**Product:** {bom['product_id']} | **Date:** {datetime.now().strftime('%Y-%m-%d')} | **Mode:** {'Live' if live else 'Dry run'}")
    lines.append("")

    # Summary
    api_available = [r for r in results if r["api_status"] == "available"]
    api_prototype = [r for r in results if r["api_status"] == "available_prototype"]
    no_api = [r for r in results if r["api_status"] == "no_api"]

    total_bom_cost = sum(r["bom_line_cost"] for r in results)
    api_quotable_cost = sum(r["bom_line_cost"] for r in api_available)
    prototype_cost = sum(r["bom_line_cost"] for r in api_prototype)

    lines.append("## Summary")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|---|---|")
    lines.append(f"| Total components | {len(results)} |")
    lines.append(f"| API-quotable (production) | {len(api_available)} ({len(api_available)/len(results)*100:.0f}%) |")
    lines.append(f"| API-quotable (prototype only) | {len(api_prototype)} |")
    lines.append(f"| Manual RFQ required | {len(no_api)} ({len(no_api)/len(results)*100:.0f}%) |")
    lines.append(f"| Total BOM cost | €{total_bom_cost:.2f} |")
    lines.append(f"| API-quotable cost | €{api_quotable_cost:.2f} ({api_quotable_cost/total_bom_cost*100:.0f}% of BOM) |")
    lines.append("")

    # API-available components
    lines.append("## API-Quotable Components")
    lines.append("")
    lines.append("| ID | Component | BOM Cost | API | Status |")
    lines.append("|---|---|---|---|---|")
    for r in api_available + api_prototype:
        status = "Production" if r["api_status"] == "available" else "Prototype only"
        lines.append(f"| {r['id']} | {r['name']} | €{r['bom_line_cost']:.2f} | {r['api_name']} | {status} |")
    lines.append("")

    # Manual RFQ components
    lines.append("## Manual RFQ Required")
    lines.append("")
    lines.append("| ID | Component | BOM Cost | Why no API |")
    lines.append("|---|---|---|---|")
    for r in no_api:
        lines.append(f"| {r['id']} | {r['name']} | €{r['bom_line_cost']:.2f} | {r['reason']} |")
    lines.append("")

    # The gap
    lines.append("## The Gap")
    lines.append("")
    lines.append(f"**{len(no_api)} of {len(results)} components** ({len(no_api)/len(results)*100:.0f}%) require manual quoting.")
    lines.append(f"These represent **€{sum(r['bom_line_cost'] for r in no_api):.2f}** of the €{total_bom_cost:.2f} BOM — "
                 f"**{sum(r['bom_line_cost'] for r in no_api)/total_bom_cost*100:.0f}%** of total cost.")
    lines.append("")
    lines.append("The components with the highest cost and no API path:")
    lines.append("")
    no_api_sorted = sorted(no_api, key=lambda r: r["bom_line_cost"], reverse=True)
    for r in no_api_sorted[:5]:
        lines.append(f"- **{r['name']}** ({r['id']}) — €{r['bom_line_cost']:.2f}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Generated by `supplier-lookup.py` — Forkable Factory reference implementation.*")

    return "\n".join(lines)


def main():
    live = "--live" in sys.argv

    print(f"Forkable Factory — Supplier Lookup {'(LIVE)' if live else '(dry run)'}")
    print(f"Reading BOM: {BOM_PATH}")
    print()

    bom = load_bom(BOM_PATH)

    # Flatten all components from all assemblies
    all_components = []
    for assembly in bom["assemblies"]:
        for component in assembly["components"]:
            all_components.append(component)

    print(f"Found {len(all_components)} components across {len(bom['assemblies'])} assemblies.")
    print()

    # Run lookups
    results = []
    for comp in all_components:
        result = lookup_component(comp, live=live)
        status_icon = {
            "available": "🟢",
            "available_prototype": "🟡",
            "no_api": "🔴",
        }[result["api_status"]]
        print(f"  {status_icon} {result['id']:10s} {result['name'][:40]:40s} €{result['bom_line_cost']:.2f}")
        results.append(result)

    print()

    # Generate report
    report = generate_report(bom, results, live)

    # Save report
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        f.write(report)

    print(f"Report saved to: {OUTPUT_PATH}")

    # Print summary
    api_count = sum(1 for r in results if r["api_status"] in ("available", "available_prototype"))
    no_api_count = sum(1 for r in results if r["api_status"] == "no_api")
    print(f"\nResult: {api_count} API-quotable, {no_api_count} manual RFQ required.")
    print(f"The gap is real. PCB = automated. Mechanical = phone calls.")


if __name__ == "__main__":
    main()
