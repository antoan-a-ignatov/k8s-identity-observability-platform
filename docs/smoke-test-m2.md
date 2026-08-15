# M2 Smoke Test: kind + Elasticsearch RAM Baseline

## Setup
- kind cluster (single node, default config)
- Elasticsearch 8.15.0, single-node mode, security disabled, heap capped at 512Mi (Xms/Xmx)
- Resource requests: 768Mi / limits: 1Gi

## Result
- Pod reached Running/Ready after ~7 min (first-time image pull, not a resource issue)
- Verified serving via GET / on port 9200 (cluster/version info returned)
- Memory after settling (WSL cap 5.8Gi):
  - used: 1.9Gi
  - buff/cache: 4.0Gi (reclaimable)
  - available: 3.9Gi

## Conclusion
kind + single-node Elasticsearch at 512Mi heap fits comfortably within the 6GB WSL cap,
with ~3.9Gi available remaining. No adjustment needed to the staging approach for M2.
Confirms plan assumption that components can be staged up/down without hitting memory
limits during normal single-component testing.
