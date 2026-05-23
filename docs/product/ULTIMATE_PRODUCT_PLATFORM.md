# Ultimate Product Platform

The product platform turns repeated delivery patterns into productized
offers.

## Pipeline

1. Productization agent observes `proposal_queue.csv`.
2. When it detects N proposals with the same scope theme, it inserts a
   row in `product/productization_candidates.csv`.
3. The Founder Console renders these in `/product`.
4. The founder decides whether to package the candidate as a public
   offer. Packaging is an A2 action; publishing the public offer is A3.

## What this enables

* Faster proposal drafts (agent reuses the package skeleton).
* Predictable delivery (agent reuses the delivery playbook).
* Trustworthy economics (`ai_unit_economics.csv` rolls up by package).
