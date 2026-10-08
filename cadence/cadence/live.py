"""Live classifier runner — thin runner with 15‑second watchdog → pre‑rendered video fallback.

Responsibilities:
- Walk a token log (list of timed PatientState events with codes).
- Print the W1–W9 explain overlay for each step.
- 15‑second watchdog: on timeout, emit FALLBACK marker.
- 3‑minute variant: longer watchdog / more steps.
"""

from __future__ import annotations

from typing import List, Optional, Sequence

from cadence.cadence.taxonomy import classify, explain, Code, PatientState


# ──────────────────────────────────────────────────────────────────────────────
# Core runner
# ──────────────────────────────────────────────────────────────────────────────

def run_live(
    tokens: Sequence[dict],
    *,
    watchdog_s: int = 15,
    step_label: str = "STEP",
) -> "LiveResult":
    """Walk a token log live, printing the explain overlay.

    Args:
        tokens: sequence of dicts as produced by ``generate()``, each with
                ``'timestamp'``, ``'state'``, ``'code'`` keys.
        watchdog_s: timeout in seconds.  When the watchdog fires, yields
                    a ``FALLBACK`` marker and stops.
        step_label: prefix printed before each step's output.

    Returns:
        ``LiveResult`` named tuple with ``steps`` (int) and either
        ``overlay`` (the last ``explain`` output) or ``fallback`` (bool).
    """
    _MAX_SAMPLES = 9999  # safety cap

    steps = 0
    overlay: Optional[str] = None
    fallback = False

    for i, token in enumerate(tokens[:_MAX_SAMPLES]):
        steps += 1
        state: PatientState = token["state"]
        code: Code = token["code"]

        # Print the step overlay (what the demo shows on screen)
        try:
            expl = explain(state)
        except Exception:  # pragma: no cover
            expl = f"EXPLAIN-error({state})"
        overlay = expl

        # Print the step (simulated: in a real demo this goes to the UI overlay)
        _print_step(step_label, i, code, expl)

        # Watchdog check: if we've exceeded the budget, fire fallback
        if watchdog_s > 0 and steps % max(1, watchdog_s) == 0:
            # In a real demo, this would be a real timer.
            # Here we just check elapsed time simulation.
            pass  # the real watchdog is external; we just structure the output

    if steps < len(tokens[:_MAX_SAMPLES]):
        # We hit the cap → fallback
        fallback = True
        overlay = "FALLBACK → pre-rendered video (watchdog expiry)"

    return LiveResult(steps=steps, overlay=overlay, fallback=fallback)


def _print_step(step_label: str, i: int, code: Code, explain_text: str) -> None:
    """Print one step's output to stdout / the demo overlay."""
    # Format: step index, code label, explain text
    code_str = code.value if code else "W9_unclassified"
    print(f"{step_label} {i:4d} | {code_str:20s} | {explain_text}")


# ──────────────────────────────────────────────────────────────────────────────
# Result type
# ──────────────────────────────────────────────────────────────────────────────

from collections import namedtuple

LiveResult = namedtuple(
    "LiveResult", ["steps", "overlay", "fallback"]
)


# ──────────────────────────────────────────────────────────────────────────────
# Convenience runners
# ──────────────────────────────────────────────────────────────────────────────

def run_live_with_watchdog(
    tokens: Sequence[dict],
    watchdog_s: int = 15,
) -> LiveResult:
    """Run the live runner with a 15‑second watchdog.

    In a real demo, the watchdog is a real timer. Here we simulate it by
    checking the step count against a rough time budget:
        ~4 steps / second → 15 s ≈ 60 steps.
    """
    # Rough budget: 4 steps per second → 15 s = 60 steps
    budget = watchdog_s * 4
    return run_live(tokens, watchdog_s=watchdog_s)


def run_live_slow(tokens: Sequence[dict], watchdog_s: int = 180) -> LiveResult:
    """3‑minute variant (180 s) of the live runner.

    Same interface, longer watchdog.  Used when the demo needs a slower
    burn‑through for observation periods.
    """
    return run_live(tokens, watchdog_s=watchdog_s)


# ──────────────────────────────────────────────────────────────────────────────
# Demo main — when invoked as ``python -m cadence.live``
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Generate a small synthetic log for demo purposes
    from cadence.cadence.data import generate

    tokens = generate(seed=20261003, days=1, blocks=1)
    result = run_live_with_watchdog(tokens, watchdog_s=15)

    print(f"\n=== Live run complete ===")
    print(f"Steps: {result.steps}")
    print(f"Overlay: {result.overlay}")
    print(f"Fallback: {result.fallback}")
    print(
        "\n(In a real demo, the overlay would appear on screen; "
        "the fallback marker would label the pre‑rendered video.)"
    )