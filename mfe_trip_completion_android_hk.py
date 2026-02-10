#!/usr/bin/env python3
"""
MFE Trip Completion Analysis: Android - Hong Kong
Analyzes entry_screen_impression and trip_completion data from Grafana.
Data source: Panel 4 - [Android][Temp] Manual Fare Entry Impression & Trip Completion
Country: Hong Kong (HK), OS: Android
Time range: 90 days (2025-11-12 to 2026-02-10), Interval: ~2.95 hours
"""
import datetime
from collections import defaultdict, OrderedDict
import statistics

# =============================================================================
# DATA - Non-zero values extracted from Grafana JSON
# =============================================================================
# First non-zero data point is at index 408 of 732 total points
# Timestamps: first_ts = 1762936020000, interval = 10620000 ms
# First non-zero ts = 1762936020000 + 408 * 10620000 = 1767268980000

first_ts_ms = 1767268980000
interval_ms = 10620000  # ~2.95 hours between samples

entry_screen_impression = [
    3407, 5512, 6547, 6938, 7504, 8886, 12865, 15956, 16178, 16845,
    17040, 17331, 17881, 16673, 17169, 17695, 17760, 17417, 17438, 17216,
    17153, 17059, 16380, 15799, 14743, 14521, 14381, 14091, 13462, 16881,
    17446, 17239, 17464, 18834, 19289, 19343, 19291, 19299, 19555, 19678,
    19688, 20125, 20590, 20740, 20811, 20839, 21215, 21333, 21622, 21617,
    21506, 21517, 21738, 21750, 22038, 22120, 22058, 22270, 22847, 22964,
    22875, 22908, 23135, 23072, 23634, 24480, 24471, 24753, 25577, 26056,
    23413, 23290, 24350, 24299, 23474, 22890, 22437, 22613, 21608, 21359,
    20978, 19980, 19394, 19218, 18814, 17652, 21267, 21527, 20311, 20474,
    21170, 21480, 21459, 21563, 21587, 21388, 21316, 21634, 21697, 21992,
    22097, 22049, 22119, 22080, 22200, 22392, 22286, 22380, 22512, 22798,
    22691, 22868, 22832, 22967, 23031, 22924, 23070, 22792, 22831, 23067,
    23070, 23279, 24069, 24153, 24246, 25560, 25801, 23092, 23061, 24441,
    24249, 23602, 22633, 22398, 22609, 21504, 20903, 20113, 19815, 18924,
    18706, 18063, 16776, 20592, 20722, 19688, 19866, 20602, 21063, 21327,
    21471, 21251, 21485, 21613, 21529, 21724, 21730, 21996, 21929, 21895,
    22064, 22102, 22288, 24978, 26434, 27035, 27381, 27913, 30664, 33013,
    33382, 33122, 33132, 33576, 33574, 33696, 34111, 34175, 34970, 35857,
    35983, 37581, 38548, 38551, 34618, 34572, 36224, 36167, 34971, 34047,
    33577, 33351, 31966, 31463, 30717, 30530, 28509, 28031, 26462, 25598,
    30518, 30734, 28625, 28591, 30547, 30820, 31177, 31220, 31023, 31226,
    31193, 31350, 31180, 31582, 31660, 31607, 31662, 31559, 31582, 31314,
    31456, 31138, 31529, 31692, 31733, 31497, 31541, 31340, 31422, 31710,
    31489, 31430, 31517, 31429, 31902, 32062, 33141, 33171, 33825, 35415,
    35510, 32470, 33509, 35228, 35650, 34757, 33504, 33377, 33542, 31953,
    30834, 29034, 27111, 26927, 25823, 24390, 24016, 28859, 29060, 27322,
    27948, 28951, 29408, 29661, 29758, 29697, 29909, 30029, 30196, 30543,
    30960, 31059, 31035, 31170, 31055, 31528, 31617, 31895, 31767, 32417,
    32586, 32610, 32820, 33163, 33018, 33609, 33553, 33910, 33974, 33812,
    33959, 33964, 34500, 35506, 36136, 37776, 38674, 38742, 35710, 35864,
    37616, 36568, 35464, 34292, 34005, 33689, 32027, 31505, 30744, 30239,
    29555, 28505, 27231, 26908, 32287, 32760, 31280, 31283, 32262, 32413,
    33301, 33317, 33041, 33323,
]

trip_completion = [
    3337, 5419, 6442, 6805, 7375, 8614, 12593, 15552, 15715, 16352,
    16519, 17132, 17312, 16171, 16178, 16793, 17308, 16930, 16981, 16769,
    16709, 16623, 15958, 15409, 14398, 14177, 14062, 13772, 13152, 16486,
    17068, 16871, 17031, 18385, 18887, 18939, 18885, 18940, 19151, 19224,
    19154, 19524, 19667, 20095, 20168, 20189, 20546, 20645, 20876, 20918,
    20832, 20859, 21069, 21115, 21371, 21469, 21404, 21650, 22148, 22256,
    22171, 22193, 22426, 22387, 22801, 23659, 23675, 23941, 24735, 25201,
    22632, 22521, 23619, 23655, 22947, 22372, 21905, 22078, 21089, 20842,
    20480, 19547, 18968, 18776, 18369, 17249, 20790, 21060, 19855, 19999,
    20740, 21026, 21003, 21105, 21118, 20903, 20832, 21132, 21087, 21477,
    21584, 21540, 21526, 21587, 21693, 21849, 21749, 21807, 21957, 22215,
    22275, 22110, 22343, 22346, 22499, 22527, 22418, 22287, 22319, 22546,
    22553, 22769, 23494, 23579, 24029, 24974, 25216, 22556, 22562, 23867,
    23767, 23132, 22171, 21933, 22121, 21133, 20443, 19664, 19406, 18507,
    18238, 17663, 16412, 20142, 20289, 19332, 19413, 20146, 20585, 20842,
    20988, 20780, 21059, 21126, 21044, 21257, 21275, 21528, 21486, 21468,
    21661, 21656, 21804, 23937, 25291, 26021, 26295, 26737, 29212, 31353,
    31690, 31675, 32134, 32053, 32053, 32239, 32705, 32758, 33654, 34566,
    34664, 36194, 37127, 37136, 33408, 33322, 34927, 34892, 33764, 32852,
    32392, 32193, 30613, 30374, 29785, 29582, 27610, 27308, 25612, 24813,
    29549, 29765, 27683, 27649, 29633, 30033, 30318, 30375, 30212, 30389,
    30381, 30513, 30359, 30682, 30783, 30733, 30786, 30706, 30711, 30475,
    30622, 30314, 30703, 30847, 30916, 30706, 30771, 30547, 30549, 30813,
    30584, 30519, 30505, 30515, 30695, 31123, 32188, 32247, 32849, 34345,
    34520, 31481, 32493, 34162, 34623, 33757, 32566, 32430, 32556, 31090,
    30017, 28313, 26449, 26262, 25195, 23823, 23453, 28019, 28353, 26651,
    27233, 28178, 28646, 28912, 29009, 28958, 29179, 29303, 29435, 29763,
    30141, 30271, 30263, 30391, 30256, 30754, 30818, 31081, 30956, 31610,
    31792, 31818, 32011, 32355, 32212, 32776, 32709, 33046, 33103, 32963,
    33117, 33147, 33647, 34611, 35188, 36808, 37666, 37740, 34763, 34902,
    36655, 35672, 34589, 33465, 33181, 32910, 31290, 30700, 30077, 29581,
    28940, 27917, 26663, 26328, 31546, 32014, 30506, 30488, 31414, 31557,
    32457, 32491, 32247, 32525,
]

# Grafana summary stats for verification
grafana_stats = {
    "entry_screen_impression": {
        "sum": 8_470_207, "max": 38_742, "min": 0, "logmin": 3_407,
        "mean": 11_571.32, "count": 732, "nonNullCount": 732,
    },
    "trip_completion": {
        "sum": 8_237_982, "max": 37_740, "min": 0, "logmin": 3_337,
        "mean": 11_254.07, "count": 732, "nonNullCount": 732,
    },
}

# Data structure constants
total_points = 732
zero_points = 408
active_points = len(entry_screen_impression)  # 324
interval_sec = interval_ms / 1000
interval_min = interval_sec / 60
interval_hr = interval_min / 60
window_size_min = 30  # each point is a 30-min moving window sum

# Generate timestamps
timestamps_ms = [first_ts_ms + i * interval_ms for i in range(active_points)]

def ms_to_dt(ms):
    return datetime.datetime.utcfromtimestamp(ms / 1000.0)

timestamps_dt = [ms_to_dt(ts) for ts in timestamps_ms]


def sep(title):
    return f"\n{'='*78}\n  {title}\n{'='*78}"


# =============================================================================
# 0. DATA VERIFICATION
# =============================================================================
print(sep("MFE TRIP COMPLETION ANALYSIS - ANDROID - HONG KONG"))
print(f"""
  Data Source:  Grafana Panel 4 - [Android][Temp] MFE Impression & Trip Completion
  Country:      Hong Kong (HK)
  Platform:     Android
  Time Range:   2025-11-12 to 2026-02-10 (90 days)
  Interval:     {interval_ms:,} ms ({interval_hr:.2f} hours, ~{interval_min:.0f} min)
  Window:       30-minute moving sum
  Total Points: {total_points} ({zero_points} zero + {active_points} active)
""")

print(sep("1. DATA VERIFICATION"))

imp_sum = sum(entry_screen_impression)
tc_sum = sum(trip_completion)

# Grafana reports sum over all 732 points (including zeros)
# Our non-zero sums should match since the zeros contribute nothing
print(f"""
  Entry Screen Impressions:
    Computed sum (non-zero):  {imp_sum:>12,}
    Grafana reported sum:     {grafana_stats['entry_screen_impression']['sum']:>12,}
    Match: {'YES' if imp_sum == grafana_stats['entry_screen_impression']['sum'] else 'NO (delta=' + str(imp_sum - grafana_stats['entry_screen_impression']['sum']) + ')'}
    Count:  {active_points} non-zero / {total_points} total
    Max:    {max(entry_screen_impression):>8,} (Grafana: {grafana_stats['entry_screen_impression']['max']:>8,})
    Min:    {min(entry_screen_impression):>8,} (Grafana logmin: {grafana_stats['entry_screen_impression']['logmin']:>8,})

  Trip Completions:
    Computed sum (non-zero):  {tc_sum:>12,}
    Grafana reported sum:     {grafana_stats['trip_completion']['sum']:>12,}
    Match: {'YES' if tc_sum == grafana_stats['trip_completion']['sum'] else 'NO (delta=' + str(tc_sum - grafana_stats['trip_completion']['sum']) + ')'}
    Count:  {active_points} non-zero / {total_points} total
    Max:    {max(trip_completion):>8,} (Grafana: {grafana_stats['trip_completion']['max']:>8,})
    Min:    {min(trip_completion):>8,} (Grafana logmin: {grafana_stats['trip_completion']['logmin']:>8,})
""")

# =============================================================================
# 2. DATE RANGE
# =============================================================================
print(sep("2. DATE RANGE OF ACTIVE DATA"))

first_dt = timestamps_dt[0]
last_dt = timestamps_dt[-1]
span = last_dt - first_dt

days_set = sorted(set(dt.date() for dt in timestamps_dt))

print(f"""
  First non-zero data:   {first_dt.strftime('%Y-%m-%d %H:%M:%S UTC')}
  Last non-zero data:    {last_dt.strftime('%Y-%m-%d %H:%M:%S UTC')}
  Total span:            {span.days} days, {span.seconds // 3600} hours
  Active calendar days:  {len(days_set)}
  Date range:            {days_set[0]} to {days_set[-1]}

  Panel start (approx):  2025-11-12 (90 days before end)
  Zero-value period:     ~{zero_points} samples = ~{zero_points * interval_hr / 24:.0f} days of no data
""")

# =============================================================================
# 3. OVERALL CONVERSION RATE
# =============================================================================
print(sep("3. OVERALL CONVERSION RATE"))

overall_cvr = tc_sum / imp_sum * 100

print(f"""
  Entry Screen Impressions (window sums): {imp_sum:>12,}
  Trip Completions (window sums):         {tc_sum:>12,}
  Drop-off (impressions - completions):   {imp_sum - tc_sum:>12,}

  Overall Conversion Rate:  {overall_cvr:.4f}%
  Drop-off Rate:            {100 - overall_cvr:.4f}%

  For every 1000 users who see the MFE entry screen,
  ~{overall_cvr * 10:.0f} complete a trip ({100 - overall_cvr:.2f}% drop off).
""")

# =============================================================================
# 4. PER-SAMPLE CONVERSION RATE ANALYSIS
# =============================================================================
print(sep("4. PER-SAMPLE CONVERSION RATE OVER TIME"))

sample_cvrs = []
for imp, tc in zip(entry_screen_impression, trip_completion):
    if imp > 0:
        sample_cvrs.append(tc / imp * 100)
    else:
        sample_cvrs.append(0)

print(f"""
  Conversion Rate Statistics (per sample):
    Mean:    {statistics.mean(sample_cvrs):.4f}%
    Median:  {statistics.median(sample_cvrs):.4f}%
    Std Dev: {statistics.stdev(sample_cvrs):.4f}%
    Min:     {min(sample_cvrs):.4f}%  (at {timestamps_dt[sample_cvrs.index(min(sample_cvrs))].strftime('%Y-%m-%d %H:%M')})
    Max:     {max(sample_cvrs):.4f}%  (at {timestamps_dt[sample_cvrs.index(max(sample_cvrs))].strftime('%Y-%m-%d %H:%M')})
""")

# Conversion rate trend: first third vs last third
third = len(sample_cvrs) // 3
cvr_t1 = statistics.mean(sample_cvrs[:third])
cvr_t2 = statistics.mean(sample_cvrs[third:2*third])
cvr_t3 = statistics.mean(sample_cvrs[2*third:])

print(f"  Conversion Rate Trend (thirds):")
print(f"    First third:  {cvr_t1:.4f}%")
print(f"    Middle third: {cvr_t2:.4f}%  ({cvr_t2 - cvr_t1:+.4f} pp)")
print(f"    Last third:   {cvr_t3:.4f}%  ({cvr_t3 - cvr_t1:+.4f} pp)")
print(f"    Direction:    {'IMPROVING' if cvr_t3 > cvr_t1 else 'DECLINING' if cvr_t3 < cvr_t1 else 'STABLE'}")

# =============================================================================
# 5. DAILY BREAKDOWN
# =============================================================================
print(sep("5. DAILY BREAKDOWN"))

daily_imp = defaultdict(list)
daily_tc = defaultdict(list)
for dt, imp, tc in zip(timestamps_dt, entry_screen_impression, trip_completion):
    daily_imp[dt.date()].append(imp)
    daily_tc[dt.date()].append(tc)

sorted_days = sorted(daily_imp.keys())

print(f"  {'Date':<12} {'Day':>4} {'Imp Sum':>10} {'TC Sum':>10} {'CVR':>8} {'Imp Peak':>9} {'TC Peak':>9} {'Samples':>8}")
print(f"  {'-'*12} {'-'*4} {'-'*10} {'-'*10} {'-'*8} {'-'*9} {'-'*9} {'-'*8}")

daily_cvrs = {}
for d in sorted_days:
    imp_s = sum(daily_imp[d])
    tc_s = sum(daily_tc[d])
    cvr = tc_s / imp_s * 100 if imp_s > 0 else 0
    daily_cvrs[d] = cvr
    print(f"  {str(d):<12} {d.strftime('%a'):>4} {imp_s:>10,} {tc_s:>10,} {cvr:>7.2f}% "
          f"{max(daily_imp[d]):>9,} {max(daily_tc[d]):>9,} {len(daily_imp[d]):>8}")

# Daily summary stats
daily_imp_sums = [sum(daily_imp[d]) for d in sorted_days]
daily_tc_sums = [sum(daily_tc[d]) for d in sorted_days]

print(f"\n  Daily Summary:")
print(f"    Impression daily avg: {statistics.mean(daily_imp_sums):>10,.1f}")
print(f"    Completion daily avg: {statistics.mean(daily_tc_sums):>10,.1f}")
print(f"    Best CVR day:   {max(daily_cvrs, key=daily_cvrs.get)} ({daily_cvrs[max(daily_cvrs, key=daily_cvrs.get)]:.2f}%)")
print(f"    Worst CVR day:  {min(daily_cvrs, key=daily_cvrs.get)} ({daily_cvrs[min(daily_cvrs, key=daily_cvrs.get)]:.2f}%)")

# =============================================================================
# 6. WEEKLY PATTERN
# =============================================================================
print(sep("6. WEEKLY PATTERN (Weekday vs Weekend)"))

dow_imp = defaultdict(list)
dow_tc = defaultdict(list)
dow_cvr = defaultdict(list)

for d in sorted_days:
    dow = d.weekday()
    imp_s = sum(daily_imp[d])
    tc_s = sum(daily_tc[d])
    dow_imp[dow].append(imp_s)
    dow_tc[dow].append(tc_s)
    if imp_s > 0:
        dow_cvr[dow].append(tc_s / imp_s * 100)

dow_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

print(f"\n  {'Day':<5} {'#Days':>6} {'Avg Imp':>12} {'Avg TC':>12} {'Avg CVR':>10}")
print(f"  {'-'*5} {'-'*6} {'-'*12} {'-'*12} {'-'*10}")

weekday_imp = []
weekend_imp = []
weekday_tc = []
weekend_tc = []

for dow_num in range(7):
    if dow_num in dow_imp:
        avg_imp = statistics.mean(dow_imp[dow_num])
        avg_tc = statistics.mean(dow_tc[dow_num])
        avg_cvr = statistics.mean(dow_cvr[dow_num]) if dow_cvr[dow_num] else 0
        print(f"  {dow_names[dow_num]:<5} {len(dow_imp[dow_num]):>6} {avg_imp:>12,.1f} {avg_tc:>12,.1f} {avg_cvr:>9.2f}%")
        if dow_num < 5:
            weekday_imp.extend(dow_imp[dow_num])
            weekday_tc.extend(dow_tc[dow_num])
        else:
            weekend_imp.extend(dow_imp[dow_num])
            weekend_tc.extend(dow_tc[dow_num])

wd_imp_avg = statistics.mean(weekday_imp) if weekday_imp else 0
we_imp_avg = statistics.mean(weekend_imp) if weekend_imp else 0
wd_tc_avg = statistics.mean(weekday_tc) if weekday_tc else 0
we_tc_avg = statistics.mean(weekend_tc) if weekend_tc else 0
wd_cvr = sum(weekday_tc) / sum(weekday_imp) * 100 if sum(weekday_imp) > 0 else 0
we_cvr = sum(weekend_tc) / sum(weekend_imp) * 100 if sum(weekend_imp) > 0 else 0

print(f"\n  Weekday vs Weekend:")
print(f"    Weekday avg impressions: {wd_imp_avg:>10,.1f}")
print(f"    Weekend avg impressions: {we_imp_avg:>10,.1f}")
print(f"    Weekday avg completions: {wd_tc_avg:>10,.1f}")
print(f"    Weekend avg completions: {we_tc_avg:>10,.1f}")
print(f"    Weekday CVR:             {wd_cvr:>9.2f}%")
print(f"    Weekend CVR:             {we_cvr:>9.2f}%")
if we_imp_avg > 0:
    pct_diff = ((wd_imp_avg - we_imp_avg) / we_imp_avg) * 100
    print(f"    Weekday traffic is {abs(pct_diff):.1f}% {'higher' if pct_diff > 0 else 'lower'} than weekend")

# =============================================================================
# 7. HOURLY DISTRIBUTION
# =============================================================================
print(sep("7. HOURLY DISTRIBUTION (UTC)"))

hour_imp = defaultdict(list)
hour_tc = defaultdict(list)

for dt, imp, tc in zip(timestamps_dt, entry_screen_impression, trip_completion):
    hour_imp[dt.hour].append(imp)
    hour_tc[dt.hour].append(tc)

print(f"  {'Hour':>6} {'#Samp':>6} {'Avg Imp':>10} {'Avg TC':>10} {'CVR':>8} {'Activity':>16}")
print(f"  {'-'*6} {'-'*6} {'-'*10} {'-'*10} {'-'*8} {'-'*16}")

for h in sorted(hour_imp.keys()):
    avg_imp = statistics.mean(hour_imp[h])
    avg_tc = statistics.mean(hour_tc[h])
    cvr = sum(hour_tc[h]) / sum(hour_imp[h]) * 100 if sum(hour_imp[h]) > 0 else 0
    if avg_imp > 30000:
        activity = "VERY HIGH"
    elif avg_imp > 25000:
        activity = "HIGH"
    elif avg_imp > 20000:
        activity = "MODERATE"
    elif avg_imp > 15000:
        activity = "LOW"
    else:
        activity = "VERY LOW"
    print(f"  {h:>4}:00 {len(hour_imp[h]):>6} {avg_imp:>10,.1f} {avg_tc:>10,.1f} {cvr:>7.2f}% {activity:>16}")

# =============================================================================
# 8. VOLUME TREND ANALYSIS
# =============================================================================
print(sep("8. VOLUME TREND ANALYSIS"))

# Weekly aggregation
weekly_data = OrderedDict()
for d in sorted_days:
    iso_year, iso_week, _ = d.isocalendar()
    week_key = f"{iso_year}-W{iso_week:02d}"
    if week_key not in weekly_data:
        weekly_data[week_key] = {'imp': 0, 'tc': 0, 'days': 0}
    weekly_data[week_key]['imp'] += sum(daily_imp[d])
    weekly_data[week_key]['tc'] += sum(daily_tc[d])
    weekly_data[week_key]['days'] += 1

print(f"\n  WEEKLY TOTALS:")
print(f"  {'Week':<12} {'Days':>5} {'Impressions':>14} {'Completions':>14} {'CVR':>8} {'WoW Imp':>10}")
print(f"  {'-'*12} {'-'*5} {'-'*14} {'-'*14} {'-'*8} {'-'*10}")

prev_imp_avg = None
week_imp_avgs = []
week_tc_avgs = []

for wk, wd in weekly_data.items():
    cvr = wd['tc'] / wd['imp'] * 100 if wd['imp'] > 0 else 0
    imp_avg = wd['imp'] / wd['days']
    tc_avg = wd['tc'] / wd['days']
    if prev_imp_avg is not None and prev_imp_avg > 0:
        wow = ((imp_avg - prev_imp_avg) / prev_imp_avg) * 100
        wow_str = f"{wow:>+8.1f}%"
    else:
        wow_str = "      N/A"
    print(f"  {wk:<12} {wd['days']:>5} {wd['imp']:>14,} {wd['tc']:>14,} {cvr:>7.2f}% {wow_str:>10}")
    prev_imp_avg = imp_avg
    week_imp_avgs.append(imp_avg)
    week_tc_avgs.append(tc_avg)

# Linear regression for impression trend
n = len(week_imp_avgs)
x_vals = list(range(n))
x_mean = sum(x_vals) / n
y_mean = sum(week_imp_avgs) / n
ss_xy = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_vals, week_imp_avgs))
ss_xx = sum((x - x_mean) ** 2 for x in x_vals)
slope_imp = ss_xy / ss_xx if ss_xx else 0
intercept_imp = y_mean - slope_imp * x_mean
y_pred = [slope_imp * x + intercept_imp for x in x_vals]
ss_res = sum((y - yp) ** 2 for y, yp in zip(week_imp_avgs, y_pred))
ss_tot = sum((y - y_mean) ** 2 for y in week_imp_avgs)
r2_imp = 1 - (ss_res / ss_tot) if ss_tot else 0

# Same for trip completion
y_mean_tc = sum(week_tc_avgs) / n
ss_xy_tc = sum((x - x_mean) * (y - y_mean_tc) for x, y in zip(x_vals, week_tc_avgs))
slope_tc = ss_xy_tc / ss_xx if ss_xx else 0
intercept_tc = y_mean_tc - slope_tc * x_mean
y_pred_tc = [slope_tc * x + intercept_tc for x in x_vals]
ss_res_tc = sum((y - yp) ** 2 for y, yp in zip(week_tc_avgs, y_pred_tc))
ss_tot_tc = sum((y - y_mean_tc) ** 2 for y in week_tc_avgs)
r2_tc = 1 - (ss_res_tc / ss_tot_tc) if ss_tot_tc else 0

def trend_label(slope):
    if slope > 5000:
        return "STRONGLY GROWING"
    elif slope > 1000:
        return "MODERATELY GROWING"
    elif slope > -1000:
        return "ROUGHLY STABLE"
    elif slope > -5000:
        return "MODERATELY DECLINING"
    else:
        return "STRONGLY DECLINING"

print(f"\n  LINEAR TREND (weekly avg/day):")
print(f"    Impressions: slope={slope_imp:>+,.1f}/week, R^2={r2_imp:.4f} => {trend_label(slope_imp)}")
print(f"    Completions: slope={slope_tc:>+,.1f}/week, R^2={r2_tc:.4f} => {trend_label(slope_tc)}")

# First half vs second half
half = active_points // 2
imp_h1 = statistics.mean(entry_screen_impression[:half])
imp_h2 = statistics.mean(entry_screen_impression[half:])
tc_h1 = statistics.mean(trip_completion[:half])
tc_h2 = statistics.mean(trip_completion[half:])
imp_change = ((imp_h2 - imp_h1) / imp_h1) * 100
tc_change = ((tc_h2 - tc_h1) / tc_h1) * 100

print(f"\n  FIRST HALF vs SECOND HALF:")
print(f"    Impressions: {imp_h1:>10,.1f} -> {imp_h2:>10,.1f}  ({imp_change:>+.1f}%)")
print(f"    Completions: {tc_h1:>10,.1f} -> {tc_h2:>10,.1f}  ({tc_change:>+.1f}%)")

# =============================================================================
# 9. DROP-OFF ANALYSIS
# =============================================================================
print(sep("9. DROP-OFF ANALYSIS (Impression -> Completion)"))

dropoffs = [imp - tc for imp, tc in zip(entry_screen_impression, trip_completion)]

print(f"""
  Per-sample drop-off statistics:
    Mean drop-off:   {statistics.mean(dropoffs):>8,.1f} users/sample
    Median drop-off: {statistics.median(dropoffs):>8,.1f} users/sample
    Max drop-off:    {max(dropoffs):>8,} users/sample
    Min drop-off:    {min(dropoffs):>8,} users/sample
    Std dev:         {statistics.stdev(dropoffs):>8,.1f}
""")

# Drop-off rate per sample
dropoff_rates = [(imp - tc) / imp * 100 if imp > 0 else 0
                 for imp, tc in zip(entry_screen_impression, trip_completion)]

print(f"  Per-sample drop-off rate statistics:")
print(f"    Mean:   {statistics.mean(dropoff_rates):.4f}%")
print(f"    Median: {statistics.median(dropoff_rates):.4f}%")
print(f"    Min:    {min(dropoff_rates):.4f}% (best conversion)")
print(f"    Max:    {max(dropoff_rates):.4f}% (worst conversion)")

# Daily drop-off
print(f"\n  Daily drop-off analysis:")
print(f"  {'Date':<12} {'Impressions':>12} {'Completions':>12} {'Drop-off':>10} {'Drop %':>8}")
print(f"  {'-'*12} {'-'*12} {'-'*12} {'-'*10} {'-'*8}")

for d in sorted_days:
    imp_s = sum(daily_imp[d])
    tc_s = sum(daily_tc[d])
    drop = imp_s - tc_s
    drop_pct = drop / imp_s * 100 if imp_s > 0 else 0
    print(f"  {str(d):<12} {imp_s:>12,} {tc_s:>12,} {drop:>10,} {drop_pct:>7.2f}%")

# =============================================================================
# 10. ESTIMATED ACTUAL VALUES
# =============================================================================
print(sep("10. ESTIMATED ACTUAL TRIP COMPLETIONS"))

coverage_ratio = (window_size_min / 60) / interval_hr
active_hours = active_points * interval_hr
active_days_count = active_hours / 24

est_imp = imp_sum / coverage_ratio
est_tc = tc_sum / coverage_ratio

print(f"""
  Coverage ratio: {window_size_min}-min window / {interval_hr:.2f}-hr sampling
                = {coverage_ratio:.4f} (~{coverage_ratio*100:.1f}% of events captured)

  Active period:  {active_points} data points x {interval_hr:.2f} hrs
                = {active_hours:,.1f} hours (~{active_days_count:.1f} days)

  Estimated ACTUAL values over the ~{active_days_count:.0f}-day active window:
  ----------------------------------------------------------------
  Metric              Window Sums     Est. Actual     Daily Average
  ----------------------------------------------------------------
  Impressions         {imp_sum:>12,}    {est_imp:>12,.0f}    {est_imp/active_days_count:>12,.0f}
  Completions         {tc_sum:>12,}    {est_tc:>12,.0f}    {est_tc/active_days_count:>12,.0f}
  ----------------------------------------------------------------

  Key: The conversion rate ({overall_cvr:.2f}%) applies regardless of scaling,
  since both numerator and denominator scale by the same coverage ratio.
""")

# =============================================================================
# 11. PEAK ANALYSIS
# =============================================================================
print(sep("11. PEAK AND TROUGH ANALYSIS"))

# Top 10 peaks by impressions
indexed_imp = list(enumerate(entry_screen_impression))
indexed_imp_desc = sorted(indexed_imp, key=lambda x: x[1], reverse=True)
indexed_imp_asc = sorted(indexed_imp, key=lambda x: x[1])

print(f"\n  TOP 10 IMPRESSION PEAKS:")
print(f"  {'Rank':>4} {'Imp':>8} {'TC':>8} {'CVR':>8} {'Timestamp (UTC)':>22} {'Day':>4}")
print(f"  {'-'*4} {'-'*8} {'-'*8} {'-'*8} {'-'*22} {'-'*4}")
for rank, (idx, val) in enumerate(indexed_imp_desc[:10], 1):
    dt = timestamps_dt[idx]
    tc_val = trip_completion[idx]
    cvr = tc_val / val * 100 if val > 0 else 0
    print(f"  {rank:>4} {val:>8,} {tc_val:>8,} {cvr:>7.2f}% {dt.strftime('%Y-%m-%d %H:%M'):>22} {dt.strftime('%a'):>4}")

print(f"\n  TOP 10 IMPRESSION TROUGHS (among non-zero):")
print(f"  {'Rank':>4} {'Imp':>8} {'TC':>8} {'CVR':>8} {'Timestamp (UTC)':>22} {'Day':>4}")
print(f"  {'-'*4} {'-'*8} {'-'*8} {'-'*8} {'-'*22} {'-'*4}")
for rank, (idx, val) in enumerate(indexed_imp_asc[:10], 1):
    dt = timestamps_dt[idx]
    tc_val = trip_completion[idx]
    cvr = tc_val / val * 100 if val > 0 else 0
    print(f"  {rank:>4} {val:>8,} {tc_val:>8,} {cvr:>7.2f}% {dt.strftime('%Y-%m-%d %H:%M'):>22} {dt.strftime('%a'):>4}")

# =============================================================================
# 12. CNY / SEASONAL SPIKE ANALYSIS
# =============================================================================
print(sep("12. NOTABLE PATTERNS AND SPIKES"))

# Find the biggest week-over-week jumps
print(f"\n  Looking for sudden volume changes (daily sums):")
print(f"  {'Date':<12} {'Day Imp':>10} {'Prev Day':>10} {'Change':>10} {'Change%':>9}")
print(f"  {'-'*12} {'-'*10} {'-'*10} {'-'*10} {'-'*9}")

prev_imp_day = None
for d in sorted_days:
    imp_s = sum(daily_imp[d])
    if prev_imp_day is not None:
        change = imp_s - prev_imp_day
        pct = change / prev_imp_day * 100 if prev_imp_day > 0 else 0
        if abs(pct) > 10:  # Show only significant changes (>10%)
            print(f"  {str(d):<12} {imp_s:>10,} {prev_imp_day:>10,} {change:>+10,} {pct:>+8.1f}%")
    prev_imp_day = imp_s

# =============================================================================
# SUMMARY
# =============================================================================
print(sep("SUMMARY"))
print(f"""
  Region:             Hong Kong
  Platform:           Android
  Active Period:      {days_set[0]} to {days_set[-1]} ({len(days_set)} days)

  VOLUME:
    Total impressions (window sums):  {imp_sum:>12,}
    Total completions (window sums):  {tc_sum:>12,}
    Estimated actual completions:     {est_tc:>12,.0f}
    Estimated daily completions:      {est_tc/active_days_count:>12,.0f}

  CONVERSION:
    Overall CVR:  {overall_cvr:.2f}%
    Mean sample CVR: {statistics.mean(sample_cvrs):.2f}%
    CVR trend: first third {cvr_t1:.2f}% -> last third {cvr_t3:.2f}% ({cvr_t3 - cvr_t1:+.2f} pp)

  VOLUME TREND:
    Impression trend: {trend_label(slope_imp)} (slope={slope_imp:+,.0f}/week)
    Completion trend: {trend_label(slope_tc)} (slope={slope_tc:+,.0f}/week)
    First->Second half impressions: {imp_change:+.1f}%
    First->Second half completions: {tc_change:+.1f}%

  PATTERNS:
    Weekday CVR: {wd_cvr:.2f}%  |  Weekend CVR: {we_cvr:.2f}%
    Peak hour (UTC): {max(hour_imp, key=lambda h: statistics.mean(hour_imp[h]))}:00
    Trough hour (UTC): {min(hour_imp, key=lambda h: statistics.mean(hour_imp[h]))}:00
""")
print("=" * 78)
