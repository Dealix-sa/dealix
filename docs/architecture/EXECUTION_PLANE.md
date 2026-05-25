# Hermes Execution Plane

The execution plane is the set of *executors* that the control plane
hands off to once a request has cleared every gate. Executors are
deliberately thin: they do work, produce artifacts, and call
`outcome_gate.REGISTRY.record(...)` before returning.

## Executor contract

```python
def execute(context: RequestContext) -> Any:
    artifact = do_work(context)
    REGISTRY.record(Outcome(
        request_id=context.request_id,
        status=OutcomeStatus.SUCCESS,
        artifacts=(artifact.id,),
        metrics={"latency_ms": ...},
    ))
    return artifact
```

If the executor fails to record an outcome, the control plane treats
the call as denied and rolls forward only the audit record.

## Examples

- Revenue Hunter scoring step → produces ranked leads + Outcome.
- Proposal Factory draft step → produces draft + Outcome.
- AI Trust Kit policy draft → produces evidence pack + Outcome.
