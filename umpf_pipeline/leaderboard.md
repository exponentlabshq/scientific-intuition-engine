# Eureka Engine — Leaderboard

**Regenerated from**: `verification-log.jsonl` (750 entries — 749 scored, 1 held out). Do not hand-edit this file — re-run `python3 score_hypotheses.py`.

Ranked by **confidence tier** first, points as a tie-breaker within a tier only — see `score_hypotheses.py`'s `tier_for()` docstring for the real bug this replaced (a refuted claim could outrank a genuine survivor under flat points). Self-reported novelty is shown per entry as context but is not scored (near-zero predictive signal, Failure 5). Tiers, high to low confidence: ✅ Peer-Endorsed → 🛡️ Survived Refutation → 🗺️ Verified, Unrefuted → ⏳ Pending → 🌗 Contested → 💀 Refuted / Rejected.

## Department performance

Per-mode averages, computed fresh from the live ledger every run — not a one-time snapshot. A high NO_SIGNAL rate isn't a mode failing; it's that mode's real base rate for reaching a novel, unresolved claim.

| Mode | n | Avg points | NO_SIGNAL rate |
|---|---|---|---|
| janusian | 216 | +29.5 | 8% |
| bisociation | 275 | +17.9 | 25% |
| homospatial | 246 | +11.5 | 36% |
| case-study | 12 | +6.2 | 25% |

## Pre-filter signal (Phase 0.5, observe-only)

The composability pre-filter never gates generation — it only logs a signal (see `prefilter_observe.py`). This is that signal's real, live correlation with downstream outcome, joined by slug against the ledger fresh every run — not a one-time control-test result.

**By pair type:**

| Pair type | n | Good outcome |
|---|---|---|
| formalism-shaped | 42 | 76.2% |
| narrative-shaped | 97 | 74.2% |
| mixed-uncertain | 213 | 62.9% |

**By pre-filter recommendation:**

| Recommendation | n | Good outcome |
|---|---|---|
| would_promote | 9 | 88.9% |
| would_deprioritize | 301 | 65.8% |

## Ranking

| Rank | Tier | Pairing | Points | Verdict | Refutation | Pair type | Badges |
|---|---|---|---|---|---|---|---|
| 1 | 🛡️ Survived Refutation | Literature — unreliable-narrator technique | **+67** | ADJACENT_ACTIVE | 67% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 🛡️ Survived the Gauntlet 🔬🔥 Actively Researched (current) |
| 2 | 🛡️ Survived Refutation | Computer science — compiler instruction scheduling | **+60** | ADJACENT_ACTIVE | 100% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 🛡️ Survived the Gauntlet 🔬 Actively Researched (historical) |
| 3 | 🛡️ Survived Refutation | Fisheries — stock recruitment dynamics | **+57** | ADJACENT_ACTIVE | 67% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 🛡️ Survived the Gauntlet 🔬 Actively Researched |
| 4 | 🛡️ Survived Refutation | Cognitive psychology — working memory and chunking | **+57** | ADJACENT_ACTIVE | 67% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 🛡️ Survived the Gauntlet 🔬 Actively Researched |
| 5 | 🛡️ Survived Refutation | Zoology — animal migration navigation | **+57** | ADJACENT_ACTIVE | 67% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 🛡️ Survived the Gauntlet 🔬 Actively Researched |
| 6 | 🛡️ Survived Refutation | Mathematics — topology — knot invariants | **+52** | ADJACENT_ACTIVE | 67% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 🛡️ Survived the Gauntlet 🔬 Actively Researched (historical) |
| 7 | 🛡️ Survived Refutation | Nash — Game Theory × Evolutionary Biology | **+20** | COLLISION | 100% survived | — | 🧬 Bisociative 🏆 Nobel Ground Truth (calibration benchmark, not engine-generated) 🏛️ Established Department 🛡️ Survived the Gauntlet |
| 8 | 🛡️ Survived Refutation | Kahneman & Tversky — Cognitive Bias × Rational-Choice Theory | **+12** | COLLISION | 67% survived | — | 🧬 Bisociative 🏆 Nobel Ground Truth (calibration benchmark, not engine-generated) 🏛️ Established Department 🛡️ Survived the Gauntlet |
| 9 | 🛡️ Survived Refutation | Planck — Quantization × Thermodynamics | **+12** | ADJACENT_ACTIVE | 67% survived | — | 🧬 Bisociative 🏆 Nobel Ground Truth (calibration benchmark, not engine-generated) 🗺️ Frontier Research Group 🛡️ Survived the Gauntlet |
| 10 | 🛡️ Survived Refutation | Jacob & Monod — Gene Regulation × Control Engineering | **+12** | NO_SIGNAL | 67% survived | — | 🧬 Bisociative 🏆 Nobel Ground Truth (calibration benchmark, not engine-generated) 🛡️ Survived the Gauntlet |
| 11 | 🛡️ Survived Refutation | Ostrom — Commons Governance × Ecology | **+12** | ADJACENT_ACTIVE | 67% survived | — | 🧬 Bisociative 🏆 Nobel Ground Truth (calibration benchmark, not engine-generated) 🗺️ Frontier Research Group 🛡️ Survived the Gauntlet |
| 12 | 🛡️ Survived Refutation | Simon — Bounded Rationality × Heuristic Search | **+12** | COLLISION | 67% survived | — | 🧬 Bisociative 🏆 Nobel Ground Truth (calibration benchmark, not engine-generated) 🏛️ Established Department 🛡️ Survived the Gauntlet |
| 13 | 🛡️ Survived Refutation | Hayek — Dispersed Knowledge × Market Price Signals | **+12** | ADJACENT_ACTIVE | 67% survived | — | 🧬 Bisociative 🏆 Nobel Ground Truth (calibration benchmark, not engine-generated) 🗺️ Frontier Research Group 🛡️ Survived the Gauntlet |
| 14 | 🛡️ Survived Refutation | Einstein — Special Relativity × Maxwell — Electromagnetism | **+12** | ADJACENT_ACTIVE | 67% survived | — | 🧬 Bisociative 🏆 Nobel Ground Truth (calibration benchmark, not engine-generated) 🗺️ Frontier Research Group 🛡️ Survived the Gauntlet |
| 15 | 🛡️ Survived Refutation | Oceanography — thermocline stratification | **+12** | NO_SIGNAL | 67% survived | — | 🎭 Janusian 🛡️ Survived the Gauntlet |
| 16 | 🗺️ Verified, Unrefuted | Linguistics — Historical Sound Change | **+55** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 17 | 🗺️ Verified, Unrefuted | Self-Assembly of Molecular Structures × Gaming Narrative Systems | **+55** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 18 | 🗺️ Verified, Unrefuted | Human Trust Variance × Cryptography — Zero-Knowledge Proofs | **+55** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 19 | 🗺️ Verified, Unrefuted | Physical Quantum Measurement | **+55** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 20 | 🗺️ Verified, Unrefuted | Physical Mechanical Spring Systems × Human Emotional Fluctuation | **+55** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 21 | 🗺️ Verified, Unrefuted | Creative Narrative Arc Development × Informational Distributed Consensus | **+55** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 22 | 🗺️ Verified, Unrefuted | Self-Assembly of Molecular Structures × Informational Event-Driven Systems | **+55** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 23 | 🗺️ Verified, Unrefuted | Adaptive Immune Memory × Human Urban Planning | **+55** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 24 | 🗺️ Verified, Unrefuted | Law × Informational Database State | **+55** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 25 | 🗺️ Verified, Unrefuted | Swarm Robotics × Physical Acoustic Resonance | **+55** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 26 | 🗺️ Verified, Unrefuted | Cognitive Attention Map Evolution × Creative Artistic Critique | **+55** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 27 | 🗺️ Verified, Unrefuted | Social Systems × Human Team Collaboration | **+55** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 28 | 🗺️ Verified, Unrefuted | Creative Narrative Arc Development × Human Committee Formation | **+55** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 29 | 🗺️ Verified, Unrefuted | Creative Artistic Critique × Creative Idea Uncertainty | **+55** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 30 | 🗺️ Verified, Unrefuted | Swarm Robotics × Creative Performance Monitoring | **+55** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 31 | 🗺️ Verified, Unrefuted | Informational Database Sharding | **+55** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 32 | 🗺️ Verified, Unrefuted | Climatology — feedback loops in ice-albedo effect | **+55** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 33 | 🗺️ Verified, Unrefuted | Language Linguistics × Military Strategy | **+55** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 34 | 🗺️ Verified, Unrefuted | Biological Systems × Creative Musical Motif Deviation | **+55** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 35 | 🗺️ Verified, Unrefuted | Ocean Current Circulation × Epigenetics | **+55** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 36 | 🗺️ Verified, Unrefuted | Healthcare (Human & Social Systems) × Creative Idea Uncertainty | **+55** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 37 | 🗺️ Verified, Unrefuted | Creative Inspiration Variability | **+55** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 38 | 🗺️ Verified, Unrefuted | Human Financial Market Systems | **+55** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 39 | 🗺️ Verified, Unrefuted | Education (Information & Intelligence Systems) × Human Meeting Participation | **+55** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 40 | 🗺️ Verified, Unrefuted | Climate Science × Gaming Narrative | **+55** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 41 | 🗺️ Verified, Unrefuted | Human Urban Planning × Physical Ecosystem Succession | **+55** | ADJACENT_ACTIVE | — | narrative-shaped | 🪞 Homospatial 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 42 | 🗺️ Verified, Unrefuted | Informational Error Probability × Physical Circuit Evolution | **+55** | ADJACENT_ACTIVE | — | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 43 | 🗺️ Verified, Unrefuted | Supply Chain Logistics × Cryptography | **+55** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 44 | 🗺️ Verified, Unrefuted | Human Urban Planning | **+55** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 45 | 🗺️ Verified, Unrefuted | Sports Athletics × Physical Thermal Variation | **+55** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 46 | 🗺️ Verified, Unrefuted | Human Financial Trading Algorithms × Physical Power Grid Orchestration | **+55** | ADJACENT_ACTIVE | — | narrative-shaped | 🪞 Homospatial 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 47 | 🗺️ Verified, Unrefuted | Physical Gear System Mechanics | **+55** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 48 | 🗺️ Verified, Unrefuted | Physical Power Grid Orchestration | **+55** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 49 | 🗺️ Verified, Unrefuted | Epigenetics × Physical Magnetic Fluctuation | **+55** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 50 | 🗺️ Verified, Unrefuted | Creative Improvisation Coordination × Physical Evolutionary Selection | **+55** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 51 | 🗺️ Verified, Unrefuted | Healthcare × Creative Album Production Orchestration | **+55** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 52 | 🗺️ Verified, Unrefuted | Music Theory × Physical Acoustic Resonance | **+55** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 53 | 🗺️ Verified, Unrefuted | Control Theory — Kalman Filtering × Quantum Physics | **+55** | ADJACENT_ACTIVE | — | formalism-shaped | 🪞 Homospatial 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 54 | 🗺️ Verified, Unrefuted | Thermodynamics × Creative Inspiration Variability | **+55** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 55 | 🗺️ Verified, Unrefuted | Urban Planning × Telecommunications | **+55** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 56 | 🗺️ Verified, Unrefuted | Knowledge Systems × Physical Power Grid Orchestration | **+55** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 57 | 🗺️ Verified, Unrefuted | Comedy × Cognitive AI Attention | **+55** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 58 | 🗺️ Verified, Unrefuted | Economics × Cognitive AI Attention | **+55** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 59 | 🗺️ Verified, Unrefuted | Game Theory × Gaming Narrative | **+55** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 60 | 🗺️ Verified, Unrefuted | Informational Routing Policy Enforcement × Physical Evolutionary Selection | **+55** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 61 | 🗺️ Verified, Unrefuted | Cognitive AI Pipeline Orchestration | **+55** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 62 | 🗺️ Verified, Unrefuted | Cognitive Streaming Data Processing × Creative Film Production Orchestration | **+55** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 63 | 🗺️ Verified, Unrefuted | Banking — fractional reserve credit multiplier | **+55** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 64 | 🗺️ Verified, Unrefuted | Dance — choreographic phrase repetition | **+55** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 65 | 🗺️ Verified, Unrefuted | Metallurgy — annealing and grain refinement | **+55** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 66 | 🗺️ Verified, Unrefuted | Military strategy — asymmetric guerrilla tactics | **+55** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 67 | 🗺️ Verified, Unrefuted | Informational Database Sharding × Informational Distributed Consensus | **+55** | ADJACENT_ACTIVE | — | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 68 | 🗺️ Verified, Unrefuted | Physics — particle physics — Standard Model symmetry breaking × Physics — optics — diffraction and interference patterns | **+55** | ADJACENT_ACTIVE | — | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 69 | 🗺️ Verified, Unrefuted | Physical Circuit Evolution × Physical Mechanical Vibration | **+55** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 70 | 🗺️ Verified, Unrefuted | Ethics — trolley-problem moral reasoning | **+55** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬🔥 Actively Researched (current) |
| 71 | 🗺️ Verified, Unrefuted | Ecology × Telecommunications | **+45** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 72 | 🗺️ Verified, Unrefuted | Materials Science — Crystal Lattice Defects | **+45** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched |
| 73 | 🗺️ Verified, Unrefuted | Anthropology × Military Strategy | **+45** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 74 | 🗺️ Verified, Unrefuted | Creative Musical Motif Deviation × Evolutionary Biology — Punctuated Equilibrium | **+45** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 75 | 🗺️ Verified, Unrefuted | Human Financial Trading Algorithms × Ecology — Predator-Prey Population Dynamics | **+45** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 76 | 🗺️ Verified, Unrefuted | Creative Block | **+45** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched |
| 77 | 🗺️ Verified, Unrefuted | Physical Chemical Reaction Networks × Human Committee Formation | **+45** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group 🔬 Actively Researched |
| 78 | 🗺️ Verified, Unrefuted | Culinary Arts (Creative & Performance Systems) | **+45** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched |
| 79 | 🗺️ Verified, Unrefuted | Epidemiology — Herd Immunity Thresholds | **+45** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched |
| 80 | 🗺️ Verified, Unrefuted | Physical Ecosystem Succession × Physical Immune System | **+45** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 81 | 🗺️ Verified, Unrefuted | Auction Theory × Human Defense Coordination | **+45** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 82 | 🗺️ Verified, Unrefuted | Biological Systems × Human Social Network Dynamics | **+45** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group 🔬 Actively Researched |
| 83 | 🗺️ Verified, Unrefuted | Gaming Narrative × Cognitive Attention Map Evolution | **+45** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 84 | 🗺️ Verified, Unrefuted | Biological Systems × Informational Scientific Experiment Orchestration | **+45** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 85 | 🗺️ Verified, Unrefuted | Creative Narrative Arc Development × Human Team Collaboration | **+45** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 86 | 🗺️ Verified, Unrefuted | Human Meeting Participation | **+45** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched |
| 87 | 🗺️ Verified, Unrefuted | Immunology × Behavioral Psychology | **+45** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group 🔬 Actively Researched |
| 88 | 🗺️ Verified, Unrefuted | Architecture — load-bearing structural design | **+45** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched |
| 89 | 🗺️ Verified, Unrefuted | Telecommunications × Quantum Physics | **+45** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group 🔬 Actively Researched |
| 90 | 🗺️ Verified, Unrefuted | Creative Musical Composition | **+45** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched |
| 91 | 🗺️ Verified, Unrefuted | Urban Planning × Creative Improvisation Adjustment | **+45** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 92 | 🗺️ Verified, Unrefuted | Creative Instrument Track Development | **+45** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched |
| 93 | 🗺️ Verified, Unrefuted | Physical Evolutionary Selection | **+45** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched |
| 94 | 🗺️ Verified, Unrefuted | Chemistry × Human Social Network Dynamics | **+45** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 95 | 🗺️ Verified, Unrefuted | Informational Software Version Control | **+45** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched |
| 96 | 🗺️ Verified, Unrefuted | Telecommunications × Cognitive Streaming Data Processing | **+45** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 97 | 🗺️ Verified, Unrefuted | Urban Planning × Cryptography | **+45** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group 🔬 Actively Researched |
| 98 | 🗺️ Verified, Unrefuted | Human Social Influence × Informational Sensor Networks | **+45** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 99 | 🗺️ Verified, Unrefuted | Music Theory × Human Social Network Dynamics | **+45** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 100 | 🗺️ Verified, Unrefuted | Healthcare × Creative Film Production Orchestration | **+45** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 101 | 🗺️ Verified, Unrefuted | Urban Planning × Physical Chemical Reaction Networks | **+45** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 102 | 🗺️ Verified, Unrefuted | Anthropology × Creative Film Production Orchestration | **+45** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 103 | 🗺️ Verified, Unrefuted | Urban Planning × Informational Sensor Networks | **+45** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 104 | 🗺️ Verified, Unrefuted | Education (Information & Intelligence Systems) | **+45** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched |
| 105 | 🗺️ Verified, Unrefuted | Chemistry × Physical Immune System | **+45** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 106 | 🗺️ Verified, Unrefuted | Cognitive Reinforcement Learning × Informational OS Thread Scheduling | **+45** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 107 | 🗺️ Verified, Unrefuted | Physical Thermal Variation | **+45** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched |
| 108 | 🗺️ Verified, Unrefuted | Organizational Theory × Creative Inspiration Variability | **+45** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 109 | 🗺️ Verified, Unrefuted | Urban Planning × Agriculture | **+45** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 110 | 🗺️ Verified, Unrefuted | Music theory — counterpoint and voice leading | **+45** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched |
| 111 | 🗺️ Verified, Unrefuted | Creative Artistic Arrangement × Informational Distributed Consensus | **+45** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 112 | 🗺️ Verified, Unrefuted | Human Meeting Participation × Informational Sensor Networks | **+45** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group 🔬 Actively Researched |
| 113 | 🗺️ Verified, Unrefuted | Physical Chemical Reaction Networks × Physical Magnetic Fluctuation | **+45** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group 🔬 Actively Researched |
| 114 | 🗺️ Verified, Unrefuted | Prigogine — thermodynamics × Complex systems | **+45** | ADJACENT_ACTIVE | — | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 115 | 🗺️ Verified, Unrefuted | Watson & Crick — DNA × Information theory | **+45** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 116 | 🗺️ Verified, Unrefuted | Genetics — Mendelian inheritance and linkage | **+45** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched |
| 117 | 🗺️ Verified, Unrefuted | Logic — Gödel incompleteness and self-reference | **+45** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched |
| 118 | 🗺️ Verified, Unrefuted | Sociology — social network diffusion of innovation | **+45** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched |
| 119 | 🗺️ Verified, Unrefuted | Viticulture — terroir and grape ripening | **+45** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched |
| 120 | 🗺️ Verified, Unrefuted | Astrophysics — orbital resonance | **+45** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched |
| 121 | 🗺️ Verified, Unrefuted | Forestry — controlled burn succession | **+45** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched |
| 122 | 🗺️ Verified, Unrefuted | Microbiology — biofilm formation | **+45** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched |
| 123 | 🗺️ Verified, Unrefuted | Veterinary medicine — zoonotic disease transmission | **+45** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched |
| 124 | 🗺️ Verified, Unrefuted | Physical Flux Regulation × Materials science — phase transitions | **+45** | ADJACENT_ACTIVE | — | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 125 | 🗺️ Verified, Unrefuted | Physical Thermal Variation × Materials science — crystal lattice defects | **+45** | ADJACENT_ACTIVE | — | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 126 | 🗺️ Verified, Unrefuted | Physical Circuit Evolution × Physical Magnetic Field Control | **+45** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 127 | 🗺️ Verified, Unrefuted | Physical Circuit Evolution × Physical Electrical Noise | **+45** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched |
| 128 | 🗺️ Verified, Unrefuted | Compiler optimization × Neural network training | **+40** | ADJACENT_ACTIVE | — | — | 📜 Pre-existing case study 🗺️ Frontier Research Group 🔬 Actively Researched (historical) |
| 129 | 🗺️ Verified, Unrefuted | Finance (Human & Social Systems) | **+40** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched (historical) |
| 130 | 🗺️ Verified, Unrefuted | Informational Cache Miss Handling × Human Individual Indecision | **+40** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group 🔬 Actively Researched (historical) |
| 131 | 🗺️ Verified, Unrefuted | Immunology × Military Strategy | **+40** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched (historical) |
| 132 | 🗺️ Verified, Unrefuted | Physical Feedback Loop Control | **+40** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched (historical) |
| 133 | 🗺️ Verified, Unrefuted | Game Theory Nash Bargaining × Human Social Network Dynamics | **+40** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group 🔬 Actively Researched (historical) |
| 134 | 🗺️ Verified, Unrefuted | Informational Database State | **+40** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched (historical) |
| 135 | 🗺️ Verified, Unrefuted | Behavioral Psychology Operant Conditioning × Physical Magnetic Field Control | **+40** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group 🔬 Actively Researched (historical) |
| 136 | 🗺️ Verified, Unrefuted | Anthropology × Physical Evolutionary Selection | **+40** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched (historical) |
| 137 | 🗺️ Verified, Unrefuted | Human Social Influence | **+40** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched (historical) |
| 138 | 🗺️ Verified, Unrefuted | Physical Immune System | **+40** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched (historical) |
| 139 | 🗺️ Verified, Unrefuted | Informational OS Thread Scheduling | **+40** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched (historical) |
| 140 | 🗺️ Verified, Unrefuted | Climatology — Ocean Current Circulation (Thermohaline) | **+40** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched (historical) |
| 141 | 🗺️ Verified, Unrefuted | Informational Event-Driven Systems | **+40** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched (historical) |
| 142 | 🗺️ Verified, Unrefuted | Supply Chain Logistics — Bullwhip Effect | **+40** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched (historical) |
| 143 | 🗺️ Verified, Unrefuted | Physical Photon Emission | **+40** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched (historical) |
| 144 | 🗺️ Verified, Unrefuted | Creative Performance Monitoring | **+40** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched (historical) |
| 145 | 🗺️ Verified, Unrefuted | Creative Instrument Track Development × Physical Circuit Evolution | **+40** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched (historical) |
| 146 | 🗺️ Verified, Unrefuted | Law — Contract Formation and Offer/Acceptance | **+40** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched (historical) |
| 147 | 🗺️ Verified, Unrefuted | Social Systems × Physical Feedback Loop Control | **+40** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group 🔬 Actively Researched (historical) |
| 148 | 🗺️ Verified, Unrefuted | History — path dependence in institutional change | **+40** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched (historical) |
| 149 | 🗺️ Verified, Unrefuted | Marketing — diffusion of innovation adoption curve | **+40** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched (historical) |
| 150 | 🗺️ Verified, Unrefuted | Robotics — inverse kinematics | **+40** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group 🔬 Actively Researched (historical) |
| 151 | 🗺️ Verified, Unrefuted | Law — common law precedent and stare decisis | **+30** | COLLISION | — | — | 🎭 Janusian 🏛️ Established Department 🔬🔥 Actively Researched (current) |
| 152 | 🗺️ Verified, Unrefuted | Distributed Consensus Algorithms (Raft, PBFT) × Distributed Cache Coherence Protocols (MESI, Directory-based) | **+30** | ADJACENT_ACTIVE | — | — | 📜 Pre-existing case study 🗺️ Frontier Research Group |
| 153 | 🗺️ Verified, Unrefuted | Dirac's large numbers hypothesis × Belnap four-valued logic / explainable AI | **+30** | ADJACENT_ACTIVE | — | — | 📜 Pre-existing case study 🗺️ Frontier Research Group |
| 154 | 🗺️ Verified, Unrefuted | Astronomy — gravitational lensing | **+30** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group |
| 155 | 🗺️ Verified, Unrefuted | Informational Hash Collisions × Human Social Network Dynamics | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group |
| 156 | 🗺️ Verified, Unrefuted | Game Theory — Nash Bargaining × Music — Sample-Based Hip-Hop Production | **+30** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group |
| 157 | 🗺️ Verified, Unrefuted | Architecture × Cross Domain Pattern Recognition | **+30** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group |
| 158 | 🗺️ Verified, Unrefuted | Control theory — PID feedback loops | **+30** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group |
| 159 | 🗺️ Verified, Unrefuted | Cryptography × Cognitive Development | **+30** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group |
| 160 | 🗺️ Verified, Unrefuted | Chemistry × Creative Album Production Orchestration | **+30** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group |
| 161 | 🗺️ Verified, Unrefuted | Creative Musical Composition × Human Emotional Fluctuation | **+30** | COLLISION | — | — | 🧬 Bisociative 🏛️ Established Department 🔬🔥 Actively Researched (current) |
| 162 | 🗺️ Verified, Unrefuted | Comedy × Cognitive AI Hyperparameter Orchestration | **+30** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group |
| 163 | 🗺️ Verified, Unrefuted | Creative Musical Motif Deviation × Human Committee Formation | **+30** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group |
| 164 | 🗺️ Verified, Unrefuted | Decision Support Systems × Informational Queue Overflow | **+30** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group |
| 165 | 🗺️ Verified, Unrefuted | Geology × Music Sound | **+30** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group |
| 166 | 🗺️ Verified, Unrefuted | Informational Backup Systems × Informational Bit Flips | **+30** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group |
| 167 | 🗺️ Verified, Unrefuted | Informational Load Balancing × Physical Immune System | **+30** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group |
| 168 | 🗺️ Verified, Unrefuted | Linguistics — Creole Genesis × Cognitive Model Adaptation | **+30** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group |
| 169 | 🗺️ Verified, Unrefuted | Neuroscience × Law | **+30** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group |
| 170 | 🗺️ Verified, Unrefuted | Architecture (Creative & Performance Systems) | **+30** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group |
| 171 | 🗺️ Verified, Unrefuted | Physical Electrical Noise | **+30** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group |
| 172 | 🗺️ Verified, Unrefuted | Materials Science — Phase Transitions × Cognitive Streaming Data Processing | **+30** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group |
| 173 | 🗺️ Verified, Unrefuted | Chemistry × Music Sound | **+30** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group |
| 174 | 🗺️ Verified, Unrefuted | Education (Information & Intelligence Systems) × Human Facilitator Cueing | **+30** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group |
| 175 | 🗺️ Verified, Unrefuted | Agriculture × Creative Improvisation Adjustment | **+30** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group |
| 176 | 🗺️ Verified, Unrefuted | Agriculture × Telecommunications | **+30** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group |
| 177 | 🗺️ Verified, Unrefuted | Cross Domain Pattern Recognition × Human Team Collaboration | **+30** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group |
| 178 | 🗺️ Verified, Unrefuted | Modular Construction × Agricultural Ecosystems | **+30** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group |
| 179 | 🗺️ Verified, Unrefuted | Auction Theory × Cognitive Attention Map Evolution | **+30** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group |
| 180 | 🗺️ Verified, Unrefuted | Quantum Physics × Physical Magnetic Field Control | **+30** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group |
| 181 | 🗺️ Verified, Unrefuted | Human Urban Planning × Physical Magnetic Fluctuation | **+30** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group |
| 182 | 🗺️ Verified, Unrefuted | Immunology × Creative Album Production Orchestration | **+30** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group |
| 183 | 🗺️ Verified, Unrefuted | Creative Film Production Orchestration | **+30** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group |
| 184 | 🗺️ Verified, Unrefuted | Urban Planning × Astronomy | **+30** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group |
| 185 | 🗺️ Verified, Unrefuted | Decision Support Systems × Creative Brainstorming Facilitation | **+30** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group |
| 186 | 🗺️ Verified, Unrefuted | Cryptography × Physical Photon Emission | **+30** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group |
| 187 | 🗺️ Verified, Unrefuted | Fluid Dynamics × Knowledge Systems | **+30** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group |
| 188 | 🗺️ Verified, Unrefuted | Artificial Intelligence × Informational Database State | **+30** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group |
| 189 | 🗺️ Verified, Unrefuted | Cognitive AI Hyperparameter Orchestration × Creative Improvisation Adjustment | **+30** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group |
| 190 | 🗺️ Verified, Unrefuted | Culinary Arts × Informational Error Probability | **+30** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group |
| 191 | 🗺️ Verified, Unrefuted | Law × Creative Idea Uncertainty | **+30** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group |
| 192 | 🗺️ Verified, Unrefuted | Military Strategy × Informational Load Balancing | **+30** | ADJACENT_ACTIVE | — | — | 🪞 Homospatial 🗺️ Frontier Research Group |
| 193 | 🗺️ Verified, Unrefuted | Human Meeting Participation × Informational Ledger State Evolution | **+30** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group |
| 194 | 🗺️ Verified, Unrefuted | Cognitive Concept Drift | **+30** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group |
| 195 | 🗺️ Verified, Unrefuted | Linguistics × Cognitive Concept Drift | **+30** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group |
| 196 | 🗺️ Verified, Unrefuted | Materials Science × Cognitive AI Pipeline Orchestration | **+30** | COLLISION | — | — | 🧬 Bisociative 🏛️ Established Department 🔬🔥 Actively Researched (current) |
| 197 | 🗺️ Verified, Unrefuted | Music Sound × Physical Circuit Evolution | **+30** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group |
| 198 | 🗺️ Verified, Unrefuted | Sports Athletics × Cognitive Swarm Intelligence | **+30** | ADJACENT_ACTIVE | — | — | 🧬 Bisociative 🗺️ Frontier Research Group |
| 199 | 🗺️ Verified, Unrefuted | Healthcare Systems × Physical Power Grid Orchestration | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 200 | 🗺️ Verified, Unrefuted | Physical Mechanical Vibration × Physical Power Grid Orchestration | **+30** | COLLISION | — | mixed-uncertain | 🪞 Homospatial 🏛️ Established Department 🔬🔥 Actively Researched (current) |
| 201 | 🗺️ Verified, Unrefuted | Cognitive Concept Drift × Physical Power Grid Orchestration | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 202 | 🗺️ Verified, Unrefuted | Urban Planning × Architecture (Creative & Performance Systems) | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🪞 Homospatial 🗺️ Frontier Research Group |
| 203 | 🗺️ Verified, Unrefuted | Cryptography — public-key infrastructure | **+30** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group |
| 204 | 🗺️ Verified, Unrefuted | Music Theory × Informational Database Sharding | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group |
| 205 | 🗺️ Verified, Unrefuted | Human Social Network Dynamics × Informational OS Thread Scheduling | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group |
| 206 | 🗺️ Verified, Unrefuted | Neuroscience × Comedy | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group |
| 207 | 🗺️ Verified, Unrefuted | Architecture × Cognitive Streaming Data Processing | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group |
| 208 | 🗺️ Verified, Unrefuted | Creative Album Production Orchestration × Physical Flux Regulation | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group |
| 209 | 🗺️ Verified, Unrefuted | Ecology × Creative Inspiration Variability | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🪞 Homospatial 🗺️ Frontier Research Group |
| 210 | 🗺️ Verified, Unrefuted | Neuroscience — Synaptic Pruning × Physical Power Grid Orchestration | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 211 | 🗺️ Verified, Unrefuted | Informational Mobile System Coordination × Physical Ecosystem Succession | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group |
| 212 | 🗺️ Verified, Unrefuted | Astronomy × Military Strategy | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group |
| 213 | 🗺️ Verified, Unrefuted | Cross Domain Pattern Recognition × Human Role Ambiguity | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group |
| 214 | 🗺️ Verified, Unrefuted | Thermodynamics × Physical Elastic Deformation | **+30** | ADJACENT_ACTIVE | — | formalism-shaped | 🪞 Homospatial 🗺️ Frontier Research Group |
| 215 | 🗺️ Verified, Unrefuted | Control Theory × Physical Chemical Reaction Networks | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 216 | 🗺️ Verified, Unrefuted | Finance (Human & Social Systems) × Physical Magnetic Field Control | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 217 | 🗺️ Verified, Unrefuted | Informational Error Probability × Physical Chemical Reaction Networks | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 218 | 🗺️ Verified, Unrefuted | Informational Scientific Experiment Orchestration × Physical Voltage Spikes | **+30** | ADJACENT_ACTIVE | — | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group |
| 219 | 🗺️ Verified, Unrefuted | Telecommunications × Creative Narrative Arc Development | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group |
| 220 | 🗺️ Verified, Unrefuted | Telecommunications × Human Cognitive Bias | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group |
| 221 | 🗺️ Verified, Unrefuted | Astrophysics × Human Trust Variance | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group |
| 222 | 🗺️ Verified, Unrefuted | Cognitive AI Hyperparameter Orchestration × Human Learning Uncertainty | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🪞 Homospatial 🗺️ Frontier Research Group |
| 223 | 🗺️ Verified, Unrefuted | Chemistry — catalysis and reaction pathways | **+30** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group |
| 224 | 🗺️ Verified, Unrefuted | Cell Biology × Informational Scientific Experiment Orchestration | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group |
| 225 | 🗺️ Verified, Unrefuted | Architecture — modular/prefab construction × Physical Photon Emission | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 226 | 🗺️ Verified, Unrefuted | Creative Improvisation Adjustment × Informational Measurement Data Evolution | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 227 | 🗺️ Verified, Unrefuted | Materials Science × Military Strategy | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group |
| 228 | 🗺️ Verified, Unrefuted | Creative Narrative Arc Development × Informational OS Thread Scheduling | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group |
| 229 | 🗺️ Verified, Unrefuted | Behavioral Psychology × Human Financial Market Systems | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🪞 Homospatial 🗺️ Frontier Research Group |
| 230 | 🗺️ Verified, Unrefuted | Informational Ledger State Evolution × Informational Sensor Networks | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 231 | 🗺️ Verified, Unrefuted | Legal Systems × Sports Athletics | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group |
| 232 | 🗺️ Verified, Unrefuted | Architecture × Anthropology | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group |
| 233 | 🗺️ Verified, Unrefuted | Anthropology × Gaming Narrative | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🪞 Homospatial 🗺️ Frontier Research Group |
| 234 | 🗺️ Verified, Unrefuted | Architecture — modular/prefab construction × Human Defense Coordination | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 235 | 🗺️ Verified, Unrefuted | Astronomy — gravitational lensing × Informational Scientific Experiment Orchestration | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 236 | 🗺️ Verified, Unrefuted | Physical Elastic Deformation | **+30** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group |
| 237 | 🗺️ Verified, Unrefuted | Law × Informational Ledger State Evolution | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group |
| 238 | 🗺️ Verified, Unrefuted | Behavioral psychology — operant conditioning | **+30** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group |
| 239 | 🗺️ Verified, Unrefuted | Legal Systems × Physical Magnetic Field Control | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group |
| 240 | 🗺️ Verified, Unrefuted | Neuroscience × Sports Athletics | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group |
| 241 | 🗺️ Verified, Unrefuted | Cognitive AI Preprocessing Pipelines × Physical Ecosystem Succession | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group |
| 242 | 🗺️ Verified, Unrefuted | Language Linguistics × Cognitive AI Attention | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🪞 Homospatial 🗺️ Frontier Research Group |
| 243 | 🗺️ Verified, Unrefuted | Informational Backup Systems × Physical Magnetic Fluctuation | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group |
| 244 | 🗺️ Verified, Unrefuted | Cognitive AI Attention × Human Committee Formation | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group |
| 245 | 🗺️ Verified, Unrefuted | Neuroscience — cortical map reorganization × Behavioral psychology — habit formation loops | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🪞 Homospatial 🗺️ Frontier Research Group |
| 246 | 🗺️ Verified, Unrefuted | Political Science × Physical Elastic Deformation | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 247 | 🗺️ Verified, Unrefuted | Sports Athletics × Cognitive Reinforcement Learning | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🪞 Homospatial 🗺️ Frontier Research Group |
| 248 | 🗺️ Verified, Unrefuted | Urban Planning × Architecture | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🪞 Homospatial 🗺️ Frontier Research Group |
| 249 | 🗺️ Verified, Unrefuted | Music Sound × Informational Hash Collisions | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group |
| 250 | 🗺️ Verified, Unrefuted | Creative Musical Composition × Human Social Influence | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group |
| 251 | 🗺️ Verified, Unrefuted | Evolutionary Biology × Cryptography | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group |
| 252 | 🗺️ Verified, Unrefuted | Human Cognitive Bias × Informational Backup Systems | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🪞 Homospatial 🗺️ Frontier Research Group |
| 253 | 🗺️ Verified, Unrefuted | Cryptography — zero-knowledge proofs | **+30** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group |
| 254 | 🗺️ Verified, Unrefuted | Music Theory × Anthropology | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group |
| 255 | 🗺️ Verified, Unrefuted | Creative Artistic Arrangement × Human Financial Trading Algorithms | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group |
| 256 | 🗺️ Verified, Unrefuted | Epigenetics × Human Urban Planning | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group |
| 257 | 🗺️ Verified, Unrefuted | Basketball Pick-and-Roll Offense × Cognitive Attention Map Evolution | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 258 | 🗺️ Verified, Unrefuted | Organizational Theory × Architecture | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group |
| 259 | 🗺️ Verified, Unrefuted | Informational Sensor Networks × Physical Power Grid Orchestration | **+30** | COLLISION | — | narrative-shaped | 🪞 Homospatial 🏛️ Established Department 🔬🔥 Actively Researched (current) |
| 260 | 🗺️ Verified, Unrefuted | Cognitive AI Attention × Creative Brainstorming Facilitation | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group |
| 261 | 🗺️ Verified, Unrefuted | Creative Improvisation Coordination × Informational Signal Jitter | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group |
| 262 | 🗺️ Verified, Unrefuted | Culinary Arts × Human Financial Market Systems | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group |
| 263 | 🗺️ Verified, Unrefuted | Creative Narrative Arc Development × Informational Protocol Coordination | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 264 | 🗺️ Verified, Unrefuted | Human Role Ambiguity × Physical Telescope Telemetry | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group |
| 265 | 🗺️ Verified, Unrefuted | Culinary Arts × Human Committee Formation | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group |
| 266 | 🗺️ Verified, Unrefuted | Behavioral Psychology × Music Sound | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🪞 Homospatial 🗺️ Frontier Research Group |
| 267 | 🗺️ Verified, Unrefuted | Cognitive AI Preprocessing Pipelines × Creative Performance Monitoring | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🪞 Homospatial 🗺️ Frontier Research Group |
| 268 | 🗺️ Verified, Unrefuted | Music Theory × Informational Load Balancing | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 269 | 🗺️ Verified, Unrefuted | Human Meeting Participation × Informational Event-Driven Systems | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group |
| 270 | 🗺️ Verified, Unrefuted | Comedy — crowd work and audience read | **+30** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group |
| 271 | 🗺️ Verified, Unrefuted | Sports — basketball pick-and-roll offense | **+30** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group |
| 272 | 🗺️ Verified, Unrefuted | Healthcare × Legal Systems | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group |
| 273 | 🗺️ Verified, Unrefuted | Cognitive AI Attention × Human Facilitator Cueing | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🪞 Homospatial 🗺️ Frontier Research Group |
| 274 | 🗺️ Verified, Unrefuted | Creative Artistic Critique × Physical Thermal Variation | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 275 | 🗺️ Verified, Unrefuted | Creative Improvisation Coordination × Informational Software Version Control | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 276 | 🗺️ Verified, Unrefuted | Organizational Theory — Bureaucratic Hierarchy × Cognitive AI Hyperparameter Orchestration | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🪞 Homospatial 🗺️ Frontier Research Group |
| 277 | 🗺️ Verified, Unrefuted | Agriculture (Physical & Natural Systems) | **+30** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group |
| 278 | 🗺️ Verified, Unrefuted | Architecture × Physical Immune System | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group |
| 279 | 🗺️ Verified, Unrefuted | Cognitive Attention Map Evolution | **+30** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group |
| 280 | 🗺️ Verified, Unrefuted | Physical Ecosystem Succession × Physical Feedback Loop Control | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group |
| 281 | 🗺️ Verified, Unrefuted | Creative Improvisation Coordination × Human Learning Uncertainty | **+30** | COLLISION | — | mixed-uncertain | 🧬 Bisociative 🏛️ Established Department 🔬🔥 Actively Researched (current) |
| 282 | 🗺️ Verified, Unrefuted | Epidemiology — Herd Immunity Thresholds × Informational Sensor Networks | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 283 | 🗺️ Verified, Unrefuted | Baseball Pitch Sequencing × Informational Protocol Coordination | **+30** | COLLISION | — | mixed-uncertain | 🪞 Homospatial 🏛️ Established Department 🔬🔥 Actively Researched (current) |
| 284 | 🗺️ Verified, Unrefuted | Law × Creative Idea Uncertainty | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group |
| 285 | 🗺️ Verified, Unrefuted | Cell biology — protein folding chaperones × Cognitive AI Pipeline Orchestration | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 286 | 🗺️ Verified, Unrefuted | Gaming Narrative (Creative & Performance Systems) — Atomic: Player action succeeds/fails, Character status unknown, Multiple dialogue choices; Domain: Game world evolves, Game rules context, Log player actions; Control: Player input from controllers, Concurrent NPCs & physics, Atomic world consistency; Orchestration: Game engine coordination, Narrative vs gameplay environments × Informational Sensor Networks | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 287 | 🗺️ Verified, Unrefuted | Informational Database State × Physical Circuit Evolution | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 288 | 🗺️ Verified, Unrefuted | Telecommunications — error-correcting codes × Informational Ledger State Evolution | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 289 | 🗺️ Verified, Unrefuted | Architecture (Creative & Performance Systems) — Atomic: Building permits approved/denied, Material availability uncertain, Multiple design options; Domain: Building construction progresses, Building codes, Log construction events; Control: Building inspections & permits, Concurrent construction, Atomic structural updates; Orchestration: City planning coordination, Design vs construction environments × Human Learning Uncertainty | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 290 | 🗺️ Verified, Unrefuted | Informational Error Probability × Physical Thermal Variation | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 291 | 🗺️ Verified, Unrefuted | Informational Error Probability × Physical Immune System | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group |
| 292 | 🗺️ Verified, Unrefuted | Chemistry — catalysis and reaction pathways × Cognitive Development (Information & Intelligence Systems) — Atomic: Learning outcome uncertain, Skill acquisition succeeds/fails, Multiple learning paths; Domain: Cognitive skills evolve, Learning context, Log development milestones; Control: External learning resources, Parallel skill development, Atomic knowledge integration; Orchestration: Learning system coordination, Practice vs application environments | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 293 | 🗺️ Verified, Unrefuted | Cross Domain Pattern Recognition (Cognitive & Pattern Recognition Systems) — Atomic: Pattern recognition uncertain, Mapping valid/invalid, Multiple domain analogies; Domain: Cross-domain understanding evolves, Universal monadic patterns, Log successful transfers; Control: Multiple data sources, Parallel analysis, Atomic synthesis; Orchestration: Cross-domain coordination & system integration × Creative Narrative Arc Development | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🪞 Homospatial 🗺️ Frontier Research Group |
| 294 | 🗺️ Verified, Unrefuted | Finance (Human & Social Systems) — Atomic: Transaction succeeds/fails, Account lookup missing, Multiple positions; Domain: Portfolio evolves, Market context, Audit logging; Control: External trades & APIs, Streaming market data, Atomic account updates; Orchestration: Regulatory coordination, Simulation vs live trading × Informational Database Sharding | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group |
| 295 | 🗺️ Verified, Unrefuted | Sports — basketball pick-and-roll offense × Human Emotional Fluctuation | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🪞 Homospatial 🗺️ Frontier Research Group |
| 296 | 🗺️ Verified, Unrefuted | Urban planning — zoning and land use × Physical Power Grid Orchestration | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group |
| 297 | 🗺️ Verified, Unrefuted | Epidemiology — disease outbreak spread × Creative Brainstorming Facilitation | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group |
| 298 | 🗺️ Verified, Unrefuted | Control theory — Kalman filtering × Creative Improvisation Adjustment | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 299 | 🗺️ Verified, Unrefuted | Supply chain logistics — bullwhip effect × Swarm robotics — flocking / boids behavior | **+30** | ADJACENT_ACTIVE | — | narrative-shaped | 🪞 Homospatial 🗺️ Frontier Research Group |
| 300 | 🗺️ Verified, Unrefuted | Botany — phototropism and plant signaling | **+30** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group |
| 301 | 🗺️ Verified, Unrefuted | Pharmacology — drug receptor binding kinetics | **+30** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group |
| 302 | 🗺️ Verified, Unrefuted | Philosophy — epistemology — justified true belief | **+30** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group |
| 303 | 🗺️ Verified, Unrefuted | Computer science — distributed consensus protocols | **+30** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group |
| 304 | 🗺️ Verified, Unrefuted | Developmental psychology — attachment theory | **+30** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group |
| 305 | 🗺️ Verified, Unrefuted | Education — spaced repetition and forgetting curves | **+30** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group |
| 306 | 🗺️ Verified, Unrefuted | Visual art — color theory and composition | **+30** | ADJACENT_ACTIVE | — | — | 🎭 Janusian 🗺️ Frontier Research Group |
| 307 | 🗺️ Verified, Unrefuted | Cognitive psychology — working memory and chunking × Finance (Human & Social Systems) — Atomic: Transaction succeeds/fails, Account lookup missing, Multiple positions; Domain: Portfolio evolves, Market context, Audit logging; Control: External trades & APIs, Streaming market data, Atomic account updates; Orchestration: Regulatory coordination, Simulation vs live trading | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 308 | 🗺️ Verified, Unrefuted | Urban planning — zoning and land use × Physical Mechanical Vibration | **+30** | ADJACENT_ACTIVE | — | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group |
| 309 | 🗺️ Verified, Unrefuted | Jazz Improvisation × Counterpoint and Voice Leading | **+20** | COLLISION | — | — | 🧬 Bisociative 🏛️ Established Department 🔬 Actively Researched |
| 310 | 🗺️ Verified, Unrefuted | Informational — distributed consensus | **+20** | COLLISION | — | — | 🎭 Janusian 🏛️ Established Department 🔬 Actively Researched |
| 311 | 🗺️ Verified, Unrefuted | Informational — load balancing | **+20** | COLLISION | — | — | 🎭 Janusian 🏛️ Established Department 🔬 Actively Researched |
| 312 | 🗺️ Verified, Unrefuted | Cognitive Attention Map Evolution × Informational Sensor Networks | **+20** | COLLISION | — | — | 🪞 Homospatial 🏛️ Established Department 🔬 Actively Researched |
| 313 | 🗺️ Verified, Unrefuted | Climate Science × Creative Artistic Arrangement | **+20** | COLLISION | — | — | 🪞 Homospatial 🏛️ Established Department 🔬 Actively Researched |
| 314 | 🗺️ Verified, Unrefuted | Human Emotional Fluctuation | **+20** | COLLISION | — | — | 🎭 Janusian 🏛️ Established Department 🔬 Actively Researched |
| 315 | 🗺️ Verified, Unrefuted | Fluid dynamics — turbulence and laminar flow | **+20** | COLLISION | — | — | 🎭 Janusian 🏛️ Established Department 🔬 Actively Researched |
| 316 | 🗺️ Verified, Unrefuted | Healthcare (Human & Social Systems) × Physical Circuit Evolution | **+20** | COLLISION | — | mixed-uncertain | 🪞 Homospatial 🏛️ Established Department 🔬 Actively Researched |
| 317 | 🗺️ Verified, Unrefuted | Ecology — Mycorrhizal Fungal Networks | **+20** | COLLISION | — | — | 🎭 Janusian 🏛️ Established Department 🔬 Actively Researched |
| 318 | 🗺️ Verified, Unrefuted | Genetic algorithms × Simulated annealing | **+15** | COLLISION | — | — | 📜 Pre-existing case study 🏛️ Established Department 🔬 Actively Researched (historical) |
| 319 | 🗺️ Verified, Unrefuted | Raft consensus × PBFT consensus | **+15** | COLLISION | — | — | 📜 Pre-existing case study 🏛️ Established Department 🔬 Actively Researched (historical) |
| 320 | 🗺️ Verified, Unrefuted | Urban planning — traffic flow optimization | **+15** | COLLISION | — | — | 🎭 Janusian 🏛️ Established Department 🔬 Actively Researched (historical) |
| 321 | 🗺️ Verified, Unrefuted | Finance — options pricing and volatility smile | **+15** | COLLISION | — | — | 🎭 Janusian 🏛️ Established Department 🔬 Actively Researched (historical) |
| 322 | 🗺️ Verified, Unrefuted | Graph traversal algorithms (Dijkstra's, A*) × Minimax game tree search | **+5** | COLLISION | — | — | 📜 Pre-existing case study 🏛️ Established Department |
| 323 | 🗺️ Verified, Unrefuted | Informational Measurement Data Evolution | **+5** | COLLISION | — | — | 🎭 Janusian 🏛️ Established Department |
| 324 | 🗺️ Verified, Unrefuted | Human Financial Market Systems × Physical Mechanical Spring Systems | **+5** | COLLISION | — | mixed-uncertain | 🧬 Bisociative 🏛️ Established Department |
| 325 | 🗺️ Verified, Unrefuted | Language Linguistics × Cognitive Reinforcement Learning | **+5** | COLLISION | — | mixed-uncertain | 🪞 Homospatial 🏛️ Established Department |
| 326 | 🗺️ Verified, Unrefuted | Cognitive Reinforcement Learning × Informational OS Thread Scheduling | **+5** | COLLISION | — | mixed-uncertain | 🪞 Homospatial 🏛️ Established Department |
| 327 | 🗺️ Verified, Unrefuted | Fluid Dynamics × Creative Narrative Arc Development | **+5** | COLLISION | — | mixed-uncertain | 🪞 Homospatial 🏛️ Established Department |
| 328 | 🗺️ Verified, Unrefuted | Astrophysics × Creative Narrative Arc Development | **+5** | COLLISION | — | mixed-uncertain | 🪞 Homospatial 🏛️ Established Department |
| 329 | 🗺️ Verified, Unrefuted | Decision Support Systems × Legal Systems | **+5** | COLLISION | — | narrative-shaped | 🪞 Homospatial 🏛️ Established Department |
| 330 | 🗺️ Verified, Unrefuted | Informational Hash Collisions | **+5** | COLLISION | — | — | 🎭 Janusian 🏛️ Established Department |
| 331 | 🗺️ Verified, Unrefuted | Meteorology — supercell storm rotation | **+5** | COLLISION | — | — | 🎭 Janusian 🏛️ Established Department |
| 332 | 🌗 Contested | Aerospace engineering — aerodynamic stall | **+50** | ADJACENT_ACTIVE | 33% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 🌗 Contested (1-of-3) 🔬🔥 Actively Researched (current) |
| 333 | 🌗 Contested | Acoustics — resonance and standing waves | **+35** | ADJACENT_ACTIVE | 33% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 🌗 Contested (1-of-3) 🔬 Actively Researched (historical) |
| 334 | 🌗 Contested | Gaming Narrative × Human Financial Trading Algorithms | **-5** | NO_SIGNAL | 33% survived | — | 🧬 Bisociative 🌗 Contested (1-of-3) |
| 335 | 🌗 Contested | Watson & Crick — Molecular Biology × Franklin — X-Ray Crystallography | **-5** | COLLISION | 33% survived | — | 🧬 Bisociative 🏆 Nobel Ground Truth (calibration benchmark, not engine-generated) 🏛️ Established Department 🌗 Contested (1-of-3) |
| 336 | 🌗 Contested | Hopfield — Statistical Physics × Neural Networks | **-5** | COLLISION | 33% survived | — | 🧬 Bisociative 🏆 Nobel Ground Truth (calibration benchmark, not engine-generated) 🏛️ Established Department 🌗 Contested (1-of-3) |
| 337 | 🌗 Contested | Coase — Transaction Costs × Property Rights | **-5** | ADJACENT_ACTIVE | 33% survived | — | 🧬 Bisociative 🏆 Nobel Ground Truth (calibration benchmark, not engine-generated) 🗺️ Frontier Research Group 🌗 Contested (1-of-3) |
| 338 | 🌗 Contested | Becker — Rational Choice × Household Behavior | **-5** | COLLISION | 33% survived | — | 🧬 Bisociative 🏆 Nobel Ground Truth (calibration benchmark, not engine-generated) 🏛️ Established Department 🌗 Contested (1-of-3) |
| 339 | 🌗 Contested | Feynman — quantum mechanics × Computation — simulation | **-5** | COLLISION | 33% survived | — | 🧬 Bisociative 🏆 Nobel Ground Truth (calibration benchmark, not engine-generated) 🏛️ Established Department 🌗 Contested (1-of-3) |
| 340 | 💀 Refuted / Rejected | Control theory — Kalman filtering × Physical Magnetic Fluctuation | **+57** | ADJACENT_ACTIVE | 67% survived | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 🛡️ Survived the Gauntlet 🔬🔥 Actively Researched (current) |
| 341 | 💀 Refuted / Rejected | Political science — coalition government formation | **+47** | ADJACENT_ACTIVE | 67% survived | — | 🎭 Janusian 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 🛡️ Survived the Gauntlet 🔬 Actively Researched |
| 342 | 💀 Refuted / Rejected | Cognitive Attention Map Evolution × Informational Event-Driven Systems | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🧬 Bisociative 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 343 | 💀 Refuted / Rejected | Epidemiology × Creative Inspiration Variability | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🧬 Bisociative 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 344 | 💀 Refuted / Rejected | Linguistics × Fluid Dynamics | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 345 | 💀 Refuted / Rejected | Cognitive AI Preprocessing Pipelines | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 346 | 💀 Refuted / Rejected | Organizational Theory — Self-Organizing Teams × Finance (Human & Social Systems) | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🧬 Bisociative 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 347 | 💀 Refuted / Rejected | Efficient Market Hypothesis | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 348 | 💀 Refuted / Rejected | Human Learning Uncertainty | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 349 | 💀 Refuted / Rejected | Artificial Intelligence (Information & Intelligence Systems) | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 350 | 💀 Refuted / Rejected | Creative Improvisation Adjustment | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 351 | 💀 Refuted / Rejected | Music theory — jazz improvisation over changes | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 352 | 💀 Refuted / Rejected | Healthcare (Human & Social Systems) | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 353 | 💀 Refuted / Rejected | Immunology — Innate Immune Response | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 354 | 💀 Refuted / Rejected | Immunology — Adaptive Immune Memory | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 355 | 💀 Refuted / Rejected | Legal Systems | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 356 | 💀 Refuted / Rejected | Economics — Auction Theory | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 357 | 💀 Refuted / Rejected | Gaming Narrative (Creative & Performance Systems) | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 358 | 💀 Refuted / Rejected | Creative Idea Uncertainty | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 359 | 💀 Refuted / Rejected | Informational Ledger State Evolution | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 360 | 💀 Refuted / Rejected | Sports — baseball pitch sequencing | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 361 | 💀 Refuted / Rejected | Quantum Physics | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 362 | 💀 Refuted / Rejected | Creative Improvisation Coordination | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 363 | 💀 Refuted / Rejected | Language Linguistics (Information & Intelligence Systems) | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 364 | 💀 Refuted / Rejected | Creative Brainstorming Facilitation | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 365 | 💀 Refuted / Rejected | Human Facilitator Cueing | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 366 | 💀 Refuted / Rejected | Social Systems | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 367 | 💀 Refuted / Rejected | Cognitive Reinforcement Learning | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 368 | 💀 Refuted / Rejected | Game Theory — Nash Bargaining | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 369 | 💀 Refuted / Rejected | Creative Performance Monitoring × Human Cognitive Bias | **+40** | ADJACENT_ACTIVE | 0% survived | narrative-shaped | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 370 | 💀 Refuted / Rejected | Informational Packet Buffer Management | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 371 | 💀 Refuted / Rejected | Creative Artistic Arrangement | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 372 | 💀 Refuted / Rejected | Human Social Network Dynamics | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 373 | 💀 Refuted / Rejected | Agriculture — crop rotation and soil health | **+40** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬🔥 Actively Researched (current) |
| 374 | 💀 Refuted / Rejected | Physical Acoustic Resonance × Physical Photon Emission | **+40** | ADJACENT_ACTIVE | 33% survived | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 🌗 Contested (1-of-3) 🔬🔥 Actively Researched (current) |
| 375 | 💀 Refuted / Rejected | Physical Bridge Cable Tension × Physical Elastic Deformation | **+40** | ADJACENT_ACTIVE | 33% survived | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 🌗 Contested (1-of-3) 🔬🔥 Actively Researched (current) |
| 376 | 💀 Refuted / Rejected | Physics — condensed matter — Bose-Einstein condensate coherence (Gross-Pitaevskii dynamics, quantum pressure) × Cosmology — early-universe scalar field dynamics (corpuscular inflation, axion/ultralight BEC dark matter, Fukuyama-Morikawa stagflation) | **+40** | ADJACENT_ACTIVE | 33% survived | — | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 🌗 Contested (1-of-3) 🔬🔥 Actively Researched (current) |
| 377 | 💀 Refuted / Rejected | Ecology × Materials Science | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🧬 Bisociative 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 378 | 💀 Refuted / Rejected | Game Theory — Repeated Prisoner's Dilemma × Informational Measurement Data Evolution | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🧬 Bisociative 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 379 | 💀 Refuted / Rejected | Human Individual Indecision × Physical Voltage Spikes | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 380 | 💀 Refuted / Rejected | Behavioral psychology — habit formation loops | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 381 | 💀 Refuted / Rejected | Neuroscience — cortical map reorganization | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 382 | 💀 Refuted / Rejected | Thermodynamics × Informational Signal Jitter | **+30** | ADJACENT_ACTIVE | 33% survived | — | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 🌗 Contested (1-of-3) 🔬 Actively Researched |
| 383 | 💀 Refuted / Rejected | Fluid Dynamics × Physical Telescope Telemetry | **+30** | ADJACENT_ACTIVE | 33% survived | — | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 🌗 Contested (1-of-3) 🔬 Actively Researched |
| 384 | 💀 Refuted / Rejected | Adaptive Immune Memory × Human Defense Coordination | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 385 | 💀 Refuted / Rejected | Swarm Robotics — Ant Colony Optimization | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬🔥 Actively Researched (current) |
| 386 | 💀 Refuted / Rejected | Human Financial Trading Algorithms | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 387 | 💀 Refuted / Rejected | Physical Ecosystem Succession | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 388 | 💀 Refuted / Rejected | Human Committee Formation | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 389 | 💀 Refuted / Rejected | Informational Protocol Coordination | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 390 | 💀 Refuted / Rejected | Cell biology — mitochondrial energy production | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 391 | 💀 Refuted / Rejected | Architecture × Human Financial Trading Algorithms | **+30** | ADJACENT_ACTIVE | 0% survived | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬🔥 Actively Researched (current) |
| 392 | 💀 Refuted / Rejected | Cognitive Swarm Intelligence | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 393 | 💀 Refuted / Rejected | Human Role Ambiguity | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 394 | 💀 Refuted / Rejected | Linguistics — Creole Genesis | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 395 | 💀 Refuted / Rejected | Telecommunications — packet switching and routing | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 396 | 💀 Refuted / Rejected | Human Team Collaboration | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 397 | 💀 Refuted / Rejected | Organizational theory — self-organizing teams | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 398 | 💀 Refuted / Rejected | Creative Musical Motif Deviation × Informational Error Probability | **+30** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬🔥 Actively Researched (current) |
| 399 | 💀 Refuted / Rejected | Climate Science (Physical & Natural Systems) | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 400 | 💀 Refuted / Rejected | Music — sample-based hip-hop production | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 401 | 💀 Refuted / Rejected | Cross Domain Pattern Recognition (Cognitive & Pattern Recognition Systems) | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 402 | 💀 Refuted / Rejected | Swarm Robotics — Flocking / Boids Behavior | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 403 | 💀 Refuted / Rejected | Chemistry — self-assembly of molecular structures | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 404 | 💀 Refuted / Rejected | Physical Mechanical Vibration | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 405 | 💀 Refuted / Rejected | Astrophysics (Physical & Natural Systems) | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 406 | 💀 Refuted / Rejected | Informational Error Probability | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 407 | 💀 Refuted / Rejected | Physical Protein Folding | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 408 | 💀 Refuted / Rejected | Cognitive Swarm Intelligence × Human Trust Variance | **+30** | ADJACENT_ACTIVE | 0% survived | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬🔥 Actively Researched (current) |
| 409 | 💀 Refuted / Rejected | Learning Systems (Cognitive & Pattern Recognition Systems) — Atomic: Learning outcomes uncertain, Skill acquisition succeeds/fails, Multiple learning states; Domain: Learning progresses, Educational context, Log development; Control: External learning resources, Parallel skill development, Atomic knowledge updates; Orchestration: Individual vs collective learning coordination | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 410 | 💀 Refuted / Rejected | Neuroscience — synaptic pruning | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 411 | 💀 Refuted / Rejected | Knowledge Systems (Cognitive & Pattern Recognition Systems) — Atomic: Data interpretation uncertain, Model output ambiguous, Multiple insights; Domain: Knowledge evolves, Historical context, Log insights; Control: Distributed analysis, Parallel computation, Atomic integration; Orchestration: Knowledge deployment coordination × Informational Scientific Experiment Orchestration | **+30** | ADJACENT_ACTIVE | 0% survived | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬🔥 Actively Researched (current) |
| 412 | 💀 Refuted / Rejected | Immunology — innate immune response | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 413 | 💀 Refuted / Rejected | Informational Mobile System Coordination | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 414 | 💀 Refuted / Rejected | Political science — coalition government formation | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 415 | 💀 Refuted / Rejected | Political science — coalition government formation | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 416 | 💀 Refuted / Rejected | Toxicology — dose-response curves | **+30** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched |
| 417 | 💀 Refuted / Rejected | Physical Elastic Deformation × Materials science — crystal lattice defects | **+30** | ADJACENT_ACTIVE | 33% survived | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 🌗 Contested (1-of-3) 🔬 Actively Researched |
| 418 | 💀 Refuted / Rejected | Physical Magnetic Field Control × Physical Voltage Spikes | **+30** | ADJACENT_ACTIVE | 33% survived | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 🌗 Contested (1-of-3) 🔬 Actively Researched |
| 419 | 💀 Refuted / Rejected | Informational Protocol Coordination × Cryptography — public-key infrastructure | **+30** | ADJACENT_ACTIVE | 33% survived | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 🌗 Contested (1-of-3) 🔬 Actively Researched |
| 420 | 💀 Refuted / Rejected | Physical Immune System × Materials science — phase transitions | **+30** | ADJACENT_ACTIVE | 0% survived | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬🔥 Actively Researched (current) |
| 421 | 💀 Refuted / Rejected | Physical Mechanical Spring Systems × Physical Circuit Evolution | **+30** | ADJACENT_ACTIVE | 33% survived | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 🌗 Contested (1-of-3) 🔬 Actively Researched |
| 422 | 💀 Refuted / Rejected | Physical Mechanical Spring Systems × Physical Mechanical Vibration | **+30** | ADJACENT_ACTIVE | 33% survived | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 🌗 Contested (1-of-3) 🔬 Actively Researched |
| 423 | 💀 Refuted / Rejected | Physical Acoustic Resonance × Physical Mechanical Vibration | **+30** | ADJACENT_ACTIVE | 33% survived | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 🌗 Contested (1-of-3) 🔬 Actively Researched |
| 424 | 💀 Refuted / Rejected | Physical Electrical Noise × Physical Gear System Mechanics | **+30** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬🔥 Actively Researched (current) |
| 425 | 💀 Refuted / Rejected | Physical Mechanical Vibration × Physical Gear System Mechanics | **+30** | ADJACENT_ACTIVE | 33% survived | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 🌗 Contested (1-of-3) 🔬 Actively Researched |
| 426 | 💀 Refuted / Rejected | Behavioral psychology — habit formation loops × Creative Musical Motif Deviation | **+30** | ADJACENT_ACTIVE | 0% survived | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬🔥 Actively Researched (current) |
| 427 | 💀 Refuted / Rejected | Knowledge Systems (Cognitive & Pattern Recognition Systems) | **+25** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched (historical) |
| 428 | 💀 Refuted / Rejected | Astronomy × Telecommunications | **+25** | ADJACENT_ACTIVE | 0% survived | — | 🧬 Bisociative 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched (historical) |
| 429 | 💀 Refuted / Rejected | Informational Cache Miss Handling | **+25** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched (historical) |
| 430 | 💀 Refuted / Rejected | Human Individual Indecision | **+25** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched (historical) |
| 431 | 💀 Refuted / Rejected | Cognitive Development (Information & Intelligence Systems) | **+25** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched (historical) |
| 432 | 💀 Refuted / Rejected | Informational Sensor Networks | **+25** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched (historical) |
| 433 | 💀 Refuted / Rejected | Immunology — Adaptive Immune Memory | **+25** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched (historical) |
| 434 | 💀 Refuted / Rejected | Supply Chain Logistics — Just-in-Time Inventory | **+25** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched (historical) |
| 435 | 💀 Refuted / Rejected | Physical Magnetic Fluctuation | **+25** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched (historical) |
| 436 | 💀 Refuted / Rejected | Cognitive Streaming Data Processing | **+25** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched (historical) |
| 437 | 💀 Refuted / Rejected | Economics — market microstructure and order books | **+25** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched (historical) |
| 438 | 💀 Refuted / Rejected | Epidemiology — disease outbreak spread | **+25** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched (historical) |
| 439 | 💀 Refuted / Rejected | Physical Chemical Reaction Networks | **+25** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted 🔬 Actively Researched (historical) |
| 440 | 💀 Refuted / Rejected | Cognitive Neuron Activation | **+20** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬 Actively Researched |
| 441 | 💀 Refuted / Rejected | Education (Information & Intelligence Systems) × Human Social Influence | **+20** | ADJACENT_ACTIVE | 0% survived | — | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬 Actively Researched |
| 442 | 💀 Refuted / Rejected | Materials Science × Architecture | **+20** | ADJACENT_ACTIVE | 0% survived | — | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬 Actively Researched |
| 443 | 💀 Refuted / Rejected | Organizational Theory × Physical Magnetic Field Control | **+20** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬 Actively Researched |
| 444 | 💀 Refuted / Rejected | Finance × Informational Routing Policy Enforcement | **+20** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬 Actively Researched |
| 445 | 💀 Refuted / Rejected | Game Theory — Repeated Prisoner's Dilemma | **+20** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬 Actively Researched |
| 446 | 💀 Refuted / Rejected | Human Team Collaboration × Physical Flux Regulation | **+20** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬 Actively Researched |
| 447 | 💀 Refuted / Rejected | Quantum Physics (Physical & Natural Systems) — Atomic: Particle position uncertain, Measurement binary, Superposition states; Domain: Quantum system evolves, Physical laws context, Log measurements; Control: Measurement apparatus, Parallel quantum processes, Atomic wavefunction collapse; Orchestration: Universal law coordination, Theoretical vs experimental environments × Informational Signal Jitter | **+20** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬 Actively Researched |
| 448 | 💀 Refuted / Rejected | Fleming — bacteriology × Contamination | **+20** | ADJACENT_ACTIVE | 0% survived | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬 Actively Researched |
| 449 | 💀 Refuted / Rejected | Nash — equilibrium × Malthus — scarcity | **+20** | ADJACENT_ACTIVE | 0% survived | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬 Actively Researched |
| 450 | 💀 Refuted / Rejected | Physical Mechanical Vibration × Physical Circuit Evolution | **+20** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬 Actively Researched |
| 451 | 💀 Refuted / Rejected | Physical Acoustic Resonance × Physical Mechanical Spring Systems | **+20** | ADJACENT_ACTIVE | 0% survived | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬 Actively Researched |
| 452 | 💀 Refuted / Rejected | Astronomy — gravitational lensing × Physics — optics — diffraction and interference patterns | **+20** | COLLISION | — | formalism-shaped | 🧬 Bisociative 🏛️ Established Department ⚠️ Failed Honesty Check 🔬🔥 Actively Researched (current) |
| 453 | 💀 Refuted / Rejected | Materials science — phase transitions × Informational Distributed Consensus | **+20** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬 Actively Researched |
| 454 | 💀 Refuted / Rejected | Fluid dynamics — turbulence and laminar flow × Physical Magnetic Fluctuation | **+20** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬 Actively Researched |
| 455 | 💀 Refuted / Rejected | Physical Mechanical Spring Systems × Physical Gear System Mechanics | **+20** | ADJACENT_ACTIVE | 0% survived | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬 Actively Researched |
| 456 | 💀 Refuted / Rejected | Physical Acoustic Resonance × Physical Gear System Mechanics | **+20** | ADJACENT_ACTIVE | 0% survived | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬 Actively Researched |
| 457 | 💀 Refuted / Rejected | Physical Electrical Noise × Physical Mechanical Vibration | **+20** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬 Actively Researched |
| 458 | 💀 Refuted / Rejected | Physical Mechanical Spring Systems | **+15** | FACT_CHECK_FAIL | — | — | 🎭 Janusian ⚠️ Retracted 🔬🔥 Actively Researched (current) |
| 459 | 💀 Refuted / Rejected | Urban planning — zoning and land use | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted |
| 460 | 💀 Refuted / Rejected | Supply Chain Logistics × Physical Thermal Variation | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🧬 Bisociative 🗺️ Frontier Research Group 💀 Refuted |
| 461 | 💀 Refuted / Rejected | Physical Bridge Cable Tension | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted |
| 462 | 💀 Refuted / Rejected | Artificial Intelligence × Informational Queue Overflow | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🧬 Bisociative 🗺️ Frontier Research Group 💀 Refuted |
| 463 | 💀 Refuted / Rejected | Fluid Dynamics × Human Emotional Fluctuation | **+15** | FACT_CHECK_FAIL | — | — | 🪞 Homospatial ⚠️ Retracted 🔬🔥 Actively Researched (current) |
| 464 | 💀 Refuted / Rejected | Creative Performance Monitoring × Physical Voltage Spikes | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🧬 Bisociative 🗺️ Frontier Research Group 💀 Refuted |
| 465 | 💀 Refuted / Rejected | Climatology × Cognitive Model Adaptation | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🧬 Bisociative 🗺️ Frontier Research Group 💀 Refuted |
| 466 | 💀 Refuted / Rejected | Ecology × Informational Ledger State Evolution | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🧬 Bisociative 🗺️ Frontier Research Group 💀 Refuted |
| 467 | 💀 Refuted / Rejected | Creative Idea Uncertainty × Creative Musical Motif Deviation | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted |
| 468 | 💀 Refuted / Rejected | Physical Telescope Telemetry | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted |
| 469 | 💀 Refuted / Rejected | Biological Systems × Cognitive Concept Drift | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted |
| 470 | 💀 Refuted / Rejected | Music Theory × Sports | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted |
| 471 | 💀 Refuted / Rejected | Cognitive AI Hyperparameter Orchestration | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted |
| 472 | 💀 Refuted / Rejected | Creative Musical Motif Deviation | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted |
| 473 | 💀 Refuted / Rejected | Decision Support (Cognitive & Pattern Recognition Systems) | **+15** | COLLISION | 0% survived | — | 🎭 Janusian 🏛️ Established Department 💀 Refuted 🔬🔥 Actively Researched (current) |
| 474 | 💀 Refuted / Rejected | Finance (Human & Social Systems) | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted |
| 475 | 💀 Refuted / Rejected | Astrophysics × Military Strategy | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted |
| 476 | 💀 Refuted / Rejected | Geology × Cognitive Attention Map Evolution | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted |
| 477 | 💀 Refuted / Rejected | Informational Cache Miss Handling × Physical Telescope Telemetry | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted |
| 478 | 💀 Refuted / Rejected | Organizational Theory — Bureaucratic Hierarchy × Informational Bit Flips | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted |
| 479 | 💀 Refuted / Rejected | Creative Artistic Critique | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted |
| 480 | 💀 Refuted / Rejected | Ecology — predator-prey population dynamics | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted |
| 481 | 💀 Refuted / Rejected | Epigenetics × Physical Bridge Cable Tension | **+15** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group 💀 Refuted |
| 482 | 💀 Refuted / Rejected | Neuroscience — cortical map reorganization × Economics — market microstructure and order books | **+15** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted |
| 483 | 💀 Refuted / Rejected | Swarm Robotics × Law | **+15** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted |
| 484 | 💀 Refuted / Rejected | Geology — sedimentary layering and stratigraphy | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted |
| 485 | 💀 Refuted / Rejected | Astrophysics × Human Social Influence | **+15** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted |
| 486 | 💀 Refuted / Rejected | Human Role Ambiguity × Informational Error Probability | **+15** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted |
| 487 | 💀 Refuted / Rejected | Music Sound × Human Cognitive Bias | **+15** | ADJACENT_ACTIVE | 0% survived | narrative-shaped | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted |
| 488 | 💀 Refuted / Rejected | Human Role Ambiguity × Informational Hash Collisions | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted |
| 489 | 💀 Refuted / Rejected | Human Defense Coordination | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted |
| 490 | 💀 Refuted / Rejected | Climatology × Creative Instrument Track Development | **+15** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted |
| 491 | 💀 Refuted / Rejected | Informational Software Version Control × Physical Flux Regulation | **+15** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted |
| 492 | 💀 Refuted / Rejected | Biological Systems | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted |
| 493 | 💀 Refuted / Rejected | Cognitive AI Weight Initialization | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted |
| 494 | 💀 Refuted / Rejected | Linguistics — Creole Genesis × Creative Film Production Orchestration | **+15** | ADJACENT_ACTIVE | 0% survived | narrative-shaped | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted |
| 495 | 💀 Refuted / Rejected | Creative Album Production Orchestration | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted |
| 496 | 💀 Refuted / Rejected | Music Theory × Informational Ledger State Evolution | **+15** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group 💀 Refuted |
| 497 | 💀 Refuted / Rejected | Auction Theory × Astrophysics | **+15** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted |
| 498 | 💀 Refuted / Rejected | Informational Backup Systems | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted |
| 499 | 💀 Refuted / Rejected | Physical Magnetic Field Control | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted |
| 500 | 💀 Refuted / Rejected | Human Trust Variance | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬 Actively Researched (historical) |
| 501 | 💀 Refuted / Rejected | Informational Signal Jitter | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted |
| 502 | 💀 Refuted / Rejected | Music Sound (Creative & Performance Systems) | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted |
| 503 | 💀 Refuted / Rejected | Cognitive AI Weight Initialization × Creative Artistic Critique | **+15** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group 💀 Refuted |
| 504 | 💀 Refuted / Rejected | Materials Science — Phase Transitions | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted |
| 505 | 💀 Refuted / Rejected | Organizational theory — bureaucratic hierarchy | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted |
| 506 | 💀 Refuted / Rejected | Informational Scientific Experiment Orchestration | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted |
| 507 | 💀 Refuted / Rejected | Mitochondrial Energy Production × Physical Electrical Noise | **+15** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted |
| 508 | 💀 Refuted / Rejected | Cognitive Attention Map Evolution × Informational Protocol Coordination | **+15** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted |
| 509 | 💀 Refuted / Rejected | Cell biology — protein folding chaperones | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted |
| 510 | 💀 Refuted / Rejected | Creative Narrative Arc Development | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted |
| 511 | 💀 Refuted / Rejected | Mitochondrial Energy Production × Human Financial Market Systems | **+15** | ADJACENT_ACTIVE | 0% survived | narrative-shaped | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted |
| 512 | 💀 Refuted / Rejected | Cognitive AI Attention | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted |
| 513 | 💀 Refuted / Rejected | Thermodynamics — entropy and irreversibility | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted |
| 514 | 💀 Refuted / Rejected | Informational Backup Systems × Physical Acoustic Resonance | **+15** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted |
| 515 | 💀 Refuted / Rejected | Black–Scholes — financial pricing × Physics — diffusion equations | **+15** | ADJACENT_ACTIVE | 0% survived | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬 Actively Researched (historical) |
| 516 | 💀 Refuted / Rejected | Creative Instrument Track Development × Informational Error Probability | **+15** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬 Actively Researched (historical) |
| 517 | 💀 Refuted / Rejected | Cell biology — protein folding chaperones × Creative Musical Composition | **+15** | ADJACENT_ACTIVE | 0% survived | narrative-shaped | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted |
| 518 | 💀 Refuted / Rejected | Creative Album Production Orchestration × Physical Voltage Spikes | **+15** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group 💀 Refuted |
| 519 | 💀 Refuted / Rejected | Social psychology — conformity and groupthink | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬 Actively Researched (historical) |
| 520 | 💀 Refuted / Rejected | Textile engineering — weave structure and tensile strength | **+15** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group 💀 Refuted |
| 521 | 💀 Refuted / Rejected | Cryptography — zero-knowledge proofs × Mathematics — topology — knot invariants | **+15** | ADJACENT_ACTIVE | 33% survived | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 🌗 Contested (1-of-3) |
| 522 | 💀 Refuted / Rejected | Informational Backup Systems × Informational Packet Buffer Management | **+15** | ADJACENT_ACTIVE | 0% survived | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬 Actively Researched (historical) |
| 523 | 💀 Refuted / Rejected | Physical Photon Emission × Quantum Physics (Physical & Natural Systems) — Atomic: Particle position uncertain, Measurement binary, Superposition states; Domain: Quantum system evolves, Physical laws context, Log measurements; Control: Measurement apparatus, Parallel quantum processes, Atomic wavefunction collapse; Orchestration: Universal law coordination, Theoretical vs experimental environments | **+15** | ADJACENT_ACTIVE | 0% survived | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted 🔬 Actively Researched (historical) |
| 524 | 💀 Refuted / Rejected | Cryptography — public-key infrastructure × Mathematics — combinatorics — extremal counting | **+15** | ADJACENT_ACTIVE | 33% survived | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 🌗 Contested (1-of-3) |
| 525 | 💀 Refuted / Rejected | Physical Mechanical Spring Systems × Physical Electrical Noise | **+15** | ADJACENT_ACTIVE | 33% survived | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 🌗 Contested (1-of-3) |
| 526 | 💀 Refuted / Rejected | Cognitive AI Hyperparameter Orchestration × Physical Immune System | **+10** | NO_SIGNAL | 0% survived | — | 🪞 Homospatial 💀 Refuted 🔬🔥 Actively Researched (current) |
| 527 | 💀 Refuted / Rejected | Informational Bit Flips | **+10** | NO_SIGNAL | 0% survived | — | 🎭 Janusian 💀 Refuted 🔬🔥 Actively Researched (current) |
| 528 | 💀 Refuted / Rejected | Military Strategy × Creative Album Production Orchestration | **+10** | NO_SIGNAL | 0% survived | narrative-shaped | 🪞 Homospatial 💀 Refuted 🔬🔥 Actively Researched (current) |
| 529 | 💀 Refuted / Rejected | Epidemiology — herd immunity thresholds × Human Trust Variance | **+10** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted 🔬🔥 Actively Researched (current) |
| 530 | 💀 Refuted / Rejected | Human Learning Uncertainty × Physical Quantum Measurement | **+10** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative 💀 Refuted 🔬🔥 Actively Researched (current) |
| 531 | 💀 Refuted / Rejected | Black–Scholes — finance × Wiener processes | **+10** | COLLISION | — | formalism-shaped | 🧬 Bisociative 🏛️ Established Department ⚠️ Failed Honesty Check 🔬 Actively Researched |
| 532 | 💀 Refuted / Rejected | Informational Ledger State Evolution × Cryptography — zero-knowledge proofs | **+10** | COLLISION | — | formalism-shaped | 🧬 Bisociative 🏛️ Established Department ⚠️ Failed Honesty Check 🔬 Actively Researched |
| 533 | 💀 Refuted / Rejected | Comedy × Sports | **+5** | COLLISION | 0% survived | — | 🪞 Homospatial 🏛️ Established Department ⚠️ Failed Honesty Check 💀 Refuted 🔬🔥 Actively Researched (current) |
| 534 | 💀 Refuted / Rejected | Human Cognitive Bias | **+5** | FACT_CHECK_FAIL | — | — | 🎭 Janusian ⚠️ Retracted 🔬 Actively Researched |
| 535 | 💀 Refuted / Rejected | Basketball Pick-and-Roll Offense × Physical Flux Regulation | **+5** | COLLISION | 0% survived | — | 🪞 Homospatial 🏛️ Established Department 💀 Refuted 🔬 Actively Researched |
| 536 | 💀 Refuted / Rejected | Cognitive Neuron Activation × Physical Ecosystem Succession | **+5** | ADJACENT_ACTIVE | 0% survived | — | 🪞 Homospatial 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 537 | 💀 Refuted / Rejected | Control theory — Kalman filtering | **+5** | COLLISION | 0% survived | — | 🎭 Janusian 🏛️ Established Department 💀 Refuted 🔬 Actively Researched |
| 538 | 💀 Refuted / Rejected | Cognitive Model Adaptation × Physical Bridge Cable Tension | **+5** | ADJACENT_ACTIVE | 0% survived | — | 🪞 Homospatial 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 539 | 💀 Refuted / Rejected | Linguistics × Creative Idea Uncertainty | **+5** | ADJACENT_ACTIVE | 0% survived | — | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 540 | 💀 Refuted / Rejected | Game Theory Nash Bargaining × Cell Biology Protein Folding Chaperones | **+5** | ADJACENT_ACTIVE | 0% survived | — | 🪞 Homospatial 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 541 | 💀 Refuted / Rejected | Behavioral Psychology × Law | **+5** | ADJACENT_ACTIVE | 0% survived | — | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 542 | 💀 Refuted / Rejected | Culinary Arts × Physical Bridge Cable Tension | **+5** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 543 | 💀 Refuted / Rejected | Informational Routing Policy Enforcement | **+5** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 544 | 💀 Refuted / Rejected | Human Meeting Participation × Physical Quantum Measurement | **+5** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 545 | 💀 Refuted / Rejected | Creative Instrument Track Development × Physical Chemical Reaction Networks | **+5** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 546 | 💀 Refuted / Rejected | Cryptography × Physical Voltage Spikes | **+5** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 547 | 💀 Refuted / Rejected | Supply Chain Logistics × Physical Evolutionary Selection | **+5** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 548 | 💀 Refuted / Rejected | Comedy × Physical Gear System Mechanics | **+5** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 549 | 💀 Refuted / Rejected | Social Systems × Physical Chemical Reaction Networks | **+5** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 550 | 💀 Refuted / Rejected | Mycorrhizal Fungal Networks × Quantum Physics | **+5** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 551 | 💀 Refuted / Rejected | Music Theory × Human Trust Variance | **+5** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 552 | 💀 Refuted / Rejected | Education × Language Linguistics | **+5** | ADJACENT_ACTIVE | 0% survived | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 553 | 💀 Refuted / Rejected | Cognitive Concept Drift × Human Meeting Participation | **+5** | ADJACENT_ACTIVE | 0% survived | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 554 | 💀 Refuted / Rejected | Music Theory × Auction Theory | **+5** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 555 | 💀 Refuted / Rejected | Informational Hash Collisions × Physical Ecosystem Succession | **+5** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 556 | 💀 Refuted / Rejected | Fluid Dynamics × Behavioral Psychology | **+5** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 557 | 💀 Refuted / Rejected | Evolutionary Biology × Creative Inspiration Variability | **+5** | ADJACENT_ACTIVE | 0% survived | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 558 | 💀 Refuted / Rejected | Human Facilitator Cueing × Informational Cache Miss Handling | **+5** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 559 | 💀 Refuted / Rejected | Cognitive Neuron Activation × Informational Software Version Control | **+5** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 560 | 💀 Refuted / Rejected | Physical Acoustic Resonance | **+5** | COLLISION | 0% survived | — | 🎭 Janusian 🏛️ Established Department 💀 Refuted 🔬 Actively Researched |
| 561 | 💀 Refuted / Rejected | Behavioral psychology — habit formation loops × Informational Sensor Networks | **+5** | ADJACENT_ACTIVE | 0% survived | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 562 | 💀 Refuted / Rejected | Economics — auction theory × Informational Ledger State Evolution | **+5** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 563 | 💀 Refuted / Rejected | Immunology — innate immune response × Informational Sensor Networks | **+5** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🪞 Homospatial 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 564 | 💀 Refuted / Rejected | Cell biology — mitochondrial energy production × Human Social Network Dynamics | **+5** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 565 | 💀 Refuted / Rejected | Agriculture — crop rotation and soil health | **+5** | ADJACENT_ACTIVE | 0% survived | — | 🎭 Janusian 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 566 | 💀 Refuted / Rejected | Marconi — radio × Telegraphy | **+5** | ADJACENT_ACTIVE | 0% survived | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 567 | 💀 Refuted / Rejected | Astronomy — gravitational lensing × Human Defense Coordination | **+5** | ADJACENT_ACTIVE | 0% survived | mixed-uncertain | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 568 | 💀 Refuted / Rejected | Music theory — jazz improvisation over changes × Linguistics — creole genesis | **+5** | ADJACENT_ACTIVE | 0% survived | narrative-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 569 | 💀 Refuted / Rejected | Informational Database State × Mathematics — combinatorics — extremal counting | **+5** | ADJACENT_ACTIVE | 0% survived | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 570 | 💀 Refuted / Rejected | Informational Database State × Mathematics — topology — knot invariants | **+5** | ADJACENT_ACTIVE | 0% survived | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 571 | 💀 Refuted / Rejected | Physical Electrical Noise × Physical Acoustic Resonance | **+5** | ADJACENT_ACTIVE | 0% survived | formalism-shaped | 🧬 Bisociative 🗺️ Frontier Research Group ⚠️ Failed Honesty Check 💀 Refuted |
| 572 | 💀 Refuted / Rejected | Physical Flux Regulation | **+0** | NO_SIGNAL | 0% survived | — | 🎭 Janusian 💀 Refuted 🔬 Actively Researched |
| 573 | 💀 Refuted / Rejected | Informational Queue Overflow | **+0** | NO_SIGNAL | 0% survived | — | 🎭 Janusian 💀 Refuted 🔬 Actively Researched |
| 574 | 💀 Refuted / Rejected | Agriculture × Human Team Collaboration | **+0** | NO_SIGNAL | 0% survived | — | 🧬 Bisociative ⚠️ Failed Honesty Check 💀 Refuted 🔬🔥 Actively Researched (current) |
| 575 | 💀 Refuted / Rejected | Creative Improvisation Coordination × Human Individual Indecision | **+0** | NO_SIGNAL | 0% survived | — | 🧬 Bisociative 💀 Refuted 🔬 Actively Researched |
| 576 | 💀 Refuted / Rejected | Learning Systems × Informational Load Balancing | **+0** | NO_SIGNAL | 0% survived | — | 🪞 Homospatial 💀 Refuted 🔬 Actively Researched |
| 577 | 💀 Refuted / Rejected | Physical Circuit Evolution | **+0** | NO_SIGNAL | 0% survived | — | 🎭 Janusian 💀 Refuted 🔬 Actively Researched |
| 578 | 💀 Refuted / Rejected | Anthropology — gift economies and reciprocity | **+0** | NO_SIGNAL | 0% survived | — | 🎭 Janusian 💀 Refuted 🔬 Actively Researched |
| 579 | 💀 Refuted / Rejected | Materials Science — Phase Transitions × Human Social Movements | **+0** | NO_SIGNAL | 0% survived | — | 🧬 Bisociative ⚠️ Failed Honesty Check 💀 Refuted 🔬🔥 Actively Researched (current) |
| 580 | 💀 Refuted / Rejected | Sports Athletics (Creative & Performance Systems) — Atomic: Performance succeeds/fails, Opponent capabilities unknown, Multiple strategic approaches; Domain: Athletic performance evolves, Sports rules, Log training sessions; Control: Performance monitoring, Concurrent team coordination, Atomic score updates; Orchestration: Sports federation coordination, Training vs championship environments | **+0** | NO_SIGNAL | 0% survived | — | 🎭 Janusian 💀 Refuted 🔬 Actively Researched |
| 581 | 💀 Refuted / Rejected | Physics — optics — diffraction and interference patterns | **+0** | NO_SIGNAL | 0% survived | — | 🎭 Janusian 💀 Refuted 🔬 Actively Researched |
| 582 | 💀 Refuted / Rejected | Physical Mechanical Vibration × Materials science — crystal lattice defects | **+0** | NO_SIGNAL | 0% survived | formalism-shaped | 🧬 Bisociative ⚠️ Failed Honesty Check 💀 Refuted 🔬🔥 Actively Researched (current) |
| 583 | 💀 Refuted / Rejected | Graph traversal algorithms × State space search algorithms | **-5** | COLLISION | — | — | 📜 Pre-existing case study 🚫 Not a Valid Bisociation |
| 584 | 💀 Refuted / Rejected | Quantum entanglement / Bell inequalities × Quantum information science | **-5** | COLLISION | — | — | 📜 Pre-existing case study 🚫 Not a Valid Bisociation |
| 585 | 💀 Refuted / Rejected | Trigonometric function analysis × Fourier transform / spectral decomposition | **-5** | COLLISION | — | — | 📜 Pre-existing case study 🚫 Not a Valid Bisociation |
| 586 | 💀 Refuted / Rejected | Human Committee Formation × Physical Acoustic Resonance | **-5** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative 💀 Refuted 🔬 Actively Researched (historical) |
| 587 | 💀 Refuted / Rejected | Astronomy — stellar nucleosynthesis | **-5** | NO_SIGNAL | 0% survived | — | 🎭 Janusian 💀 Refuted 🔬 Actively Researched (historical) |
| 588 | 💀 Refuted / Rejected | Thermodynamics × Physical Power Grid Orchestration | **-5** | NO_SIGNAL | 0% survived | narrative-shaped | 🪞 Homospatial 💀 Refuted 🔬 Actively Researched (historical) |
| 589 | 💀 Refuted / Rejected | Evolutionary biology — punctuated equilibrium | **-5** | NO_SIGNAL | 0% survived | — | 🎭 Janusian 💀 Refuted 🔬 Actively Researched (historical) |
| 590 | 💀 Refuted / Rejected | Culinary arts — flavor pairing and Maillard reaction | **-5** | NO_SIGNAL | 0% survived | — | 🎭 Janusian 💀 Refuted 🔬 Actively Researched (historical) |
| 591 | 💀 Refuted / Rejected | Cognitive AI Hyperparameter Orchestration × Physical Mechanical Spring Systems | **-10** | COLLISION | 0% survived | — | 🧬 Bisociative 🏛️ Established Department 💀 Refuted |
| 592 | 💀 Refuted / Rejected | Human Team Collaboration × Informational Load Balancing | **-10** | COLLISION | 0% survived | — | 🪞 Homospatial 🏛️ Established Department 💀 Refuted |
| 593 | 💀 Refuted / Rejected | Cryptography × Cognitive AI Hyperparameter Orchestration | **-10** | COLLISION | 0% survived | mixed-uncertain | 🧬 Bisociative 🏛️ Established Department 💀 Refuted |
| 594 | 💀 Refuted / Rejected | Military Strategy (Human & Social Systems) | **-10** | COLLISION | 0% survived | — | 🎭 Janusian 🏛️ Established Department 💀 Refuted |
| 595 | 💀 Refuted / Rejected | Cryptography — Zero-Knowledge Proofs × Biological Systems | **-10** | FACT_CHECK_FAIL | — | mixed-uncertain | 🪞 Homospatial ⚠️ Retracted |
| 596 | 💀 Refuted / Rejected | Physical Circuit Evolution × Thermodynamics — entropy and irreversibility | **-10** | NO_SIGNAL | 0% survived | formalism-shaped | 🧬 Bisociative ⚠️ Failed Honesty Check 💀 Refuted 🔬 Actively Researched |
| 597 | 💀 Refuted / Rejected | Physical Circuit Evolution × Physical Acoustic Resonance | **-10** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative ⚠️ Failed Honesty Check 💀 Refuted 🔬 Actively Researched |
| 598 | 💀 Refuted / Rejected | Neuroscience — cortical map reorganization × Climatology — ocean current circulation (thermohaline) | **-15** | NO_SIGNAL | 0% survived | — | 🧬 Bisociative 💀 Refuted |
| 599 | 💀 Refuted / Rejected | Human immune system × Distributed ledger technology | **-15** | NO_SIGNAL | 0% survived | — | 📜 Pre-existing case study 💀 Refuted |
| 600 | 💀 Refuted / Rejected | Neural networks × Coral reef ecosystems | **-15** | NO_SIGNAL | 0% survived | — | 📜 Pre-existing case study 💀 Refuted |
| 601 | 💀 Refuted / Rejected | Sample variance / statistical estimation × Protein structure prediction | **-15** | NO_SIGNAL | 0% survived | — | 📜 Pre-existing case study 💀 Refuted |
| 602 | 💀 Refuted / Rejected | Swarm Robotics × Culinary Arts | **-15** | NO_SIGNAL | 0% survived | — | 🧬 Bisociative 💀 Refuted |
| 603 | 💀 Refuted / Rejected | Physical Bridge Cable Tension × Organizational Theory — Bureaucratic Hierarchy | **-15** | NO_SIGNAL | 0% survived | — | 🧬 Bisociative 💀 Refuted |
| 604 | 💀 Refuted / Rejected | Stellar Nucleosynthesis × Creative Album Production Orchestration | **-15** | NO_SIGNAL | 0% survived | — | 🪞 Homospatial 💀 Refuted |
| 605 | 💀 Refuted / Rejected | Language Linguistics × Physical Telescope Telemetry | **-15** | NO_SIGNAL | 0% survived | — | 🧬 Bisociative 💀 Refuted |
| 606 | 💀 Refuted / Rejected | Creative Brainstorming Facilitation × Physical Electrical Noise | **-15** | NO_SIGNAL | 0% survived | — | 🧬 Bisociative 💀 Refuted |
| 607 | 💀 Refuted / Rejected | Informational Scientific Experiment Orchestration × Physical Magnetic Fluctuation | **-15** | NO_SIGNAL | 0% survived | — | 🪞 Homospatial 💀 Refuted |
| 608 | 💀 Refuted / Rejected | Load-Bearing Structural Design × Informational Load Balancing | **-15** | NO_SIGNAL | 0% survived | — | 🪞 Homospatial 💀 Refuted |
| 609 | 💀 Refuted / Rejected | Linguistics — Creole Genesis × Economics — Market Microstructure and Order Books | **-15** | NO_SIGNAL | 0% survived | — | 🪞 Homospatial 💀 Refuted |
| 610 | 💀 Refuted / Rejected | Creative Instrument Track Development × Informational Load Balancing | **-15** | NO_SIGNAL | 0% survived | — | 🧬 Bisociative 💀 Refuted |
| 611 | 💀 Refuted / Rejected | Creative Musical Composition × Physical Mechanical Spring Systems | **-15** | NO_SIGNAL | 0% survived | — | 🪞 Homospatial 💀 Refuted |
| 612 | 💀 Refuted / Rejected | Linguistics — Creole Genesis × Informational Backup Systems | **-15** | NO_SIGNAL | 0% survived | — | 🪞 Homospatial 💀 Refuted |
| 613 | 💀 Refuted / Rejected | Linguistics — Creole Genesis × Learning Systems | **-15** | NO_SIGNAL | 0% survived | — | 🪞 Homospatial 💀 Refuted |
| 614 | 💀 Refuted / Rejected | Neuroscience — Synaptic Pruning × Human Trust Variance | **-15** | NO_SIGNAL | 0% survived | — | 🪞 Homospatial 💀 Refuted |
| 615 | 💀 Refuted / Rejected | Human Urban Planning × Physical Photon Emission | **-15** | NO_SIGNAL | 0% survived | — | 🧬 Bisociative 💀 Refuted |
| 616 | 💀 Refuted / Rejected | Informational Routing Policy Enforcement × Physical Thermal Variation | **-15** | NO_SIGNAL | 0% survived | — | 🧬 Bisociative 💀 Refuted |
| 617 | 💀 Refuted / Rejected | Healthcare × Physical Voltage Spikes | **-15** | NO_SIGNAL | 0% survived | — | 🧬 Bisociative 💀 Refuted |
| 618 | 💀 Refuted / Rejected | Urban Planning × Informational Packet Buffer Management | **-15** | NO_SIGNAL | 0% survived | — | 🪞 Homospatial 💀 Refuted |
| 619 | 💀 Refuted / Rejected | Geology × Human Committee Formation | **-15** | NO_SIGNAL | 0% survived | — | 🧬 Bisociative 💀 Refuted |
| 620 | 💀 Refuted / Rejected | Behavioral psychology — habit formation loops × Informational Error Probability | **-15** | NO_SIGNAL | 0% survived | — | 🪞 Homospatial 💀 Refuted |
| 621 | 💀 Refuted / Rejected | Cognitive Streaming Data Processing × Creative Film Production Orchestration | **-15** | NO_SIGNAL | 0% survived | — | 🪞 Homospatial 💀 Refuted |
| 622 | 💀 Refuted / Rejected | Ecology × Informational Load Balancing | **-15** | NO_SIGNAL | 0% survived | — | 🪞 Homospatial 💀 Refuted |
| 623 | 💀 Refuted / Rejected | Evolutionary Biology — Punctuated Equilibrium × Physical Photon Emission | **-15** | NO_SIGNAL | 0% survived | — | 🪞 Homospatial 💀 Refuted |
| 624 | 💀 Refuted / Rejected | Music — sample-based hip-hop production × Human Financial Market Systems | **-15** | NO_SIGNAL | 0% survived | — | 🪞 Homospatial 💀 Refuted |
| 625 | 💀 Refuted / Rejected | Cognitive Model Adaptation | **-15** | NO_SIGNAL | 0% survived | — | 🎭 Janusian 💀 Refuted |
| 626 | 💀 Refuted / Rejected | Linguistics × Cognitive AI Preprocessing Pipelines | **-15** | NO_SIGNAL | 0% survived | — | 🧬 Bisociative 💀 Refuted |
| 627 | 💀 Refuted / Rejected | Ecology × Human Learning Uncertainty | **-15** | NO_SIGNAL | 0% survived | — | 🧬 Bisociative 💀 Refuted |
| 628 | 💀 Refuted / Rejected | Climatology — ocean current circulation × Anthropology — gift economies and reciprocity | **-15** | NO_SIGNAL | 0% survived | — | 🪞 Homospatial 💀 Refuted |
| 629 | 💀 Refuted / Rejected | Informational OS Thread Scheduling × Physical Ecosystem Succession | **-15** | NO_SIGNAL | 0% survived | — | 🧬 Bisociative 💀 Refuted |
| 630 | 💀 Refuted / Rejected | Epigenetics — gene expression regulation without DNA change | **-15** | NO_SIGNAL | 0% survived | — | 🎭 Janusian 💀 Refuted |
| 631 | 💀 Refuted / Rejected | Immunology × Linguistics | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative 💀 Refuted |
| 632 | 💀 Refuted / Rejected | Organizational Theory × Physical Thermal Variation | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative 💀 Refuted |
| 633 | 💀 Refuted / Rejected | Cell Biology × Creative Album Production Orchestration | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative 💀 Refuted |
| 634 | 💀 Refuted / Rejected | Cognitive Neuron Activation × Informational Backup Systems | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative 💀 Refuted |
| 635 | 💀 Refuted / Rejected | Cross Domain Pattern Recognition × Informational Backup Systems | **-15** | NO_SIGNAL | 0% survived | narrative-shaped | 🪞 Homospatial 💀 Refuted |
| 636 | 💀 Refuted / Rejected | Cryptography × Epigenetics | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative 💀 Refuted |
| 637 | 💀 Refuted / Rejected | Climatology × Military Strategy | **-15** | NO_SIGNAL | 0% survived | narrative-shaped | 🪞 Homospatial 💀 Refuted |
| 638 | 💀 Refuted / Rejected | Coalition Government Formation × Climate Science | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 639 | 💀 Refuted / Rejected | Geology × Informational Cache Miss Handling | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative 💀 Refuted |
| 640 | 💀 Refuted / Rejected | Cryptography — zero-knowledge proofs × Physical Thermal Variation | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 641 | 💀 Refuted / Rejected | Geology × Cross Domain Pattern Recognition | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 642 | 💀 Refuted / Rejected | Telecommunications — error-correcting codes | **-15** | NO_SIGNAL | 0% survived | — | 🎭 Janusian 💀 Refuted |
| 643 | 💀 Refuted / Rejected | Physical Bridge Cable Tension × Physical Elastic Deformation | **-15** | NO_SIGNAL | 0% survived | formalism-shaped | 🪞 Homospatial 💀 Refuted |
| 644 | 💀 Refuted / Rejected | Law × Informational Load Balancing | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative 💀 Refuted |
| 645 | 💀 Refuted / Rejected | Baseball Pitch Sequencing × Human Social Influence | **-15** | NO_SIGNAL | 0% survived | narrative-shaped | 🧬 Bisociative 💀 Refuted |
| 646 | 💀 Refuted / Rejected | Ocean Current Circulation × Cognitive Concept Drift | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 647 | 💀 Refuted / Rejected | Neuroscience — Synaptic Pruning × Telecommunications — Error-Correcting Codes | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 648 | 💀 Refuted / Rejected | Architecture — load-bearing structural design × Cognitive Neuron Activation | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 649 | 💀 Refuted / Rejected | Human Facilitator Cueing × Informational Database Sharding | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 650 | 💀 Refuted / Rejected | Cross Domain Pattern Recognition × Informational Software Version Control | **-15** | NO_SIGNAL | 0% survived | narrative-shaped | 🧬 Bisociative 💀 Refuted |
| 651 | 💀 Refuted / Rejected | Cross Domain Pattern Recognition × Physical Voltage Spikes | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative 💀 Refuted |
| 652 | 💀 Refuted / Rejected | Human Role Ambiguity × Human Trust Variance | **-15** | NO_SIGNAL | 0% survived | narrative-shaped | 🪞 Homospatial 💀 Refuted |
| 653 | 💀 Refuted / Rejected | Organizational Theory — Bureaucratic Hierarchy × Music — Sample-Based Hip-Hop Production | **-15** | NO_SIGNAL | 0% survived | narrative-shaped | 🪞 Homospatial 💀 Refuted |
| 654 | 💀 Refuted / Rejected | Physical Voltage Spikes | **-15** | NO_SIGNAL | 0% survived | — | 🎭 Janusian 💀 Refuted |
| 655 | 💀 Refuted / Rejected | Biological Systems × Informational Cache Miss Handling | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative 💀 Refuted |
| 656 | 💀 Refuted / Rejected | Geology — Plate Tectonics | **-15** | NO_SIGNAL | 0% survived | — | 🎭 Janusian 💀 Refuted |
| 657 | 💀 Refuted / Rejected | Cross Domain Pattern Recognition × Human Cognitive Bias | **-15** | NO_SIGNAL | 0% survived | narrative-shaped | 🧬 Bisociative 💀 Refuted |
| 658 | 💀 Refuted / Rejected | Astrophysics × Informational Hash Collisions | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 659 | 💀 Refuted / Rejected | Cognitive AI Attention × Informational Software Version Control | **-15** | NO_SIGNAL | 0% survived | narrative-shaped | 🪞 Homospatial 💀 Refuted |
| 660 | 💀 Refuted / Rejected | Creative Artistic Critique × Physical Gear System Mechanics | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative 💀 Refuted |
| 661 | 💀 Refuted / Rejected | Supply Chain Logistics × Telecommunications | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 662 | 💀 Refuted / Rejected | Linguistics — Creole Genesis × Human Financial Market Systems | **-15** | NO_SIGNAL | 0% survived | narrative-shaped | 🧬 Bisociative 💀 Refuted |
| 663 | 💀 Refuted / Rejected | Astronomy — stellar nucleosynthesis × Epidemiology — herd immunity thresholds | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 664 | 💀 Refuted / Rejected | Immunology × Human Meeting Participation | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative 💀 Refuted |
| 665 | 💀 Refuted / Rejected | Architecture (Creative & Performance Systems) × Human Individual Indecision | **-15** | NO_SIGNAL | 0% survived | narrative-shaped | 🪞 Homospatial 💀 Refuted |
| 666 | 💀 Refuted / Rejected | Creative Idea Uncertainty × Physical Electrical Noise | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 667 | 💀 Refuted / Rejected | Knowledge Systems × Informational Distributed Consensus | **-15** | NO_SIGNAL | 0% survived | narrative-shaped | 🪞 Homospatial 💀 Refuted |
| 668 | 💀 Refuted / Rejected | Fluid Dynamics × Sports Athletics | **-15** | NO_SIGNAL | 0% survived | narrative-shaped | 🧬 Bisociative 💀 Refuted |
| 669 | 💀 Refuted / Rejected | Geology × Sports | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative 💀 Refuted |
| 670 | 💀 Refuted / Rejected | Behavioral Psychology — Operant Conditioning × Creative Improvisation Adjustment | **-15** | NO_SIGNAL | 0% survived | narrative-shaped | 🪞 Homospatial 💀 Refuted |
| 671 | 💀 Refuted / Rejected | Mitochondrial Energy Production × Physical Chemical Reaction Networks | **-15** | NO_SIGNAL | 0% survived | formalism-shaped | 🪞 Homospatial 💀 Refuted |
| 672 | 💀 Refuted / Rejected | Control Theory — Kalman Filtering × Informational Bit Flips | **-15** | NO_SIGNAL | 0% survived | formalism-shaped | 🪞 Homospatial 💀 Refuted |
| 673 | 💀 Refuted / Rejected | Informational Protocol Coordination × Physical Elastic Deformation | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 674 | 💀 Refuted / Rejected | Linguistics — creole genesis × Law — contract formation and offer/acceptance | **-15** | NO_SIGNAL | 0% survived | narrative-shaped | 🪞 Homospatial 💀 Refuted |
| 675 | 💀 Refuted / Rejected | Music × Human Learning Uncertainty | **-15** | NO_SIGNAL | 0% survived | narrative-shaped | 🧬 Bisociative 💀 Refuted |
| 676 | 💀 Refuted / Rejected | Creative Block × Bridge Cable Tension | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative 💀 Refuted |
| 677 | 💀 Refuted / Rejected | Climatology — ocean current circulation × Human Defense Coordination | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 678 | 💀 Refuted / Rejected | Ecology — predator-prey population dynamics × Physical Magnetic Field Control | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 679 | 💀 Refuted / Rejected | Mycorrhizal Fungal Networks × Packet Switching and Routing | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 680 | 💀 Refuted / Rejected | Crystal Lattice Defects × Linguistic Evolution | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 681 | 💀 Refuted / Rejected | Informational Cache Miss Handling × Physical Gear System Mechanics | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative 💀 Refuted |
| 682 | 💀 Refuted / Rejected | Astronomy × Cognitive AI Preprocessing Pipelines | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 683 | 💀 Refuted / Rejected | Cell Biology × Culinary Arts | **-15** | NO_SIGNAL | 0% survived | narrative-shaped | 🧬 Bisociative 💀 Refuted |
| 684 | 💀 Refuted / Rejected | Fluid Dynamics × Informational Event-Driven Systems | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 685 | 💀 Refuted / Rejected | Baseball Pitch Sequencing × Quantum Physics | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 686 | 💀 Refuted / Rejected | Supply Chain Logistics × Physical Circuit Evolution | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 687 | 💀 Refuted / Rejected | Astronomy × Law | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative 💀 Refuted |
| 688 | 💀 Refuted / Rejected | Epigenetics × Cognitive Concept Drift | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative 💀 Refuted |
| 689 | 💀 Refuted / Rejected | Biological Systems × Cognitive AI Hyperparameter Orchestration | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 690 | 💀 Refuted / Rejected | Informational Load Balancing × Physical Evolutionary Selection | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 691 | 💀 Refuted / Rejected | Culinary Arts (Creative & Performance Systems) — Atomic: Recipe succeeds/fails, Ingredient freshness unknown, Multiple flavor combinations; Domain: Dish develops through cooking, Recipes & traditions, Log cooking steps; Control: External food suppliers, Concurrent cooking processes, Atomic seasoning adjustments; Orchestration: Restaurant coordination, Recipe vs service environments × Human Individual Indecision | **-15** | NO_SIGNAL | 0% survived | narrative-shaped | 🧬 Bisociative 💀 Refuted |
| 692 | 💀 Refuted / Rejected | Evolutionary biology — punctuated equilibrium × Physical Magnetic Field Control | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative 💀 Refuted |
| 693 | 💀 Refuted / Rejected | Urban planning — traffic flow optimization × Agriculture — crop rotation and soil health | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 694 | 💀 Refuted / Rejected | Cell biology — protein folding chaperones × Informational Software Version Control | **-15** | NO_SIGNAL | 0% survived | narrative-shaped | 🪞 Homospatial 💀 Refuted |
| 695 | 💀 Refuted / Rejected | Cognitive Development (Information & Intelligence Systems) — Atomic: Learning outcome uncertain, Skill acquisition succeeds/fails, Multiple learning paths; Domain: Cognitive skills evolve, Learning context, Log development milestones; Control: External learning resources, Parallel skill development, Atomic knowledge integration; Orchestration: Learning system coordination, Practice vs application environments × Informational Bit Flips | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 696 | 💀 Refuted / Rejected | Agriculture — crop rotation and soil health × Creative Narrative Arc Development | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative 💀 Refuted |
| 697 | 💀 Refuted / Rejected | Creative Musical Motif Deviation × Informational Bit Flips | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative 💀 Refuted |
| 698 | 💀 Refuted / Rejected | Geology — sedimentary layering and stratigraphy × Epidemiology — herd immunity thresholds | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 699 | 💀 Refuted / Rejected | Education (Information & Intelligence Systems) — Atomic: Assignment grade uncertain, Learning succeeds/fails, Multiple styles; Domain: Student knowledge evolves, Educational standards, Log progress; Control: External assessment systems, Concurrent learning paths, Atomic grade updates; Orchestration: Curriculum coordination, Practice vs real-world environments × Physical Magnetic Field Control | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative 💀 Refuted |
| 700 | 💀 Refuted / Rejected | Creative Inspiration Variability × Informational Packet Buffer Management | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 701 | 💀 Refuted / Rejected | Supply chain logistics — bullwhip effect × Geology — sedimentary layering and stratigraphy | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 702 | 💀 Refuted / Rejected | Anthropology — gift economies and reciprocity × Cognitive AI Attention | **-15** | NO_SIGNAL | 0% survived | narrative-shaped | 🪞 Homospatial 💀 Refuted |
| 703 | 💀 Refuted / Rejected | Telecommunications — packet switching and routing × Music Sound (Creative & Performance Systems) — Atomic: Note pitch flat/sharp, Instrument availability uncertain, Multiple harmonic possibilities; Domain: Musical composition evolves, Music theory context, Log performances; Control: Live audience feedback, Concurrent musician coordination, Atomic tempo synchronization; Orchestration: Music industry coordination, Composition vs performance environments | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial 💀 Refuted |
| 704 | 💀 Refuted / Rejected | Agriculture — crop rotation and soil health | **-15** | NO_SIGNAL | 0% survived | — | 🎭 Janusian 💀 Refuted |
| 705 | 💀 Refuted / Rejected | Control theory — Kalman filtering × Physics — particle physics — Standard Model symmetry breaking | **-15** | NO_SIGNAL | 0% survived | formalism-shaped | 🧬 Bisociative 💀 Refuted |
| 706 | 💀 Refuted / Rejected | Physical Gear System Mechanics × Physical Circuit Evolution | **-15** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative 💀 Refuted |
| 707 | 💀 Refuted / Rejected | Epidemiology × Human Cognitive Bias | **-20** | COLLISION | 0% survived | — | 🧬 Bisociative 🏛️ Established Department ⚠️ Failed Honesty Check 💀 Refuted |
| 708 | 💀 Refuted / Rejected | Baseball Pitch Sequencing × Finance Transaction Dynamics | **-25** | NO_SIGNAL | 0% survived | — | 🪞 Homospatial ⚠️ Failed Honesty Check 💀 Refuted |
| 709 | 💀 Refuted / Rejected | Human Role Ambiguity × Informational Hash Collisions | **-25** | NO_SIGNAL | 0% survived | — | 🪞 Homospatial ⚠️ Failed Honesty Check 💀 Refuted |
| 710 | 💀 Refuted / Rejected | Protein Folding Chaperones × Linguistic Systems | **-25** | NO_SIGNAL | 0% survived | — | 🪞 Homospatial ⚠️ Failed Honesty Check 💀 Refuted |
| 711 | 💀 Refuted / Rejected | Human Facilitator Cueing × Informational Bit Flips | **-25** | NO_SIGNAL | 0% survived | — | 🧬 Bisociative ⚠️ Failed Honesty Check 💀 Refuted |
| 712 | 💀 Refuted / Rejected | Culinary Arts × Informational Mobile System Coordination | **-25** | NO_SIGNAL | 0% survived | — | 🧬 Bisociative ⚠️ Failed Honesty Check 💀 Refuted |
| 713 | 💀 Refuted / Rejected | Market Microstructure × Legal Systems | **-25** | NO_SIGNAL | 0% survived | — | 🪞 Homospatial ⚠️ Failed Honesty Check 💀 Refuted |
| 714 | 💀 Refuted / Rejected | Neuroscience — Cortical Map Reorganization × Informational Backup Systems | **-25** | NO_SIGNAL | 0% survived | — | 🪞 Homospatial ⚠️ Failed Honesty Check 💀 Refuted |
| 715 | 💀 Refuted / Rejected | Cognitive Development × Physical Immune System | **-25** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial ⚠️ Failed Honesty Check 💀 Refuted |
| 716 | 💀 Refuted / Rejected | Human Facilitator Cueing × Physical Chemical Reaction Networks | **-25** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial ⚠️ Failed Honesty Check 💀 Refuted |
| 717 | 💀 Refuted / Rejected | Astronomy — Stellar Nucleosynthesis × Creative Improvisation Adjustment | **-25** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial ⚠️ Failed Honesty Check 💀 Refuted |
| 718 | 💀 Refuted / Rejected | Cognitive Model Adaptation × Physical Chemical Reaction Networks | **-25** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative ⚠️ Failed Honesty Check 💀 Refuted |
| 719 | 💀 Refuted / Rejected | Cognitive AI Hyperparameter Orchestration × Creative Narrative Arc Development | **-25** | NO_SIGNAL | 0% survived | narrative-shaped | 🪞 Homospatial ⚠️ Failed Honesty Check 💀 Refuted |
| 720 | 💀 Refuted / Rejected | Cognitive Neuron Activation × Physical Gear System Mechanics | **-25** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial ⚠️ Failed Honesty Check 💀 Refuted |
| 721 | 💀 Refuted / Rejected | Sports Athletics × Informational Software Version Control | **-25** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial ⚠️ Failed Honesty Check 💀 Refuted |
| 722 | 💀 Refuted / Rejected | Human Social Network Dynamics × Physical Immune System | **-25** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial ⚠️ Failed Honesty Check 💀 Refuted |
| 723 | 💀 Refuted / Rejected | Cell Biology × Human Trust Variance | **-25** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative ⚠️ Failed Honesty Check 💀 Refuted |
| 724 | 💀 Refuted / Rejected | Supply Chain Logistics × Music Production | **-25** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial ⚠️ Failed Honesty Check 💀 Refuted |
| 725 | 💀 Refuted / Rejected | Legal Systems × Physical Protein Folding | **-25** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial ⚠️ Failed Honesty Check 💀 Refuted |
| 726 | 💀 Refuted / Rejected | Cell Biology — Protein Folding Chaperones × Informational OS Thread Scheduling | **-25** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial ⚠️ Failed Honesty Check 💀 Refuted |
| 727 | 💀 Refuted / Rejected | Urban Planning Traffic Flow Optimization × Informational Cache Miss Handling | **-25** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial ⚠️ Failed Honesty Check 💀 Refuted |
| 728 | 💀 Refuted / Rejected | Materials Science — Phase Transitions × Physical Mechanical Spring Systems | **-25** | NO_SIGNAL | 0% survived | formalism-shaped | 🪞 Homospatial ⚠️ Failed Honesty Check 💀 Refuted |
| 729 | 💀 Refuted / Rejected | Mitochondrial Energy Production × Cross Domain Pattern Recognition | **-25** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial ⚠️ Failed Honesty Check 💀 Refuted |
| 730 | 💀 Refuted / Rejected | Military Strategy × Creative Artistic Arrangement | **-25** | NO_SIGNAL | 0% survived | narrative-shaped | 🪞 Homospatial ⚠️ Failed Honesty Check 💀 Refuted |
| 731 | 💀 Refuted / Rejected | Music × Physical Immune System | **-25** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial ⚠️ Failed Honesty Check 💀 Refuted |
| 732 | 💀 Refuted / Rejected | Astronomy — Stellar Nucleosynthesis × Creative Improvisation Coordination | **-25** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial ⚠️ Failed Honesty Check 💀 Refuted |
| 733 | 💀 Refuted / Rejected | Music — sample-based hip-hop production × Informational Database Sharding | **-25** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial ⚠️ Failed Honesty Check 💀 Refuted |
| 734 | 💀 Refuted / Rejected | Biological Systems × Creative Block | **-25** | NO_SIGNAL | 0% survived | narrative-shaped | 🧬 Bisociative ⚠️ Failed Honesty Check 💀 Refuted |
| 735 | 💀 Refuted / Rejected | Climatology × Cognitive Model Adaptation | **-25** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative ⚠️ Failed Honesty Check 💀 Refuted |
| 736 | 💀 Refuted / Rejected | Cognitive Concept Drift × Creative Idea Uncertainty | **-25** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative ⚠️ Failed Honesty Check 💀 Refuted |
| 737 | 💀 Refuted / Rejected | Human Individual Indecision × Physical Telescope Telemetry | **-25** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial ⚠️ Failed Honesty Check 💀 Refuted |
| 738 | 💀 Refuted / Rejected | Linguistics × Behavioral Psychology | **-25** | NO_SIGNAL | 0% survived | narrative-shaped | 🧬 Bisociative ⚠️ Failed Honesty Check 💀 Refuted |
| 739 | 💀 Refuted / Rejected | Music — sample-based hip-hop production × Informational Load Balancing | **-25** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative ⚠️ Failed Honesty Check 💀 Refuted |
| 740 | 💀 Refuted / Rejected | Finance (Human & Social Systems) — Atomic: Transaction succeeds/fails, Account lookup missing, Multiple positions; Domain: Portfolio evolves, Market context, Audit logging; Control: External trades & APIs, Streaming market data, Atomic account updates; Orchestration: Regulatory coordination, Simulation vs live trading × Physical Magnetic Fluctuation | **-25** | FACT_CHECK_FAIL | 0% survived | mixed-uncertain | 🪞 Homospatial ⚠️ Retracted 💀 Refuted |
| 741 | 💀 Refuted / Rejected | Human Social Influence × Physical Mechanical Vibration | **-25** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial ⚠️ Failed Honesty Check 💀 Refuted |
| 742 | 💀 Refuted / Rejected | Astronomy — gravitational lensing × Architecture (Creative & Performance Systems) — Atomic: Building permits approved/denied, Material availability uncertain, Multiple design options; Domain: Building construction progresses, Building codes, Log construction events; Control: Building inspections & permits, Concurrent construction, Atomic structural updates; Orchestration: City planning coordination, Design vs construction environments | **-25** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative ⚠️ Failed Honesty Check 💀 Refuted |
| 743 | 💀 Refuted / Rejected | Cell biology — protein folding chaperones × Sports Athletics (Creative & Performance Systems) — Atomic: Performance succeeds/fails, Opponent capabilities unknown, Multiple strategic approaches; Domain: Athletic performance evolves, Sports rules, Log training sessions; Control: Performance monitoring, Concurrent team coordination, Atomic score updates; Orchestration: Sports federation coordination, Training vs championship environments | **-25** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial ⚠️ Failed Honesty Check 💀 Refuted |
| 744 | 💀 Refuted / Rejected | Informational Database State × Physical Gear System Mechanics | **-25** | NO_SIGNAL | 0% survived | mixed-uncertain | 🪞 Homospatial ⚠️ Failed Honesty Check 💀 Refuted |
| 745 | 💀 Refuted / Rejected | Astronomy — gravitational lensing × Informational Signal Jitter | **-25** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative ⚠️ Failed Honesty Check 💀 Refuted |
| 746 | 💀 Refuted / Rejected | Informational Error Probability × Mathematics — topology — knot invariants | **-25** | NO_SIGNAL | 0% survived | formalism-shaped | 🧬 Bisociative ⚠️ Failed Honesty Check 💀 Refuted |
| 747 | 💀 Refuted / Rejected | Physical Elastic Deformation × Physical Voltage Spikes | **-25** | NO_SIGNAL | 0% survived | formalism-shaped | 🧬 Bisociative ⚠️ Failed Honesty Check 💀 Refuted |
| 748 | 💀 Refuted / Rejected | Control theory — Kalman filtering × Astronomy — gravitational lensing | **-25** | NO_SIGNAL | 0% survived | formalism-shaped | 🧬 Bisociative ⚠️ Failed Honesty Check 💀 Refuted |
| 749 | 💀 Refuted / Rejected | Control theory — Kalman filtering × Genomics — GWAS and polygenic risk | **-25** | NO_SIGNAL | 0% survived | mixed-uncertain | 🧬 Bisociative ⚠️ Failed Honesty Check 💀 Refuted |

## Held out of scoring (non-standard verdict)

- **Physics × The empiricism problem (philosophy of science)** — verdict: "FLAGGED (not a standard bisociation pair; real factual concern found)" — not one of the four canonical outcomes the point schema is built for; see its own verification file for what was actually found.

## Score breakdown, per entry

### Literature — unreliable-narrator technique — 🛡️ Survived Refutation (+67)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation survived (2-of-3): +12
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Computer science — compiler instruction scheduling — 🛡️ Survived Refutation (+60)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation survived (3-of-3): +20
- Actively researched, most recent evidence 2008 — real, but not a currently live thread: +10

### Fisheries — stock recruitment dynamics — 🛡️ Survived Refutation (+57)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation survived (2-of-3): +12
- Actively researched, most recent evidence 2020 (6y old): +15

### Cognitive psychology — working memory and chunking — 🛡️ Survived Refutation (+57)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation survived (2-of-3): +12
- Actively researched, most recent evidence 2019 (7y old): +15

### Zoology — animal migration navigation — 🛡️ Survived Refutation (+57)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation survived (2-of-3): +12
- Actively researched, most recent evidence 2022 (4y old): +15

### Mathematics — topology — knot invariants — 🛡️ Survived Refutation (+52)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation survived (2-of-3): +12
- Actively researched, most recent evidence 2001 — real, but not a currently live thread: +10

### Nash — Game Theory × Evolutionary Biology — 🛡️ Survived Refutation (+20)

- Phase 2 COLLISION: +0 (ground truth — no discovery credit, see below)
- Adversarial refutation survived (3-of-3): +20

### Kahneman & Tversky — Cognitive Bias × Rational-Choice Theory — 🛡️ Survived Refutation (+12)

- Phase 2 COLLISION: +0 (ground truth — no discovery credit, see below)
- Adversarial refutation survived (2-of-3): +12

### Planck — Quantization × Thermodynamics — 🛡️ Survived Refutation (+12)

- Phase 2 ADJACENT_ACTIVE: +0 (ground truth — no discovery credit, see below)
- Adversarial refutation survived (2-of-3): +12

### Jacob & Monod — Gene Regulation × Control Engineering — 🛡️ Survived Refutation (+12)

- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation survived (2-of-3): +12

### Ostrom — Commons Governance × Ecology — 🛡️ Survived Refutation (+12)

- Phase 2 ADJACENT_ACTIVE: +0 (ground truth — no discovery credit, see below)
- Adversarial refutation survived (2-of-3): +12

### Simon — Bounded Rationality × Heuristic Search — 🛡️ Survived Refutation (+12)

- Phase 2 COLLISION: +0 (ground truth — no discovery credit, see below)
- Adversarial refutation survived (2-of-3): +12

### Hayek — Dispersed Knowledge × Market Price Signals — 🛡️ Survived Refutation (+12)

- Phase 2 ADJACENT_ACTIVE: +0 (ground truth — no discovery credit, see below)
- Adversarial refutation survived (2-of-3): +12

### Einstein — Special Relativity × Maxwell — Electromagnetism — 🛡️ Survived Refutation (+12)

- Phase 2 ADJACENT_ACTIVE: +0 (ground truth — no discovery credit, see below)
- Adversarial refutation survived (2-of-3): +12

### Oceanography — thermocline stratification — 🛡️ Survived Refutation (+12)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation survived (2-of-3): +12

### Linguistics — Historical Sound Change — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Self-Assembly of Molecular Structures × Gaming Narrative Systems — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Human Trust Variance × Cryptography — Zero-Knowledge Proofs — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Physical Quantum Measurement — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Physical Mechanical Spring Systems × Human Emotional Fluctuation — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Creative Narrative Arc Development × Informational Distributed Consensus — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Self-Assembly of Molecular Structures × Informational Event-Driven Systems — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Adaptive Immune Memory × Human Urban Planning — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Law × Informational Database State — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Swarm Robotics × Physical Acoustic Resonance — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Cognitive Attention Map Evolution × Creative Artistic Critique — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Social Systems × Human Team Collaboration — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (3/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Creative Narrative Arc Development × Human Committee Formation — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Creative Artistic Critique × Creative Idea Uncertainty — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Swarm Robotics × Creative Performance Monitoring — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Informational Database Sharding — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Climatology — feedback loops in ice-albedo effect — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Language Linguistics × Military Strategy — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Biological Systems × Creative Musical Motif Deviation — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Ocean Current Circulation × Epigenetics — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Healthcare (Human & Social Systems) × Creative Idea Uncertainty — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Creative Inspiration Variability — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Human Financial Market Systems — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Education (Information & Intelligence Systems) × Human Meeting Participation — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Climate Science × Gaming Narrative — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Human Urban Planning × Physical Ecosystem Succession — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Informational Error Probability × Physical Circuit Evolution — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Supply Chain Logistics × Cryptography — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Human Urban Planning — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Sports Athletics × Physical Thermal Variation — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Human Financial Trading Algorithms × Physical Power Grid Orchestration — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Physical Gear System Mechanics — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Physical Power Grid Orchestration — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Epigenetics × Physical Magnetic Fluctuation — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Creative Improvisation Coordination × Physical Evolutionary Selection — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Healthcare × Creative Album Production Orchestration — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Music Theory × Physical Acoustic Resonance — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Control Theory — Kalman Filtering × Quantum Physics — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Thermodynamics × Creative Inspiration Variability — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Urban Planning × Telecommunications — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Knowledge Systems × Physical Power Grid Orchestration — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Comedy × Cognitive AI Attention — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Economics × Cognitive AI Attention — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Game Theory × Gaming Narrative — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Informational Routing Policy Enforcement × Physical Evolutionary Selection — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Cognitive AI Pipeline Orchestration — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Cognitive Streaming Data Processing × Creative Film Production Orchestration — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Banking — fractional reserve credit multiplier — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Dance — choreographic phrase repetition — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Metallurgy — annealing and grain refinement — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Military strategy — asymmetric guerrilla tactics — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Informational Database Sharding × Informational Distributed Consensus — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Physics — particle physics — Standard Model symmetry breaking × Physics — optics — diffraction and interference patterns — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Physical Circuit Evolution × Physical Mechanical Vibration — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Ethics — trolley-problem moral reasoning — 🗺️ Verified, Unrefuted (+55)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Ecology × Telecommunications — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2021 (5y old): +15

### Materials Science — Crystal Lattice Defects — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2022 (4y old): +15

### Anthropology × Military Strategy — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2023 (3y old): +15

### Creative Musical Motif Deviation × Evolutionary Biology — Punctuated Equilibrium — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2022 (4y old): +15

### Human Financial Trading Algorithms × Ecology — Predator-Prey Population Dynamics — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2021 (5y old): +15

### Creative Block — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2021 (5y old): +15

### Physical Chemical Reaction Networks × Human Committee Formation — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2021 (5y old): +15

### Culinary Arts (Creative & Performance Systems) — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2020 (6y old): +15

### Epidemiology — Herd Immunity Thresholds — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2021 (5y old): +15

### Physical Ecosystem Succession × Physical Immune System — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2022 (4y old): +15

### Auction Theory × Human Defense Coordination — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2023 (3y old): +15

### Biological Systems × Human Social Network Dynamics — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2019 (7y old): +15

### Gaming Narrative × Cognitive Attention Map Evolution — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2017 (9y old): +15

### Biological Systems × Informational Scientific Experiment Orchestration — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2018 (8y old): +15

### Creative Narrative Arc Development × Human Team Collaboration — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2020 (6y old): +15

### Human Meeting Participation — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2017 (9y old): +15

### Immunology × Behavioral Psychology — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2018 (8y old): +15

### Architecture — load-bearing structural design — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2019 (7y old): +15

### Telecommunications × Quantum Physics — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2023 (3y old): +15

### Creative Musical Composition — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2019 (7y old): +15

### Urban Planning × Creative Improvisation Adjustment — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2023 (3y old): +15

### Creative Instrument Track Development — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2021 (5y old): +15

### Physical Evolutionary Selection — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2022 (4y old): +15

### Chemistry × Human Social Network Dynamics — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2021 (5y old): +15

### Informational Software Version Control — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2020 (6y old): +15

### Telecommunications × Cognitive Streaming Data Processing — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2019 (7y old): +15

### Urban Planning × Cryptography — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2023 (3y old): +15

### Human Social Influence × Informational Sensor Networks — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2017 (9y old): +15

### Music Theory × Human Social Network Dynamics — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2022 (4y old): +15

### Healthcare × Creative Film Production Orchestration — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2023 (3y old): +15

### Urban Planning × Physical Chemical Reaction Networks — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2023 (3y old): +15

### Anthropology × Creative Film Production Orchestration — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2023 (3y old): +15

### Urban Planning × Informational Sensor Networks — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2020 (6y old): +15

### Education (Information & Intelligence Systems) — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2022 (4y old): +15

### Chemistry × Physical Immune System — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2023 (3y old): +15

### Cognitive Reinforcement Learning × Informational OS Thread Scheduling — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2022 (4y old): +15

### Physical Thermal Variation — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2020 (6y old): +15

### Organizational Theory × Creative Inspiration Variability — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2022 (4y old): +15

### Urban Planning × Agriculture — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2020 (6y old): +15

### Music theory — counterpoint and voice leading — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2020 (6y old): +15

### Creative Artistic Arrangement × Informational Distributed Consensus — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2021 (5y old): +15

### Human Meeting Participation × Informational Sensor Networks — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2021 (5y old): +15

### Physical Chemical Reaction Networks × Physical Magnetic Fluctuation — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2021 (5y old): +15

### Prigogine — thermodynamics × Complex systems — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2020 (6y old): +15

### Watson & Crick — DNA × Information theory — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2016 (10y old): +15

### Genetics — Mendelian inheritance and linkage — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2016 (10y old): +15

### Logic — Gödel incompleteness and self-reference — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2021 (5y old): +15

### Sociology — social network diffusion of innovation — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2018 (8y old): +15

### Viticulture — terroir and grape ripening — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2017 (9y old): +15

### Astrophysics — orbital resonance — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2022 (4y old): +15

### Forestry — controlled burn succession — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2016 (10y old): +15

### Microbiology — biofilm formation — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (3/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2022 (4y old): +15

### Veterinary medicine — zoonotic disease transmission — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2019 (7y old): +15

### Physical Flux Regulation × Materials science — phase transitions — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2020 (6y old): +15

### Physical Thermal Variation × Materials science — crystal lattice defects — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2023 (3y old): +15

### Physical Circuit Evolution × Physical Magnetic Field Control — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2017 (9y old): +15

### Physical Circuit Evolution × Physical Electrical Noise — 🗺️ Verified, Unrefuted (+45)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2020 (6y old): +15

### Compiler optimization × Neural network training — 🗺️ Verified, Unrefuted (+40)

- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched (no date recovered) — real, but not a currently live thread: +10

### Finance (Human & Social Systems) — 🗺️ Verified, Unrefuted (+40)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2015 — real, but not a currently live thread: +10

### Informational Cache Miss Handling × Human Individual Indecision — 🗺️ Verified, Unrefuted (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2015 — real, but not a currently live thread: +10

### Immunology × Military Strategy — 🗺️ Verified, Unrefuted (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2014 — real, but not a currently live thread: +10

### Physical Feedback Loop Control — 🗺️ Verified, Unrefuted (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2004 — real, but not a currently live thread: +10

### Game Theory Nash Bargaining × Human Social Network Dynamics — 🗺️ Verified, Unrefuted (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2015 — real, but not a currently live thread: +10

### Informational Database State — 🗺️ Verified, Unrefuted (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2004 — real, but not a currently live thread: +10

### Behavioral Psychology Operant Conditioning × Physical Magnetic Field Control — 🗺️ Verified, Unrefuted (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 1988 — real, but not a currently live thread: +10

### Anthropology × Physical Evolutionary Selection — 🗺️ Verified, Unrefuted (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2010 — real, but not a currently live thread: +10

### Human Social Influence — 🗺️ Verified, Unrefuted (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 1964 — real, but not a currently live thread: +10

### Physical Immune System — 🗺️ Verified, Unrefuted (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2012 — real, but not a currently live thread: +10

### Informational OS Thread Scheduling — 🗺️ Verified, Unrefuted (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2002 — real, but not a currently live thread: +10

### Climatology — Ocean Current Circulation (Thermohaline) — 🗺️ Verified, Unrefuted (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2008 — real, but not a currently live thread: +10

### Informational Event-Driven Systems — 🗺️ Verified, Unrefuted (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2015 — real, but not a currently live thread: +10

### Supply Chain Logistics — Bullwhip Effect — 🗺️ Verified, Unrefuted (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2012 — real, but not a currently live thread: +10

### Physical Photon Emission — 🗺️ Verified, Unrefuted (+40)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2015 — real, but not a currently live thread: +10

### Creative Performance Monitoring — 🗺️ Verified, Unrefuted (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2013 — real, but not a currently live thread: +10

### Creative Instrument Track Development × Physical Circuit Evolution — 🗺️ Verified, Unrefuted (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2008 — real, but not a currently live thread: +10

### Law — Contract Formation and Offer/Acceptance — 🗺️ Verified, Unrefuted (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2014 — real, but not a currently live thread: +10

### Social Systems × Physical Feedback Loop Control — 🗺️ Verified, Unrefuted (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2015 — real, but not a currently live thread: +10

### History — path dependence in institutional change — 🗺️ Verified, Unrefuted (+40)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2015 — real, but not a currently live thread: +10

### Marketing — diffusion of innovation adoption curve — 🗺️ Verified, Unrefuted (+40)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 2015 — real, but not a currently live thread: +10

### Robotics — inverse kinematics — 🗺️ Verified, Unrefuted (+40)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Actively researched, most recent evidence 1992 — real, but not a currently live thread: +10

### Law — common law precedent and stare decisis — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Distributed Consensus Algorithms (Raft, PBFT) × Distributed Cache Coherence Protocols (MESI, Directory-based) — 🗺️ Verified, Unrefuted (+30)

- Phase 2 ADJACENT_ACTIVE: +30

### Dirac's large numbers hypothesis × Belnap four-valued logic / explainable AI — 🗺️ Verified, Unrefuted (+30)

- Phase 2 ADJACENT_ACTIVE: +30

### Astronomy — gravitational lensing — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Informational Hash Collisions × Human Social Network Dynamics — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Game Theory — Nash Bargaining × Music — Sample-Based Hip-Hop Production — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Architecture × Cross Domain Pattern Recognition — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Control theory — PID feedback loops — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Cryptography × Cognitive Development — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Chemistry × Creative Album Production Orchestration — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Creative Musical Composition × Human Emotional Fluctuation — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Comedy × Cognitive AI Hyperparameter Orchestration — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Creative Musical Motif Deviation × Human Committee Formation — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Decision Support Systems × Informational Queue Overflow — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Geology × Music Sound — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Informational Backup Systems × Informational Bit Flips — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Informational Load Balancing × Physical Immune System — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Linguistics — Creole Genesis × Cognitive Model Adaptation — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Neuroscience × Law — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Architecture (Creative & Performance Systems) — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Physical Electrical Noise — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Materials Science — Phase Transitions × Cognitive Streaming Data Processing — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Chemistry × Music Sound — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Education (Information & Intelligence Systems) × Human Facilitator Cueing — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Agriculture × Creative Improvisation Adjustment — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Agriculture × Telecommunications — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Cross Domain Pattern Recognition × Human Team Collaboration — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Modular Construction × Agricultural Ecosystems — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Auction Theory × Cognitive Attention Map Evolution — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Quantum Physics × Physical Magnetic Field Control — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Human Urban Planning × Physical Magnetic Fluctuation — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Immunology × Creative Album Production Orchestration — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Creative Film Production Orchestration — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Urban Planning × Astronomy — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Decision Support Systems × Creative Brainstorming Facilitation — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Cryptography × Physical Photon Emission — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Fluid Dynamics × Knowledge Systems — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Artificial Intelligence × Informational Database State — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Cognitive AI Hyperparameter Orchestration × Creative Improvisation Adjustment — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Culinary Arts × Informational Error Probability — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Law × Creative Idea Uncertainty — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Military Strategy × Informational Load Balancing — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Human Meeting Participation × Informational Ledger State Evolution — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Cognitive Concept Drift — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Linguistics × Cognitive Concept Drift — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Materials Science × Cognitive AI Pipeline Orchestration — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Music Sound × Physical Circuit Evolution — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Sports Athletics × Cognitive Swarm Intelligence — 🗺️ Verified, Unrefuted (+30)

- Phase 2 ADJACENT_ACTIVE: +30

### Healthcare Systems × Physical Power Grid Orchestration — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Physical Mechanical Vibration × Physical Power Grid Orchestration — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Cognitive Concept Drift × Physical Power Grid Orchestration — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Urban Planning × Architecture (Creative & Performance Systems) — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Cryptography — public-key infrastructure — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Music Theory × Informational Database Sharding — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Human Social Network Dynamics × Informational OS Thread Scheduling — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Neuroscience × Comedy — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Architecture × Cognitive Streaming Data Processing — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Creative Album Production Orchestration × Physical Flux Regulation — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Ecology × Creative Inspiration Variability — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Neuroscience — Synaptic Pruning × Physical Power Grid Orchestration — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Informational Mobile System Coordination × Physical Ecosystem Succession — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Astronomy × Military Strategy — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Cross Domain Pattern Recognition × Human Role Ambiguity — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Thermodynamics × Physical Elastic Deformation — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Control Theory × Physical Chemical Reaction Networks — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Finance (Human & Social Systems) × Physical Magnetic Field Control — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Informational Error Probability × Physical Chemical Reaction Networks — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Informational Scientific Experiment Orchestration × Physical Voltage Spikes — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Telecommunications × Creative Narrative Arc Development — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Telecommunications × Human Cognitive Bias — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Astrophysics × Human Trust Variance — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Cognitive AI Hyperparameter Orchestration × Human Learning Uncertainty — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Chemistry — catalysis and reaction pathways — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Cell Biology × Informational Scientific Experiment Orchestration — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Architecture — modular/prefab construction × Physical Photon Emission — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Creative Improvisation Adjustment × Informational Measurement Data Evolution — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Materials Science × Military Strategy — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Creative Narrative Arc Development × Informational OS Thread Scheduling — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Behavioral Psychology × Human Financial Market Systems — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Informational Ledger State Evolution × Informational Sensor Networks — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Legal Systems × Sports Athletics — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Architecture × Anthropology — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Anthropology × Gaming Narrative — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Architecture — modular/prefab construction × Human Defense Coordination — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Astronomy — gravitational lensing × Informational Scientific Experiment Orchestration — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Physical Elastic Deformation — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Law × Informational Ledger State Evolution — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Behavioral psychology — operant conditioning — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Legal Systems × Physical Magnetic Field Control — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Neuroscience × Sports Athletics — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Cognitive AI Preprocessing Pipelines × Physical Ecosystem Succession — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Language Linguistics × Cognitive AI Attention — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Informational Backup Systems × Physical Magnetic Fluctuation — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Cognitive AI Attention × Human Committee Formation — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Neuroscience — cortical map reorganization × Behavioral psychology — habit formation loops — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Political Science × Physical Elastic Deformation — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Sports Athletics × Cognitive Reinforcement Learning — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Urban Planning × Architecture — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Music Sound × Informational Hash Collisions — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Creative Musical Composition × Human Social Influence — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Evolutionary Biology × Cryptography — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Human Cognitive Bias × Informational Backup Systems — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Cryptography — zero-knowledge proofs — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Music Theory × Anthropology — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Creative Artistic Arrangement × Human Financial Trading Algorithms — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Epigenetics × Human Urban Planning — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Basketball Pick-and-Roll Offense × Cognitive Attention Map Evolution — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Organizational Theory × Architecture — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Informational Sensor Networks × Physical Power Grid Orchestration — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Cognitive AI Attention × Creative Brainstorming Facilitation — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Creative Improvisation Coordination × Informational Signal Jitter — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Culinary Arts × Human Financial Market Systems — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Creative Narrative Arc Development × Informational Protocol Coordination — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Human Role Ambiguity × Physical Telescope Telemetry — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Culinary Arts × Human Committee Formation — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Behavioral Psychology × Music Sound — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Cognitive AI Preprocessing Pipelines × Creative Performance Monitoring — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Music Theory × Informational Load Balancing — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Human Meeting Participation × Informational Event-Driven Systems — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Comedy — crowd work and audience read — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Sports — basketball pick-and-roll offense — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Healthcare × Legal Systems — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Cognitive AI Attention × Human Facilitator Cueing — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Creative Artistic Critique × Physical Thermal Variation — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Creative Improvisation Coordination × Informational Software Version Control — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Organizational Theory — Bureaucratic Hierarchy × Cognitive AI Hyperparameter Orchestration — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Agriculture (Physical & Natural Systems) — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Architecture × Physical Immune System — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Cognitive Attention Map Evolution — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Physical Ecosystem Succession × Physical Feedback Loop Control — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Creative Improvisation Coordination × Human Learning Uncertainty — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Epidemiology — Herd Immunity Thresholds × Informational Sensor Networks — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Baseball Pitch Sequencing × Informational Protocol Coordination — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Law × Creative Idea Uncertainty — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Cell biology — protein folding chaperones × Cognitive AI Pipeline Orchestration — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Gaming Narrative (Creative & Performance Systems) — Atomic: Player action succeeds/fails, Character status unknown, Multiple dialogue choices; Domain: Game world evolves, Game rules context, Log player actions; Control: Player input from controllers, Concurrent NPCs & physics, Atomic world consistency; Orchestration: Game engine coordination, Narrative vs gameplay environments × Informational Sensor Networks — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Informational Database State × Physical Circuit Evolution — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Telecommunications — error-correcting codes × Informational Ledger State Evolution — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Architecture (Creative & Performance Systems) — Atomic: Building permits approved/denied, Material availability uncertain, Multiple design options; Domain: Building construction progresses, Building codes, Log construction events; Control: Building inspections & permits, Concurrent construction, Atomic structural updates; Orchestration: City planning coordination, Design vs construction environments × Human Learning Uncertainty — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Informational Error Probability × Physical Thermal Variation — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Informational Error Probability × Physical Immune System — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Chemistry — catalysis and reaction pathways × Cognitive Development (Information & Intelligence Systems) — Atomic: Learning outcome uncertain, Skill acquisition succeeds/fails, Multiple learning paths; Domain: Cognitive skills evolve, Learning context, Log development milestones; Control: External learning resources, Parallel skill development, Atomic knowledge integration; Orchestration: Learning system coordination, Practice vs application environments — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Cross Domain Pattern Recognition (Cognitive & Pattern Recognition Systems) — Atomic: Pattern recognition uncertain, Mapping valid/invalid, Multiple domain analogies; Domain: Cross-domain understanding evolves, Universal monadic patterns, Log successful transfers; Control: Multiple data sources, Parallel analysis, Atomic synthesis; Orchestration: Cross-domain coordination & system integration × Creative Narrative Arc Development — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Finance (Human & Social Systems) — Atomic: Transaction succeeds/fails, Account lookup missing, Multiple positions; Domain: Portfolio evolves, Market context, Audit logging; Control: External trades & APIs, Streaming market data, Atomic account updates; Orchestration: Regulatory coordination, Simulation vs live trading × Informational Database Sharding — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Sports — basketball pick-and-roll offense × Human Emotional Fluctuation — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Urban planning — zoning and land use × Physical Power Grid Orchestration — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Epidemiology — disease outbreak spread × Creative Brainstorming Facilitation — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Control theory — Kalman filtering × Creative Improvisation Adjustment — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Supply chain logistics — bullwhip effect × Swarm robotics — flocking / boids behavior — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Botany — phototropism and plant signaling — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Pharmacology — drug receptor binding kinetics — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Philosophy — epistemology — justified true belief — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Computer science — distributed consensus protocols — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Developmental psychology — attachment theory — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Education — spaced repetition and forgetting curves — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Visual art — color theory and composition — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Cognitive psychology — working memory and chunking × Finance (Human & Social Systems) — Atomic: Transaction succeeds/fails, Account lookup missing, Multiple positions; Domain: Portfolio evolves, Market context, Audit logging; Control: External trades & APIs, Streaming market data, Atomic account updates; Orchestration: Regulatory coordination, Simulation vs live trading — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Urban planning — zoning and land use × Physical Mechanical Vibration — 🗺️ Verified, Unrefuted (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30

### Jazz Improvisation × Counterpoint and Voice Leading — 🗺️ Verified, Unrefuted (+20)

- Phase 1 self-report (3/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Actively researched, most recent evidence 2019 (7y old): +15

### Informational — distributed consensus — 🗺️ Verified, Unrefuted (+20)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Actively researched, most recent evidence 2022 (4y old): +15

### Informational — load balancing — 🗺️ Verified, Unrefuted (+20)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Actively researched, most recent evidence 2023 (3y old): +15

### Cognitive Attention Map Evolution × Informational Sensor Networks — 🗺️ Verified, Unrefuted (+20)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Actively researched, most recent evidence 2023 (3y old): +15

### Climate Science × Creative Artistic Arrangement — 🗺️ Verified, Unrefuted (+20)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Actively researched, most recent evidence 2023 (3y old): +15

### Human Emotional Fluctuation — 🗺️ Verified, Unrefuted (+20)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Actively researched, most recent evidence 2016 (10y old): +15

### Fluid dynamics — turbulence and laminar flow — 🗺️ Verified, Unrefuted (+20)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Actively researched, most recent evidence 2020 (6y old): +15

### Healthcare (Human & Social Systems) × Physical Circuit Evolution — 🗺️ Verified, Unrefuted (+20)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Actively researched, most recent evidence 2023 (3y old): +15

### Ecology — Mycorrhizal Fungal Networks — 🗺️ Verified, Unrefuted (+20)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Actively researched, most recent evidence 2016 (10y old): +15

### Genetic algorithms × Simulated annealing — 🗺️ Verified, Unrefuted (+15)

- Phase 2 COLLISION (genuine): +5
- Actively researched (no date recovered) — real, but not a currently live thread: +10

### Raft consensus × PBFT consensus — 🗺️ Verified, Unrefuted (+15)

- Phase 2 COLLISION (genuine): +5
- Actively researched (no date recovered) — real, but not a currently live thread: +10

### Urban planning — traffic flow optimization — 🗺️ Verified, Unrefuted (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Actively researched, most recent evidence 2010 — real, but not a currently live thread: +10

### Finance — options pricing and volatility smile — 🗺️ Verified, Unrefuted (+15)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Actively researched, most recent evidence 2014 — real, but not a currently live thread: +10

### Graph traversal algorithms (Dijkstra's, A*) × Minimax game tree search — 🗺️ Verified, Unrefuted (+5)

- Phase 2 COLLISION (genuine): +5

### Informational Measurement Data Evolution — 🗺️ Verified, Unrefuted (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5

### Human Financial Market Systems × Physical Mechanical Spring Systems — 🗺️ Verified, Unrefuted (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5

### Language Linguistics × Cognitive Reinforcement Learning — 🗺️ Verified, Unrefuted (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5

### Cognitive Reinforcement Learning × Informational OS Thread Scheduling — 🗺️ Verified, Unrefuted (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5

### Fluid Dynamics × Creative Narrative Arc Development — 🗺️ Verified, Unrefuted (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5

### Astrophysics × Creative Narrative Arc Development — 🗺️ Verified, Unrefuted (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5

### Decision Support Systems × Legal Systems — 🗺️ Verified, Unrefuted (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5

### Informational Hash Collisions — 🗺️ Verified, Unrefuted (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5

### Meteorology — supercell storm rotation — 🗺️ Verified, Unrefuted (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5

### Aerospace engineering — aerodynamic stall — 🌗 Contested (+50)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, but a real near-miss (1-of-3 survive): -5
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Acoustics — resonance and standing waves — 🌗 Contested (+35)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, but a real near-miss (1-of-3 survive): -5
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2011 — real, but not a currently live thread: +10

### Gaming Narrative × Human Financial Trading Algorithms — 🌗 Contested (-5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, but a real near-miss (1-of-3 survive): -5
-   independently confirmed (3 separate agents, full agreement)

### Watson & Crick — Molecular Biology × Franklin — X-Ray Crystallography — 🌗 Contested (-5)

- Phase 2 COLLISION: +0 (ground truth — no discovery credit, see below)
- Adversarial refutation REFUTED, but a real near-miss (1-of-3 survive): -5
-   independently confirmed (3 separate agents, full agreement)

### Hopfield — Statistical Physics × Neural Networks — 🌗 Contested (-5)

- Phase 2 COLLISION: +0 (ground truth — no discovery credit, see below)
- Adversarial refutation REFUTED, but a real near-miss (1-of-3 survive): -5
-   independently confirmed (3 separate agents, full agreement)

### Coase — Transaction Costs × Property Rights — 🌗 Contested (-5)

- Phase 2 ADJACENT_ACTIVE: +0 (ground truth — no discovery credit, see below)
- Adversarial refutation REFUTED, but a real near-miss (1-of-3 survive): -5
-   independently confirmed (3 separate agents, full agreement)

### Becker — Rational Choice × Household Behavior — 🌗 Contested (-5)

- Phase 2 COLLISION: +0 (ground truth — no discovery credit, see below)
- Adversarial refutation REFUTED, but a real near-miss (1-of-3 survive): -5
-   independently confirmed (3 separate agents, full agreement)

### Feynman — quantum mechanics × Computation — simulation — 🌗 Contested (-5)

- Phase 2 COLLISION: +0 (ground truth — no discovery credit, see below)
- Adversarial refutation REFUTED, but a real near-miss (1-of-3 survive): -5
-   independently confirmed (3 separate agents, full agreement)

### Control theory — Kalman filtering × Physical Magnetic Fluctuation — 💀 Refuted / Rejected (+57)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation survived (2-of-3): +12
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Political science — coalition government formation — 💀 Refuted / Rejected (+47)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation survived (2-of-3): +12
- Actively researched, most recent evidence 2020 (6y old): +15

### Cognitive Attention Map Evolution × Informational Event-Driven Systems — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Epidemiology × Creative Inspiration Variability — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Linguistics × Fluid Dynamics — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Cognitive AI Preprocessing Pipelines — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Organizational Theory — Self-Organizing Teams × Finance (Human & Social Systems) — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Efficient Market Hypothesis — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Human Learning Uncertainty — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Artificial Intelligence (Information & Intelligence Systems) — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Creative Improvisation Adjustment — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Music theory — jazz improvisation over changes — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Healthcare (Human & Social Systems) — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Immunology — Innate Immune Response — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Immunology — Adaptive Immune Memory — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Legal Systems — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Economics — Auction Theory — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Gaming Narrative (Creative & Performance Systems) — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Creative Idea Uncertainty — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Informational Ledger State Evolution — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Sports — baseball pitch sequencing — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Quantum Physics — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Creative Improvisation Coordination — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Language Linguistics (Information & Intelligence Systems) — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Creative Brainstorming Facilitation — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Human Facilitator Cueing — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Social Systems — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Cognitive Reinforcement Learning — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Game Theory — Nash Bargaining — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Creative Performance Monitoring × Human Cognitive Bias — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Informational Packet Buffer Management — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Creative Artistic Arrangement — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Human Social Network Dynamics — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Agriculture — crop rotation and soil health — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Physical Acoustic Resonance × Physical Photon Emission — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, but a real near-miss (1-of-3 survive): -5
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Physical Bridge Cable Tension × Physical Elastic Deformation — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, but a real near-miss (1-of-3 survive): -5
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Physics — condensed matter — Bose-Einstein condensate coherence (Gross-Pitaevskii dynamics, quantum pressure) × Cosmology — early-universe scalar field dynamics (corpuscular inflation, axion/ultralight BEC dark matter, Fukuyama-Morikawa stagflation) — 💀 Refuted / Rejected (+40)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, but a real near-miss (1-of-3 survive): -5
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Ecology × Materials Science — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2017 (9y old): +15

### Game Theory — Repeated Prisoner's Dilemma × Informational Measurement Data Evolution — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2022 (4y old): +15

### Human Individual Indecision × Physical Voltage Spikes — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2022 (4y old): +15

### Behavioral psychology — habit formation loops — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2020 (6y old): +15

### Neuroscience — cortical map reorganization — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2018 (8y old): +15

### Thermodynamics × Informational Signal Jitter — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, but a real near-miss (1-of-3 survive): -5
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2021 (5y old): +15

### Fluid Dynamics × Physical Telescope Telemetry — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, but a real near-miss (1-of-3 survive): -5
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2021 (5y old): +15

### Adaptive Immune Memory × Human Defense Coordination — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2021 (5y old): +15

### Swarm Robotics — Ant Colony Optimization — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Human Financial Trading Algorithms — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2023 (3y old): +15

### Physical Ecosystem Succession — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2019 (7y old): +15

### Human Committee Formation — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2019 (7y old): +15

### Informational Protocol Coordination — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2016 (10y old): +15

### Cell biology — mitochondrial energy production — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2023 (3y old): +15

### Architecture × Human Financial Trading Algorithms — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Cognitive Swarm Intelligence — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2019 (7y old): +15

### Human Role Ambiguity — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2020 (6y old): +15

### Linguistics — Creole Genesis — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2020 (6y old): +15

### Telecommunications — packet switching and routing — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2018 (8y old): +15

### Human Team Collaboration — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2017 (9y old): +15

### Organizational theory — self-organizing teams — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2017 (9y old): +15

### Creative Musical Motif Deviation × Informational Error Probability — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Climate Science (Physical & Natural Systems) — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2020 (6y old): +15

### Music — sample-based hip-hop production — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2019 (7y old): +15

### Cross Domain Pattern Recognition (Cognitive & Pattern Recognition Systems) — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2023 (3y old): +15

### Swarm Robotics — Flocking / Boids Behavior — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2019 (7y old): +15

### Chemistry — self-assembly of molecular structures — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2022 (4y old): +15

### Physical Mechanical Vibration — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2022 (4y old): +15

### Astrophysics (Physical & Natural Systems) — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2021 (5y old): +15

### Informational Error Probability — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2023 (3y old): +15

### Physical Protein Folding — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2020 (6y old): +15

### Cognitive Swarm Intelligence × Human Trust Variance — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Learning Systems (Cognitive & Pattern Recognition Systems) — Atomic: Learning outcomes uncertain, Skill acquisition succeeds/fails, Multiple learning states; Domain: Learning progresses, Educational context, Log development; Control: External learning resources, Parallel skill development, Atomic knowledge updates; Orchestration: Individual vs collective learning coordination — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2021 (5y old): +15

### Neuroscience — synaptic pruning — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2021 (5y old): +15

### Knowledge Systems (Cognitive & Pattern Recognition Systems) — Atomic: Data interpretation uncertain, Model output ambiguous, Multiple insights; Domain: Knowledge evolves, Historical context, Log insights; Control: Distributed analysis, Parallel computation, Atomic integration; Orchestration: Knowledge deployment coordination × Informational Scientific Experiment Orchestration — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Immunology — innate immune response — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2022 (4y old): +15

### Informational Mobile System Coordination — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2022 (4y old): +15

### Political science — coalition government formation — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2020 (6y old): +15

### Political science — coalition government formation — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2023 (3y old): +15

### Toxicology — dose-response curves — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2018 (8y old): +15

### Physical Elastic Deformation × Materials science — crystal lattice defects — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, but a real near-miss (1-of-3 survive): -5
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2021 (5y old): +15

### Physical Magnetic Field Control × Physical Voltage Spikes — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, but a real near-miss (1-of-3 survive): -5
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2020 (6y old): +15

### Informational Protocol Coordination × Cryptography — public-key infrastructure — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, but a real near-miss (1-of-3 survive): -5
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2020 (6y old): +15

### Physical Immune System × Materials science — phase transitions — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Physical Mechanical Spring Systems × Physical Circuit Evolution — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, but a real near-miss (1-of-3 survive): -5
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2022 (4y old): +15

### Physical Mechanical Spring Systems × Physical Mechanical Vibration — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (3/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, but a real near-miss (1-of-3 survive): -5
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2022 (4y old): +15

### Physical Acoustic Resonance × Physical Mechanical Vibration — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, but a real near-miss (1-of-3 survive): -5
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2021 (5y old): +15

### Physical Electrical Noise × Physical Gear System Mechanics — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Physical Mechanical Vibration × Physical Gear System Mechanics — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, but a real near-miss (1-of-3 survive): -5
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2016 (10y old): +15

### Behavioral psychology — habit formation loops × Creative Musical Motif Deviation — 💀 Refuted / Rejected (+30)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Knowledge Systems (Cognitive & Pattern Recognition Systems) — 💀 Refuted / Rejected (+25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2005 — real, but not a currently live thread: +10

### Astronomy × Telecommunications — 💀 Refuted / Rejected (+25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2015 — real, but not a currently live thread: +10

### Informational Cache Miss Handling — 💀 Refuted / Rejected (+25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2012 — real, but not a currently live thread: +10

### Human Individual Indecision — 💀 Refuted / Rejected (+25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2014 — real, but not a currently live thread: +10

### Cognitive Development (Information & Intelligence Systems) — 💀 Refuted / Rejected (+25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2004 — real, but not a currently live thread: +10

### Informational Sensor Networks — 💀 Refuted / Rejected (+25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2008 — real, but not a currently live thread: +10

### Immunology — Adaptive Immune Memory — 💀 Refuted / Rejected (+25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2012 — real, but not a currently live thread: +10

### Supply Chain Logistics — Just-in-Time Inventory — 💀 Refuted / Rejected (+25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2010 — real, but not a currently live thread: +10

### Physical Magnetic Fluctuation — 💀 Refuted / Rejected (+25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2007 — real, but not a currently live thread: +10

### Cognitive Streaming Data Processing — 💀 Refuted / Rejected (+25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2007 — real, but not a currently live thread: +10

### Economics — market microstructure and order books — 💀 Refuted / Rejected (+25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2014 — real, but not a currently live thread: +10

### Epidemiology — disease outbreak spread — 💀 Refuted / Rejected (+25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2013 — real, but not a currently live thread: +10

### Physical Chemical Reaction Networks — 💀 Refuted / Rejected (+25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2014 — real, but not a currently live thread: +10

### Cognitive Neuron Activation — 💀 Refuted / Rejected (+20)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2017 (9y old): +15

### Education (Information & Intelligence Systems) × Human Social Influence — 💀 Refuted / Rejected (+20)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2023 (3y old): +15

### Materials Science × Architecture — 💀 Refuted / Rejected (+20)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2020 (6y old): +15

### Organizational Theory × Physical Magnetic Field Control — 💀 Refuted / Rejected (+20)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2020 (6y old): +15

### Finance × Informational Routing Policy Enforcement — 💀 Refuted / Rejected (+20)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2017 (9y old): +15

### Game Theory — Repeated Prisoner's Dilemma — 💀 Refuted / Rejected (+20)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2022 (4y old): +15

### Human Team Collaboration × Physical Flux Regulation — 💀 Refuted / Rejected (+20)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2018 (8y old): +15

### Quantum Physics (Physical & Natural Systems) — Atomic: Particle position uncertain, Measurement binary, Superposition states; Domain: Quantum system evolves, Physical laws context, Log measurements; Control: Measurement apparatus, Parallel quantum processes, Atomic wavefunction collapse; Orchestration: Universal law coordination, Theoretical vs experimental environments × Informational Signal Jitter — 💀 Refuted / Rejected (+20)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2020 (6y old): +15

### Fleming — bacteriology × Contamination — 💀 Refuted / Rejected (+20)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2023 (3y old): +15

### Nash — equilibrium × Malthus — scarcity — 💀 Refuted / Rejected (+20)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2023 (3y old): +15

### Physical Mechanical Vibration × Physical Circuit Evolution — 💀 Refuted / Rejected (+20)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2023 (3y old): +15

### Physical Acoustic Resonance × Physical Mechanical Spring Systems — 💀 Refuted / Rejected (+20)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2023 (3y old): +15

### Astronomy — gravitational lensing × Physics — optics — diffraction and interference patterns — 💀 Refuted / Rejected (+20)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Materials science — phase transitions × Informational Distributed Consensus — 💀 Refuted / Rejected (+20)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2021 (5y old): +15

### Fluid dynamics — turbulence and laminar flow × Physical Magnetic Fluctuation — 💀 Refuted / Rejected (+20)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2021 (5y old): +15

### Physical Mechanical Spring Systems × Physical Gear System Mechanics — 💀 Refuted / Rejected (+20)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2021 (5y old): +15

### Physical Acoustic Resonance × Physical Gear System Mechanics — 💀 Refuted / Rejected (+20)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2022 (4y old): +15

### Physical Electrical Noise × Physical Mechanical Vibration — 💀 Refuted / Rejected (+20)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2017 (9y old): +15

### Physical Mechanical Spring Systems — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 FACT_CHECK_FAIL: -10
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Urban planning — zoning and land use — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Supply Chain Logistics × Physical Thermal Variation — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Physical Bridge Cable Tension — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Artificial Intelligence × Informational Queue Overflow — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Fluid Dynamics × Human Emotional Fluctuation — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 FACT_CHECK_FAIL: -10
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Creative Performance Monitoring × Physical Voltage Spikes — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Climatology × Cognitive Model Adaptation — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Ecology × Informational Ledger State Evolution — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Creative Idea Uncertainty × Creative Musical Motif Deviation — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Physical Telescope Telemetry — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Biological Systems × Cognitive Concept Drift — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Music Theory × Sports — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cognitive AI Hyperparameter Orchestration — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Creative Musical Motif Deviation — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Decision Support (Cognitive & Pattern Recognition Systems) — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Finance (Human & Social Systems) — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Astrophysics × Military Strategy — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Geology × Cognitive Attention Map Evolution — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Informational Cache Miss Handling × Physical Telescope Telemetry — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Organizational Theory — Bureaucratic Hierarchy × Informational Bit Flips — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Creative Artistic Critique — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Ecology — predator-prey population dynamics — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Epigenetics × Physical Bridge Cable Tension — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Neuroscience — cortical map reorganization × Economics — market microstructure and order books — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Swarm Robotics × Law — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Geology — sedimentary layering and stratigraphy — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Astrophysics × Human Social Influence — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Human Role Ambiguity × Informational Error Probability — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Music Sound × Human Cognitive Bias — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Human Role Ambiguity × Informational Hash Collisions — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Human Defense Coordination — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Climatology × Creative Instrument Track Development — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Informational Software Version Control × Physical Flux Regulation — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Biological Systems — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cognitive AI Weight Initialization — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Linguistics — Creole Genesis × Creative Film Production Orchestration — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Creative Album Production Orchestration — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Music Theory × Informational Ledger State Evolution — 💀 Refuted / Rejected (+15)

- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Auction Theory × Astrophysics — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Informational Backup Systems — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Physical Magnetic Field Control — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Human Trust Variance — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2010 — real, but not a currently live thread: +10

### Informational Signal Jitter — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Music Sound (Creative & Performance Systems) — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cognitive AI Weight Initialization × Creative Artistic Critique — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Materials Science — Phase Transitions — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Organizational theory — bureaucratic hierarchy — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Informational Scientific Experiment Orchestration — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Mitochondrial Energy Production × Physical Electrical Noise — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cognitive Attention Map Evolution × Informational Protocol Coordination — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cell biology — protein folding chaperones — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Creative Narrative Arc Development — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Mitochondrial Energy Production × Human Financial Market Systems — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cognitive AI Attention — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Thermodynamics — entropy and irreversibility — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Informational Backup Systems × Physical Acoustic Resonance — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Black–Scholes — financial pricing × Physics — diffusion equations — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2007 — real, but not a currently live thread: +10

### Creative Instrument Track Development × Informational Error Probability — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2007 — real, but not a currently live thread: +10

### Cell biology — protein folding chaperones × Creative Musical Composition — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Creative Album Production Orchestration × Physical Voltage Spikes — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Social psychology — conformity and groupthink — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2008 — real, but not a currently live thread: +10

### Textile engineering — weave structure and tensile strength — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cryptography — zero-knowledge proofs × Mathematics — topology — knot invariants — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, but a real near-miss (1-of-3 survive): -5
-   independently confirmed (3 separate agents, full agreement)

### Informational Backup Systems × Informational Packet Buffer Management — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2013 — real, but not a currently live thread: +10

### Physical Photon Emission × Quantum Physics (Physical & Natural Systems) — Atomic: Particle position uncertain, Measurement binary, Superposition states; Domain: Quantum system evolves, Physical laws context, Log measurements; Control: Measurement apparatus, Parallel quantum processes, Atomic wavefunction collapse; Orchestration: Universal law coordination, Theoretical vs experimental environments — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2015 — real, but not a currently live thread: +10

### Cryptography — public-key infrastructure × Mathematics — combinatorics — extremal counting — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, but a real near-miss (1-of-3 survive): -5
-   independently confirmed (3 separate agents, full agreement)

### Physical Mechanical Spring Systems × Physical Electrical Noise — 💀 Refuted / Rejected (+15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, but a real near-miss (1-of-3 survive): -5
-   independently confirmed (3 separate agents, full agreement)

### Cognitive AI Hyperparameter Orchestration × Physical Immune System — 💀 Refuted / Rejected (+10)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Informational Bit Flips — 💀 Refuted / Rejected (+10)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Military Strategy × Creative Album Production Orchestration — 💀 Refuted / Rejected (+10)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Epidemiology — herd immunity thresholds × Human Trust Variance — 💀 Refuted / Rejected (+10)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Human Learning Uncertainty × Physical Quantum Measurement — 💀 Refuted / Rejected (+10)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Black–Scholes — finance × Wiener processes — 💀 Refuted / Rejected (+10)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Actively researched, most recent evidence 2023 (3y old): +15

### Informational Ledger State Evolution × Cryptography — zero-knowledge proofs — 💀 Refuted / Rejected (+10)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Actively researched, most recent evidence 2023 (3y old): +15

### Comedy × Sports — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Human Cognitive Bias — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 FACT_CHECK_FAIL: -10
- Actively researched, most recent evidence 2022 (4y old): +15

### Basketball Pick-and-Roll Offense × Physical Flux Regulation — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2021 (5y old): +15

### Cognitive Neuron Activation × Physical Ecosystem Succession — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Control theory — Kalman filtering — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2023 (3y old): +15

### Cognitive Model Adaptation × Physical Bridge Cable Tension — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Linguistics × Creative Idea Uncertainty — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Game Theory Nash Bargaining × Cell Biology Protein Folding Chaperones — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Behavioral Psychology × Law — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Culinary Arts × Physical Bridge Cable Tension — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Informational Routing Policy Enforcement — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Human Meeting Participation × Physical Quantum Measurement — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Creative Instrument Track Development × Physical Chemical Reaction Networks — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cryptography × Physical Voltage Spikes — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Supply Chain Logistics × Physical Evolutionary Selection — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Comedy × Physical Gear System Mechanics — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Social Systems × Physical Chemical Reaction Networks — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Mycorrhizal Fungal Networks × Quantum Physics — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Music Theory × Human Trust Variance — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Education × Language Linguistics — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cognitive Concept Drift × Human Meeting Participation — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Music Theory × Auction Theory — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Informational Hash Collisions × Physical Ecosystem Succession — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Fluid Dynamics × Behavioral Psychology — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Evolutionary Biology × Creative Inspiration Variability — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Human Facilitator Cueing × Informational Cache Miss Handling — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cognitive Neuron Activation × Informational Software Version Control — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Physical Acoustic Resonance — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2022 (4y old): +15

### Behavioral psychology — habit formation loops × Informational Sensor Networks — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Economics — auction theory × Informational Ledger State Evolution — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Immunology — innate immune response × Informational Sensor Networks — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cell biology — mitochondrial energy production × Human Social Network Dynamics — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Agriculture — crop rotation and soil health — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Marconi — radio × Telegraphy — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Astronomy — gravitational lensing × Human Defense Coordination — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Music theory — jazz improvisation over changes × Linguistics — creole genesis — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Informational Database State × Mathematics — combinatorics — extremal counting — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Informational Database State × Mathematics — topology — knot invariants — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Physical Electrical Noise × Physical Acoustic Resonance — 💀 Refuted / Rejected (+5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 ADJACENT_ACTIVE: +30
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Physical Flux Regulation — 💀 Refuted / Rejected (+0)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2022 (4y old): +15

### Informational Queue Overflow — 💀 Refuted / Rejected (+0)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2023 (3y old): +15

### Agriculture × Human Team Collaboration — 💀 Refuted / Rejected (+0)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2025 (1y old — a live, current research thread): +25

### Creative Improvisation Coordination × Human Individual Indecision — 💀 Refuted / Rejected (+0)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2020 (6y old): +15

### Learning Systems × Informational Load Balancing — 💀 Refuted / Rejected (+0)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2023 (3y old): +15

### Physical Circuit Evolution — 💀 Refuted / Rejected (+0)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2022 (4y old): +15

### Anthropology — gift economies and reciprocity — 💀 Refuted / Rejected (+0)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2022 (4y old): +15

### Materials Science — Phase Transitions × Human Social Movements — 💀 Refuted / Rejected (+0)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2024 (2y old — a live, current research thread): +25

### Sports Athletics (Creative & Performance Systems) — Atomic: Performance succeeds/fails, Opponent capabilities unknown, Multiple strategic approaches; Domain: Athletic performance evolves, Sports rules, Log training sessions; Control: Performance monitoring, Concurrent team coordination, Atomic score updates; Orchestration: Sports federation coordination, Training vs championship environments — 💀 Refuted / Rejected (+0)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2022 (4y old): +15

### Physics — optics — diffraction and interference patterns — 💀 Refuted / Rejected (+0)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2022 (4y old): +15

### Physical Mechanical Vibration × Materials science — crystal lattice defects — 💀 Refuted / Rejected (+0)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2026 (0y old — a live, current research thread): +25

### Graph traversal algorithms × State space search algorithms — 💀 Refuted / Rejected (-5)

- Phase 2 COLLISION (not a valid bisociation): -5

### Quantum entanglement / Bell inequalities × Quantum information science — 💀 Refuted / Rejected (-5)

- Phase 2 COLLISION (not a valid bisociation): -5

### Trigonometric function analysis × Fourier transform / spectral decomposition — 💀 Refuted / Rejected (-5)

- Phase 2 COLLISION (not a valid bisociation): -5

### Human Committee Formation × Physical Acoustic Resonance — 💀 Refuted / Rejected (-5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2013 — real, but not a currently live thread: +10

### Astronomy — stellar nucleosynthesis — 💀 Refuted / Rejected (-5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2012 — real, but not a currently live thread: +10

### Thermodynamics × Physical Power Grid Orchestration — 💀 Refuted / Rejected (-5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2013 — real, but not a currently live thread: +10

### Evolutionary biology — punctuated equilibrium — 💀 Refuted / Rejected (-5)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2009 — real, but not a currently live thread: +10

### Culinary arts — flavor pairing and Maillard reaction — 💀 Refuted / Rejected (-5)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2013 — real, but not a currently live thread: +10

### Cognitive AI Hyperparameter Orchestration × Physical Mechanical Spring Systems — 💀 Refuted / Rejected (-10)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Human Team Collaboration × Informational Load Balancing — 💀 Refuted / Rejected (-10)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cryptography × Cognitive AI Hyperparameter Orchestration — 💀 Refuted / Rejected (-10)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Military Strategy (Human & Social Systems) — 💀 Refuted / Rejected (-10)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cryptography — Zero-Knowledge Proofs × Biological Systems — 💀 Refuted / Rejected (-10)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 FACT_CHECK_FAIL: -10

### Physical Circuit Evolution × Thermodynamics — entropy and irreversibility — 💀 Refuted / Rejected (-10)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2022 (4y old): +15

### Physical Circuit Evolution × Physical Acoustic Resonance — 💀 Refuted / Rejected (-10)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)
- Actively researched, most recent evidence 2017 (9y old): +15

### Neuroscience — cortical map reorganization × Climatology — ocean current circulation (thermohaline) — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Human immune system × Distributed ledger technology — 💀 Refuted / Rejected (-15)

- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Neural networks × Coral reef ecosystems — 💀 Refuted / Rejected (-15)

- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Sample variance / statistical estimation × Protein structure prediction — 💀 Refuted / Rejected (-15)

- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Swarm Robotics × Culinary Arts — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Physical Bridge Cable Tension × Organizational Theory — Bureaucratic Hierarchy — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Stellar Nucleosynthesis × Creative Album Production Orchestration — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Language Linguistics × Physical Telescope Telemetry — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Creative Brainstorming Facilitation × Physical Electrical Noise — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Informational Scientific Experiment Orchestration × Physical Magnetic Fluctuation — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Load-Bearing Structural Design × Informational Load Balancing — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Linguistics — Creole Genesis × Economics — Market Microstructure and Order Books — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Creative Instrument Track Development × Informational Load Balancing — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Creative Musical Composition × Physical Mechanical Spring Systems — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Linguistics — Creole Genesis × Informational Backup Systems — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Linguistics — Creole Genesis × Learning Systems — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Neuroscience — Synaptic Pruning × Human Trust Variance — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Human Urban Planning × Physical Photon Emission — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Informational Routing Policy Enforcement × Physical Thermal Variation — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Healthcare × Physical Voltage Spikes — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Urban Planning × Informational Packet Buffer Management — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Geology × Human Committee Formation — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Behavioral psychology — habit formation loops × Informational Error Probability — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cognitive Streaming Data Processing × Creative Film Production Orchestration — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Ecology × Informational Load Balancing — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Evolutionary Biology — Punctuated Equilibrium × Physical Photon Emission — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Music — sample-based hip-hop production × Human Financial Market Systems — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cognitive Model Adaptation — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Linguistics × Cognitive AI Preprocessing Pipelines — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Ecology × Human Learning Uncertainty — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Climatology — ocean current circulation × Anthropology — gift economies and reciprocity — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Informational OS Thread Scheduling × Physical Ecosystem Succession — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Epigenetics — gene expression regulation without DNA change — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Immunology × Linguistics — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Organizational Theory × Physical Thermal Variation — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cell Biology × Creative Album Production Orchestration — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cognitive Neuron Activation × Informational Backup Systems — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cross Domain Pattern Recognition × Informational Backup Systems — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cryptography × Epigenetics — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Climatology × Military Strategy — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Coalition Government Formation × Climate Science — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Geology × Informational Cache Miss Handling — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cryptography — zero-knowledge proofs × Physical Thermal Variation — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Geology × Cross Domain Pattern Recognition — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Telecommunications — error-correcting codes — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Physical Bridge Cable Tension × Physical Elastic Deformation — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Law × Informational Load Balancing — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Baseball Pitch Sequencing × Human Social Influence — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Ocean Current Circulation × Cognitive Concept Drift — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Neuroscience — Synaptic Pruning × Telecommunications — Error-Correcting Codes — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Architecture — load-bearing structural design × Cognitive Neuron Activation — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Human Facilitator Cueing × Informational Database Sharding — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cross Domain Pattern Recognition × Informational Software Version Control — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cross Domain Pattern Recognition × Physical Voltage Spikes — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Human Role Ambiguity × Human Trust Variance — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Organizational Theory — Bureaucratic Hierarchy × Music — Sample-Based Hip-Hop Production — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Physical Voltage Spikes — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Biological Systems × Informational Cache Miss Handling — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Geology — Plate Tectonics — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cross Domain Pattern Recognition × Human Cognitive Bias — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Astrophysics × Informational Hash Collisions — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cognitive AI Attention × Informational Software Version Control — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Creative Artistic Critique × Physical Gear System Mechanics — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Supply Chain Logistics × Telecommunications — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Linguistics — Creole Genesis × Human Financial Market Systems — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Astronomy — stellar nucleosynthesis × Epidemiology — herd immunity thresholds — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Immunology × Human Meeting Participation — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Architecture (Creative & Performance Systems) × Human Individual Indecision — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Creative Idea Uncertainty × Physical Electrical Noise — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Knowledge Systems × Informational Distributed Consensus — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Fluid Dynamics × Sports Athletics — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Geology × Sports — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Behavioral Psychology — Operant Conditioning × Creative Improvisation Adjustment — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Mitochondrial Energy Production × Physical Chemical Reaction Networks — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Control Theory — Kalman Filtering × Informational Bit Flips — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Informational Protocol Coordination × Physical Elastic Deformation — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Linguistics — creole genesis × Law — contract formation and offer/acceptance — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Music × Human Learning Uncertainty — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Creative Block × Bridge Cable Tension — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Climatology — ocean current circulation × Human Defense Coordination — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Ecology — predator-prey population dynamics × Physical Magnetic Field Control — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Mycorrhizal Fungal Networks × Packet Switching and Routing — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Crystal Lattice Defects × Linguistic Evolution — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Informational Cache Miss Handling × Physical Gear System Mechanics — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Astronomy × Cognitive AI Preprocessing Pipelines — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cell Biology × Culinary Arts — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Fluid Dynamics × Informational Event-Driven Systems — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Baseball Pitch Sequencing × Quantum Physics — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Supply Chain Logistics × Physical Circuit Evolution — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Astronomy × Law — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Epigenetics × Cognitive Concept Drift — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Biological Systems × Cognitive AI Hyperparameter Orchestration — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Informational Load Balancing × Physical Evolutionary Selection — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Culinary Arts (Creative & Performance Systems) — Atomic: Recipe succeeds/fails, Ingredient freshness unknown, Multiple flavor combinations; Domain: Dish develops through cooking, Recipes & traditions, Log cooking steps; Control: External food suppliers, Concurrent cooking processes, Atomic seasoning adjustments; Orchestration: Restaurant coordination, Recipe vs service environments × Human Individual Indecision — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Evolutionary biology — punctuated equilibrium × Physical Magnetic Field Control — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Urban planning — traffic flow optimization × Agriculture — crop rotation and soil health — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cell biology — protein folding chaperones × Informational Software Version Control — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cognitive Development (Information & Intelligence Systems) — Atomic: Learning outcome uncertain, Skill acquisition succeeds/fails, Multiple learning paths; Domain: Cognitive skills evolve, Learning context, Log development milestones; Control: External learning resources, Parallel skill development, Atomic knowledge integration; Orchestration: Learning system coordination, Practice vs application environments × Informational Bit Flips — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Agriculture — crop rotation and soil health × Creative Narrative Arc Development — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Creative Musical Motif Deviation × Informational Bit Flips — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Geology — sedimentary layering and stratigraphy × Epidemiology — herd immunity thresholds — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Education (Information & Intelligence Systems) — Atomic: Assignment grade uncertain, Learning succeeds/fails, Multiple styles; Domain: Student knowledge evolves, Educational standards, Log progress; Control: External assessment systems, Concurrent learning paths, Atomic grade updates; Orchestration: Curriculum coordination, Practice vs real-world environments × Physical Magnetic Field Control — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Creative Inspiration Variability × Informational Packet Buffer Management — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Supply chain logistics — bullwhip effect × Geology — sedimentary layering and stratigraphy — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Anthropology — gift economies and reciprocity × Cognitive AI Attention — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Telecommunications — packet switching and routing × Music Sound (Creative & Performance Systems) — Atomic: Note pitch flat/sharp, Instrument availability uncertain, Multiple harmonic possibilities; Domain: Musical composition evolves, Music theory context, Log performances; Control: Live audience feedback, Concurrent musician coordination, Atomic tempo synchronization; Orchestration: Music industry coordination, Composition vs performance environments — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Agriculture — crop rotation and soil health — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Control theory — Kalman filtering × Physics — particle physics — Standard Model symmetry breaking — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Physical Gear System Mechanics × Physical Circuit Evolution — 💀 Refuted / Rejected (-15)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Epidemiology × Human Cognitive Bias — 💀 Refuted / Rejected (-20)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 COLLISION (genuine): +5
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Baseball Pitch Sequencing × Finance Transaction Dynamics — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Human Role Ambiguity × Informational Hash Collisions — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Protein Folding Chaperones × Linguistic Systems — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Human Facilitator Cueing × Informational Bit Flips — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Culinary Arts × Informational Mobile System Coordination — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Market Microstructure × Legal Systems — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Neuroscience — Cortical Map Reorganization × Informational Backup Systems — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cognitive Development × Physical Immune System — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Human Facilitator Cueing × Physical Chemical Reaction Networks — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Astronomy — Stellar Nucleosynthesis × Creative Improvisation Adjustment — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cognitive Model Adaptation × Physical Chemical Reaction Networks — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cognitive AI Hyperparameter Orchestration × Creative Narrative Arc Development — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cognitive Neuron Activation × Physical Gear System Mechanics — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Sports Athletics × Informational Software Version Control — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Human Social Network Dynamics × Physical Immune System — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cell Biology × Human Trust Variance — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Supply Chain Logistics × Music Production — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Legal Systems × Physical Protein Folding — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cell Biology — Protein Folding Chaperones × Informational OS Thread Scheduling — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Urban Planning Traffic Flow Optimization × Informational Cache Miss Handling — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Materials Science — Phase Transitions × Physical Mechanical Spring Systems — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Mitochondrial Energy Production × Cross Domain Pattern Recognition — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Military Strategy × Creative Artistic Arrangement — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Music × Physical Immune System — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Astronomy — Stellar Nucleosynthesis × Creative Improvisation Coordination — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (5/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Music — sample-based hip-hop production × Informational Database Sharding — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Biological Systems × Creative Block — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Climatology × Cognitive Model Adaptation — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cognitive Concept Drift × Creative Idea Uncertainty — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Human Individual Indecision × Physical Telescope Telemetry — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Linguistics × Behavioral Psychology — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Music — sample-based hip-hop production × Informational Load Balancing — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Finance (Human & Social Systems) — Atomic: Transaction succeeds/fails, Account lookup missing, Multiple positions; Domain: Portfolio evolves, Market context, Audit logging; Control: External trades & APIs, Streaming market data, Atomic account updates; Orchestration: Regulatory coordination, Simulation vs live trading × Physical Magnetic Fluctuation — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 FACT_CHECK_FAIL: -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Human Social Influence × Physical Mechanical Vibration — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Astronomy — gravitational lensing × Architecture (Creative & Performance Systems) — Atomic: Building permits approved/denied, Material availability uncertain, Multiple design options; Domain: Building construction progresses, Building codes, Log construction events; Control: Building inspections & permits, Concurrent construction, Atomic structural updates; Orchestration: City planning coordination, Design vs construction environments — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Cell biology — protein folding chaperones × Sports Athletics (Creative & Performance Systems) — Atomic: Performance succeeds/fails, Opponent capabilities unknown, Multiple strategic approaches; Domain: Athletic performance evolves, Sports rules, Log training sessions; Control: Performance monitoring, Concurrent team coordination, Atomic score updates; Orchestration: Sports federation coordination, Training vs championship environments — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Informational Database State × Physical Gear System Mechanics — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Astronomy — gravitational lensing × Informational Signal Jitter — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Informational Error Probability × Mathematics — topology — knot invariants — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Physical Elastic Deformation × Physical Voltage Spikes — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Control theory — Kalman filtering × Astronomy — gravitational lensing — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

### Control theory — Kalman filtering × Genomics — GWAS and polygenic risk — 💀 Refuted / Rejected (-25)

- Phase 1 self-report (4/5): not scored — near-zero predictive signal, see Failure 5
- Phase 2 NO_SIGNAL: +0 (pending)
- Mechanical honesty check failed twice (disguised compromise, uncorrected): -10
- Adversarial refutation REFUTED, unanimous (0-of-3 survive): -15
-   independently confirmed (3 separate agents, full agreement)

