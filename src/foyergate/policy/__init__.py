"""Policy engine integration.

Wraps the OPA HTTP API. Rego policy code is loaded into OPA at deploy
time; FoyerGate sends findings and component metadata as input and
receives a verdict in return.
"""
