# Normalized data contract

Helpers accept UTF-8 JSON arrays (or CSV where noted) and emit JSON to stdout unless `--output` is supplied. Unknown fields are preserved where practical. Numbers may be JSON numbers or numeric strings; blanks become null.

## Quote row

Required: `symbol`, `market`, `last`, `prev_close`.

Recommended: `name`, `desk_ticker`, `currency`, `timestamp`, `session`, `open`, `high`, `low`, `volume`, `turnover`, `avg_volume_20d`, `avg_turnover_20d`, `vwap`, `sector`, `benchmark`, `benchmark_pct`, `peer_median_pct`, `index_weight`, `fresh_announcement`, `policy_headline`, `commodity_shock`, `unusual_flow`, `ah_divergence_pct`, `close`, `dma20`, `high_52w`, `low_52w`.

Timestamps must include an offset or the pack must provide a timezone. Do not merge quotes from materially different as-of times without a warning.

## News row

Required: `id`, `title`, `source`, `published_at`, `url`. Recommended: `body`, `symbols`, `evidence_level` (1–4), `source_type`, `language`.

## A/H pair

Required: `a_symbol`, `a_price_cny`, `h_symbol`, `h_price_hkd`, `hkd_per_cny`, `timestamp`. Premium is `(A price × HKD per CNY / H price − 1) × 100`.

## Market-colour pack

Top-level fields: `as_of`, `subject`, `move`, `relative`, `catalysts`, `flow_technical`, `chatter`, `read_through`, `watch`, `sources`, `data_gaps`. Each catalyst should include `summary`, `evidence_level`, `status`, `confidence`, `source_ids`, and whether it is `new_today`.

## Market-wrap pack

Top-level fields: `date`, `as_of`, `regional_lead`, `markets`, `cross_asset`, `tomorrow`, `sources`, `data_gaps`. Each market contains `name`, `indices`, `breadth`, `sectors`, `movers`, `flows`, `catalysts` and `as_of`.

## Fact-check bundle

```json
{
  "as_of": "2026-09-18T16:10:00+08:00",
  "claims": [{"id":"c1","text":"...","source_ids":["s1"],"causal":true}],
  "sources": [{"id":"s1","evidence_level":1,"url":"https://...","published_at":"..."}]
}
```

Optional claim fields: `value`, `unit`, `tolerance`, `new_today`, `confirmed`. The checker flags missing citations, causal claims supported only by Level 4, stale/malformed sources and contradictory numeric claims sharing the same `fact_key`.

