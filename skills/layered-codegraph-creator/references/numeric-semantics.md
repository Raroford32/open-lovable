# Numeric Semantics (units, scale, rounding, dust)

Goal: make numbers mean something concrete so you can detect drift/rounding primitives instead of hand-waving “modulo rounding”.

## Minimal schema extensions (declare only if you need them)
Node types (examples):
- `UNIT` (ex: `UNIT:underlying`, `UNIT:shares`, `UNIT:mantissa1e18`, `UNIT:usd1e8`, `UNIT:block`, `UNIT:seconds`)
- `ROUNDING_RULE` (optional, only if complex)
- `THRESHOLD` (dust, min/max)

Edge types (examples):
- `HAS_UNIT` (`VAR/FUNC -> UNIT`) with `scale=1e18|1e8|raw`
- `CONVERTS` (`FUNC -> UNIT`) with `from=... to=...`
- `ROUNDS` (`FUNC/VAR -> ROUNDING_RULE`) with `dir=down|up|bankers|towardZero`
- `HAS_THRESHOLD` (`FUNC/VAR -> THRESHOLD`) with `kind=dust|minOut|maxIn|cap`

## Procedure: annotate units and rounding where they matter
1. For every value-bearing `VAR` (balances, shares, debts, indices, reserves, fees), attach a unit and scale.
2. For every conversion function (exchange rate, share math, price math), record:
   - input/output units
   - scaling factors
   - rounding direction (truncate/divide, `mulDiv` behavior, integer division)
3. For every check that uses a converted value, record:
   - which unit is being checked (raw token units vs scaled mantissa)
   - where rounding happens *relative to the check* (before/after)
4. Look for accumulation surfaces:
   - repeated mint/redeem with dust
   - repay/borrow with share-based repay
   - fee calculation that truncates
   - interest index updates that truncate each block

## Evidence discipline
For each rounding-relevant claim, attach:
- the exact expression (or instruction chain) where rounding occurs
- a smallest falsifier: “repeat operation N times with chosen amounts” and the expected drift sign

