# Client Ops Max

## Purpose

Client Ops Max turns Dealix into a complete service delivery OS for the client after the sale.

## What it does for the client

- prepares the client workspace
- collects intake requirements
- maps workflow and owners
- builds command queue
- prepares draft routes
- prepares daily proof notes
- prepares weekly proof report
- prepares next-week action plan
- prepares renewal or expansion brief

## Client input is minimized

The client only needs to approve sample data use, confirm owners, review proof, and approve external actions.

## Delivery lifecycle

sale_ready, intake, diagnosis, setup, daily_ops, weekly_review, renewal.

## Run

```bash
python client_ops_max.py
python -m pytest -q test_client_ops_max.py
```

## Rule

Dealix automates internal preparation, reporting, proof, queue building, and renewal planning. External sends and final commitments remain approval-gated.
