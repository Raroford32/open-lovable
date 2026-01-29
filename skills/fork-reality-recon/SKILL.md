---
name: fork-reality-recon
description: "Establish a reproducible fork environment and on-chain “reality snapshot” for a target protocol: deployed topology, bytecode/source alignment, live gating (pause/caps/oracle/enable flags), and a minimal fork smoke test. Use when starting an investigation, when deployed addresses/topology are uncertain, or before investing in Foundry falsifiers that might be dead due to live guards."
---

# Fork Reality Recon

## Outputs (mandatory artifacts)
- `deployment_snapshot.md` (topology + alignment record)
- fork metadata (chain/chainId/RPC provider, `DEV_FORK_BLOCK`, `PROMOTION_FORK_BLOCK`, timestamps)
- gating checks evidence (pause/caps/oracle/enable flags) attached to the hypothesis ledger
- a fork smoke test (read-only sanity) to avoid tooling drift

## Procedure (run in this order)
1) **Choose two fork blocks**
   - `DEV_FORK_BLOCK`: stable iteration anchor
   - `PROMOTION_FORK_BLOCK`: near-latest block for promotion
2) **Create the deployment snapshot**
   - Enumerate deployed contracts, proxies, implementations, registries, markets, vaults, routers.
   - Record controller addresses (owners/roles/admins) and upgrade wiring.
3) **Align bytecode/source**
   - Confirm deployed bytecode matches repo build outputs (or record mismatches explicitly).
   - If verified sources are needed, prefer Etherscan v2 API or an explorer source-of-truth (do not hardcode API keys into the repo; use env vars).
4) **Verify “live gating” up front (E1 evidence)**
   - pause flags / guardians
   - caps/limits (borrow/mint/per-user/etc.)
   - market enabled flags
   - oracle freshness/bounds checks
   - exit-route liquidity (if your hypotheses require exits)
5) **Create a fork smoke test**
   - Pin `DEV_FORK_BLOCK`.
   - Load key addresses from the snapshot.
   - Perform only read-only assertions (code size, proxy impl, key config vars).

## What to do when something is unclear
- If any deployed address/topology is uncertain: stop and finish the snapshot first (otherwise you audit the wrong system).
- If bytecode alignment fails: treat it as a first-class finding; do not proceed assuming equivalence.

## Primary Reference (load only as needed)
- `/root/.codex/skills/layered-codegraph-creator/references/fork-reality-recon.md`

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Not every skill requires all three types of resources.**
