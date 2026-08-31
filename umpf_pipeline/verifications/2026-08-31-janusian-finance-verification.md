# Verification: Janusian — Finance — options pricing and volatility smile

**Verifies**: `hypotheses/2026-08-31-janusian-finance.md`
**Verified**: 2026-08-31 · **Method**: OpenAI web_search (gpt-4o-mini) + classification, single call (`verify_hypothesis.py`, unattended)

## Verdict: **COLLISION**

## Queries
- `Black-Scholes model options pricing`
- `volatility smile phenomenon in options trading`
- `Friedman’s theory on market volatility`
- `Merton model and implied volatility`
- `research on options pricing and volatility skew`

## What was found
The Black-Scholes model assumes constant volatility, leading to a flat implied volatility curve. However, real markets exhibit a volatility smile, where implied volatility varies across strike prices, indicating deviations from the model's assumptions. ([en.wikipedia.org](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model?utm_source=openai)) This pattern suggests that the Black-Scholes model's assumptions about constant volatility and log-normal returns are inconsistent with observed market behavior. ([en.wikipedia.org](https://en.wikipedia.org/wiki/Volatility_smile?utm_source=openai)) Alternative models, such as stochastic volatility models, have been developed to address these discrepancies. ([stockanalysis.org](https://stockanalysis.org/options-pricing-and-trading/black-scholes-and-non-gaussian-price-distributions/2025/?utm_source=openai))

## Reasoning
The observed volatility smile contradicts the Black-Scholes model's assumption of constant volatility, indicating that the model does not fully capture market dynamics.
