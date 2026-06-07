---
type: SERIES-INTAKE
series: outcome-based-cyber
series-title: "Outcome-Based Cyber: The Horizon Constraint"
paper-prefix: OBC
proposed-shape: decalogy (7 core + 3 extension; ships 7–10)
author: Edna (Tier-A first pass)
status: PRE-INTAKE — operator-directed ideation, not promote-ready
date: 2026-06-07
file-on: yks-spine-binder (target repo for the intake issue)
parent-frameworks:
  - HGC³AE² (MR-P1) — Human-governed, Curated Context, Agentically Engineered & Executed
  - Skipjack Protocol (MR-P5) — runtime enforcement
inherits-substrate:
  - Intent Horizon Theory (IH-1 … IH-5) — the horizon primitive, intent-CIA-NR, epistemic weather, horizon-governance gates
  - HGC³AE² Cyber Pillar — agentic-cyber grounding pattern
hands-off-to:
  - Cyber Governance for Emergent Stacks (#348)
  - Governed Autonomy (#349)
---

# SERIES-INTAKE — Outcome-Based Cyber: The Horizon Constraint

> **One line.** Outcome-based cyber is not a metrics program — it is the *acceptance
> criterion* of the intent horizon. This series makes the security **outcome** a
> runtime constraint on the horizon, enforced at the same boundary Skipjack already gates.

## 1. The thesis

The Intent Horizon Theory series specified the horizon as an **intent envelope** — *what
the operator commits the system to doing* — and secured it with intent-CIA-NR (IH-2). What
the IH series never pinned is the **acceptance criterion**: by what measure is the system
judged to be *still inside* its envelope? Today that question is answered in coherence /
alignment terms.

**Outcome-based cyber supplies the missing acceptance criterion — as a constraint, not a
dashboard.** The load-bearing relation:

```
horizon-integral  ⟺  realized security outcome  ∈  operator-pinned outcome envelope
```

This reframes outcome-based cyber (Gartner Outcome-Driven Metrics, CISA / NIST
outcome-driven posture, protection-level agreements, FAIR risk quantification) from a
*boardroom reporting layer* into a **runtime horizon constraint**. The horizon stops being
only an intent envelope and becomes an **outcome envelope**. Activity and control
inventories (NIST SP 800-53, ISO/IEC 27001, SOC 2) demote from *pass criterion* to
*evidence inputs* feeding an outcome attestation.

## 2. The gap this closes (why it is not already in canon)

- **Cyber Governance in Emergent Stacks (#348)** diagnoses the failure: *"conventional cyber
  reports green and the system fails anyway,"* because activity-based controls pass while the
  outcome fails. That paper opens the gap. **It does not prescribe the positive doctrine.**
  This series is the cure to the green-board-but-breached pathology: govern the outcome
  envelope, not the control list.
- **Intent Horizon Theory** supplies the envelope machinery (boundary conditions, weather,
  gates) but bases the envelope on *intent coherence*, not *realized outcome*. Outcome is
  never named as a horizon boundary dimension.
- **The Cyber Pillar** adversarial papers (denial-of-validation, confident-misalignment-
  attack-surface) describe the exact failure this series formalizes — *"outcome breached
  while the system reports green"* is an **outcome-envelope storm under intent-availability
  illusion** — but treat it as an attack class, not as the absence of an outcome-acceptance
  criterion.

The novel primitive is the **outcome envelope**: an operator-pinned, runtime-verifiable,
fail-closed acceptance boundary on the *realized security outcome*, integrated as a fifth
horizon boundary dimension.

## 3. Prior art to anchor (Klaus citation-honesty audit required at promote)

All `[VERIFY:]` — enumerated as citation slots, not yet sourced:

- `[VERIFY:]` Gartner — Outcome-Driven Metrics (ODM) / outcome-driven security framing
- `[VERIFY:]` CISA / NIST — outcome-based / outcome-driven cyber posture language
- `[VERIFY:]` NIST CSF 2.0; NIST SP 800-53 Rev. 5; ISO/IEC 27001:2022; SOC 2 (TSC) — the
  activity/control corpus being re-based as evidence
- `[VERIFY:]` FAIR (Factor Analysis of Information Risk) — quantified-risk-outcome grounding
- `[VERIFY:]` Gartner CARTA — continuous adaptive risk and trust assessment (closest moving
  prior art; distinguish: CARTA adapts *trust*, OBC constrains *outcome*)
- `[VERIFY:]` Protection-Level Agreements (PLA) literature — outcome-as-contract
- `[VERIFY:]` EU AI Act — outcome / risk-tier obligations; sectoral regimes (defense, health,
  financial services)
- `[VERIFY:]` MITRE ATT&CK / ATLAS; OWASP LLM Top 10 — attack-surface placement (P7)

`[INHERIT-PENDING:]` references to IH-1…IH-5, MR-P1, MR-P5, MR-P9, MAO-P10, and the Cyber
Pillar papers resolve on Cowork sourcing pass once those canons reach the required maturity.

## 4. The arc (10 papers — 7 core, 3 extension)

**Cite-without-redefinition (H-21) scope for the whole series:** OBC cites and extends —
never redefines — the intent horizon (IH-1), intent-CIA-NR (IH-2), confident misalignment
(MR-P1 / IH-3), epistemic weather (IH-4), and the Skipjack Protocol (MR-P5 / IH-5). Each
paper's contribution is a *structural extension* layered on the canonical specification.

| # | Slug | Working title | Tier | Inherits |
|---|---|---|---|---|
| OBC-P1 | `outcome-envelope` | The Outcome Envelope: Outcome-Based Cyber as a Horizon Constraint | core | IH-1 |
| OBC-P2 | `controls-to-outcomes` | From Controls to Outcomes: Why Activity-Based Assurance Fails Governed Agentic Systems | core | #348, MR-P1 |
| OBC-P3 | `outcome-cia-nr` | Outcome-CIA-NR: Security Properties of the Outcome Claim | core | IH-2 |
| OBC-P4 | `pinning-the-outcome-envelope` | Pinning the Outcome Envelope: Operator-Defined Acceptance Boundaries | core | IH-1, IH-2 |
| OBC-P5 | `outcome-weather` | Outcome Weather: Reading Realized-Outcome Distance-to-Edge | core | IH-4 |
| OBC-P6 | `outcome-acceptance-gate` | The Outcome-Acceptance Gate: Runtime Enforcement of the Envelope | core | IH-5, MR-P5 |
| OBC-P7 | `outcome-spoofing` | Outcome Spoofing: Attacking the Attestation Layer | extension | Cyber Pillar, MITRE ATLAS |
| OBC-P8 | `evidence-not-acceptance` | Evidence, Not Acceptance: Re-basing the Control Corpus as Attestation Inputs | extension | #348 |
| OBC-P9 | `outcome-bound-slas` | Outcome-Bound SLAs: Protection-Level Agreements as Horizon Contracts | extension | regulatory |
| OBC-P10 | `outcome-governed-federation` | The Outcome-Governed Federation: A Production Account | core-close | MR-P9, MAO-P10 |

### Per-paper thesis

**OBC-P1 — The Outcome Envelope** *(the primitive).*
Names the outcome envelope as a horizon boundary condition. Establishes the constraint
relation (`horizon-integral ⟺ realized outcome ∈ envelope`) and argues outcome-based cyber
is a *runtime constraint*, not a metrics layer. Situates the envelope in HGC³AE² role
ordering: humans pin the outcome envelope, curated context supplies the realized-outcome
evidence, agentic execution operates within the envelope, runtime verification reads
distance-to-edge.

**OBC-P2 — From Controls to Outcomes** *(the foundation / critique).*
The diagnostic half. Control-based and compliance-based assurance measures *activity*, not
*outcome*; in agentic systems the activity↔outcome gap is both wide and silent. Develops the
positive doctrine that #348 opens: the green board is an activity statement, not an outcome
statement. Surveys ODM / CARTA / FAIR as partial prior art and names what they each miss
(none is a *runtime fail-closed constraint* on a governed horizon).

**OBC-P3 — Outcome-CIA-NR** *(the security model).*
Extends intent-CIA-NR (IH-2) to the **outcome claim** itself. Confidentiality (only authorized
governance reads/sets the envelope), integrity (the realized-outcome assertion is not
tampered between measurement and acceptance), availability (the operator can recover the
*current* outcome state in real time, not a cached one), non-repudiation (every
envelope-event — pin, drift, breach, recalibration — is signed and attributable). Distinct
from both data-CIA-NR and intent-CIA-NR; same artifact-vs-property discipline as IH-2.

**OBC-P4 — Pinning the Outcome Envelope** *(the specification).*
How an operator *pins* an outcome envelope: acceptance-boundary classes, acceptable-outcome
regions, residual-risk tolerance, and the envelope as policy-as-code. Specifies the governance
ceremony that sets and re-pins the envelope and the audit record it produces.

**OBC-P5 — Outcome Weather** *(the instruments).*
Extends epistemic weather (IH-4) with the **outcome dimension** — realized-outcome
distance-to-edge as a continuous, readable signal graded clear → drift → fog → storm. The
*green-board-but-breached* case is the canonical **outcome storm under availability illusion**:
the activity instruments read clear while the outcome instrument reads storm. Distinguishing
the two is the operator's core read.

**OBC-P6 — The Outcome-Acceptance Gate** *(the enforcement).*
Extends Skipjack horizon-governance (IH-5) with the **outcome-acceptance gate**: per-action /
per-checkpoint, fail-closed on envelope exit. Specifies firing conditions (drawing on P5
weather classes and P3 outcome-CIA-NR states) and the refusal-of-silent-acceptance discipline
that converts a silent envelope breach into an observable, gated incident.

**OBC-P7 — Outcome Spoofing** *(the adversarial surface).* *[extension]*
The attack surface against the acceptance machinery itself: forging the outcome claim,
poisoning the evidence inputs, attestation replay, envelope-pin staleness as an exploit.
Places the class within MITRE ATLAS / ATT&CK and OWASP LLM Top 10. The structural defense is
P3 (outcome-NR) + P6 (fail-closed gate) — the attestation must itself be a signed,
fresh, non-repudiable artifact.

**OBC-P8 — Evidence, Not Acceptance** *(compliance re-basing).* *[extension]*
The integration doctrine for existing programs. Re-bases the full 800-53 / ISO 27001 /
ATT&CK / SOC 2 corpus as **evidence inputs** to the outcome attestation rather than as the
pass criterion. Shows how a CISO keeps their compliance program intact while subordinating it
to the outcome envelope — controls become *signals*, the envelope is the *verdict*.

**OBC-P9 — Outcome-Bound SLAs** *(commercial + regulatory).* *[extension]*
Turns the outcome envelope into a contractible artifact: protection-level agreements,
outcome-bound SLAs, shared-responsibility expressed in outcome terms. Regulatory placement
(EU AI Act outcome/risk-tier obligations; defense / health / financial-services regimes where
outcome traceability is a compliance requirement, not a nicety).

**OBC-P10 — The Outcome-Governed Federation** *(the empirical capstone).* *(closes series.)*
Demonstrates the outcome constraint operating in the heterogeneous federation documented in
MR-P9 (Operational Plan) / MAO-P10 (Robo Stack): measured outcome-envelope adherence under
contact, which envelope-breach events were caught by the acceptance gate, what the activity
instruments reported during each, and the unit-economics of running the outcome layer. Closes
the series and hands the outcome envelope down to #348 and #349.

## 5. Series-level gate-state

```
PRE-GATE-SEED — not for promote past v0.1-seed.

This intake proposes a series whose v0.1-seed deposits BELOW the inheritance gate
(matching the Governed Autonomy / Cyber Governance discipline). Promote past v0.1-seed
REQUIRES:
  (a) foundational canon at v1.0-canonical — specifically Intent Horizon Theory
      (IH-1…IH-5) and the HGC³AE² Cyber Pillar, plus AI Gov / MAO / EDO substrate;
  (b) #348 Cyber Governance in Emergent Stacks at preprint-complete or canonical
      (OBC-P2 and OBC-P8 inherit it directly);
  (c) Klaus citation-honesty audit clears every [VERIFY:] marker in §3;
  (d) Cowork sourcing pass closes the chain-of-evidence on every [INHERIT-PENDING:]
      reference;
  (e) two-key promote: TM-shape + Klaus-citation + Edna-editorial.

v0.1-seed artifacts are scaffolding seeds — structure, vocabulary, forward map. They
are not drafts and are not promote-ready. Each seed timestamps the IP claim on the
outcome-envelope primitive while the full papers continue in R&E.
```

**Seed-order recommendation:** seed **OBC-P1, P3, P5, P6** first — they carry the load-bearing
primitive, security model, instruments, and gate, and they timestamp the novel IP. P2/P8
follow #348. P10 seeds last (depends on MR-P9 / MAO-P10 production evidence).

## 6. Dependencies & sequencing

- **Hard upstream:** IH Theory at v1.0-canonical; #348 at preprint+ (for P2, P8); MR-P9 /
  MAO-P10 production evidence (for P10).
- **Lateral:** must not collide with the Cyber Pillar adversarial papers — OBC-P7 cites
  denial-of-validation and confident-misalignment-attack-surface; it does not re-derive them.
- **Downstream:** #348 and #349 inherit the outcome envelope as substrate; coordinate so the
  hand-off matches the IH-5 → #348/#349 hand-off already in place.

## 7. Open questions for operator review

1. **Series title** — "Outcome-Based Cyber: The Horizon Constraint" vs. a primitive-first
   title ("The Outcome Envelope"). Title sets the canon's search/identity surface.
2. **Shape** — ship the **core 7** (P1–P6 + P10) and hold P7–P9 as a v2 extension, or commit
   the full decalogy up front? (Intake is written for 10 with a clean core/extension split.)
3. **Relationship to #348** — sibling series that cross-inherit, or is OBC the formal
   "positive doctrine" volume *of* #348? Affects the inheritance graph and gate (b).
4. **Primitive naming** — "outcome envelope" vs. "acceptance envelope" vs. "assurance
   envelope." Locks early; downstream cite-without-redefinition keys off it.

## 8. Success criteria (what "good" looks like at promote)

- The outcome-envelope primitive is specified precisely enough to be policy-as-code (P4) and
  runtime-verifiable (P6) — not a metaphor.
- The constraint relation is shown to *subsume* outcome-driven metrics (ODM) and CARTA as
  special / weaker cases (P2), establishing genuine novelty for the Klaus audit.
- Every paper holds H-21 cite-without-redefinition cleanly against IH / MR canon.
- ≥10 peer-reviewed / authoritative load-bearing citations per paper at promote; v0.1-seed
  enumerates the slots with `[VERIFY:]` markers.
- P10 closes with measured production evidence, not assertion — the same empirical bar MR-P9
  and MAO-P10 set.
