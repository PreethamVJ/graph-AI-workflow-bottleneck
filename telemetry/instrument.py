"""
Langfuse instrumentation for CrewAI.

ORDER MATTERS -- verified against langfuse 4.12.0 + openinference-instrumentation-crewai:

  get_client()                     # installs Langfuse as the OTEL TracerProvider
  CrewAIInstrumentor().instrument() # hooks into that provider

If you call instrument() before get_client(), CrewAI spans go to the default
ProxyTracerProvider (a no-op) and nothing appears in Langfuse -- which is
exactly the bug that caused "Waiting for first trace" even though the batch
ran successfully.
"""

from __future__ import annotations

import os

_instrumented = False


def instrument_crewai() -> None:
    global _instrumented
    if _instrumented:
        return

    os.environ.setdefault("LANGFUSE_HOST", "https://cloud.langfuse.com")

    # Step 1: initialise the Langfuse client. This installs Langfuse as the
    # global OTEL TracerProvider. Must happen before any instrumentation.
    from langfuse import get_client
    get_client()

    # Step 2: hook CrewAI into the now-configured OTEL provider.
    from openinference.instrumentation.crewai import CrewAIInstrumentor
    CrewAIInstrumentor().instrument()

    _instrumented = True