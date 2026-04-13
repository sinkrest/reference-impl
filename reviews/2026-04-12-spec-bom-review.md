# HeatMug USB-C (HM-001) – Design Review

**Spec Revision:** 0.1 | **BOM Revision:** 0.1 | **Review Date:** 2026-04-12
**Reviewer:** Claude agent (AT-001: review-spec-bom)

---

## Summary

| Severity | Count | Key Items |
|---|---|---|
| BLOCKER | 3 | No mug detection sensor, PTC 9V/12V mismatch, thermal interface silicone pad is an insulator |
| WARNING | 8 | Missing voltage regulator, MOSFET thermals, EMC provisions, REACH gaps, food contact on silicone pad, BOM math error, missing components, single-source PTC, NTC placement, adhesive durability, IP rating |
| NOTE | 4 | TVS clamp scope, food contact indirect chain, FUSB302→HUSB238 simplification, through-hole LED |

**The three blockers must be resolved before any prototyping spend is committed.**

---

## 1. Spec → BOM Coverage

| Requirement | Status | Components |
|---|---|---|
| FR-01 (Maintain temp ±2°C) | Covered | BASE-010, BASE-014, BASE-012, BASE-019, BASE-003 |
| FR-02 (3 presets) | Covered | BASE-012 (firmware), BASE-016 |
| FR-03 (Reach target in 5 min) | Covered | BASE-010 at 20W. See electrical concerns. |
| FR-04 (LED indicator) | Covered | BASE-015 |
| FR-05 (Touch button) | Covered | BASE-016 |
| FR-06 (Auto-shutoff 4h) | Covered | BASE-012 (firmware), BASE-017 (backup) |
| FR-07 (Auto-standby on removal) | **GAP** | No detection sensor in BOM |
| FR-08 (Resume on return) | **GAP** | Same as FR-07 |
| FR-09 (Dishwasher safe) | Covered | MUG-001, MUG-002, MUG-003 materials |
| FR-10 (Wipes clean) | Covered | BASE-004 silicone, ABS housing |

### Findings

**🔴 BLOCKER – FR-07/FR-08: No mug detection sensor in BOM**

The spec requires mug presence detection (auto-standby within 10s when removed, resume when returned). No component in the BOM provides this. The NTC thermistor could theoretically detect a temperature drop, but that's slow, unreliable, and not mentioned as the detection method. Common approaches: hall effect sensor + magnet in mug base plate, weight/microswitch, or dedicated capacitive sensing.

**Recommendation:** Add a reed switch + small magnet in the mug base plate (~€0.08 combined). Or a microswitch under the silicone pad. Clarify detection method in spec.

---

**🟡 WARNING – No 3.3V voltage regulator in BOM**

The MCU (STM32G030) operates at 2.0–3.6V. USB-C PD input is 9V or 12V. No LDO or DC-DC converter in the BOM to step down. The passives set (BASE-020) does not include a regulator – a regulator is not a passive component.

**Recommendation:** Add a 3.3V LDO (e.g., AMS1117-3.3 or ME6211, ~€0.05) as a separate BOM line item. Critical power rail.

---

## 2. BOM → Spec Traceability

All BOM components trace to spec requirements or reasonable assembly/manufacturing needs. No orphan components.

---

## 3. Electrical Consistency

**🔴 BLOCKER – PTC heater voltage vs. 9V PD profile mismatch**

PTC heater (BASE-010) is rated at 12V/20W. Spec lists two PD profiles: 9V/3A and 12V/2.25A. If the charger only supports 9V, heater power drops to ~11.25W (V²/R scaling). FR-03 (reach 55°C from 40°C in 5 min) likely unachievable on 9V.

**Recommendation:** (1) Mandate 12V PD as minimum and state on packaging, OR (2) select a PTC heater rated for 9V, OR (3) add a boost converter for guaranteed 12V from 9V. At minimum, define fallback firmware behaviour for 9V operation.

---

**🟡 WARNING – MOSFET current rating marginal**

MOSFET (BASE-019) at SOT-23 with 25mΩ Rds_on. At 1.67A steady state it's fine (~70mW), but no overcurrent protection if firmware holds gate high.

**Recommendation:** Add a fuse or current sense resistor in series with heater. Consider SOT-223 if PWM frequency > 10kHz.

---

**🟢 NOTE – TVS diode clamp voltage scope**

TVS (BASE-018) clamps at 5.5V – fine for data/CC lines but would be destroyed on VBUS (9–12V). Needs separate VBUS TVS rated 20V+.

**Recommendation:** Clarify TVS is data-only. Add VBUS TVS to BOM or passives set.

---

## 4. Compliance Gaps

| Spec Requirement | BOM Coverage | Status |
|---|---|---|
| CR-01 (CE Marking) | PKG-004 label | System-level |
| CR-02 (LVD EN 62368-1) | BASE-017, BASE-021 | ✅ |
| CR-03 (EMC EN 55032/55035) | **Not referenced** | ⚠️ |
| CR-04 (RoHS) | All components | ✅ |
| CR-05 (REACH) | Most – some missing | ⚠️ |
| CR-06 (WEEE) | PKG-004 label | ✅ |
| CR-07 (EU Food Contact) | MUG-001, MUG-002, MUG-003 | ✅ |
| CR-08 (USB-IF) | Not referenced | Stretch goal |
| CR-09 (FCC Part 15) | Not referenced | Stretch goal |
| CR-10 (Packaging Directive) | PKG-001, PKG-002 | ✅ |

**🟡 WARNING – CR-03 (EMC) not addressed**

No EMC design provisions: no common-mode choke on USB-C input, no ferrite beads in passives set, no shielding. PWM switching of heater MOSFET is a known emissions source.

**Recommendation:** Add common-mode choke + ferrite beads. Plan EMC pre-compliance testing early.

---

**🟡 WARNING – REACH not listed on all components**

Many electronics components don't explicitly list REACH. Standard parts from major distributors are typically compliant, but must be confirmed.

**Recommendation:** Request REACH declarations from all suppliers.

---

**🟢 NOTE – Food contact indirect chain**

Silicone pad (BASE-004) contacts mug base plate, which contacts beverage. Indirect but potentially relevant. BASE-004 has no food-contact compliance.

**Recommendation:** Add food-contact compliance to BASE-004 or document risk assessment.

---

## 5. Cost Sanity

**🟡 WARNING – BOM cost summary math is wrong**

| Assembly | BOM claims | Actual sum |
|---|---|---|
| ASM-MUG | €3.50 | €3.50 ✅ |
| ASM-BASE | €5.97 | **€7.03** ❌ |
| ASM-PKG | €1.05 | €1.05 ✅ |
| **Total** | **€10.52** | **€11.58** |

Electronics subtotal is €4.86, not €3.06 as claimed. Buffer to €13.20 target shrinks from €2.68 to €1.62.

---

**🔴 BLOCKER – Tooling amortisation not addressed**

Mug mould ~€2,500 + housing mould ~€4,000 = €6,500 total. At MOQ 2,000 = €3.25/unit. If included in COGS: €11.58 + €3.25 = **€14.83 — exceeds €13.20 target by €1.63**.

**Recommendation:** Decide whether COGS includes tooling. If yes: increase MOQ to ~4,000+ units, or revise target, or treat tooling as separate capex.

---

**🟡 WARNING – Missing components add ~€0.25–0.35**

Voltage regulator, mug detection sensor, common-mode choke, VBUS TVS, thermal paste = ~€0.30. Revised COGS: ~€11.85–11.95. Buffer: ~€1.25.

---

## 6. Open Risks

**🔴 BLOCKER – Thermal interface chain is unvalidated**

The heat path: PTC heater → aluminium plate → **silicone pad (1mm, ~0.2 W/m·K)** → mug SS304 base → ceramic → liquid.

The silicone pad is a thermal insulator. Quick estimate: R = 0.001 / (0.2 × 0.00385) ≈ 1.3 K/W. At 20W that's a **26°C drop across the silicone pad alone**. If aluminium plate is at 80°C (PTC max), mug base sees ~54°C. Almost zero margin to heat liquid above 50°C through another ceramic wall. **FR-03 may be physically impossible with this thermal stack.**

**Recommendation:** This is the single biggest risk. Options:
1. Use thermally conductive filled silicone (1–3 W/m·K) instead of standard silicone rubber
2. Reduce pad thickness
3. Remove pad – direct aluminium-to-steel contact (lose anti-slip, gain thermal)
4. **Build a thermal prototype immediately before any other spend**

---

**🟡 WARNING – Single source risk: PTC heater**

DBK (Germany) is sole European source. Heatron (US) alternative has higher MOQ. No Chinese source listed.

**Recommendation:** Sample from DBK, Heatron, and Chinese suppliers early.

---

**🟡 WARNING – NTC placement unvalidated (OI-06 still open)**

NTC reads plate temperature, not liquid. Offset could be 25–30°C depending on thermal stack. PID tuning will be difficult without validated thermal model.

**Recommendation:** Resolve before PCB layout. Consider second NTC (ambient reference) for differential measurement.

---

**🟡 WARNING – Adhesive bond durability under thermal cycling**

Ceramic CTE ~5–8 ppm/K vs. SS304 ~17 ppm/K. Repeated cycling from 20°C to 80°C could crack bond or ceramic.

**Recommendation:** Add thermal cycling test (500 cycles, 20–80°C) to performance requirements.

---

**🟡 WARNING – IP20 rating with liquid proximity**

No ingress protection, but spills are inevitable at a desk. Coffee entering housing seam could short PCB.

**Recommendation:** Tongue-and-groove seal for IPX1 drip protection (~€0.10). Conformal coating on PCB (~€0.10).

---

**🟢 NOTE – Consider HUSB238 over FUSB302**

For fixed 12V application, HUSB238 is simpler (resistor strapping, no I²C), cheaper, more available. Removes firmware complexity.

**Recommendation:** Make HUSB238 primary, FUSB302 as alternative.

---

**🟢 NOTE – Switch through-hole LED to SMD**

BASE-015 is 5mm through-hole on an SMT board. Requires separate soldering step.

**Recommendation:** Switch to SMD RGB LED (WS2812B-Mini or 3528 RGB) for single-pass SMT assembly.

---

## Action Items (Priority Order)

1. **Thermal prototype** – validate heat path with representative materials before anything else
2. **Add mug detection sensor** to BOM + clarify method in spec
3. **Decide PD voltage strategy** – mandate 12V or design for 9V
4. **Add voltage regulator** to BOM
5. **Fix BOM cost summary** math
6. **Decide tooling amortisation** treatment
7. **Add EMC provisions** (choke, ferrites) to BOM
8. **Evaluate HUSB238** as primary PD controller
9. **Add thermal cycling test** to performance requirements
10. **Resolve OI-06** (NTC placement validation)
