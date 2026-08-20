# Synthetic company demo

This directory is the public entry point for the synthetic end-to-end example.
It contains no real company, customer, employee, chat, document or source data.

Run the canonical walkthrough from the repository root:

~~~bash
python3 -m unittest discover -s skills/topprismwiki/tests -v
python3 skills/topprismwiki/scripts/check_public_safety.py .
~~~

For the full preview, reviewed update, validation, query, graph and dashboard
commands, see [the English walkthrough](../../docs/en/synthetic-walkthrough.md)
or [the Chinese walkthrough](../../docs/zh-CN/synthetic-walkthrough.md).

The expected invariants are:

- preview records input units and does not write formal pages;
- update requires explicit authorization and a review package;
- successful update is atomic and produces a commit report;
- evidence-insufficient units remain retryable or reviewable;
- query and graph outputs identify formal state and do not promote candidates.
