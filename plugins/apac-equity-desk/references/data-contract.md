# Normalized data contract

Calculation helpers accept UTF-8 JSON arrays (or CSV where noted) and emit JSON to stdout unless `--output` is supplied. Draft renderers accept JSON objects and emit Markdown. Unknown fields are preserved where practical in calculation helpers; narrative renderers output only their documented fields. Numbers may be JSON numbers or numeric strings; blanks become null.

## Quote row

Required: `symbol`, `market`, `last`, `prev_close`.

Recommended: `name`, `desk_ticker`, `currency`, `timestamp`, `session`, `open`, `high`, `low`, `volume`, `turnover`, `avg_volume_20d`, `avg_turnover_20d`, `vwap`, `sector`, `benchmark`, `benchmark_pct`, `peer_median_pct`, `index_weight`, `fresh_announcement`, `policy_headline`, `commodity_shock`, `unusual_flow`, `ah_divergence_pct`, `close`, `dma20`, `high_52w`, `low_52w`.

Timestamps must include an offset or the pack must provide a timezone. Do not merge quotes from materially different as-of times without a warning.

## News row

Required: `id`, `title`, `source`, `published_at`, `url`. Recommended: `body`, `symbols`, `evidence_level` (1–4), `source_type`, `language`.

## A/H pair

Required: `a_symbol`, `a_price_cny`, `h_symbol`, `h_price_hkd`, `hkd_per_cny`, `timestamp`. Premium is `(A price × HKD per CNY / H price − 1) × 100`.

## Market-colour pack

The default developed note uses `format: desk-theme`; see House narrative packs below. The following single-stock labelled layout remains supported when `format` is absent or `single-stock`.

Top-level fields: `as_of`, `subject`, `move`, `relative`, `catalysts`, `flow_technical`, `chatter`, `read_through`, `watch`, `sources`, `data_gaps`. Each catalyst should include `summary`, `evidence_level`, `status`, `confidence`, `source_ids`, and whether it is `new_today`.

## Market-wrap pack

The default country close uses `format: desk-narrative`; see House narrative packs below. The following regional digest remains supported when `format` is absent or `regional-summary`.

Top-level fields: `date`, `as_of`, `regional_lead`, `markets`, `cross_asset`, `tomorrow`, `sources`, `data_gaps`. Each market contains `name`, `indices`, `breadth`, `sectors`, `movers`, `flows`, `catalysts` and `as_of`.

## Fact-check bundle

```json
{
  "as_of": "2026-09-18T16:10:00+08:00",
  "claims": [{"id":"c1","text":"...","source_ids":["s1"],"causal":true}],
  "sources": [{"id":"s1","evidence_level":1,"url":"https://...","published_at":"..."}]
}
```

Optional claim fields: `value`, `unit`, `tolerance`, `new_today`, `confirmed`. The checker flags missing citations, causal claims supported only by Level 4, malformed source URLs/timestamps and contradictory numeric claims sharing the same `fact_key`. Source age, source independence, semantic support and whether an event caused a move still require analyst verification.

## House narrative packs

Build the underlying quote/news/claim pack first, then author the narrative entries below from that evidence. Renderers format supplied prose; they do not generate research or determine causality. They reject structural errors but cannot verify a paragraph's truth or a ticker's identity.

All three formats require `as_of` as an ISO timestamp with a timezone offset. Optional `sources` is an array of objects with unique `id`, an HTTP(S) `url` and optional `label`. A text entry is either an analyst-reviewed string or `{"summary":"Supported paragraph.","source_ids":["s1"]}`. Linked entries retain their citations inline; missing IDs and malformed URLs fail validation. Bare strings are allowed for reviewed prose and are not automatically verified.

Use lists of text entries for paragraph fields and bullet fields. Omit optional fields or use empty arrays; the renderer does not insert empty-section filler. Optional `data_gaps` and `review_notes` are bullet arrays displayed separately after the note. Set `synthetic: true` for fabricated layout examples; their output is visibly labelled.

### Country close: desk-narrative

Required: `format`, `as_of`, ISO `date`, and nonempty `markets`. Each market requires `name`, `session: closed`, and a nonempty `lead` paragraph array. Optional paragraph arrays, in display order: `local_policy`, `fx_rates`, `macro_data`, `sector_laggards`, `sector_leaders`. Optional `desk_aside` is one supplied text entry, followed by a `corporate_headlines` bullet array.

One market gives a developed country wrap. Multiple market blocks retain the same narrative depth. The renderer rejects an open market instead of calling it a close. Breadth, flow and contribution data remain in the underlying evidence pack even when not reproduced as prose.

Example: `tests/fixtures/japan_close_house.json` in the repository.

### Intraday theme: desk-theme

Required: `format`, `as_of`, `headline`, nonempty `tickers` (verified display strings), `move_context` paragraph array and `watch` bullet array.

Optional: `fundamental_hook` paragraph array, `mixed_evidence` bullet array and `implications` bullet array. Preserve conflicting evidence and separate different stock exposures. Each ticker appears on its own line; a narrative template does not validate exchange mappings.

Example: `tests/fixtures/optical_theme_house.json`. Its placeholder tickers are deliberately fictional.

### Morning snippet: desk-morning

Required: `format`, `as_of`, `country`, `session`, `overnight_context` and `sector_drivers` paragraph arrays. Optional `country_tag` is a supplied/configured string such as `{JA}`.

For `session: open`, require `opening_tape` and omit `pre_open_setup`. For `session: pre_open`, require `pre_open_setup` and omit `opening_tape`. These are paragraph arrays. The renderer rejects contradictory session fields. It cannot validate whether prose describes an observed move correctly, so check the market clock and source timestamps before constructing the pack.

Example: `tests/fixtures/japan_morning_house.json`.
