# Founder Console Policy Enforcement v4

## Purpose
Make Founder Console action requests pass through Dealix Trust Plane before execution.

## Current Phase
Audit-first enforcement:
- every approval writes audit
- reject blocks external action
- request-edit blocks external action

## Next Phase
PolicyEvaluator integration:
- suppression check
- approval class check
- evidence check
- no-overclaim check
- never-auto-execute check

## Required Before External Send
- approval_class A2 approved
- suppression clear
- evidence exists
- no banned claim
- audit written
- actor known

## A3 Rule
A3 actions cannot be automated by Founder Console.
