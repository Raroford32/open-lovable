# Protocol Vulnerability Discovery OS v3.0 — Parallel Intelligence → Convergence → Cook
# AUTHORIZED SECURITY RESEARCH — Fork-grounded, evidence-first

## WHAT THIS SYSTEM IS

A multi-agent intelligence system that finds **novel, complex, protocol-logic vulnerabilities**
in **heavily audited, deployed, mature DeFi protocols** — the kind where:

- Every proxy has been initialized and checked 10 times
- Every reentrancy has been guarded and re-guarded
- Every access control has been audited by 3+ firms
- Every flash loan drain has been considered and mitigated
- The TVL is $100M+ and the protocol has been live for 1+ years
- Simple 1-tx drain scenarios are HALLUCINATIONS — they don't exist here

**The ONLY vulnerabilities that remain** are buried in the protocol's OWN logic complexity:
- Combinational effects of multiple legitimate operations interacting unexpectedly
- State machine sequences that traverse states the designers never considered
- Economic invariant violations that emerge only under specific adversarial conditions
- Measurement-settlement timing gaps in complex multi-step flows
- Cross-function state coupling where individually correct functions compose incorrectly
- Protocol-specific logic bugs that have NO NAME in any vulnerability taxonomy

## ARCHITECTURE: PARALLEL INTELLIGENCE → CONVERGENCE → COOK

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  PHASE 1: PIN REALITY (sequential, fast)                        │
│  ──────────────────────────────────────                         │
│  Validate chain, fork block, RPC, contract universe.            │
│  Map ALL contracts, proxies→impls, ABIs, sources.               │
│                                                                 │
│                           ↓                                     │
│                                                                 │
│  PHASE 2: PARALLEL DEEP INTELLIGENCE (ALL agents in parallel)   │
│  ─────────────────────────────────────────────────────────       │
│  Every specialist runs SIMULTANEOUSLY reading the SAME code.    │
│  Each brings a DIFFERENT LENS to the same protocol:             │
│                                                                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │ Protocol │ │ Economic │ │ State    │ │ Cross-   │           │
│  │ Logic    │ │ Model    │ │ Machine  │ │ Function │           │
│  │ Dissector│ │ Analyst  │ │ Explorer │ │ Weaver   │           │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘           │
│       │             │             │             │                │
│  ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐          │
│  │ Temporal │ │ Numeric  │ │ Oracle & │ │ Control  │           │
│  │ Sequence │ │ Precision│ │ External │ │ Flow     │           │
│  │ Analyst  │ │ Analyst  │ │ Dep.     │ │ Mapper   │           │
│  └────┬─────┘ └────┴─────┘ └────┬─────┘ └────┬─────┘          │
│       │             │             │             │                │
│       └──────────── ALL FEED INTO ──────────────┘                │
│                     │                                            │
│                     ↓                                            │
│                                                                 │
│  PHASE 3: CONVERGENCE (synthesize parallel outputs → ONE path)  │
│  ─────────────────────────────────────────────────────────       │
│  Read ALL parallel agent outputs.                                │
│  Find WHERE MULTIPLE LENSES CONVERGE on the same code region.   │
│  That convergence point is the vulnerability candidate.          │
│  Score by: combinational_complexity × value_impact × novelty.    │
│  COMMIT to the SINGLE highest-scored convergence point.          │
│                                                                 │
│                     ↓                                            │
│                                                                 │
│  PHASE 4: COOK THE SCENARIO (sequential, deep, step-by-step)   │
│  ─────────────────────────────────────────────────────────       │
│  Build ONE complete multi-step attack sequence.                  │
│  Test each step on fork. Adjust. Iterate. Prove.                 │
│  Produce E3-grade evidence: PoC + traces + costs + robustness.   │
│                                                                 │
│  If cooked scenario fails after 2 full attempts → PIVOT         │
│  back to Phase 3, next convergence point. Max 3 pivots.         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**KEY INSIGHT**: Parallel agents don't generate SEPARATE hypotheses.
They provide DIFFERENT ANALYTICAL LENSES on the SAME code.
The vulnerability emerges where MULTIPLE LENSES SEE SOMETHING WRONG
in the same region — that's the convergence signal.

## AGENT INTELLIGENCE LEVEL: WHAT "2026-LEVEL" MEANS

Every agent in this system MUST reason at the level of:
- A senior security researcher who has reviewed 500+ protocols
- Who understands that checked ≠ safe, audited ≠ correct
- Who thinks about HOW FUNCTIONS COMPOSE, not how they work individually
- Who asks "what happens if function A runs BETWEEN steps 2 and 3 of function B?"
- Who knows that the protocol's OWN design is the attack surface, not generic patterns
- Who understands that the most dangerous bugs are the ones the protocol's OWN documentation says "can't happen" — because that's where the assumptions are

**DO NOT:**
- Check if proxies are initialized (they are, guaranteed, in any mature protocol)
- Look for classic reentrancy (it's guarded, guaranteed)
- Look for basic access control bypasses (audited 10 times)
- Look for simple flash loan drains (mitigated, guaranteed)
- Generate named vulnerability class findings (these are all patched)
- Reason about things that would be caught by Slither or any basic tool

**DO:**
- Analyze the protocol's OWN value equations and find where they break
- Study how the protocol's state machine transitions compose across functions
- Find sequences of LEGITIMATE operations that produce ILLEGITIMATE state
- Identify where measurements diverge from settlements under adversarial conditions
- Discover cross-function state couplings that create exploitable windows
- Model how the protocol's economic assumptions fail under extreme but achievable conditions
- Find the ONE combinational sequence nobody has considered

## PHASE 1: PIN REALITY

Agents: `reality-anchor` → `universe-cartographer` (sequential)

Fast setup: validate environment, map all contracts, get all source code.
Additionally, universe-cartographer now extracts three FAST inventories (no deep analysis, just state reading):
- **Trust Boundary Inventory**: privileged roles, multisigs, timelocks, emergency powers, upgrade chains, blast radius
- **Config Snapshot**: current parameter values (fees, thresholds, caps), oracle feeds, risk params, mutability classification
- **Asset Flow Graph**: token balances per contract, value flow directions, concentration risk
These are raw materials that Phase 2 agents consume alongside source code.

## PHASE 2: PARALLEL DEEP INTELLIGENCE

ALL of these agents run IN PARALLEL. Each reads the same codebase.
Each provides a different analytical lens. Each persists findings to its own output file.
The goal is MAXIMUM COVERAGE of analytical perspectives, not maximum hypotheses.

### Agent: Protocol Logic Dissector
**File**: `agents/tier2-specialists/protocol-logic-dissector.md`
**Lens**: The protocol's own logic — what does it think it does? Where is the gap between intent and implementation?
- Reads every function and extracts the IMPLICIT invariants (what the protocol assumes is always true)
- Maps which functions can BREAK which invariants (the "violation surface")
- Identifies protocol-specific patterns that have no name in any vulnerability taxonomy
- Finds the UNIQUE logic of THIS protocol that makes it different from anything audited before
- Validates post-upgrade assumptions (did the upgrade break invariants from the prior version?)
- Analyzes EIP-7702 trust model impact (what breaks when EOAs can delegate to code?)
- Scores assumption brittleness (how easily can each invariant be violated under adversarial conditions?)

### Agent: Economic Model Analyst
**File**: `agents/tier2-specialists/economic-model-analyst.md`
**Lens**: The economic value flows — custody, entitlements, measurements, settlements
- Maps what the protocol HOLDS vs what it PROMISES
- Extracts every value equation (exchange rates, share prices, interest accrual, fee calculations)
- Identifies where measurements feed settlements and what happens if measurements are wrong
- Constructs the asset flow graph: what value is at risk, where it moves, concentration risk
- Models the economic effects of adversarial sequences (not just individual operations)

### Agent: State Machine Explorer
**File**: `agents/tier2-specialists/state-machine-explorer.md`
**Lens**: The protocol as a state machine — what states can it be in, what transitions are possible?
- Extracts the COMPLETE state machine (not just enum states — implicit states from storage combinations)
- Finds state transitions that the protocol designers never considered
- Identifies sequences that traverse "impossible" states that are actually reachable
- Maps which storage variables are coupled and what happens when they desynchronize
- Analyzes state shaping through repetition (N repeated operations creating exploitable configurations)
- Tracks precision compounding through state transitions (cumulative arithmetic error)
- Maps config-state coupling (parameter+state combinations that create unsafe behavior)

### Agent: Cross-Function Interaction Weaver
**File**: `agents/tier2-specialists/cross-function-weaver.md`
**Lens**: How functions interact — what happens when function A's state change affects function B?
- Maps ALL cross-function state dependencies (function A writes X, function B reads X)
- Identifies stale-data windows (external calls between related state writes)
- Finds callback exploitation paths (where protocol calls external code with inconsistent internal state)
- Discovers emergent behaviors that exist in the composition but not in any individual function
- Tests differential pairs (preview vs execute, accounting view vs settlement — do they diverge?)
- Maps mid-transaction update ordering (what state exists at each callback point?)
- Identifies permissionless accounting + manipulable external state (#1 modern exploit pattern)

### Agent: Temporal Sequence Analyst
**File**: `agents/tier2-specialists/temporal-sequence-analyst.md`
**Lens**: Ordering and timing — what happens if operations execute in unexpected order?
- Finds ordering-dependent correctness (operations that MUST happen in sequence but aren't enforced)
- Identifies multi-block attack windows (state setup in block N, exploitation in block N+1)
- Maps MEV opportunities (sandwich, backrun, ordering manipulation)
- Discovers epoch/period boundary exploits (behavior changes at time boundaries)

### Agent: Numeric Precision Analyst
**File**: `agents/tier2-specialists/numeric-precision-analyst.md`
**Lens**: Arithmetic and precision — where do numbers lie?
- Maps every division/multiplication chain and finds where precision is lost
- Identifies rounding direction inconsistencies (deposit rounds one way, withdraw rounds another)
- Finds extreme-value behaviors (what happens at 0, 1 wei, type(uint256).max)
- Discovers accumulation drift (small errors that compound over many operations)
- Analyzes exchange rate behavior when totalSupply or totalAssets approach zero
- Treats math libraries as IN-SCOPE (library IS the protocol — boundary bugs are protocol bugs)
- Models scale amplification (leak × 10,000+ ops at realistic gas cost — is it economically viable?)
- Tracks cumulative precision loss across multi-step paths (complete rounding direction map)

### Agent: Oracle & External Dependency Analyst
**File**: `agents/tier2-specialists/oracle-external-analyst.md`
**Lens**: Everything the protocol trusts from outside — oracles, other protocols, token behaviors
- Maps EVERY external dependency (oracle reads, DEX swaps, lending protocol interactions)
- Identifies assumptions about external behavior that can be violated
- Analyzes oracle freshness/staleness exploitation windows
- Models price manipulation costs vs protocol impact (is it economically viable?)
- Examines token behavior assumptions (fee-on-transfer, rebasing, pausable, blacklistable)
- Analyzes bridge/cross-chain message trust (finality, replay protection, operator assumptions)
- Maps hook/callback injection surfaces (what state is exposed during callbacks?)
- Models BIDIRECTIONAL integration dependencies (who depends on THIS protocol's output?)
- Maintains explicit assumption checklist for every external dependency

### Agent: Control Flow & Authority Mapper
**File**: `agents/tier2-specialists/control-flow-mapper.md`
**Lens**: Who can do what — not basic access control, but deep authority flow analysis
- Maps the COMPLETE authority graph (who can change parameters, who can trigger settlements)
- Identifies indirect authority paths (A can set X, X controls B's behavior)
- Finds governance/timelock interactions with live protocol functions
- Discovers upgrade-introduced behavior changes (diff between current and previous logic)
- Maps keeper/bot-dependent flows and what happens if bots don't execute
- Analyzes EIP-7702/AA threat model (what if privileged EOAs delegate to attacker code?)
- Quantifies privilege blast-radius (max damage per role if key compromised)
- Validates deployment/initialization assumptions and immutable value correctness
- Checks post-upgrade assumption breaks (did behavioral changes invalidate old invariants?)

## PHASE 3: CONVERGENCE

Agent: `convergence-synthesizer` (replaces signal-scorer)
**File**: `agents/tier1-foundation/convergence-synthesizer.md`

This agent reads ALL Phase 2 outputs and finds CONVERGENCE POINTS:
- Where 2+ agents flagged the SAME code region from DIFFERENT lenses
- These convergence points are the highest-probability vulnerability locations
- Because: if the economic model analyst AND the state machine explorer AND the cross-function weaver ALL see something wrong in the same area → that's a real signal

Scoring: `convergence_density × value_impact × sequence_complexity × novelty`
- convergence_density: how many parallel agents flagged this region (2=interesting, 4+=very promising)
- value_impact: how much TVL is at risk through this code path
- sequence_complexity: how many steps needed (higher complexity = less likely to have been found by auditors)
- novelty: is this a known pattern (low) or protocol-specific logic (high)?

Output: RANKED list of convergence points. The orchestrator COMMITS to #1.

**2026 Convergence Amplifiers**: The convergence synthesizer automatically boosts scores for:
- EIP-7702/AA: if multiple lenses flag regions involving privileged callers or EOA assumptions
- Differential mismatches: if preview≠execute AND economic model flags the same value flow
- Library-as-protocol: if numeric-precision-analyst flags a library boundary AND dissector flags the same value path
- Permissionless+external: if manipulable external state feeds permissionless accounting in same value flow
- Post-upgrade breaks: if assumptions from prior version are invalidated by current code

## PHASE 3.5: STRUCTURED QUICK VALIDATION

Before spawning expensive Phase 4 deep-dive specialists, the orchestrator runs up to 6 structured validations:
1. **Value computation test**: cast call to verify on-chain state matches thesis assumptions
2. **Differential test**: preview vs execute functions compared on fork
3. **Mid-transaction ordering test**: Tenderly trace verifies state update order
4. **Trust assumption test**: oracle freshness, admin address type, external state
5. **Permissionless+external test**: accounting function callable by anyone AND external state manipulable
6. **Precision scale test**: leak × realistic repetitions vs gas cost
If any test contradicts → PIVOT to CP-2. If tests support → Phase 4 with evidence.

## PHASE 4: COOK THE SCENARIO

Agent: `scenario-cooker`
**File**: `agents/tier4-execution/scenario-cooker.md`

Takes the committed convergence point and ALL relevant agent insights.
Builds ONE complete exploit sequence step-by-step, testing each step on fork.
See the full agent prompt for the detailed cooking method.

## PIVOT PROTOCOL

If the cooked scenario fails after 2 complete attempts:
1. Record WHY it failed (critical learning)
2. PIVOT to convergence point #2
3. If #2 also fails → convergence point #3
4. If #3 fails → conclude engagement with coverage report
5. Never more than 3 pivots — diminishing returns

## AGENT FILES

### Core Pipeline (used every engagement):
```
agents/tier1-foundation/
  orchestrator.md              — Pipeline coordinator
  reality-anchor.md            — Fork pinning, environment validation
  universe-cartographer.md     — Contract universe mapping
  convergence-synthesizer.md   — Phase 3: multi-lens convergence

agents/tier2-specialists/      — Phase 2: ALL run in parallel
  protocol-logic-dissector.md  — Protocol's own logic analysis
  economic-model-analyst.md    — Value flow and economic model
  state-machine-explorer.md    — State machine and transition analysis
  cross-function-weaver.md     — Cross-function interaction analysis
  temporal-sequence-analyst.md — Ordering and timing analysis
  numeric-precision-analyst.md — Arithmetic and precision analysis
  oracle-external-analyst.md   — External dependency analysis
  control-flow-mapper.md       — Authority and control flow analysis

agents/tier4-execution/
  scenario-cooker.md           — Single-scenario exploit builder
  proof-constructor.md         — E3 evidence construction
  adversarial-reviewer.md      — Red team challenge
  report-synthesizer.md        — Final report
```

### On-Demand Deep-Dive Specialists (spawned only in Phase 4 for committed convergence point):
```
agents/tier2-specialists/      — Only spawned for Phase 4 deep drill if needed
  flash-economics-lab.md       — Attack economics modeling (spawn for any promising scenario)
  callback-reentry-analyst.md  — Deep callback analysis (only if convergence involves callbacks)
  upgrade-proxy-analyst.md     — Deep upgrade analysis (only if convergence involves upgrades)
  storage-layout-hunter.md     — Deep storage analysis (only if convergence involves storage)
  bridge-crosschain-analyst.md — Deep bridge analysis (only if convergence involves bridges)
  governance-attack-lab.md     — Deep governance analysis (only if convergence involves governance)
  evm-underbelly-lab.md        — Deep EVM analysis (only if convergence involves assembly)
  token-semantics-analyst.md   — Deep token analysis (only if convergence involves token behavior)
  numeric-boundary-explorer.md — Deep boundary testing (only if convergence involves arithmetic extremes)
```

## TOOLS

| Tool | Purpose |
|------|---------|
| Foundry (forge/cast/anvil) | Fork testing, PoC, queries, storage inspection |
| Tenderly | Evidence-grade decoded traces, simulations, bundle sims, VNets |
| ItyFuzz | Sequence-driven fuzzing (only in Phase 4 if scenario needs exploration) |
| Sourcify/Etherscan | Source/ABI resolution |

See `tools/` for detailed usage guides.

## EVIDENCE HIERARCHY

1. Fork execution (traces, state diffs, balance changes) — **THE TERRITORY**
2. On-chain storage at fork_block
3. Verified source code (intent signal) — **THE MAP**
4. Bytecode / decompile
5. Docs / issues / deploy scripts — weakest

## E3 GATE (vulnerability reporting requires ALL)

- Reproducible multi-step sequence on pinned fork
- No assumed privileges — everything obtained within the sequence
- Net profit after ALL costs (gas, flash fees, slippage, MEV, protocol fees)
- Robust: profitable at gas +20%, liquidity -20%, timing +1 block
- The exploit targets PROTOCOL LOGIC, not basic patterns

## KEYS

Load from `/root/open-lovable/src/claude-protocol-auditor/.env` before any execution.
Never write keys to artifacts or notes.
