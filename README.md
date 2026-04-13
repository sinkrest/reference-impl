# reference-impl

A reference implementation of a forkable factory.

> "Physical products should be developed the way software is."

This repo contains a real (fictional) industrial product – a USB-C powered heated mug – developed entirely as structured files an agent can read, reason over, and act inside of.

The spec, the BOM, the supplier network, the compliance matrix, the stage-gate – all of it lives here as structured data. Not Word docs. Not PDF binders. Not email threads.

Files that version. Files that fork. Files that survive the person who wrote them.

---

## What's here

### Core product files

| File | What it is |
|---|---|
| [`spec.md`](spec.md) | Full product specification – functional, physical, electrical, compliance, economics |
| [`bom.yaml`](bom.yaml) | Bill of materials – 26 components across 3 assemblies, costed at MOQ 2,000 |
| [`bom-schema.yaml`](bom-schema.yaml) | JSON Schema for BOM validation – defines the structure any forkable BOM should follow |
| [`compliance.yaml`](compliance.yaml) | 9 EU directives mapped to components, evidence needed, test costs, and status |
| [`stage-gate.yaml`](stage-gate.yaml) | Product development workflow as a state machine – 6 stages, 35 gate criteria |
| [`supplier-api-landscape.md`](supplier-api-landscape.md) | Survey of distributed manufacturing APIs (Xometry, Protolabs, JLCPCB, PCBWay) |

### Agent experiments

| File | What it proves |
|---|---|
| [`agent-tasks/review-spec-bom.md`](agent-tasks/review-spec-bom.md) | Prompt that asks an agent to review spec + BOM for gaps |
| [`reviews/2026-04-12-spec-bom-review.md`](reviews/2026-04-12-spec-bom-review.md) | Agent review output – found 3 missing EMC components, REACH gaps, food contact chain |
| [`agent-bom-draft.py`](agent-bom-draft.py) | Script that asks Claude to generate a BOM from spec alone |
| [`agent-bom.yaml`](agent-bom.yaml) | Agent-generated BOM – 33 components, no access to human BOM |
| [`agent-bom-comparison.md`](agent-bom-comparison.md) | Comparison report: 96% component match, pricing unreliable |

### Scripts

| File | What it does |
|---|---|
| [`scripts/supplier-lookup.py`](scripts/supplier-lookup.py) | Queries Xometry-style APIs for component quotes |

### Reports

| File | What it covers |
|---|---|
| [`reports/supplier-lookup-2026-04-12.md`](reports/supplier-lookup-2026-04-12.md) | Supplier API feasibility – what you can automate today, what you can't |

---

## The product

**HeatMug USB-C** – a USB-C PD powered heated mug for desk use. Ceramic double-wall mug + heated base unit. No battery, no Bluetooth, no app. Just heat.

Simple enough to model in weeks. Complex enough to need a real BOM, real suppliers, and real compliance (CE marking, LVD, EMC, RoHS, REACH, WEEE, food contact).

### Key numbers

| Metric | Value |
|---|---|
| Components | 26 (3 mug + 19 base unit + 4 packaging) |
| Total COGS | €11.58 at MOQ 2,000 |
| Target retail | €49.95 DTC |
| Gross margin | ~74% (before tooling amortisation) |
| Compliance testing | €6,200–11,500 (EU mandatory) |
| Tooling | €6,500 one-time (mug mould + housing moulds) |

---

## The thesis

Three ingredients are converging:

1. **Agentic environments** – folders that become reasoning substrates. A product repo with structured files is a workspace an agent can navigate, review, and extend.

2. **Distributed manufacturing APIs** – supply chains as curl requests. Xometry, Protolabs, JLCPCB already have APIs. The gap between "API exists" and "agent can use it" is closing.

3. **Compliance as code** – standards as structured files, test protocols as scripts. Instead of a binder, a YAML file that maps directives to components and tracks evidence status.

Nobody has stirred them together yet. This repo is the experiment.

---

## What the agent experiments proved

### Experiment 1: Agent reviews spec + BOM (Week 3)

Gave Claude the spec and BOM. Asked it to find gaps.

**Result:** Found 3 missing EMC components (common-mode choke, ferrite beads, VBUS TVS diode), flagged REACH compliance gaps on 12 components, identified an indirect food contact chain on the silicone pad. All legitimate findings that a human reviewer confirmed.

### Experiment 2: Agent generates BOM from spec (Week 7)

Gave Claude only the spec and BOM schema. No access to the human-crafted BOM. Asked it to generate a complete bill of materials.

**Result:**
- **96% component match** – 25 of 26 human components identified independently
- **Added 3 components** the human BOM was missing (voltage regulator, EMC filters)
- **Pricing is unreliable** – individual component costs off by 10–30x in some cases
- **Structure is excellent** – right assemblies, right materials, right compliance tags

**The takeaway:** An agent can draft *what to build*. It can't quote *what it costs*. Structure from AI, pricing from APIs.

---

## How to fork this

The whole point is forkability. To adapt for your product:

1. **Fork this repo**
2. **Replace `spec.md`** with your product's specification
3. **Run the agent review** (`agent-tasks/review-spec-bom.md`) to get AI feedback on gaps
4. **Generate a draft BOM** using `agent-bom-draft.py` (needs `ANTHROPIC_API_KEY`)
5. **Edit `bom.yaml`** with real supplier quotes
6. **Adapt `compliance.yaml`** for your product's regulatory requirements
7. **Use `stage-gate.yaml`** to track development progress

The schema (`bom-schema.yaml`) works for any product. The compliance and stage-gate files need adaptation per product category and target market.

---

## Build log

This repo was built one slice per week, in public.

| Week | Slice | Artifact | LinkedIn angle |
|---|---|---|---|
| 1 | Product spec | `spec.md` | "What if a product spec was a context file?" |
| 2 | BOM as data | `bom.yaml` + `bom-schema.yaml` | "The binder becomes a repo" |
| 3 | Agent reads spec | `reviews/2026-04-12-spec-bom-review.md` | "I pointed an agent at a product spec" |
| 4 | Supplier lookup | `supplier-api-landscape.md` + `scripts/supplier-lookup.py` | "Physical supply chain as a curl request" |
| 5 | Compliance file | `compliance.yaml` | "Compliance as code – ugly, early, real" |
| 6 | Stage-gate | `stage-gate.yaml` | "Stage-gate as a state machine" |
| 7 | Agent BOM draft | `agent-bom.yaml` + `agent-bom-comparison.md` | "The agent wrote a bill of materials" |
| 8 | README + ship | This file | "You can fork this factory" |

---

## Follow along

- Blog: [The Forkable Factory](https://romanmartins.com/blog/the-forkable-factory)
- LinkedIn: [Roman Martins](https://www.linkedin.com/in/romanmartins/)
- GitHub org: [github.com/forkable-factory](https://github.com/forkable-factory)

If you build something with this, I'd love to know. Open an issue or find me on LinkedIn.

---

## License

MIT
