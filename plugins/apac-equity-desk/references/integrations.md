# Integration notes

## Longbridge — primary

The plugin points to the official hosted streamable-HTTP MCP at `https://mcp.longbridge.com`. Authentication is interactive OAuth; do not place access tokens in this repository. Official resources:

- MCP server: https://github.com/longbridge/longbridge-mcp
- Developer overview: https://open.longbridge.com/docs
- Quote symbol conventions and coverage: https://open.longbridge.com/docs/quote/overview

The official MCP exposes both read and write tools. This desk intentionally permits read-only research behavior at the instruction layer. Do not call order, account-mutation, alert, watchlist, DCA, grid or sharelist write methods.

Coverage and quote entitlements vary. The official hosted MCP currently emphasizes US/HK, while the developer SDK/CLI documents China symbols. Singapore real-time quotes are not currently supplied through Longbridge Developers. Treat unsupported markets and entitlement failures as data gaps, then use only a configured/approved fallback.

## Optional China and news adapters

AKShare is suitable for China-local breadth and cross-checks; Tushare for structured A-share fundamentals, classifications and flows; Jin10 for time-sensitive China/macro headlines. They are disabled in `config/providers.example.toml` because each installation has different authentication, licensing and data definitions.

Adapters should output the normalized contract in `data-contract.md`. Preserve provider name, source URL or endpoint identity, timestamp, timezone and delayed/live status. A fallback may fill a gap, but it must not silently overwrite a conflicting primary observation.

## Adding an adapter

Keep credentials in environment variables or the provider's authenticated connector. Add a small read-only collector outside the core calculation helpers, normalize its output, and add fixture-based tests. Never add order-routing capabilities to this plugin.
