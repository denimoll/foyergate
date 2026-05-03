"""Background workers.

The API server enqueues scan jobs; workers (powered by arq) pick them
up, run the checker pipeline, evaluate the policy, and persist the
verdict.
"""
