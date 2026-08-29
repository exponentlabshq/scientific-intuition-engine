"""
retry.py — real retry/backoff for OpenAI calls, added 2026-08-29 after a
verification audit found none existed anywhere in the pipeline. Every
client.chat.completions.create() call site (hypothesis_engine.py,
verify_hypothesis.py, refute_hypothesis.py, audit_agent.py) was a single
unguarded call -- a transient rate limit or timeout crashed that stage
outright, with no distinction from a real, permanent failure.

Only retries errors that are actually transient. Auth failures, bad
requests, and content-policy rejections retrying won't fix -- those raise
immediately, unretried, so a real misconfiguration still fails fast and
loud rather than burning three attempts on something that will never
succeed.
"""
import random
import time

import openai

RETRYABLE_EXCEPTIONS = (
    openai.APIConnectionError,
    openai.APITimeoutError,
    openai.RateLimitError,
    openai.InternalServerError,  # OpenAI 5xx
)


def call_with_retry(fn, *args, max_retries: int = 3, base_delay: float = 2.0, **kwargs):
    """Call fn(*args, **kwargs), retrying on transient OpenAI errors with
    exponential backoff + jitter. Re-raises the last exception if every
    attempt fails -- callers see a real failure, not a silently swallowed
    one, once retries are exhausted."""
    last_exc = None
    for attempt in range(max_retries + 1):
        try:
            return fn(*args, **kwargs)
        except RETRYABLE_EXCEPTIONS as e:
            last_exc = e
            if attempt == max_retries:
                break
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            print(f"    ! transient OpenAI error ({type(e).__name__}: {e}) — retry {attempt + 1}/{max_retries} in {delay:.1f}s")
            time.sleep(delay)
    raise last_exc
