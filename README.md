# reference-impl

A reference implementation of a forkable factory.

> "Physical products should be developed the way software is."

This repo contains a real (fake) industrial product – a USB-C powered heated mug – developed entirely as structured files an agent can read, reason over, and act inside of.

The spec, the BOM, the supplier network, the compliance matrix, the stage-gate – all of it lives here as structured data. Not Word docs. Not PDF binders. Not email threads.

Files that version. Files that fork. Files that survive the person who wrote them.

## What's here

| File | Status | Description |
|---|---|---|
| `spec.md` | Done | Full product specification – functional, physical, electrical, compliance, economics |
| `bom.yaml` | Coming | Bill of materials as structured data |
| `compliance.md` | Coming | CE, LVD, RoHS, WEEE as a structured checklist |
| `stage-gate.yaml` | Coming | Stage-gate workflow as a state machine |
| Agent tasks | Coming | Claude tasks that reason over these files |

## The product

**HeatMug USB-C** – a USB-C PD powered heated mug for desk use. Ceramic double-wall mug + heated base unit. No battery, no Bluetooth, no app. Just heat.

Simple enough to model in weeks. Complex enough to need a real BOM, real suppliers, and real compliance (CE marking, LVD, EMC, RoHS, REACH, WEEE, food contact).

## The thesis

Three ingredients are converging:

1. **Agentic environments** – folders that become reasoning substrates
2. **Distributed manufacturing APIs** – supply chains as curl requests
3. **Compliance as code** – standards as structured files, test protocols as scripts

Nobody has stirred them together yet. This repo is the experiment.

## Build in public

I'm shipping one slice per week and writing build logs. Follow along:

- Blog: [The Forkable Factory](https://romanmartins.com/blog/the-forkable-factory)
- LinkedIn: [Roman Martins](https://www.linkedin.com/in/romanmartins/)

## Fork it

That's the whole point. Clone this repo, swap the product, adapt for your market. If you build something with it, I'd love to know.

## License

MIT
