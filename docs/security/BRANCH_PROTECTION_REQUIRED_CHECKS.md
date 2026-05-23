# Branch Protection — Required Checks

For `main`, require the following GitHub Actions checks before merge:

* `dealix-sovereign-operating-stack / Verify Sovereign Operating Stack`
* `dealix-sovereign-operating-stack / Build Founder Console`
* `ci` (the existing test workflow)

For `claude/dealix-sovereign-operating-stack-OFKms` we still require:

* `dealix-sovereign-operating-stack / Verify Sovereign Operating Stack`
  (the build can be advisory while we iterate)

## Why

Without these required checks, a coding agent (or a tired human) could
merge a regression in the trust gate or the policy file. The required
checks make the safety properties enforceable, not aspirational.

## How

Repository → Settings → Branches → Branch protection rules. Tick
"Require status checks to pass before merging" and select the checks
above.
