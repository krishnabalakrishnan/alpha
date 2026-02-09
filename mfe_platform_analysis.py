#!/usr/bin/env python3
"""
MFE Platform Analysis: iOS vs Android
Analyzes pre-computed sums from Grafana panels.
"""

# ── Raw data from Grafana ──────────────────────────────────────────────
ios = {
    "entry_screen_impression": {"sum": 309_889, "max": 2_011, "min": 0, "logmin": 125},
    "trip_completion":         {"sum": 275_238, "max": 1_805, "min": 0, "logmin": 113},
}

android = {
    "entry_screen_impression": {"sum": 1_279_286, "max": 7_307, "min": 0, "logmin": 564},
    "trip_completion":         {"sum": 1_216_473, "max": 6_975, "min": 0, "logmin": 548},
}

combined_impressions_given = 1_611_658  # previously calculated all-OS value

# Data structure constants
total_points = 732
zero_points = 407
active_points = 325
sampling_interval_hrs = 2.95       # approx hours between samples
window_size_min = 30               # each point is a 30-min moving window sum

# ── Derived values ─────────────────────────────────────────────────────
ios_imp   = ios["entry_screen_impression"]["sum"]
ios_tc    = ios["trip_completion"]["sum"]
andr_imp  = android["entry_screen_impression"]["sum"]
andr_tc   = android["trip_completion"]["sum"]

total_imp = ios_imp + andr_imp
total_tc  = ios_tc + andr_tc

# Coverage ratio: 30 min window / 2.95 hr sampling  =>  0.5 / 2.95
coverage_ratio = (window_size_min / 60) / sampling_interval_hrs

# ── Output ─────────────────────────────────────────────────────────────
def sep(title):
    return f"\n{'='*70}\n  {title}\n{'='*70}"

print(sep("MFE PLATFORM ANALYSIS  -  iOS vs Android"))

# ── 1. Platform Volume Split ───────────────────────────────────────────
print(sep("1. Platform Volume Split"))

andr_imp_share = andr_imp / total_imp * 100
ios_imp_share  = ios_imp  / total_imp * 100
andr_tc_share  = andr_tc  / total_tc  * 100
ios_tc_share   = ios_tc   / total_tc  * 100

print(f"""
  Entry Screen Impressions (moving-window sums)
  -----------------------------------------------
  {'Android:':<12} {andr_imp:>12,}   ({andr_imp_share:5.1f}%)
  {'iOS:':<12} {ios_imp:>12,}   ({ios_imp_share:5.1f}%)
  {'Total:':<12} {total_imp:>12,}

  Trip Completions (moving-window sums)
  -----------------------------------------------
  {'Android:':<12} {andr_tc:>12,}   ({andr_tc_share:5.1f}%)
  {'iOS:':<12} {ios_tc:>12,}   ({ios_tc_share:5.1f}%)
  {'Total:':<12} {total_tc:>12,}

  Verification: Android + iOS impressions = combined total?
    {andr_imp:,} + {ios_imp:,} = {total_imp:,}
    Previously given combined total    = {combined_impressions_given:,}
    Match: {'YES' if total_imp == combined_impressions_given else 'NO  (delta = {:,})'.format(total_imp - combined_impressions_given)}

  Note: The combined figure ({combined_impressions_given:,}) was computed from a
  separate all-OS query. A difference of {abs(total_imp - combined_impressions_given):,} suggests
  {'perfect alignment.' if total_imp == combined_impressions_given else 'a small amount of traffic from other platforms (e.g., mWeb) or rounding.'}""")

# ── 2. Conversion Rates ───────────────────────────────────────────────
print(sep("2. Conversion Rates  (Impression -> Trip Completion)"))

ios_cvr  = ios_tc  / ios_imp  * 100
andr_cvr = andr_tc / andr_imp * 100
comb_cvr = total_tc / total_imp * 100

better = "Android" if andr_cvr > ios_cvr else "iOS"
gap    = abs(andr_cvr - ios_cvr)

print(f"""
  Platform        Impressions     Completions     CVR
  ─────────────────────────────────────────────────────
  iOS             {ios_imp:>12,}    {ios_tc:>12,}    {ios_cvr:6.2f}%
  Android         {andr_imp:>12,}    {andr_tc:>12,}    {andr_cvr:6.2f}%
  Combined        {total_imp:>12,}    {total_tc:>12,}    {comb_cvr:6.2f}%
  ─────────────────────────────────────────────────────

  Winner: {better} by {gap:.2f} percentage points
  - iOS CVR:      {ios_tc:,} / {ios_imp:,} = {ios_cvr:.4f}%
  - Android CVR:  {andr_tc:,} / {andr_imp:,} = {andr_cvr:.4f}%""")

# ── 3. Estimated Total Trip Completions ───────────────────────────────
print(sep("3. Estimated Total Trip Completions"))

est_ios_tc   = ios_tc   / coverage_ratio
est_andr_tc  = andr_tc  / coverage_ratio
est_total_tc = total_tc / coverage_ratio

# Also estimate impressions for completeness
est_ios_imp  = ios_imp  / coverage_ratio
est_andr_imp = andr_imp / coverage_ratio
est_total_imp = total_imp / coverage_ratio

# Active period duration
active_hours = active_points * sampling_interval_hrs
active_days  = active_hours / 24

print(f"""
  Coverage ratio: {window_size_min}-min window / {sampling_interval_hrs}-hr sampling
                = {coverage_ratio:.4f}  (~{coverage_ratio*100:.1f}% of events captured)

  Active period:  {active_points} data points x {sampling_interval_hrs} hrs
                = {active_hours:,.1f} hours  (~{active_days:.1f} days)

  Estimated ACTUAL trip completions over the ~{active_days:.0f}-day window:
  ──────────────────────────────────────────────────────────────
  Platform     Window Sums     Est. Actual      Daily Average
  ──────────────────────────────────────────────────────────────
  iOS          {ios_tc:>12,}    {est_ios_tc:>12,.0f}      {est_ios_tc/active_days:>10,.0f}
  Android      {andr_tc:>12,}    {est_andr_tc:>12,.0f}      {est_andr_tc/active_days:>10,.0f}
  Combined     {total_tc:>12,}    {est_total_tc:>12,.0f}      {est_total_tc/active_days:>10,.0f}
  ──────────────────────────────────────────────────────────────

  Estimated ACTUAL impressions over the same period:
  ──────────────────────────────────────────────────────────────
  iOS          {ios_imp:>12,}    {est_ios_imp:>12,.0f}      {est_ios_imp/active_days:>10,.0f}
  Android      {andr_imp:>12,}    {est_andr_imp:>12,.0f}      {est_andr_imp/active_days:>10,.0f}
  Combined     {total_imp:>12,}    {est_total_imp:>12,.0f}      {est_total_imp/active_days:>10,.0f}
  ──────────────────────────────────────────────────────────────""")

# ── 4. Platform Parity Analysis ───────────────────────────────────────
print(sep("4. Platform Parity Analysis"))

ratio_imp = andr_imp / ios_imp
ratio_tc  = andr_tc  / ios_tc
ratio_max_imp = android["entry_screen_impression"]["max"] / ios["entry_screen_impression"]["max"]
ratio_max_tc  = android["trip_completion"]["max"] / ios["trip_completion"]["max"]
ratio_logmin_imp = android["entry_screen_impression"]["logmin"] / ios["entry_screen_impression"]["logmin"]
ratio_logmin_tc  = android["trip_completion"]["logmin"] / ios["trip_completion"]["logmin"]

print(f"""
  Android : iOS Ratios
  ──────────────────────────────────────────────────────
  Metric                     Android    iOS      Ratio
  ──────────────────────────────────────────────────────
  Impression sum             {andr_imp:>9,}  {ios_imp:>9,}   {ratio_imp:.2f}x
  Completion sum             {andr_tc:>9,}  {ios_tc:>9,}   {ratio_tc:.2f}x
  Impression peak (max)      {android['entry_screen_impression']['max']:>9,}  {ios['entry_screen_impression']['max']:>9,}   {ratio_max_imp:.2f}x
  Completion peak (max)      {android['trip_completion']['max']:>9,}  {ios['trip_completion']['max']:>9,}   {ratio_max_tc:.2f}x
  Impression trough (logmin) {android['entry_screen_impression']['logmin']:>9,}  {ios['entry_screen_impression']['logmin']:>9,}   {ratio_logmin_imp:.2f}x
  Completion trough (logmin) {android['trip_completion']['logmin']:>9,}  {ios['trip_completion']['logmin']:>9,}   {ratio_logmin_tc:.2f}x
  ──────────────────────────────────────────────────────

  Key Observations:
  1. Android dominates volume at ~{ratio_imp:.1f}x iOS across all metrics.
  2. The impression ratio ({ratio_imp:.2f}x) vs completion ratio ({ratio_tc:.2f}x)
     are {'very close, indicating proportional behavior.' if abs(ratio_imp - ratio_tc) < 0.1 else 'noticeably different.'}
     {'Android has a slightly HIGHER completion ratio, meaning it converts' if ratio_tc > ratio_imp else 'Android has a slightly LOWER completion ratio, meaning iOS converts'}
     {'proportionally more of its impressions.' if ratio_tc > ratio_imp else 'proportionally more of its impressions.'}
  3. Peak ratios  - impressions: {ratio_max_imp:.2f}x, completions: {ratio_max_tc:.2f}x
     Trough ratios - impressions: {ratio_logmin_imp:.2f}x, completions: {ratio_logmin_tc:.2f}x
     The ratios are {'remarkably stable across peaks and troughs.' if abs(ratio_max_imp - ratio_logmin_imp) < 0.5 else 'more divergent at peaks vs troughs, suggesting different usage patterns.'}
  4. Both platforms show identical data structure (407 zero points, 325 active),
     confirming they share the same observation window.""")

# ── Summary ────────────────────────────────────────────────────────────
print(sep("SUMMARY"))
print(f"""
  - Android handles {andr_imp_share:.0f}% of impressions and {andr_tc_share:.0f}% of completions.
  - iOS handles {ios_imp_share:.0f}% of impressions and {ios_tc_share:.0f}% of completions.
  - Conversion rates are nearly identical: iOS {ios_cvr:.2f}% vs Android {andr_cvr:.2f}%.
  - Estimated ~{est_total_tc:,.0f} actual trip completions over the ~{active_days:.0f}-day period
    (~{est_total_tc/active_days:,.0f}/day combined).
  - Android + iOS sums ({total_imp:,}) {'exactly match' if total_imp == combined_impressions_given else 'slightly differ from'} the
    previously computed combined total ({combined_impressions_given:,}).
    {'This confirms the data is a clean iOS + Android split with no other platforms.' if total_imp == combined_impressions_given else f'Delta of {total_imp - combined_impressions_given:,} may indicate rounding or other platform traffic.'}
""")
