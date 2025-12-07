# Tune File Recommendations - v10
## Analysis Date: 2025-12-03
## Tune File: Keith Proseus_1999JDMSTI_DW740_VF28_21builtStroker_v10_20251203_155625.tune
## Datalog: tuner_log_25-12-03_1610_v10.csv

---

## EXECUTIVE SUMMARY

Analysis of 30,111 data points over 2,348 seconds reveals:

### Key Findings:
1. **Fuel Trimming**: Generally good (LTFT: -0.32%, STFT: -1.72%), but STFT variability (5.48% std) suggests some areas need refinement
2. **Boost Control**: **CRITICAL ISSUE** - Significant boost control problems:
   - Low RPM (0-3000): Severe overboost (67.43 kPa error average)
   - Higher RPM (3000+): Underboost issues
   - Wastegate duty cycle very low (7.5% mean, max 80.1%)
   - 75.8% of boost samples show overboost conditions
3. **Lambda Control**: Good in power mode (0.010 error), slightly lean in closed loop (1.047 average)

### Priority Actions:
1. **HIGH**: Fix boost control at low RPM - reduce boost targets or increase wastegate response
2. **HIGH**: Review wastegate base duty table - appears insufficient for proper boost control
3. **MEDIUM**: Smooth fuel_base table to reduce STFT variability
4. **MEDIUM**: Fine-tune PE lambda tables for better consistency

---

## 1. BOOST CONTROL - CRITICAL ISSUES

### 1.1 Low RPM Overboost Problem

**Current Situation:**
- At 0-3000 RPM in boost conditions: Average boost error = **+67.43 kPa** (severe overboost)
- 563 samples affected
- Wastegate duty cycle averaging only **5.4%** at these conditions
- Boost target appears too aggressive for low RPM conditions

**Root Cause Analysis:**
Looking at the tune file:
- `boost_target` table shows values up to **199.5 kPa** at low RPM/high TPS
- `wg_base` table shows **0.0%** duty at low RPM/low TPS, increasing to **80.5%** at high RPM/TPS
- `wg_overboost_step` values: **8.6, 5.5, 3.9, 3.1%** (indexed by boost error: 20.3, 11.7, 5.3, 2.1 kPa)

**Recommendations:**

#### A. Reduce Boost Targets at Low RPM
**Current `boost_target` values (RPM row 1, TPS columns 5-8):**
```
Row 1 (0 rpm): 100.3, 128.0, 128.0, 134.4, 169.6, 169.6, 169.6, 199.5
```

**Recommended Changes:**
- Reduce boost targets at low RPM (rows 1-2, 0-2900 rpm) and high TPS:
  - Row 1, Column 8 (0 rpm, 62.5% TPS): **199.5 → 150.0 kPa** (reduce by ~25%)
  - Row 1, Columns 5-7: **169.6 → 140.0 kPa** (reduce by ~17%)
  - Row 2, Column 8 (2800 rpm, 62.5% TPS): **199.5 → 160.0 kPa**

**Rationale:** Low RPM boost targets are too aggressive. The turbo cannot efficiently build boost at low RPM, leading to wastegate being unable to control properly.

#### B. Increase Wastegate Base Duty at Low RPM
**Current `wg_base` values (RPM row 1):**
```
Row 1 (0 rpm): 0.0, 80.5, 80.5, 80.5, 80.5, 80.5, 80.5, 80.5
```

**Recommended Changes:**
- Increase base wastegate duty at low RPM to provide better control authority:
  - Row 1, Column 1 (0 rpm, 0% TPS): **0.0 → 10.0%** (prevent wastegate from being fully closed)
  - Row 1, Columns 2-8: **80.5 → 85.0%** (increase control range)
  - Row 2, Column 1 (2800 rpm, 0% TPS): **0.0 → 5.0%**

**Rationale:** Higher base duty provides more control authority and prevents wastegate from being fully closed, which can cause boost spikes.

#### C. Increase Overboost Response Steps
**Current `wg_overboost_step` values:**
```
8.6, 5.5, 3.9, 3.1%  (for errors: 20.3, 11.7, 5.3, 2.1 kPa)
```

**Recommended Changes:**
```
12.0, 8.0, 5.0, 3.5%  (increase by ~40% for larger errors)
```

**Rationale:** With 67 kPa average overboost, the system needs more aggressive correction. Current steps are too small to respond quickly enough.

#### D. Review Boost Limit Table
**Current `boost_limit` values:**
```
141.9, 149.3, 157.9, 164.3, 171.7, 178.1, 184.5, 190.9, 198.4, 204.8, 211.2, 217.6, 224.0, 229.3, 234.7, 234.7 kPa
```

**Recommendation:** Ensure boost limits are appropriate for engine safety. Current limits appear reasonable, but verify they're not being exceeded in the overboost conditions.

### 1.2 High RPM Underboost

**Current Situation:**
- At 3000-4000 RPM: Average boost error = **-5.08 kPa** (slight underboost)
- At 4000-5000 RPM: Average boost error = **-27.10 kPa** (significant underboost)
- Wastegate duty: 19.9% at 3000-4000 RPM, 18.0% at 4000-5000 RPM

**Recommendations:**

#### A. Increase Wastegate Base Duty at Mid-High RPM
**Current `wg_base` values (RPM rows 3-5, ~3000-5400 rpm):**
- Review and increase base duty by 5-10% in these regions

**Rationale:** Higher base duty allows wastegate to close more, building boost faster.

#### B. Increase Underboost Response Steps
**Current `wg_underboost_step` values:**
```
2.7, 1.2, 0.4, 0.0%  (for errors: 20.3, 11.7, 5.3, 2.1 kPa)
```

**Recommended Changes:**
```
5.0, 2.5, 1.0, 0.5%  (nearly double the response)
```

**Rationale:** More aggressive underboost correction will help achieve boost targets faster.

### 1.3 Wastegate Control Parameters

**Current Settings:**
- `wg_freq`: 14.50 Hz
- `wg_update_interval`: 120 ms
- `wg_integral_limit`: 10.2%

**Recommendations:**
- Consider reducing `wg_update_interval` to **80-100 ms** for faster response
- Review `wg_integral_limit` - current 10.2% may be limiting integral term effectiveness

---

## 2. FUEL TRIM OPTIMIZATION

### 2.1 Short-Term Fuel Trim Variability

**Current Situation:**
- STFT Mean: **-1.72%** (good, slightly rich)
- STFT Std Dev: **5.48%** (moderate variability)
- STFT Max: **25.00%** (some extreme corrections)

**Analysis:**
While overall fuel trimming is good (LTFT: -0.32%), the STFT variability suggests the `fuel_base` table may have some abrupt transitions or areas that don't match actual engine requirements.

**Recommendations:**

#### A. Smooth Fuel Base Table Transitions
- Review `fuel_base` table for abrupt value changes between adjacent cells
- Ensure smooth gradients, especially in commonly used regions (2000-5000 RPM, 0.5-1.5 g/rev)
- Target: Reduce STFT std dev from 5.48% to <4.0%

#### B. Fine-Tune Problematic Regions
While the automated analysis didn't flag specific regions (threshold may be too high), review areas where:
- STFT frequently exceeds ±10%
- Rapid STFT oscillations occur (indicates table mismatch)

**Method:**
1. Identify RPM/Load bins with high STFT variance
2. Adjust `fuel_base` values in those regions by 2-5% in the direction opposite to average STFT
3. Re-log and verify improvement

### 2.2 Long-Term Fuel Trim

**Current Situation:**
- LTFT Mean: **-0.32%** (excellent - very close to 0%)
- LTFT Std Dev: **0.87%** (very good consistency)
- LTFT Max: **3.12%** (acceptable)

**Status:** ✅ **No action required** - LTFT is well-controlled, indicating systematic fueling is accurate.

---

## 3. LAMBDA/AIR-FUEL RATIO

### 3.1 Power Mode Lambda

**Current Situation:**
- Power Mode Lambda Error: **0.010** (actual vs target)
- Power Mode Samples: 163
- Error Std Dev: **0.059**

**Analysis:**
Lambda control in power mode is good. Average error of 0.010 λ is within acceptable range.

**Recommendations:**
- ✅ **No major changes needed**
- Consider fine-tuning `pe_initial` and `pe_safe` tables if specific RPM/Load regions show consistent lambda errors >0.02

### 3.2 Closed Loop Lambda

**Current Situation:**
- Closed Loop Lambda Mean: **1.047** (slightly lean of stoichiometric)
- Closed Loop Lambda Std Dev: **0.190** (high variability)

**Analysis:**
Target lambda in closed loop should be 1.000 (stoichiometric). Current 1.047 average suggests slight lean condition, but this may be intentional for emissions.

**Recommendations:**
- If emissions allow, consider adjusting closed-loop target toward 1.000
- High variability (0.190 std dev) may indicate:
  - MAF sensor calibration issues
  - Fuel injector inconsistencies
  - Intake/exhaust leaks
- Review `fuel_base` table in closed-loop operating regions (low load, <1.0 g/rev)

---

## 4. ADDITIONAL OBSERVATIONS

### 4.1 Boost Target Barometric Compensation

**Current:** `boost_target_baro_comp` - All values are **0.0%** (disabled)

**Recommendation:**
- If operating at varying altitudes, consider enabling barometric compensation
- Base file shows values from -44.5% to 0.0% (reduces boost target at altitude)
- Current disabled state is fine for sea-level operation

### 4.2 Boost Target IAT Compensation

**Current:** `boost_target_iat_comp` - All values are **0.0%** (disabled)

**Recommendation:**
- Consider adding IAT compensation to reduce boost targets at high IAT
- Protects engine from heat-related issues
- Typical: -2% to -5% per 10°C above 30°C

### 4.3 Wastegate Max Duty Limits

**Current:** `wg_max` shows values up to **90.6%**

**Analysis:**
- Maximum wastegate duty reached: **80.1%** (from datalog)
- Still within limits, but approaching maximum

**Recommendation:**
- Monitor if wastegate duty frequently hits `wg_max` limits
- If so, may need mechanical wastegate adjustment or higher `wg_max` values

---

## 5. IMPLEMENTATION PRIORITY

### Phase 1: Critical Boost Control Fixes (IMMEDIATE)
1. ✅ Reduce `boost_target` at low RPM (rows 1-2, high TPS columns)
2. ✅ Increase `wg_base` duty at low RPM
3. ✅ Increase `wg_overboost_step` values
4. ✅ Re-log and verify boost control improvement

### Phase 2: Boost Control Refinement (HIGH PRIORITY)
1. ✅ Increase `wg_underboost_step` values
2. ✅ Adjust `wg_base` at mid-RPM for better boost response
3. ✅ Consider reducing `wg_update_interval` for faster response

### Phase 3: Fuel Trim Optimization (MEDIUM PRIORITY)
1. Review and smooth `fuel_base` table transitions
2. Fine-tune regions with high STFT variability
3. Verify improvements with re-logging

### Phase 4: Lambda Fine-Tuning (LOW PRIORITY)
1. Fine-tune `pe_initial` and `pe_safe` if needed
2. Review closed-loop lambda target if emissions allow

---

## 6. SPECIFIC TUNE FILE CHANGES

### 6.1 Boost Target Table Adjustments

**File:** `boost_target`

**Current Row 1 (0 rpm):**
```
100.3, 122.7, 123.7, 124.8, 126.9, 128.0, 129.1, 130.1,
100.3, 128.0, 124.8, 134.4, 134.4, 134.4, 134.4, 134.4,
100.3, 128.0, 128.0, 134.4, 169.6, 169.6, 169.6, 169.6,
100.3, 128.0, 128.0, 134.4, 169.6, 169.6, 169.6, 199.5
```

**Recommended Row 1 (0 rpm):**
```
100.3, 122.7, 123.7, 124.8, 126.9, 128.0, 129.1, 130.1,
100.3, 128.0, 124.8, 134.4, 134.4, 134.4, 134.4, 134.4,
100.3, 128.0, 128.0, 134.4, 140.0, 140.0, 140.0, 140.0,  ← Reduced from 169.6
100.3, 128.0, 128.0, 134.4, 140.0, 140.0, 140.0, 150.0   ← Reduced from 199.5
```

**Recommended Row 2 (2800 rpm):**
```
100.3, 122.7, 123.7, 124.8, 126.9, 128.0, 129.1, 130.1,
100.3, 128.0, 124.8, 134.4, 134.4, 134.4, 134.4, 134.4,
100.3, 128.0, 128.0, 134.4, 150.0, 150.0, 150.0, 150.0,  ← Reduced from 169.6
100.3, 128.0, 128.0, 134.4, 150.0, 150.0, 150.0, 160.0   ← Reduced from 199.5
```

### 6.2 Wastegate Base Duty Adjustments

**File:** `wg_base`

**Current Row 1 (0 rpm):**
```
0.0, 80.5, 80.5, 80.5, 80.5, 80.5, 80.5, 80.5
```

**Recommended Row 1 (0 rpm):**
```
10.0, 85.0, 85.0, 85.0, 85.0, 85.0, 85.0, 85.0  ← Increased base duty
```

### 6.3 Overboost Step Adjustments

**File:** `wg_overboost_step`

**Current:**
```
8.6, 5.5, 3.9, 3.1
```

**Recommended:**
```
12.0, 8.0, 5.0, 3.5  ← More aggressive response
```

### 6.4 Underboost Step Adjustments

**File:** `wg_underboost_step`

**Current:**
```
2.7, 1.2, 0.4, 0.0
```

**Recommended:**
```
5.0, 2.5, 1.0, 0.5  ← More aggressive response
```

---

## 7. VERIFICATION PROCEDURE

After implementing changes:

1. **Data Logging Requirements:**
   - Log multiple WOT pulls from 2000-6000 RPM
   - Include partial throttle boost building scenarios
   - Monitor boost error, wastegate duty, and fuel trims

2. **Success Criteria:**
   - Boost error at low RPM (0-3000): <10 kPa (currently 67.43 kPa)
   - Boost error at mid-high RPM (3000+): <5 kPa absolute
   - STFT std dev: <4.0% (currently 5.48%)
   - No overboost events >10 kPa
   - Wastegate duty cycle responsive and within 10-80% range

3. **Safety Checks:**
   - Verify boost does not exceed `boost_limit` values
   - Monitor for knock events
   - Verify IAM remains stable (should be 0.50-1.00)

---

## 8. NOTES

- All recommendations are based on analysis of the provided datalog
- Changes should be implemented incrementally and verified with re-logging
- Boost control issues are the highest priority due to safety and performance implications
- Fuel trim is generally good but can be refined for better consistency
- Always verify changes on a safe test environment before aggressive driving

---

**End of Recommendations**

