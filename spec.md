# Product Specification: HeatMug USB-C

**Product ID:** HM-001
**Revision:** 0.1
**Date:** 2026-04-11
**Status:** Draft
**Author:** Roman Martins

---

## 1. Product Overview

### 1.1 Description

A USB-C powered heated mug that maintains beverages at a user-selected temperature. Designed for desk use. Powered directly from a USB-C PD (Power Delivery) source – no battery, no separate power adapter. The mug sits on a heated base connected via USB-C cable.

### 1.2 Target User

Knowledge workers, remote workers, and office workers who drink hot beverages at a desk and want them to stay at a consistent temperature without microwaving.

### 1.3 Target Market

EU (primary), US (secondary). All units must meet EU regulatory requirements. US regulatory compliance is a stretch goal for v1.

### 1.4 Product Architecture

The system has two physical components:

1. **Mug** – double-wall insulated ceramic mug with a conductive base plate
2. **Base unit** – USB-C powered heating pad with controller, thermal sensor, LED indicator, and touch control

The mug sits on the base. The base heats the mug through contact with the conductive base plate. No electrical connection between mug and base – heat transfer only.

---

## 2. Functional Requirements

| ID | Requirement | Priority | Rationale |
|---|---|---|---|
| FR-01 | Maintain beverage temperature at user-set target (±2°C) | Must | Core value proposition |
| FR-02 | User-selectable temperature: 50°C, 55°C, 60°C (3 presets) | Must | Covers espresso (55°C), tea (60°C), warm drink (50°C) |
| FR-03 | Reach target temperature from 40°C within 5 minutes (250 ml) | Must | Reasonable reheat time for desk use |
| FR-04 | LED indicator shows current state: heating (amber), at target (green), standby (off) | Must | User needs feedback without an app |
| FR-05 | Touch button on base to cycle between temperature presets | Must | Single-control simplicity |
| FR-06 | Auto-shutoff after 4 hours of continuous use | Must | Safety – prevents unattended heating |
| FR-07 | Auto-standby when mug is removed from base (detect absence within 10 s) | Must | Energy saving + safety |
| FR-08 | Resume heating when mug is returned to base | Should | Convenience |
| FR-09 | Mug is dishwasher safe (top rack) | Should | Usability expectation for ceramic mugs |
| FR-10 | Base unit wipes clean with damp cloth | Must | Desk environment – spills happen |

---

## 3. Physical Specifications

### 3.1 Mug

| Parameter | Value | Tolerance | Notes |
|---|---|---|---|
| Material (body) | Ceramic (stoneware) | – | Double-wall vacuum insulated |
| Material (base plate) | Stainless steel 304 | – | Conductive, food-safe, flat ground surface |
| Capacity | 350 ml | ±10 ml | Standard large coffee mug |
| Height | 105 mm | ±2 mm | Including base plate |
| Outer diameter | 85 mm | ±1 mm | – |
| Wall thickness | 8 mm | ±0.5 mm | Double-wall with vacuum gap |
| Weight (empty) | 380 g | ±20 g | Ceramic + steel base |
| Base plate thickness | 2 mm | ±0.2 mm | Ground flat to ≤0.1 mm deviation |
| Base plate diameter | 70 mm | ±0.5 mm | Must match base unit heating zone |
| Colour | Matte white | – | RAL 9003 or equivalent |
| Handle | Yes, D-shape | – | Integrated ceramic |

### 3.2 Base Unit

| Parameter | Value | Tolerance | Notes |
|---|---|---|---|
| Material (housing) | ABS plastic | – | UL94 V-0 flame rated |
| Material (top surface) | Silicone rubber pad over aluminium plate | – | Anti-slip + heat transfer |
| Heating element | PTC ceramic heater | – | Self-regulating, max surface temp 80°C |
| Height | 18 mm | ±1 mm | Low profile for desk |
| Diameter | 110 mm | ±1 mm | – |
| Weight | 195 g | ±15 g | – |
| Cable | USB-C, 1.2 m, integrated | ±50 mm | Not detachable (simplifies compliance) |
| Feet | 4x silicone anti-slip pads | – | – |

---

## 4. Electrical Specifications

| Parameter | Value | Notes |
|---|---|---|
| Input | USB-C PD | 9V/3A (27W) or 12V/2.25A (27W) negotiated via PD |
| Max power draw | 25W | Operating headroom below PD negotiated ceiling |
| Heating element power | 20W | PTC ceramic, self-limiting |
| Controller | MCU (e.g., STM32G030 or equivalent) | Low-cost ARM Cortex-M0+, built-in ADC for temp sensing |
| Temperature sensor | NTC thermistor (100kΩ @ 25°C) | Embedded in aluminium plate, reads surface temp |
| LED | Single RGB LED (common anode) | Amber = heating, green = at target, off = standby |
| Touch sensor | Capacitive, single-point | Integrated into top housing surface |
| USB-C PD controller | FUSB302 or equivalent | Handles PD negotiation |
| Protection | Thermal fuse (85°C, one-shot) | Backup safety – cuts power if PTC + MCU both fail |
| ESD protection | TVS diodes on USB-C lines | Required for CE compliance |

---

## 5. Performance Requirements

| ID | Requirement | Test Method |
|---|---|---|
| PR-01 | Heat 250 ml water from 40°C to 55°C in ≤5 min | Thermocouple in liquid centre, ambient 22°C |
| PR-02 | Maintain 55°C ±2°C for 4 hours continuously | Log temp every 30 s, verify ≤2°C deviation |
| PR-03 | Standby power draw ≤0.5W | Measure at USB-C input with mug removed |
| PR-04 | Mug detection latency ≤10 s | Remove mug, time to LED off |
| PR-05 | Survive 1 m drop onto concrete (base unit) | 3 samples, no crack/break, functional after |
| PR-06 | Mug survives 50 dishwasher cycles | No crazing, no base plate loosening |
| PR-07 | Cable withstands 5,000 bend cycles at strain relief | IEC 62368-1 Clause 4.6 |

---

## 6. Regulatory & Compliance Requirements

| ID | Standard | Scope | Market | Mandatory |
|---|---|---|---|---|
| CR-01 | CE Marking | EU Declaration of Conformity | EU | Yes |
| CR-02 | LVD – EN 62368-1:2020 | Audio/video, IT, and communication equipment safety | EU | Yes |
| CR-03 | EMC – EN 55032 / EN 55035 | Electromagnetic compatibility (emissions + immunity) | EU | Yes |
| CR-04 | RoHS – Directive 2011/65/EU | Restriction of hazardous substances | EU | Yes |
| CR-05 | REACH – Regulation (EC) 1907/2006 | Chemical substance registration | EU | Yes |
| CR-06 | WEEE – Directive 2012/19/EU | Waste electrical/electronic equipment (recycling marking) | EU | Yes |
| CR-07 | EU Food Contact – Regulation (EC) 1935/2004 | Materials in contact with food (mug + base plate) | EU | Yes |
| CR-08 | USB-IF Compliance | USB-C and PD protocol conformance | Global | Recommended |
| CR-09 | FCC Part 15 | Electromagnetic emissions | US | Stretch goal |
| CR-10 | Packaging – Directive 94/62/EC | Packaging and packaging waste | EU | Yes |

### 6.1 Compliance Notes

- The mug is a passive component (no electronics). Food contact compliance applies to the mug body (ceramic) and base plate (stainless steel 304). Both are well-established food-safe materials – migration testing required but straightforward.
- The base unit is classified as IT equipment under EN 62368-1 (USB-powered). Not a "household appliance" under EN 60335 because it draws power from USB, not mains.
- PTC heater with thermal fuse provides dual-layer thermal protection, satisfying LVD fault condition requirements.
- Integrated (non-detachable) cable simplifies compliance – no need for separate cable ratings.

---

## 7. Environmental Requirements

| Parameter | Value |
|---|---|
| Operating temperature | 10°C to 35°C |
| Storage temperature | -20°C to 60°C |
| Operating humidity | 20% to 80% RH (non-condensing) |
| IP rating (base unit) | IP20 (no ingress protection – desk use only) |
| Altitude | Up to 2,000 m |

---

## 8. Packaging & Labelling

| Element | Requirement |
|---|---|
| Retail box | Corrugated cardboard, printed, FSC certified |
| Inner protection | Moulded paper pulp (no EPS/styrofoam) |
| Included items | 1x mug, 1x base unit (cable attached), 1x quick start guide |
| Not included | USB-C PD power adapter (stated clearly on box) |
| Labelling (base unit) | CE mark, WEEE symbol, manufacturer, model, electrical ratings, country of origin |
| Labelling (box) | EAN barcode, product name, contents, compliance marks, "USB-C PD adapter required (not included)" |

---

## 9. Target Economics

| Parameter | Target | Notes |
|---|---|---|
| COGS (mug) | €3.50 | Ceramic + steel base plate, MOQ 2,000 |
| COGS (base unit) | €8.50 | PCB, PTC heater, housing, cable, assembly |
| COGS (packaging) | €1.20 | Box + pulp insert + QSG |
| Total COGS | €13.20 | Per unit at MOQ 2,000 |
| Target retail price | €49.95 | DTC (direct to consumer) via web |
| Target wholesale price | €27.00 | To retailers, ~2x COGS |
| Gross margin (DTC) | ~74% | Before shipping, marketing, returns |

---

## 10. Constraints & Assumptions

| ID | Constraint/Assumption | Type |
|---|---|---|
| CA-01 | No battery – USB-C PD power only | Constraint (avoids battery regulations: UN38.3, IEC 62133) |
| CA-02 | No Bluetooth/WiFi – no app | Constraint (avoids radio equipment directive RED 2014/53/EU) |
| CA-03 | Mug and base are separate products for compliance purposes | Assumption (mug = passive food contact item, base = IT equipment) |
| CA-04 | USB-C PD adapter availability is high enough to exclude from box | Assumption (reduces cost + packaging waste) |
| CA-05 | PTC heater self-regulation is sufficient primary thermal protection | Assumption (validated by PTC supplier datasheet + thermal fuse as backup) |
| CA-06 | Ceramic double-wall manufacturing is available at MOQ 2,000 from China suppliers | Assumption (verify with Alibaba/sourcing agent) |
| CA-07 | Single SKU (matte white, 350 ml) for v1 | Constraint (simplifies inventory, compliance, tooling) |

---

## 11. Open Items

| ID | Item | Owner | Status |
|---|---|---|---|
| OI-01 | Verify PTC heater supplier and datasheet | Engineering | Open |
| OI-02 | Confirm USB-C PD controller IC availability | Engineering | Open |
| OI-03 | Get ceramic mug sample quotes (MOQ 2,000) | Sourcing | Open |
| OI-04 | Confirm EN 62368-1 classification with test lab | Compliance | Open |
| OI-05 | Industrial design – mug form factor, base aesthetics | Design | Open |
| OI-06 | Determine if NTC placement in aluminium plate gives accurate liquid temp reading | Engineering | Open |

---

## Revision History

| Rev | Date | Author | Changes |
|---|---|---|---|
| 0.1 | 2026-04-11 | Roman Martins | Initial draft |
