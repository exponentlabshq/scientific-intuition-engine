# Structural Reformulation Verification: 2026-09-01-physical-acoustic-resonance-x-physical-mechanical-vibration

**Verifies**: `hypotheses/2026-09-01-physical-acoustic-resonance-x-physical-mechanical-vibration.md` (Level 3 structural block)
**Verified**: 2026-09-01 · **Method**: sharpen_structural_mapping.py (gpt-4o structural derivation + verify_hypothesis.classify() re-verify)

## Object mapping
- natural frequency of acoustic system → natural frequency of mechanical system
- sound wave amplitude → displacement amplitude of mechanical system
- acoustic impedance → mechanical impedance

## Invariant claimed
The resonance condition: maximum amplitude occurs at natural frequencies.

## Structural reasoning
In acoustic resonance, the condition for resonance is that the frequency of the external sound wave matches the natural frequency of the acoustic system, leading to a maximum amplitude of oscillation. Mathematically, this is expressed as the system's impedance being minimized, allowing maximum energy transfer and thus maximum amplitude.\n\nIn mechanical systems, resonance similarly occurs when the frequency of an external force matches the system's natural frequency, leading to maximum displacement amplitude. The mechanical impedance is minimized under these conditions, allowing maximum energy transfer.\n\nThe mapping f is as follows:\n- The natural frequency of the acoustic system maps to the natural frequency of the mechanical system.\n- The amplitude of the sound wave maps to the displacement amplitude of the mechanical system.\n- The acoustic impedance maps to the mechanical impedance.\n\nUnder this mapping, the condition for resonance (minimum impedance leading to maximum amplitude) holds in both domains, showing that the structural relationship is preserved.

## Re-verify verdict: **ADJACENT_ACTIVE**

The provided sources confirm that both acoustic and mechanical systems exhibit resonance when subjected to external forces at their respective natural frequencies, leading to maximum amplitude responses. Additionally, the concept of impedance is relevant in both domains, affecting the system's response to external forces.
