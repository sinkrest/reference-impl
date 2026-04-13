# Agent BOM Draft — Comparison Report

**Date:** 2026-04-13
**Setup:** Claude (Sonnet) given only `spec.md` + `bom-schema.yaml`. No access to human `bom.yaml`.
**Human BOM components:** 26
**Agent BOM components:** 33

---

## Summary

| Metric | Count | Notes |
|---|---|---|
| Matched (same ID) | 25 | 96% of human BOM matched by component ID |
| Missing from agent | 1 | BASE-030 (housing screws) |
| Extra in agent | 8 | Voltage regulator, ferrite beads, connectors, extra packaging |
| Total COGS (human) | €11.58 | |
| Total COGS (agent) | €10.51 | €1.07 lower — but with pricing errors on individual items |

---

## What the Agent Got Right

1. **Structure.** Three assemblies (mug, base, packaging) — identical top-level structure.
2. **Component identification.** 25/26 human components identified independently. Same IDs, same materials, same electrical specs. The agent correctly identified the MCU (STM32G030), PD controller (FUSB302), PTC heater, NTC thermistor, MOSFET driver, TVS array, and every other electrical component.
3. **Compliance mapping.** Correctly tagged food contact requirements on mug components, RoHS on electronics, LVD on safety-critical parts, packaging directive on box/insert.
4. **Design provisions.** The agent added EMC filter components (ferrite beads, common-mode choke) that the human BOM was *missing* — flagged later in the Week 3 agent review.
5. **Adhesive.** Independently identified the need for food-safe silicone adhesive (MUG-003).
6. **Assembly labour.** Included PCBA assembly as a line item (BASE-022), not just parts.

## What the Agent Got Wrong

1. **Individual pricing is unreliable.** Several components show large deltas:
   - PTC heater: agent says €0.04 vs human €1.20 (off by 30x)
   - SMT assembly: agent says €0.03 vs human €0.80 (off by 27x)
   - FUSB302: agent says €0.08 vs human €0.80 (off by 10x)
   - Silicone feet: agent says €0.90 (4x) vs human €0.08 (4x €0.02)
   - These aren't rounding errors — they're hallucinated prices.

2. **Missing fasteners.** Forgot BASE-030 (M2x6 housing screws). Small cost but real — you can't close the housing without them.

3. **Extra components that may or may not be needed:**
   - BASE-006 (3.3V LDO regulator) — probably correct, human BOM lumps this into passives
   - BASE-007/008 (ferrite beads, common-mode choke) — correct, these were flagged as missing in human BOM
   - BASE-009 (connector) — unclear, may be redundant with cable
   - BASE-023 — unclear purpose
   - PKG-005/006/007 — extra packaging items (tissue wrap, master carton, stickers)

4. **Total COGS lower than reality.** €10.51 vs €11.58 — the agent underpriced several expensive components, making the total look better than it is. A PM who trusts this number without cross-checking would get burned at quote time.

## The Verdict

**The agent nailed component identification (96%) but can't be trusted on pricing.**

This is exactly the pattern you'd expect: an LLM has broad knowledge of *what goes into* a USB-heated-mug-type product (from training data — teardowns, datasheets, engineering blogs), but it has no access to current supplier pricing, doesn't understand MOQ dynamics, and confuses unit prices across different volume tiers.

**What this means for the Forkable Factory thesis:**

An agent can generate a **draft BOM** that gets 90%+ of the structure right — the right components, the right materials, the right compliance requirements. But it needs a human (or a supplier API) to fill in the pricing. This is exactly the workflow the Forkable Factory envisions:

1. Agent drafts BOM from spec ← **this works today**
2. Human reviews structure, adds missing items ← still needed
3. Supplier API fills in pricing at volume ← Week 4 explored this
4. Agent flags compliance gaps ← Week 3 proved this works

The bottleneck isn't "can an agent reason about product structure?" — it can. The bottleneck is "can it access real-time pricing?" — and that's a data problem, not an intelligence problem.

---

## Matched Components — Cost Comparison

| ID | Name | Human | Agent | Delta |
|---|---|---|---|---|
| MUG-001 | Ceramic mug body | €2.80 | €2.40 | –€0.40 |
| MUG-002 | Base plate | €0.45 | €0.55 | +€0.10 |
| MUG-003 | Food-safe adhesive | €0.25 | €0.00 | –€0.25 |
| BASE-001 | Top housing | €0.85 | €0.65 | –€0.20 |
| BASE-002 | Bottom housing | €0.65 | €0.60 | –€0.05 |
| BASE-003 | Aluminium heat spreader | €0.40 | €0.55 | +€0.15 |
| BASE-004 | Silicone pad | €0.15 | €0.08 | –€0.07 |
| BASE-005 | Silicone feet (4x) | €0.08 | €0.90 | +€0.82 |
| BASE-010 | PTC heater | €1.20 | €0.04 | –€1.16 |
| BASE-011 | PCB | €0.35 | €0.00 | –€0.35 |
| BASE-012 | MCU (STM32G030) | €0.55 | €0.06 | –€0.49 |
| BASE-013 | PD controller (FUSB302) | €0.80 | €0.08 | –€0.72 |
| BASE-014 | NTC thermistor | €0.05 | €0.07 | +€0.02 |
| BASE-015 | RGB LED | €0.03 | €0.35 | +€0.32 |
| BASE-016 | Touch sensor IC | €0.08 | €0.25 | +€0.17 |
| BASE-017 | Thermal fuse | €0.10 | €0.00 | –€0.10 |
| BASE-018 | TVS diode array | €0.06 | €0.55 | +€0.49 |
| BASE-019 | MOSFET | €0.04 | €0.08 | +€0.04 |
| BASE-020 | Passives (set) | €0.15 | €1.10 | +€0.95 |
| BASE-021 | USB-C cable | €0.65 | €0.03 | –€0.62 |
| BASE-022 | SMT assembly | €0.80 | €0.03 | –€0.77 |
| PKG-001 | Retail box | €0.55 | €0.45 | –€0.10 |
| PKG-002 | Pulp insert | €0.40 | €0.20 | –€0.20 |
| PKG-003 | Quick start guide | €0.08 | €0.20 | +€0.12 |
| PKG-004 | Compliance label | €0.02 | €0.08 | +€0.06 |

## Missing from Agent

| ID | Name | Category | Cost |
|---|---|---|---|
| BASE-030 | Housing screws (M2x6, 4x) | fastener | €0.04 |

## Extra in Agent

| ID | Name | Category | Cost | Assessment |
|---|---|---|---|---|
| BASE-006 | 3.3V LDO voltage regulator | electrical | ? | Probably correct — human BOM doesn't list this explicitly |
| BASE-007 | Ferrite bead (EMC filter) | electrical | ? | Correct — flagged as missing in compliance review |
| BASE-008 | Common-mode choke | electrical | ? | Correct — flagged as missing in compliance review |
| BASE-009 | Board-to-wire connector | electrical | ? | Uncertain — may not be needed with integrated cable |
| BASE-023 | Final assembly labour | electrical | ? | Good addition — human BOM doesn't price final assembly |
| PKG-005 | Tissue wrap | packaging | ? | Optional — spec doesn't require it |
| PKG-006 | Master carton | packaging | ? | Realistic for shipping but not per-unit packaging |
| PKG-007 | Product sticker/seal | packaging | ? | Nice-to-have, not spec'd |
