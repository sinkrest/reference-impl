# Supplier API Landscape – April 2026

> Can you get a manufacturing quote with a curl request? The honest answer.

---

## The Map

| Platform | Process | Public API? | Buyer-side quoting? | Auth | Notes |
|---|---|---|---|---|---|
| **Xometry** | CNC, 3DP, sheet metal, molding | Yes (developer.xometry.com) | **No** – supplier-facing only | API key | Jobs, offers, DFM feedback. Web-only for buyer quotes. |
| **Protolabs** | CNC, 3DP, injection molding | **No** | No | N/A | ProDesk web UI + Fusion 360 plugin. Zero API. |
| **Hubs (Protolabs Network)** | CNC, 3DP | Deprecated | No | N/A | Legacy 3D Hubs API died post-acquisition (2021). |
| **JLCPCB** | PCB fab, SMT assembly, 3DP | **Yes** (4 APIs) | **Yes** | Application-based | Gerber upload, auto-pricing, ordering, component sourcing. Best-in-class. |
| **PCBWay** | PCB fab, assembly | **Yes** (partner API) | **Yes** | Partner approval | Quote by parameters, order, track. Partner-gated. |
| **Sculpteo** | 3D printing | Yes | **Yes** (by UUID) | Partner account | Upload → get UUID → GET price. Simple. BASF subsidiary. |
| **Shapeways** | 3D printing | **Yes** (REST) | **Yes** | OAuth | Cleanest API: upload, printability check, order, track. Business stability uncertain. |
| **SendCutSend** | Laser, waterjet, bending | **No** | No | N/A | Web-only. |
| **Fictiv** | CNC, 3DP | **No** | No | N/A | Web-only. Procurement-level integration. |
| **RapidDirect** | CNC, 3DP, sheet metal | **No** | No | N/A | Web-only. |

---

## What This Means for HeatMug HM-001

| Component | Process | API-quotable? | Best option |
|---|---|---|---|
| Ceramic mug body (MUG-001) | Ceramic manufacturing | **No** | Manual RFQ (Alibaba, sourcing agent) |
| Steel base plate (MUG-002) | CNC/stamping | **No** | Manual RFQ |
| ABS housing (BASE-001, 002) | Injection moulding | **No** | Manual RFQ (prototype via 3DP API) |
| Aluminium plate (BASE-003) | CNC machining | **No** | Manual RFQ (Xometry web, not API) |
| **PCB (BASE-011)** | PCB fabrication | **Yes** | JLCPCB API |
| **SMT assembly (BASE-022)** | Pick-and-place | **Yes** | JLCPCB API |
| **Components (BASE-012–020)** | Electronic parts | **Yes** | JLCPCB Components API, LCSC |
| PTC heater (BASE-010) | Specialty component | **No** | Direct supplier contact (DBK) |
| USB-C cable (BASE-021) | Cable assembly | **No** | Manual RFQ |
| Packaging (PKG-001–004) | Print + moulded pulp | **No** | Manual RFQ |
| **Housing prototype** | 3D printing | **Yes** | Shapeways API or Sculpteo |

**Score: 4 of 11 component groups are API-quotable.** All four are electronics. Zero mechanical/packaging components have programmatic quoting.

---

## The Gap

The missing infrastructure is a **buyer-side manufacturing API** for:

1. **CNC machining** – upload STEP, get instant quote, place order
2. **Injection moulding** – upload STEP + specify material/quantity, get tooling + unit cost
3. **Sheet metal** – upload DXF, get laser/bend quote
4. **Ceramic/specialty** – no digital path at all

Xometry and Protolabs have the data and the algorithms (their web UIs quote instantly). They just don't expose it via API. The quoting engine exists — the API layer doesn't.

**PCB is the proof that this model works.** JLCPCB went from "email us your Gerbers" to four production APIs in ~5 years. CNC/molding will follow — the question is when, not if.

---

## Open-Source Ecosystem

| Project | Platform | What it does |
|---|---|---|
| Fabrication-Toolkit | JLCPCB | KiCad → JLCPCB production files |
| JLCKicadTools | JLCPCB | Assembly service integration |
| circuit-weaver | PCBWay/JLCPCB | BOM generation for PCB fabs |
| jlcpcb-parts-database | JLCPCB | Component catalog scraper |
| 3dhubs-node | 3D Hubs | **Abandoned** – pre-acquisition |

No unified wrapper across platforms exists. Each tool targets one vendor.

---

## Implications for Forkable Factory

1. **The agent can automate PCB sourcing today.** Given a BOM, it can query JLCPCB for PCB + component quotes programmatically. This is a real demo.
2. **Mechanical sourcing requires a human in the loop.** No API path for the mug, housing, or plate. The agent can prepare RFQ documents but cannot submit them.
3. **3D-printed prototypes are API-accessible.** The housing can be prototyped via Shapeways/Sculpteo API before committing to injection mould tooling.
4. **The "distributed manufacturing API" thesis is validated but early.** PCB proves the model. CNC/molding is the frontier. Whoever builds the unified API layer for mechanical parts captures enormous value.
5. **For the reference implementation:** demonstrate what works (PCB quoting), document what doesn't (mechanical quoting), and show the gap clearly. That's the honest story.
