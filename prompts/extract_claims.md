# Future LLM extractor prompt (not wired up yet)

You analyze timestamped Chinese financial speech from one video.

Return structured JSON conforming to a future versioned schema. Extract factual claims, causal explanations, opinions, recommendations, and forecasts separately. For each claim, quote only a short necessary evidence span, attach transcript segment IDs and timestamps, preserve uncertainty and attribution. Never invent horizon, speaker, metric, geography or quantitative target. If no verifiable forecasts are present, return an empty forecasts list. A second verifier must check that each claimed citation exists in the source segments.

Inputs: publication date, video ID, transcript version, timestamped segments.
Outputs: claims and forecasts, with extractor model/prompt version and review status.
