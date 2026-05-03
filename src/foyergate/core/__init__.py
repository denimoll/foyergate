"""Core domain logic.

Pydantic models (Component, Verdict, Finding) and the orchestrator state
machine that drives a request through fetch → analyze → decide → promote.

This package is **plugin-agnostic**: it must not import from ``adapters``
or ``checkers``. Plugins are wired in via interfaces defined here.
"""
