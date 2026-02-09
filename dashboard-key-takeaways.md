# Manual Fare Entry M1 Dashboard - Key Takeaways

## Dashboard Overview

This is a Grafana monitoring dashboard for the **Manual Fare Entry (MFE)** feature on Uber's driver app. It tracks the end-to-end lifecycle of manual fare entry on mobile (Android & iOS), from screen impressions through fare estimation to cash collection and trip completion.

- **Dashboard ID**: `c0f475ce-c122-4800-be7a-150bc5187a57`
- **Data source**: M3QL (metrics service: `superflurry`)
- **Default time range**: Last 90 days
- **Default moving window**: 30 minutes

---

## Panel Inventory (10 panels)

| # | Panel Title | Type | Scope |
|---|-------------|------|-------|
| 1 | Important links | Text/Markdown | Reference links |
| 2 | [Mobile] Manual Fare Entry Screen Impression | Time series | All OS |
| 3 | [Mobile] Manual Fare Extras Impression | Time series | All OS |
| 4 | [Android][Temp] Manual Fare Entry Impression & Trip Completion | Time series | Android only |
| 5 | [iOS][Temp] Manual Fare Entry Impression & Trip Completion | Time series | iOS only |
| 6 | [Mobile] Manual Fare Estimate Success | Time series | All OS |
| 7 | [Mobile] Manual Fare Estimate Server & Network Error | Time series | All OS |
| 8 | [Mobile] Guardrails | Time series | All OS |
| 9 | [Mobile] Manual Fare Cash Collection Success & Failure | Time series | All OS |
| 10 | Driver Trip Cancellation | Time series | By city |

---

## Key Takeaways

### 1. The dashboard tracks a clear user funnel

The panels map to a sequential driver flow:

```
Screen Impression -> Extras Screen -> Fare Estimate -> Cash Collection -> Trip Completion
```

Each stage is independently monitored, making it possible to identify where drop-offs or failures occur in the manual fare entry process.

### 2. Platform-specific breakdowns exist for impression-to-completion

Panels 4 and 5 are marked `[Temp]` and provide **Android vs. iOS** side-by-side comparison of entry screen impressions overlaid with trip completions. This enables platform-specific conversion analysis (impressions that actually result in completed trips). The `[Temp]` tag suggests these may be investigative panels added for a specific analysis period.

### 3. Error monitoring covers three failure modes

The error panel (panel 7) tracks three distinct failure types for fare estimation:
- **Server errors** (`fare_estimate_server_error`) - backend failures
- **Network errors** (`fare_estimate_network_error`) - connectivity issues
- **Exceptions** (`fare_estimate_exception`) - client-side crashes

This separation allows the team to distinguish between infrastructure problems, network reliability, and app bugs.

### 4. Guardrails are monitored at four boundaries

Panel 8 tracks fare guardrail violations across four thresholds:
- **Soft min** - fare below recommended minimum (warning)
- **Soft max** - fare above recommended maximum (warning)
- **Hard min** - fare below absolute minimum (blocked)
- **Hard max** - fare above absolute maximum (blocked)

This is critical for fraud prevention and fare integrity. Spikes in guardrail violations could indicate driver abuse patterns or misconfigured fare limits for a region.

### 5. Cash collection success/failure is explicitly tracked

Panel 9 monitors whether cash collection succeeds or fails after fare entry. This is a key business metric - a completed fare entry that fails at cash collection means the driver did the work but the payment flow broke.

### 6. Driver cancellation is tracked separately with different filtering

The cancellation panel uses `city_name` as its filter dimension (rather than `country_iso2` used by all other panels). This comes from a different metric (`trip_cancelreasons_selectreason`) and tracks when drivers select a cancellation reason. It provides context on how often drivers abandon trips versus completing them through manual fare entry.

### 7. Template variables enable flexible filtering

Four template variables allow dynamic filtering:

| Variable | Description | Used By |
|----------|-------------|---------|
| `os` | Mobile operating system (multi-select) | All MFE panels |
| `country_iso2` | Country code (single-select) | All MFE panels |
| `city_name` | City name (multi-select) | Driver cancellation only |
| `window` | Moving window aggregation (default 30m) | All panels |

Note: The `country_iso2` filter does **not** apply to the Driver Cancellation panel, which uses `city_name` instead. This is called out in the variable description.

### 8. All metrics use moving window sum aggregation

Every query follows the same pattern:
```
fetch ... | sum | transformNull | moving $window sum | alias ...
```

This means all values shown are **rolling sums** over the configured window (default 30 minutes), not raw event counts. When interpreting the dashboard, the absolute numbers represent "events in the last N minutes" at any given point, not instantaneous rates.

---

## Suggested Monitoring Focus Areas

- **Conversion rate**: Compare `entry_screen_impression` against `trip_completion` to measure funnel completion
- **Error rate**: Compare `fare_estimate_success` against the sum of `server_error` + `network_error` + `exception` to get failure percentage
- **Guardrail health**: Watch for sudden spikes in `hard_min` or `hard_max` violations which may indicate configuration issues or fraud
- **Cash collection reliability**: Track the ratio of `cash_collection_failure` to `cash_collection_success` for payment flow health
- **Platform parity**: Compare Android vs. iOS impression-to-completion ratios for platform-specific issues
