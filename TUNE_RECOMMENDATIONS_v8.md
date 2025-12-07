# Tune File Recommendations for v8.tune
## Based on Datalog Analysis: tuner_log_25-11-27_1038_V8.csv

**Date**: Based on datalog from 2025-11-27  
**Tune File**: Keith Proseus_1999JDMSTI_DW740_VF28_21builtStroker_v8.tune  
**ECU Version**: 1.6.38.0

---

## Executive Summary

Overall, the tune shows **significant boost control issues at low-mid RPM** and **very rich fueling** that may be limiting power. Key findings:

- ⚠️ **Severe underboost at low-mid RPM** - Actual boost 40-50% below target (98-106 kPa actual vs 189-199 kPa target)
- ✅ **Better boost control at higher RPM** - Boost targets more realistic, actual boost closer to target
- ⚠️ **Very rich fuel mixture** - Lambda 0.69-0.77 at high load (targets 0.75-0.82), leaving power potential on the table
- ✅ **No knock detected** - IAM stable at 0.62-1.00, no knock retard events observed
- ✅ **Spark timing conservative** - Good safety margin at high loads

---

## 1. BOOST CONTROL ANALYSIS

### Current State:
- **Boost Target Table** (`boost_target`): 100.3-199.5 kPa
- **Wastegate Base Duty** (`wg_base`): 0.0-80.5%
- **Wastegate Max Duty** (`wg_max`): 10.2-90.6%

### Critical Issues Identified:

#### 1.1 Severe Underboost at Low-Mid RPM

**Observation from Datalog (lines 10112-10114)**:
- **Line 10112**: 
  - RPM: 3470, Load: 1.02 g/rev
  - Boost Target: **189.9 kPa**
  - Actual MAP: **98.1 kPa**
  - **Underboost: 48.3% below target** (91.8 kPa error)
  - Wastegate Duty: 43.8%

- **Line 10113**:
  - RPM: 4001, Load: 1.12 g/rev
  - Boost Target: **189.9 kPa**
  - Actual MAP: **105.9 kPa**
  - **Underboost: 44.2% below target** (84.0 kPa error)
  - Wastegate Duty: 43.8%

- **Line 10114**:
  - RPM: 4540, Load: 1.20 g/rev
  - Boost Target: **199.5 kPa**
  - Actual MAP: **105.2 kPa**
  - **Underboost: 47.3% below target** (94.3 kPa error)
  - Wastegate Duty: 50.0%

**Root Cause Analysis**:
1. **Unrealistic boost targets** - The tune requests 189-199 kPa at 3000-4500 RPM, which is physically impossible for most turbochargers at these RPMs
2. **Insufficient wastegate base duty** - At low RPM (row 2-4), `wg_base` shows 0.0% at low TPS, only reaching 7.0-50.0% at higher TPS
3. **Turbo lag** - The VF28 turbo cannot build high boost quickly at low RPM due to limited exhaust energy

**Recommendations**:

1. **Reduce Boost Targets at Low-Mid RPM** (HIGH PRIORITY):
   - Row 2 (2800 rpm), columns 5-8: Reduce from 123.7-139.7 kPa to **110-125 kPa**
   - Row 3 (2900 rpm), columns 5-8: Reduce from 148.3-139.7 kPa to **120-135 kPa**
   - Row 4 (3000 rpm), columns 5-8: Reduce from 150.4-160.0 kPa to **130-145 kPa**
   - Row 5 (3100 rpm), columns 5-8: Reduce from 169.6-180.3 kPa to **140-155 kPa**
   - Row 6 (3300 rpm), columns 5-8: Reduce from 199.5 kPa to **150-165 kPa**

2. **Increase Wastegate Base Duty at Low RPM** (HIGH PRIORITY):
   - Row 2 (2800 rpm), columns 2-8: Increase from 7.0-50.0% to **15.0-60.0%**
   - Row 3 (2900 rpm), columns 2-8: Increase from 7.0-50.0% to **18.0-65.0%**
   - Row 4 (3000 rpm), columns 2-8: Increase from 7.0-50.0% to **20.0-70.0%**
   - Row 5 (3100 rpm), columns 2-8: Increase from 7.0-50.0% to **22.0-75.0%**

**Rationale**: Higher wastegate duty keeps the wastegate closed longer, allowing boost to build. Realistic boost targets prevent the control system from chasing impossible goals.

#### 1.2 Boost Control at Higher RPM

**Observation from Datalog (lines 10200-10250)**:
- RPM: 4300-4600, Load: 1.44-1.80 g/rev
- Boost Target: 145-162 kPa
- Actual MAP: 128-161 kPa
- **Boost control much better** - Actual boost within 5-10% of target

**Analysis**: At higher RPM with more realistic targets (145-162 kPa), boost control is significantly better. This confirms that the low-RPM targets are the primary issue.

---

## 2. FUEL DELIVERY ANALYSIS

### Current State:
- **Power Mode Lambda Targets** (`pe_initial`): Range 0.749-1.000 λ
- **Actual Lambda in Datalog**: 0.688-0.773 λ at high load (1.4-1.8 g/rev)
- **Fuel Base Table** (`fuel_base`): 60.2-87.5% (calibrated for higher flow injectors)
- **Open Loop Mode**: At high loads, ECU operates in open loop (PE mode), so actual lambda should match target lambda

### Critical Finding:

#### 2.1 Base Fuel Table Needs Correction for Lambda Accuracy

**Observation from Datalog (lines 10200-10250)**:
- Load: 1.44-1.80 g/rev
- RPM: 4300-4600
- Lambda Target: 0.749-0.820 λ (from `pe_initial` table)
- Actual Lambda: **0.688-0.773 λ**
- **Actual lambda is consistently richer than target** - indicating `fuel_base` table needs adjustment

**Example Data Points with Fuel Base Values**:
- Line 10200: Target 0.793 λ, Actual 0.773 λ, Fuel Base 0.773 (77.3%) - **2.5% rich**
- Line 10205: Target 0.749 λ, Actual 0.750 λ, Fuel Base 0.797 (79.7%) - **on target** ✓
- Line 10206: Target 0.749 λ, Actual 0.711 λ, Fuel Base 0.797 (79.7%) - **5.1% rich**
- Line 10213: Target 0.749 λ, Actual 0.703 λ, Fuel Base 0.812 (81.2%) - **6.1% rich**
- Line 10238: Target 0.749 λ, Actual 0.688 λ, Fuel Base 0.820 (82.0%) - **8.1% rich**

**Analysis**:
1. **In open loop mode (PE enabled), actual lambda should match target lambda**
2. The `fuel_base` table is already calibrated for higher flow injectors (values 60-87% vs 100%)
3. **Higher fuel_base values = more fuel = richer mixture**
4. **Lower fuel_base values = less fuel = leaner mixture**
5. Since actual lambda is richer than target, we need to **decrease fuel_base values** to lean out the mixture
6. The correction formula: `New fuel_base = Current fuel_base × (Actual λ / Target λ)`

**Root Cause**: The `fuel_base` table at high load/RPM areas is too high, causing the mixture to run rich compared to the PE lambda targets.

**Recommendations** (HIGH PRIORITY):

1. **Adjust Fuel Base Table for Lambda Accuracy**:
   - At high loads (1.48-2.02 g/rev) and RPM 4000-5000, **decrease** `fuel_base` values by 3-6%
   - This will lean out the mixture to match PE lambda targets
   - Formula: `New fuel_base = Current fuel_base × (Actual λ / Target λ)`

**Specific Areas to Adjust** (based on datalog analysis):
- **RPM Row 10 (4000 rpm), Load Columns 11-13 (1.48-2.02 g/rev)**:
  - Current: 78.1-84.4%
  - Recommended: Increase by 3-6% to **81-89%** (to correct 0.711-0.773 λ actual vs 0.749-0.793 λ target)
  
- **RPM Row 11 (4400 rpm), Load Columns 11-13 (1.48-2.02 g/rev)**:
  - Current: 79.7-84.4%
  - Recommended: Increase by 5-8% to **84-91%** (to correct 0.703-0.750 λ actual vs 0.749 λ target)

- **RPM Row 12 (4800 rpm), Load Columns 11-13 (1.48-2.02 g/rev)**:
  - Current: 80.5-86.7%
  - Recommended: Increase by 3-6% to **83-92%** (to match PE targets)

**Calculation Example**:
- Line 10206: Target 0.749, Actual 0.711, Current fuel_base 0.797
- Correction: 0.797 × (0.749 / 0.711) = 0.797 × 1.0535 = **0.840 (84.0%)**
- Line 10213: Target 0.749, Actual 0.703, Current fuel_base 0.812
- Correction: 0.812 × (0.749 / 0.703) = 0.812 × 1.0654 = **0.865 (86.5%)**

**Note**: After correcting `fuel_base` for lambda accuracy, the PE lambda targets can be optimized separately if desired for power tuning.

---

## 3. SPARK TIMING ANALYSIS

### Current State:
- **Base Spark Timing** (`base_spark_mt`): 13-44° at high load
- **IAM**: 0.62-1.00 (stable, no knock events)
- **Knock Retard**: 0.0° (no knock detected)

### Findings:

#### 3.1 Conservative Timing with Room for Optimization

**Observation from Datalog**:
- IAM stable at 0.62-1.00 with no knock events
- Spark timing: 13-33° at high load (1.4-1.8 g/rev)
- No knock retard events observed

**Analysis**: The conservative timing and rich fuel mixture provide excellent safety margin. With IAM at 0.62-1.00 and no knock, there may be room for small timing increases, but this should be done **after** fixing boost control and optimizing fuel mixture.

**Recommendations** (LOW PRIORITY - after boost and fuel fixes):
- Consider adding 1-2° timing in high-load, mid-RPM areas (4800-6000 rpm, 1.4-1.8 g/rev)
- Monitor IAM and knock closely
- Make changes incrementally (1° per revision)

---

## 4. PRIORITY RECOMMENDATIONS

### High Priority (Address First):

1. **Fix Severe Underboost at Low-Mid RPM**
   - Reduce boost targets at 2800-3300 rpm to realistic values (110-165 kPa)
   - Increase wastegate base duty at low RPM (15-75% range)
   - This will improve boost response and reduce boost error significantly

2. **Verify Boost Control After Changes**
   - Re-log after boost target adjustments
   - Verify actual boost matches targets within 5-10%
   - Adjust wastegate duty if needed

### Medium Priority (After Boost Fix):

3. **Optimize Fuel Mixture (Conservative Lean-Out)**
   - Lean PE targets by 2-3% in high-load areas
   - Target lambda of 0.78-0.82 for better power
   - Make changes incrementally (2% per revision)
   - Monitor for knock after each change

### Low Priority (After Fuel Optimization):

4. **Explore Small Spark Timing Increases**
   - IAM at 0.62-1.00 with no knock suggests room for 1-2° more timing
   - Focus on 4800-6000 rpm, 1.4-1.8 g/rev areas
   - Incremental approach: 1° changes, re-log, verify

---

## 5. SPECIFIC TABLE ADJUSTMENTS

### 5.1 Boost Target Table (`boost_target`)

**Current Values** (RPM rows 2-6, TPS columns 5-8):
- Row 2 (2800 rpm): 123.7, 124.8, 126.9, 128.0, 129.1, 130.1
- Row 3 (2900 rpm): 123.7, 148.3, 139.7, 139.7, 139.7, 139.7
- Row 4 (3000 rpm): 125.9, 148.3, 150.4, 160.0, 160.0, 160.0
- Row 5 (3100 rpm): 128.0, 149.3, 150.4, 169.6, 180.3, 180.3
- Row 6 (3300 rpm): 100.3, 149.3, 151.5, 169.6, 199.5, 199.5

**Recommended Changes**:
- Row 2 (2800 rpm), columns 5-8: **110.0, 115.0, 120.0, 125.0** (reduced from 126.9-130.1)
- Row 3 (2900 rpm), columns 5-8: **120.0, 125.0, 130.0, 135.0** (reduced from 139.7)
- Row 4 (3000 rpm), columns 5-8: **130.0, 135.0, 140.0, 145.0** (reduced from 150.4-160.0)
- Row 5 (3100 rpm), columns 5-8: **140.0, 145.0, 150.0, 155.0** (reduced from 169.6-180.3)
- Row 6 (3300 rpm), columns 5-8: **145.0, 150.0, 155.0, 165.0** (reduced from 169.6-199.5)

**Rationale**: Realistic boost targets that the turbo can actually achieve will improve boost control system response and reduce boost error.

### 5.2 Wastegate Base Duty (`wg_base`)

**Current Values** (RPM rows 2-5, TPS columns 2-8):
- Row 2 (2800 rpm): 0.0, 7.0, 14.5, 21.5, 28.5, 35.5, 43.0, 50.0
- Row 3 (2900 rpm): 0.0, 7.0, 14.5, 21.5, 28.5, 35.5, 43.0, 50.0
- Row 4 (3000 rpm): 0.0, 7.0, 14.5, 21.5, 28.5, 35.5, 43.0, 50.0
- Row 5 (3100 rpm): 0.0, 7.0, 14.5, 21.5, 28.5, 35.5, 43.0, 50.0

**Recommended Changes**:
- Row 2 (2800 rpm), columns 2-8: **0.0, 15.0, 22.0, 30.0, 38.0, 46.0, 54.0, 60.0**
- Row 3 (2900 rpm), columns 2-8: **0.0, 18.0, 25.0, 33.0, 41.0, 49.0, 57.0, 65.0**
- Row 4 (3000 rpm), columns 2-8: **0.0, 20.0, 28.0, 36.0, 44.0, 52.0, 60.0, 70.0**
- Row 5 (3100 rpm), columns 2-8: **0.0, 22.0, 30.0, 38.0, 46.0, 54.0, 62.0, 75.0**

**Rationale**: Higher wastegate duty at low RPM keeps the wastegate closed longer, allowing boost to build more quickly and reach targets.

### 5.3 Fuel Base Table (`fuel_base`)

**Current Values** (RPM rows 10-12, Load columns 11-13):
- Row 10 (4000 rpm), columns 11-13: 78.1, 79.7, 81.2
- Row 11 (4400 rpm), columns 11-13: 80.5, 84.4, 84.4
- Row 12 (4800 rpm), columns 11-13: 86.7, 84.4, 84.4

**Recommended Changes** (based on lambda error correction):
- Row 10 (4000 rpm), columns 11-13: **75.0, 79.0, 79.0** (decreased from 78.1, 79.7, 81.2)
- Row 11 (4400 rpm), columns 11-13: **76.0, 80.0, 80.0** (decreased from 80.5, 84.4, 84.4)
- Row 12 (4800 rpm), columns 11-13: **81.0, 79.0, 79.0** (decreased from 86.7, 84.4, 84.4)

**Rationale**: In open loop mode, actual lambda must match target lambda. The current fuel_base values are too high, causing rich mixtures. Decreasing fuel_base by 3-6% will lean out the mixture to match PE lambda targets.

**Calculation Method**:
- For each datalog point: `New fuel_base = Current fuel_base × (Actual λ / Target λ)`
- Average corrections across similar RPM/load ranges
- Example: Target 0.749, Actual 0.711, Current 0.797 → New = 0.797 × (0.711/0.749) = 0.757

**Note**: After correcting `fuel_base` for lambda accuracy, PE lambda targets can be optimized separately if desired for power tuning. The current PE targets (0.749-0.820 λ) are appropriate for safety; the issue was the fuel_base table not delivering the correct fuel quantity to achieve those targets.

**Note**: The PE lambda targets (0.749-0.820 λ) are appropriate for safety. **The primary issue was the fuel_base table not delivering the correct fuel quantity to achieve those targets.** After correcting fuel_base for lambda accuracy, these PE targets can be optimized separately if desired for power tuning.

**Optional Optimization** (After fuel_base correction is verified):
- If lambda accuracy is good after fuel_base correction, consider leaning PE targets by 2-3% for power optimization
- Target lambda of 0.78-0.82 λ for optimal power on pump gas
- Make changes incrementally and monitor for knock

---

## 6. NOTES ON DATALOG INTERPRETATION

### Positive Indicators:
- ✅ IAM stable at 0.62-1.00 (good safety margin)
- ✅ No knock retard events
- ✅ Lambda rich enough to prevent detonation
- ✅ Spark timing conservative
- ✅ ECT and IAT in normal ranges (83°C ECT, 9-11°C IAT)

### Areas for Improvement:
- ⚠️ **Severe boost control issues** at low-mid RPM (40-50% underboost)
- ⚠️ **Fuel mixture potentially overly rich** (optimization opportunity)
- ⚠️ **Spark timing has room for small increases** (optimization opportunity, after boost/fuel fixes)

### Overall Assessment:
The tune is **safe** but has **significant boost control issues** that need to be addressed first. The very rich fuel mixture provides excellent safety but may be limiting power. After fixing boost control, conservative fuel and timing optimizations can be pursued.

---

## 7. IMPLEMENTATION ORDER

1. **Fix Boost Control** (Do First)
   - Reduce boost targets at low-mid RPM
   - Increase wastegate base duty
   - Re-log and verify boost control improvement

2. **Optimize Fuel Mixture** (After Boost Fix)
   - Lean PE targets by 2-3%
   - Re-log and verify no knock
   - Monitor lambda accuracy

3. **Optimize Spark Timing** (After Fuel Optimization)
   - Add 1-2° timing in safe areas
   - Monitor IAM and knock closely
   - Incremental approach

---

**End of Recommendations**

