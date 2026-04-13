# Agent Task: Review Spec + BOM

**Task ID:** AT-001
**Type:** Design review
**Inputs:** `spec.md`, `bom.yaml`, `bom-schema.yaml`
**Output:** Structured review with findings, severity, and recommendations

---

## Prompt

You are a product engineer reviewing a hardware product specification and its bill of materials. Your job is to cross-check them and surface issues that a human reviewer should look at.

Read the following files:
- `spec.md` — product specification
- `bom.yaml` — bill of materials
- `bom-schema.yaml` — BOM structure definition

Then produce a review covering:

### 1. Spec → BOM Coverage
For each functional requirement in the spec, verify that the BOM contains the components needed to fulfil it. Flag any requirement that has no corresponding BOM entry.

### 2. BOM → Spec Traceability
For each component in the BOM, verify it traces back to a spec requirement. Flag orphan components that exist in the BOM but aren't driven by the spec.

### 3. Electrical Consistency
Check that voltage, current, and power ratings are consistent across the electrical chain (USB-C PD source → PD controller → MCU → heater driver → PTC heater). Flag mismatches.

### 4. Compliance Gaps
Cross-reference the compliance requirements in Section 6 of the spec against the `compliance` fields in the BOM. Flag any spec-level compliance requirement that no component addresses.

### 5. Cost Sanity
Compare BOM cost totals against the target economics in Section 9 of the spec. Flag if over budget or if the buffer is too thin for realistic production.

### 6. Open Risks
Identify any technical risks, single-source dependencies, or assumptions that could cause problems in prototyping or production.

---

## Output Format

For each finding:
```
[SEVERITY] Category — Finding
Recommendation: ...
```

Severity levels:
- 🔴 BLOCKER — Must fix before prototyping
- 🟡 WARNING — Should address, risk if ignored
- 🟢 NOTE — Suggestion or optimisation, not blocking
