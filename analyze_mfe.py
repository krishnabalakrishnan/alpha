import datetime
from collections import defaultdict

# =============================================================================
# DATA
# =============================================================================
values = [
6124,7141,4967,7079,3848,2599,3145,5243,5163,6084,4839,3107,777,1541,5649,5305,5512,6800,5384,4438,1576,1422,5211,5754,5164,6236,4696,3878,1913,1502,4171,4784,4314,4894,4252,1688,702,1439,5037,5294,4123,5045,5084,3634,1312,920,5021,5591,3930,5473,5602,4167,1482,1172,5712,6370,4507,4866,6243,4719,1431,1210,6107,6424,4680,4883,6519,4861,1767,1145,5674,6855,4952,5274,7459,5713,4643,2302,1891,5550,6141,5569,7292,5583,5070,2508,1979,5189,5659,5020,6089,4612,2704,1231,1578,6446,4731,4790,5825,4310,4334,1293,1871,6600,7291,4910,6565,6660,5321,1385,1449,6465,7116,4827,4996,6558,5121,2273,1189,5984,6608,4473,4801,6150,4653,1804,1270,6293,6670,4934,5881,7341,5597,4652,2405,1856,5096,6018,5441,7117,5445,4583,2502,1836,4773,5166,4744,5634,4281,1909,1096,1732,6060,4454,5386,5827,4605,2262,1162,1658,5991,4809,5505,6182,6101,4579,1544,1543,6147,6837,4699,6627,7315,5627,2178,1771,7118,7776,5110,6797,7484,5988,2137,1698,7158,7796,5222,6252,8156,6291,6218,3153,2547,6322,6284,6915,8456,6472,6081,3078,2448,5540,6052,5307,6111,4928,2996,1397,2031,7359,4831,6088,6612,5028,4850,1687,1651,7228,4743,6108,5416,7025,5078,1931,1700,7539,4735,6129,5576,6939,5030,1959,1700,6501,7393,5020,5734,7459,5788,2939,2067,7055,5774,7776,6962,9153,7340,6457,3440,3213,6101,6181,7144,8901,7167,7318,3810,2918,5612,5264,6424,6805,6143,4960,2049,2181,7499,5075,6801,7407,5999,5762,2011,1984,6521,5107,7105,7485,7614,5792,2190,2129,7350,5088,7297,6374,7592,6225,2484,2102,6992,5375,7534,6646,8034,6652,2810,2298,7331,6139,8311,7634,9231,7639,6672,3486,3605,6767,6757,7241,9263,7775,7405,4077,3516,6777,6206,6441,7926,6776,5271,2397,2356,7958,6908
]

# First non-zero timestamp
first_ts_ms = 1770189480000
interval_ms = 10620000  # ms between consecutive data points

# Generate timestamps for each value
timestamps_ms = [first_ts_ms + i * interval_ms for i in range(len(values))]

# Convert to datetime (UTC)
def ms_to_dt(ms):
    return datetime.datetime.utcfromtimestamp(ms / 1000.0)

timestamps_dt = [ms_to_dt(ts) for ts in timestamps_ms]

# =============================================================================
# Verify interval
# =============================================================================
interval_sec = interval_ms / 1000
interval_min = interval_sec / 60
interval_hr = interval_min / 60

print("=" * 78)
print("MANUAL FARE ENTRY (MFE) SCREEN IMPRESSIONS - ANALYSIS REPORT")
print("=" * 78)

print(f"\n{'='*78}")
print("0. INTERVAL VERIFICATION")
print(f"{'='*78}")
print(f"  Interval between samples:  {interval_ms:,} ms")
print(f"                           = {interval_sec:,.0f} seconds")
print(f"                           = {interval_min:.1f} minutes")
print(f"                           = {interval_hr:.4f} hours (~2.95 hours)")
print(f"  Samples per day:           {24 * 3600 / interval_sec:.2f}")
print(f"  Window type:               30-minute moving sum")

# =============================================================================
# 1. Total sum
# =============================================================================
total = sum(values)
print(f"\n{'='*78}")
print("1. TOTAL SUM OF ALL VALUES")
print(f"{'='*78}")
print(f"  Sum of all {len(values)} non-zero data points: {total:,}")
print(f"  Expected:                                1,611,658")
print(f"  Match: {'YES' if total == 1611658 else 'NO (got ' + str(total) + ')'}")

# =============================================================================
# 2. Date range
# =============================================================================
first_dt = timestamps_dt[0]
last_dt = timestamps_dt[-1]

print(f"\n{'='*78}")
print("2. DATE RANGE OF ACTIVE DATA")
print(f"{'='*78}")
print(f"  First non-zero data point: {first_dt.strftime('%Y-%m-%d %H:%M:%S UTC')}")
print(f"                             (ts: {timestamps_ms[0]})")
print(f"  Last non-zero data point:  {last_dt.strftime('%Y-%m-%d %H:%M:%S UTC')}")
print(f"                             (ts: {timestamps_ms[-1]})")
print(f"  Total span:                {(last_dt - first_dt).days} days, "
      f"{(last_dt - first_dt).seconds // 3600} hours")
print(f"  Total non-zero samples:    {len(values)}")

# Full panel range context
panel_start = ms_to_dt(1762851060000)  # approximate panel start from given timestamps
print(f"\n  Panel start (approx):      {panel_start.strftime('%Y-%m-%d %H:%M:%S UTC')}")
print(f"  Zero-value period:         {panel_start.strftime('%Y-%m-%d')} to "
      f"{first_dt.strftime('%Y-%m-%d')} ({(first_dt - panel_start).days} days of silence)")

# =============================================================================
# 3. Number of active days
# =============================================================================
days_set = set()
for dt in timestamps_dt:
    days_set.add(dt.date())

active_days = sorted(days_set)
print(f"\n{'='*78}")
print("3. NUMBER OF ACTIVE DAYS")
print(f"{'='*78}")
print(f"  Unique calendar days with data: {len(active_days)}")
print(f"  First active day: {active_days[0]}")
print(f"  Last active day:  {active_days[-1]}")
print(f"  Calendar span:    {(active_days[-1] - active_days[0]).days + 1} days")

# =============================================================================
# 4. Daily averages (group by day)
# =============================================================================
daily_data = defaultdict(list)
for dt, val in zip(timestamps_dt, values):
    daily_data[dt.date()].append(val)

daily_sums = {d: sum(v) for d, v in daily_data.items()}
daily_counts = {d: len(v) for d, v in daily_data.items()}
daily_means = {d: sum(v) / len(v) for d, v in daily_data.items()}

print(f"\n{'='*78}")
print("4. DAILY BREAKDOWN")
print(f"{'='*78}")
print(f"  {'Date':<14} {'Day':>5} {'Samples':>8} {'DaySum':>10} {'Mean/Sample':>12} {'Peak':>8} {'Trough':>8}")
print(f"  {'-'*14} {'-'*5} {'-'*8} {'-'*10} {'-'*12} {'-'*8} {'-'*8}")

sorted_days = sorted(daily_data.keys())
for d in sorted_days:
    v = daily_data[d]
    day_name = d.strftime('%a')
    print(f"  {str(d):<14} {day_name:>5} {len(v):>8} {sum(v):>10,} {sum(v)/len(v):>12,.1f} "
          f"{max(v):>8,} {min(v):>8,}")

print(f"\n  Overall daily sum statistics:")
sums_list = [daily_sums[d] for d in sorted_days]
print(f"    Mean daily sum:   {sum(sums_list)/len(sums_list):>10,.1f}")
print(f"    Median daily sum: {sorted(sums_list)[len(sums_list)//2]:>10,}")
print(f"    Min daily sum:    {min(sums_list):>10,} ({min(daily_sums, key=daily_sums.get)})")
print(f"    Max daily sum:    {max(sums_list):>10,} ({max(daily_sums, key=daily_sums.get)})")

# =============================================================================
# 5. Weekly pattern analysis
# =============================================================================
print(f"\n{'='*78}")
print("5. WEEKLY PATTERN ANALYSIS (Weekday vs Weekend)")
print(f"{'='*78}")

dow_data = defaultdict(list)  # day-of-week -> list of sample values
dow_daily_sums = defaultdict(list)  # day-of-week -> list of daily sums

for d in sorted_days:
    dow = d.strftime('%a')
    dow_num = d.weekday()  # 0=Mon, 6=Sun
    dow_daily_sums[dow_num].append(daily_sums[d])

for dt, val in zip(timestamps_dt, values):
    dow_num = dt.weekday()
    dow_data[dow_num].append(val)

dow_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

print(f"\n  {'Day':<5} {'#Days':>6} {'Avg DaySum':>12} {'Avg Sample':>12} {'#Samples':>9}")
print(f"  {'-'*5} {'-'*6} {'-'*12} {'-'*12} {'-'*9}")

weekday_sums = []
weekend_sums = []

for dow_num in range(7):
    if dow_num in dow_daily_sums:
        ds = dow_daily_sums[dow_num]
        samples = dow_data[dow_num]
        avg_ds = sum(ds) / len(ds)
        avg_sample = sum(samples) / len(samples)
        print(f"  {dow_names[dow_num]:<5} {len(ds):>6} {avg_ds:>12,.1f} {avg_sample:>12,.1f} {len(samples):>9}")
        if dow_num < 5:
            weekday_sums.extend(ds)
        else:
            weekend_sums.extend(ds)

weekday_avg = sum(weekday_sums) / len(weekday_sums) if weekday_sums else 0
weekend_avg = sum(weekend_sums) / len(weekend_sums) if weekend_sums else 0

print(f"\n  Weekday (Mon-Fri) average daily sum: {weekday_avg:>10,.1f}")
print(f"  Weekend (Sat-Sun) average daily sum: {weekend_avg:>10,.1f}")
if weekend_avg > 0:
    ratio = weekday_avg / weekend_avg
    pct_diff = ((weekday_avg - weekend_avg) / weekend_avg) * 100
    print(f"  Weekday/Weekend ratio:               {ratio:.2f}x")
    print(f"  Weekday is {abs(pct_diff):.1f}% {'higher' if pct_diff > 0 else 'lower'} than weekend")

# Hourly pattern within each day
print(f"\n  Hourly distribution of sample values (hour-of-day UTC):")
hour_data = defaultdict(list)
for dt, val in zip(timestamps_dt, values):
    hour_data[dt.hour].append(val)

print(f"  {'Hour':>6} {'#Samples':>9} {'Mean':>10} {'Median':>10} {'Interpretation':>20}")
print(f"  {'-'*6} {'-'*9} {'-'*10} {'-'*10} {'-'*20}")
for h in sorted(hour_data.keys()):
    vals = hour_data[h]
    s = sorted(vals)
    median = s[len(s)//2]
    mean = sum(vals)/len(vals)
    # Simple interpretation
    if mean > 6000:
        interp = "HIGH activity"
    elif mean > 4000:
        interp = "MODERATE activity"
    elif mean > 2000:
        interp = "LOW activity"
    else:
        interp = "VERY LOW activity"
    print(f"  {h:>4}:00 {len(vals):>9} {mean:>10,.1f} {median:>10,} {interp:>20}")

# =============================================================================
# 6. Peak and trough analysis
# =============================================================================
print(f"\n{'='*78}")
print("6. PEAK AND TROUGH ANALYSIS")
print(f"{'='*78}")

# Top 10 peaks
indexed = list(enumerate(values))
indexed_sorted_desc = sorted(indexed, key=lambda x: x[1], reverse=True)
indexed_sorted_asc = sorted(indexed, key=lambda x: x[1])

print(f"\n  TOP 10 PEAKS (highest 30-min window sums):")
print(f"  {'Rank':>4} {'Value':>8} {'Timestamp (UTC)':>24} {'Day':>5}")
print(f"  {'-'*4} {'-'*8} {'-'*24} {'-'*5}")
for rank, (idx, val) in enumerate(indexed_sorted_desc[:10], 1):
    dt = timestamps_dt[idx]
    print(f"  {rank:>4} {val:>8,} {dt.strftime('%Y-%m-%d %H:%M:%S'):>24} {dt.strftime('%a'):>5}")

print(f"\n  TOP 10 TROUGHS (lowest 30-min window sums):")
print(f"  {'Rank':>4} {'Value':>8} {'Timestamp (UTC)':>24} {'Day':>5}")
print(f"  {'-'*4} {'-'*8} {'-'*24} {'-'*5}")
for rank, (idx, val) in enumerate(indexed_sorted_asc[:10], 1):
    dt = timestamps_dt[idx]
    print(f"  {rank:>4} {val:>8,} {dt.strftime('%Y-%m-%d %H:%M:%S'):>24} {dt.strftime('%a'):>5}")

# Daily peaks
print(f"\n  DAILY PEAK ANALYSIS:")
print(f"  {'Date':<14} {'Peak':>8} {'Peak Time (UTC)':>20} {'Trough':>8} {'Trough Time':>20} {'Range':>8}")
print(f"  {'-'*14} {'-'*8} {'-'*20} {'-'*8} {'-'*20} {'-'*8}")

daily_indexed = defaultdict(list)
for i, (dt, val) in enumerate(zip(timestamps_dt, values)):
    daily_indexed[dt.date()].append((dt, val))

for d in sorted_days:
    pts = daily_indexed[d]
    peak_dt, peak_val = max(pts, key=lambda x: x[1])
    trough_dt, trough_val = min(pts, key=lambda x: x[1])
    print(f"  {str(d):<14} {peak_val:>8,} {peak_dt.strftime('%H:%M'):>20} "
          f"{trough_val:>8,} {trough_dt.strftime('%H:%M'):>20} {peak_val - trough_val:>8,}")

# =============================================================================
# 7. Trend analysis
# =============================================================================
print(f"\n{'='*78}")
print("7. TREND ANALYSIS")
print(f"{'='*78}")

# Weekly aggregation for trend
from collections import OrderedDict
weekly_data = OrderedDict()
for d in sorted_days:
    # ISO week
    iso_year, iso_week, _ = d.isocalendar()
    week_key = f"{iso_year}-W{iso_week:02d}"
    if week_key not in weekly_data:
        weekly_data[week_key] = {'sum': 0, 'days': 0, 'samples': 0}
    weekly_data[week_key]['sum'] += daily_sums[d]
    weekly_data[week_key]['days'] += 1
    weekly_data[week_key]['samples'] += daily_counts[d]

print(f"\n  WEEKLY TOTALS AND TRENDS:")
print(f"  {'Week':<12} {'Days':>5} {'WeekSum':>12} {'Avg/Day':>10} {'WoW Change':>12}")
print(f"  {'-'*12} {'-'*5} {'-'*12} {'-'*10} {'-'*12}")

prev_sum = None
week_sums_for_trend = []
week_keys = list(weekly_data.keys())
for wk in week_keys:
    wd = weekly_data[wk]
    avg_per_day = wd['sum'] / wd['days'] if wd['days'] else 0
    if prev_sum is not None and prev_sum > 0:
        wow = ((wd['sum'] / wd['days']) - (prev_sum / prev_days)) / (prev_sum / prev_days) * 100
        wow_str = f"{wow:>+10.1f}%"
    else:
        wow_str = "       N/A"
    print(f"  {wk:<12} {wd['days']:>5} {wd['sum']:>12,} {avg_per_day:>10,.1f} {wow_str:>12}")
    prev_sum = wd['sum']
    prev_days = wd['days']
    week_sums_for_trend.append(avg_per_day)

# Simple linear regression for trend
n = len(week_sums_for_trend)
x_vals = list(range(n))
y_vals = week_sums_for_trend
x_mean = sum(x_vals) / n
y_mean = sum(y_vals) / n
ss_xy = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_vals, y_vals))
ss_xx = sum((x - x_mean) ** 2 for x in x_vals)
slope = ss_xy / ss_xx if ss_xx else 0
intercept = y_mean - slope * x_mean

# R-squared
y_pred = [slope * x + intercept for x in x_vals]
ss_res = sum((y - yp) ** 2 for y, yp in zip(y_vals, y_pred))
ss_tot = sum((y - y_mean) ** 2 for y in y_vals)
r_squared = 1 - (ss_res / ss_tot) if ss_tot else 0

print(f"\n  LINEAR TREND (weekly avg/day):")
print(f"    Slope:     {slope:>+,.1f} per week (avg daily sum change)")
print(f"    R-squared: {r_squared:.4f}")
if slope > 500:
    trend_desc = "STRONGLY GROWING"
elif slope > 100:
    trend_desc = "MODERATELY GROWING"
elif slope > -100:
    trend_desc = "ROUGHLY STABLE"
elif slope > -500:
    trend_desc = "MODERATELY DECLINING"
else:
    trend_desc = "STRONGLY DECLINING"
print(f"    Verdict:   {trend_desc}")

# First half vs second half comparison
half = len(values) // 2
first_half_avg = sum(values[:half]) / half
second_half_avg = sum(values[half:]) / (len(values) - half)
pct_change = ((second_half_avg - first_half_avg) / first_half_avg) * 100

print(f"\n  FIRST HALF vs SECOND HALF:")
print(f"    First half  (samples 1-{half}):      avg = {first_half_avg:,.1f}")
print(f"    Second half (samples {half+1}-{len(values)}): avg = {second_half_avg:,.1f}")
print(f"    Change: {pct_change:+.1f}%")

# Thirds analysis
third = len(values) // 3
t1_avg = sum(values[:third]) / third
t2_avg = sum(values[third:2*third]) / third
t3_avg = sum(values[2*third:]) / (len(values) - 2*third)
print(f"\n  THIRDS ANALYSIS:")
print(f"    First third:  avg = {t1_avg:,.1f}")
print(f"    Middle third: avg = {t2_avg:,.1f}  ({((t2_avg-t1_avg)/t1_avg)*100:+.1f}% vs 1st)")
print(f"    Last third:   avg = {t3_avg:,.1f}  ({((t3_avg-t1_avg)/t1_avg)*100:+.1f}% vs 1st)")

# 7-day rolling average of daily sums
print(f"\n  7-DAY ROLLING AVERAGE OF DAILY SUMS:")
if len(sorted_days) >= 7:
    daily_sum_list = [daily_sums[d] for d in sorted_days]
    for i in range(len(sorted_days)):
        if i >= 6:  # need at least 7 days
            window = daily_sum_list[i-6:i+1]
            roll_avg = sum(window) / 7
            print(f"    {sorted_days[i]}  7d_avg = {roll_avg:>10,.1f}")

# =============================================================================
# 8. Interpretation of totals
# =============================================================================
print(f"\n{'='*78}")
print("8. INTERPRETATION: WHAT DOES THE RAW SUM MEAN?")
print(f"{'='*78}")

samples_per_day = 24 * 3600 / interval_sec
print(f"""
  DATA COLLECTION METHOD:
    - Each data point = sum of MFE screen impressions in a 30-minute window
    - Sampling interval = ~{interval_min:.0f} minutes (~{interval_hr:.2f} hours)
    - Samples per day = ~{samples_per_day:.1f}

  THE OVERLAP / DOUBLE-COUNTING PROBLEM:
    Since the sampling window is 30 minutes but samples are taken every
    ~{interval_min:.0f} minutes ({interval_hr:.2f} hours), the windows do NOT overlap.
    The 30-min window is SHORTER than the ~3-hour sampling interval.

    This means there are GAPS between windows:
    - Each sample covers 30 minutes of activity
    - But samples are ~{interval_min:.0f} minutes apart
    - So only 30 / {interval_min:.0f} = {30/interval_min:.1%} of time is captured
    - ~{(1 - 30/interval_min):.1%} of the time is NOT captured by any sample

  ESTIMATING ACTUAL TOTAL IMPRESSIONS:
    Raw sum of all 30-min window sums:   {total:>12,}
    
    Method 1 - Scale by coverage ratio:
      If activity is uniform, we can estimate total impressions by scaling:
      Coverage ratio = 30 min / {interval_min:.0f} min = {30/interval_min:.4f}
      Estimated total = {total:,} / {30/interval_min:.4f} = {total / (30/interval_min):>,.0f}
      
      BUT activity is NOT uniform (there are clear daily cycles with 
      peaks and troughs), so this is a rough estimate.
    
    Method 2 - Daily estimation:
      Average daily sum from samples: {sum(sums_list)/len(sums_list):>,.0f}
      Samples per day: ~{samples_per_day:.1f}
      Each sample covers 30 min; day has {24*60} min = {24*60/30:.0f} half-hours
      Ratio of covered half-hours: {samples_per_day:.1f} / {24*60/30:.0f} = {samples_per_day/(24*60/30):.4f}
      
      Estimated actual daily impressions: {(sum(sums_list)/len(sums_list)) / (samples_per_day/(24*60/30)):>,.0f}
      Over {len(active_days)} active days: {(sum(sums_list)/len(sums_list)) / (samples_per_day/(24*60/30)) * len(active_days):>,.0f}

  IMPORTANT CAVEATS:
    1. The raw sum ({total:,}) is NOT the total number of screen impressions.
       It is the sum of {len(values)} separate 30-minute window snapshots.
    2. Since windows don't overlap, there's no double-counting, but there
       ARE gaps -- most of the day's activity is not captured.
    3. The scaling estimate assumes activity in uncaptured periods is similar
       to captured periods, which may not hold given strong intraday patterns.
    4. "Screen impressions" may include repeated views by the same user,
       so these are NOT unique users -- they are view events.

  BOTTOM LINE:
    - The {total:,} figure represents impressions observed in sampled windows only.
    - A reasonable estimate for total impressions over the full period is
      approximately {total / (30/interval_min):,.0f} (scaling by the coverage ratio).
    - Per day, that is roughly {(total / (30/interval_min)) / len(active_days):,.0f} screen impressions.
""")

# =============================================================================
# Summary statistics
# =============================================================================
print(f"{'='*78}")
print("SUMMARY STATISTICS")
print(f"{'='*78}")
import statistics
print(f"  Count:              {len(values):,}")
print(f"  Sum:                {total:,}")
print(f"  Mean:               {total/len(values):,.1f}")
print(f"  Median:             {statistics.median(values):,.1f}")
print(f"  Std Dev:            {statistics.stdev(values):,.1f}")
print(f"  Min:                {min(values):,}")
print(f"  Max:                {max(values):,}")
print(f"  Range:              {max(values) - min(values):,}")
print(f"  25th percentile:    {sorted(values)[len(values)//4]:,}")
print(f"  75th percentile:    {sorted(values)[3*len(values)//4]:,}")
print(f"  Active days:        {len(active_days)}")
print(f"  Active date range:  {active_days[0]} to {active_days[-1]}")
print(f"  Trend:              {trend_desc} (slope={slope:+,.1f}/week, R^2={r_squared:.3f})")
print(f"  Weekday/Weekend:    Weekdays {pct_diff:+.1f}% vs weekends")
print(f"{'='*78}")

