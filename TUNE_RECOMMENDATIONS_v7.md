# Tune File Recommendations for v7_keith_edit.tune
## Based on Datalog Analysis: tuner_log_25-11-16_1653_pulls and cruise v7.csv

**Date**: Based on datalog from 2025-11-16  
**Tune File**: Keith Proseus_1999JDMSTI_DW740_VF28_21builtStroker_v7_keith_edit.tune  
**ECU Version**: 1.6.36.2

---

## Executive Summary

Overall, the tune appears to be **safe and functional**, but there are opportunities for optimization. Key findings:

- ✅ **No knock detected** - IAM stable at 0.88 (88%), no knock retard events observed
- ✅ **Fuel mixture is safe** - Very rich (0.7-0.8 λ) in high-load areas, providing good safety margin
- ⚠️ **Boost control shows some inconsistency** - Some areas of underboost and occasional overboost
- ✅ **Spark timing is conservative** - Good safety margin at high loads (18-30°)
- ⚠️ **Potentially overly rich** - Lambda may be richer than necessary, reducing power potential

---

## 1. FUEL DELIVERY ANALYSIS

### Current State:
- **Power Mode Lambda Targets** (`pe_initial`, `pe_safe`): Range 0.667-0.892 λ
- **Actual Lambda in Datalog**: 0.699-0.797 λ at high load (1.4-1.8 g/rev)
- **Fuel Base Table**: 60.2-87.5% (rich correction)

### Findings:

#### 1.1 Power Enrichment Lambda May Be Overly Conservative

**Observation**: Lambda values at high load are consistently 0.70-0.80, which is very rich. While safe, this may be leaving power on the table.

**Example from Datalog (lines 3000-3016)**:
- Load: 1.52-1.81 g/rev
- Lambda: 0.711-0.742 λ
- RPM: 6341-7470 rpm
- Spark: 18-30°
- No knock detected

**Recommendation**: 
- Consider leaning out PE lambda targets by **2-3%** in high-load, high-RPM regions (load > 1.5 g/rev, RPM > 5000)
- Current `pe_initial` values of 0.667-0.736 at high load could be adjusted to 0.685-0.755 λ
- Target lambda of **0.78-0.82 λ** is typically ideal for power on pump gas while maintaining safety
- **Conservative approach**: Make small incremental changes (2% per revision) and re-log to verify no knock appears

**Specific Areas to Adjust**:
- RPM rows 11-16 (4800-6800 rpm) at load columns 12-16 (1.48-2.74 g/rev)
- Current values: 0.667-0.734 λ
- Recommended: 0.685-0.752 λ (2-3% leaner)

#### 1.2 Fuel Base Table Consistency

**Observation**: The `fuel_base` table shows values from 60.2% to 87.5%, indicating significant enrichment across the map.

**Recommendation**: 
- Review if the base fuel correction table needs this much enrichment
- Values below 85% suggest substantial tuning offset
- Ensure this is intentional and not masking another calibration issue (MAF scale, injector calibration, etc.)

---

## 2. BOOST CONTROL ANALYSIS

### Current State:
- **Boost Target Table** (`boost_target`): 60.8-199.5 kPa
- **Boost Limit** (`boost_limit`): 141.9-234.7 kPa by RPM
- **Wastegate Control**: Active duty cycle control enabled

### Findings:

#### 2.1 Boost Target vs Actual Boost Performance

**Observation from Datalog**:
- Line 15599: Target 197.3 kPa, Actual ~97 kPa (significant underboost at low RPM/high throttle)
- Lines 3000-3016: Target 153-172 kPa, Actual 134-187 kPa (some overboost reaching ~187 kPa vs 172 kPa target)

**Issues Identified**:

1. **Underboost at Low RPM/High Load**:
   - At 2006 rpm with 1.02 g/rev load: Target 197.3 kPa, Actual ~97 kPa
   - This is a significant discrepancy - likely wastegate opening too early or boost target too aggressive for that condition

2. **Overboost in High-RPM Pulls**:
   - Actual boost reaching 187 kPa when target is 172 kPa (~8.7% overboost)
   - Boost limit is 234.7 kPa, so not dangerous, but indicates control system struggling

**Recommendations**:

#### 2.1.1 Adjust Wastegate Base Duty

**Current**: `wg_base` shows 0.0% to 80.5% with 0.0% at low RPM/TPS

**Recommendation**:
- Increase `wg_base` duty cycle at low RPM (rows 1-3, 0-3000 rpm) and high TPS to improve boost response
- Current low RPM values may be allowing wastegate to open too easily

#### 2.1.2 Review Boost Target Table

**Recommendation**:
- Review boost targets at low RPM/high TPS combinations
- Line 15599 shows boost target of 197.3 kPa at ~2000 rpm - this seems unrealistic
- Consider reducing targets below 3000 rpm to more realistic values (140-160 kPa range)
- The current target table may be calling for boost levels the turbo cannot achieve at low RPM

#### 2.1.3 Wastegate Control Parameters

**Current Settings**:
- `wg_overboost_step`: 4.3, 2.7, 2.0, 1.6%
- `wg_underboost_step`: 2.7, 1.2, 0.4, 0.0%
- `wg_update_interval`: 120 ms

**Recommendations**:
- The underboost step at smallest error (0.0%) may be too small - consider increasing to 0.8-1.2%
- Overboost steps seem appropriately aggressive
- Consider if 120 ms update interval is sufficient for transient response

---

## 3. SPARK TIMING ANALYSIS

### Current State:
- **Base Spark MT**: Up to 48° advance at mid-load
- **High-Load Timing**: 18-30° at loads > 1.4 g/rev
- **IAM**: Stable at 0.88 (88%)
- **No Knock Retard**: All datalog samples show 0.0° knock retard

### Findings:

#### 3.1 Spark Timing is Conservative (Good Safety Margin)

**Observation**: At high loads (1.4-1.8 g/rev), spark timing is 18-30°, which is quite conservative. IAM is stable at 88%, indicating no knock issues.

**Analysis**:
- Conservative timing provides good safety margin
- However, there may be opportunity to add 1-2° of timing in specific areas without risk

**Recommendations**:

#### 3.1.1 Consider Small Timing Increases at High Load

**Conservative Approach**:
- Current high-load timing (1.5-1.8 g/rev, 5000-6800 rpm): 18-29°
- With IAM at 88% and no knock, could potentially add 1-2° of timing
- **Recommendation**: Add 1° in cells where:
  - Load: 1.4-1.8 g/rev
  - RPM: 4800-6400 rpm
  - Current timing < 26°

**Example Areas** (from `base_spark_mt`):
- Row 12 (5200 rpm), columns 12-16 (1.48-2.74 g/rev): Currently 14-17°, could go to 15-18°
- Row 13 (5600 rpm), columns 12-16: Currently 12-15°, could go to 13-16°
- Row 14 (6000 rpm), columns 12-16: Currently 11-14°, could go to 12-15°

**⚠️ Important**: Make changes incrementally (1° at a time) and re-log to verify no knock appears.

#### 3.1.2 Learned Spark Values

**Current**: `learned_spark_mt` shows values of 0-8° in various cells, with 8° being the maximum.

**Observation**: With IAM at 88%, the learned spark system has room to add timing, but learned values are already at maximum in some areas.

**Recommendation**: 
- Monitor learned spark values after timing increases
- If learned spark hits 8° maximum consistently, consider if timing can be increased in base tables
- The fact that IAM is 88% (not 100%) suggests the ECU has detected some knock activity historically, so be conservative

---

## 4. KNOCK DETECTION SYSTEM

### Current State:
- **Knock Retard Attack**: -4.0° per event (very aggressive)
- **Knock Retard Decay**: 0.1° per recovery (slow recovery)
- **Knock Retard Max**: -8.0°
- **IAM**: 0.88 (88%)

### Findings:

#### 4.1 IAM at 88% Indicates Previous Knock Activity

**Observation**: IAM is stable at 0.88 (88%) throughout the datalog. This means:
- IAM started at 0.50 (50%) per `iam_init`
- IAM has increased to 88%, indicating the engine has proven largely knock-free
- IAM has not reached 100%, suggesting some knock activity may have occurred previously

**Analysis**:
- The aggressive knock retard attack (-4.0°) and slow decay (0.1°) are working as designed
- The fact that IAM recovered to 88% is positive
- Current settings provide good protection

**Recommendation**:
- **No changes needed** to knock detection settings at this time
- Continue monitoring IAM - if it recovers to 95-100% over time, indicates the tune is very safe
- If IAM drops below 80%, investigate spark timing in areas where IAM decreased

---

## 5. BOOST VS LOAD RELATIONSHIP

### Finding:

#### 5.1 Load Limits May Be Limiting Performance

**Current**: `load_max` is set to 5.00 g/rev across all RPM (constant)

**Observation from Datalog**:
- Maximum load observed: ~1.83 g/rev (line 3019)
- Engine is well below the 5.00 g/rev limit
- This suggests the limit is not restrictive, which is good

**Recommendation**:
- **No changes needed** - load limits are appropriate for the application

---

## 6. TEMPERATURE CONDITIONS

### Findings:

#### 6.1 Intake Air Temperature (IAT)

**From Datalog**:
- IAT ranges: 22-47°C during pulls
- Boost target IAT compensation is enabled but table values are all 0.0% (disabled)
- Wastegate IAT compensation is active with values from -29.7% to 1.6%

**Observation**: IAT compensation is active for wastegate but not for boost targets.

**Recommendation**:
- Consider if boost targets should be reduced at high IAT
- With IAT compensation disabled in boost targets but active in wastegate, there may be inconsistency
- At IAT > 35°C, consider reducing boost targets by 3-5% to protect from heat soak

#### 6.2 Coolant Temperature

**From Datalog**:
- ECT ranges: 83-97°C during pulls
- Temperatures are in normal operating range
- No issues observed

---

## 7. PRIORITY RECOMMENDATIONS

### High Priority:

1. **Fix Underboost Issue at Low RPM** (Line 15599)
   - Review boost target table at low RPM (< 3000 rpm) / high TPS
   - Target of 197.3 kPa at ~2000 rpm is unrealistic
   - Adjust targets to 140-160 kPa range below 3000 rpm
   - Adjust wastegate base duty to improve boost response

2. **Address Overboost in High-RPM Pulls**
   - Actual boost reaching 187 kPa vs 172 kPa target
   - Increase wastegate duty cycle in high RPM/high TPS areas
   - May need to increase `wg_max` values at high RPM

### Medium Priority:

3. **Optimize Fuel Mixture (Conservative Lean-Out)**
   - Current lambda 0.70-0.80 is very rich
   - Consider leaning PE targets by 2-3% in high-load areas
   - Target lambda of 0.78-0.82 for better power
   - Make changes incrementally (2% per revision)

4. **Explore Small Spark Timing Increases**
   - IAM at 88% with no knock suggests room for 1-2° more timing
   - Focus on 4800-6400 rpm, 1.4-1.8 g/rev areas
   - Incremental approach: 1° changes, re-log, verify

### Low Priority:

5. **Review Boost Target IAT Compensation**
   - Currently disabled (all 0.0%)
   - May want to add small compensation at high IAT (> 35°C)

---

## 8. SPECIFIC TABLE ADJUSTMENTS

### 8.1 Boost Target Table (`boost_target`)

**Issue**: Unrealistic targets at low RPM

**Recommended Changes**:
- Row 1 (0 rpm): Keep as is (baseline)
- Row 2 (2800 rpm), columns 5-8 (high TPS): Reduce from 181-199 kPa to 140-160 kPa
- Row 3 (2900 rpm), columns 5-8: Reduce from 184-199 kPa to 145-165 kPa  
- Row 4 (3000 rpm), columns 5-8: Reduce from 170-199 kPa to 150-170 kPa

**Rationale**: Turbochargers typically cannot build high boost at low RPM due to limited exhaust energy. Setting realistic targets will improve boost control system response.

### 8.2 Wastegate Base Duty (`wg_base`)

**Issue**: Low duty at low RPM may cause underboost

**Recommended Changes**:
- Row 2 (2800 rpm), columns 2-8: Increase from 7.0-50.0% to 10.0-55.0%
- Row 3 (2900 rpm), columns 2-8: Increase from 7.0-50.0% to 12.0-58.0%
- Row 4 (3000 rpm), columns 2-8: Increase from 7.0-50.0% to 15.0-60.0%

**Rationale**: Higher wastegate duty at low RPM will keep wastegate closed longer, allowing boost to build more quickly.

### 8.3 Power Enrichment Initial Lambda (`pe_initial`)

**Issue**: Overly rich mixture leaving power on table

**Recommended Changes** (2% leaner, conservative approach):
- Rows 11-16 (4800-6800 rpm), columns 12-16 (1.48-2.74 g/rev)
- Example: Row 12 (5200 rpm), column 15 (2.24 g/rev): Change from 0.667 to 0.680 λ
- Row 13 (5600 rpm), column 15: Change from 0.667 to 0.680 λ
- Row 14 (6000 rpm), column 15: Change from 0.667 to 0.685 λ

**General Rule**: Increase lambda values by 0.013-0.020 λ (2-3% leaner) in high-load areas

**⚠️ Important**: Make these changes incrementally and re-log. Monitor for:
- Knock retard appearing
- IAM dropping below 85%
- EGTs increasing significantly

### 8.4 Base Spark MT (`base_spark_mt`)

**Issue**: Conservative timing with good safety margin - potential for small increases

**Recommended Changes** (add 1° timing, very conservative):
- Row 12 (5200 rpm), columns 12-16: Add 1° (e.g., 14-17° → 15-18°)
- Row 13 (5600 rpm), columns 12-16: Add 1° (e.g., 12-15° → 13-16°)
- Row 14 (6000 rpm), columns 12-16: Add 1° (e.g., 11-14° → 12-15°)

**⚠️ Important**: After timing increase, monitor for:
- Knock retard appearing
- IAM dropping
- If IAM stays stable at 88% or increases, can consider another 1° increase after extended logging

---

## 9. TESTING PROTOCOL

### After Making Adjustments:

1. **Data Logging Requirements**:
   - Perform multiple 3rd-4th gear pulls from 2500-7000 rpm
   - Log during various temperature conditions (cold start, warm, heat soaked)
   - Include both steady-state and transient (tip-in) events

2. **Key Parameters to Monitor**:
   - Knock Retard (°) - Should remain at 0.0°
   - IAM (Ignition Advance Multiplier) - Should remain ≥ 0.85 (ideally ≥ 0.88)
   - Actual vs Target Boost - Should be within ±5 kPa
   - Lambda - Should be 0.75-0.82 at high load
   - EGT (if available) - Should remain safe
   - Spark Timing - Verify it's following tables correctly

3. **Success Criteria**:
   - No knock retard events
   - IAM stable or increasing toward 1.00
   - Boost within ±5 kPa of target
   - Lambda in target range
   - Engine smooth operation

4. **Failure Criteria (Revert Changes)**:
   - Knock retard > 0.0° appears consistently
   - IAM drops below 0.80
   - Overboost > 10 kPa above target
   - Engine runs rough or shows signs of detonation

---

## 10. CAUTIONS AND WARNINGS

⚠️ **IMPORTANT SAFETY NOTES**:

1. **Incremental Changes Only**: Make ONE type of change at a time (e.g., only fuel OR only spark, not both simultaneously)

2. **Conservative Approach**: The current tune is safe. All recommendations are for optimization, not fixing critical issues.

3. **Monitor Closely**: After any change, extensive data logging is required before considering additional changes.

4. **Lambda Safety**: Do not lean out fuel mixture below 0.75 λ at high load without careful consideration. Current 0.70-0.80 range is very safe.

5. **Timing Safety**: Do not add more than 2° of timing without confirming IAM stability over multiple logging sessions.

6. **Boost Control**: Fix the low RPM boost target issue first before optimizing other areas.

---

## 11. SUMMARY OF RECOMMENDED CHANGES

### Immediate Actions:

1. **Fix Boost Target at Low RPM** (High Priority)
   - Reduce boost targets below 3000 rpm to realistic values (140-160 kPa)
   - Addresses underboost issue

2. **Increase Wastegate Duty at Low RPM** (High Priority)
   - Improve boost response and reduce underboost

### Optimization Actions (After Low-RPM Boost Fix):

3. **Conservative Fuel Leaning** (Medium Priority)
   - Lean PE targets by 2-3% in high-load areas
   - Target lambda 0.78-0.82 instead of 0.70-0.80

4. **Small Timing Increase** (Medium Priority)
   - Add 1° timing in high-load, mid-RPM areas
   - Monitor IAM and knock closely

### Future Considerations:

5. **Boost Target IAT Compensation**
   - Consider adding compensation at high IAT

---

## 12. NOTES ON DATALOG INTERPRETATION

### Positive Indicators:
- ✅ IAM stable at 0.88 (good safety margin from 1.00)
- ✅ No knock retard events
- ✅ Lambda rich enough to prevent detonation
- ✅ Spark timing conservative
- ✅ ECT and IAT in normal ranges

### Areas for Improvement:
- ⚠️ Boost control inconsistency (underboost at low RPM, slight overboost at high RPM)
- ⚠️ Fuel mixture potentially overly rich (optimization opportunity)
- ⚠️ Spark timing has room for small increases (optimization opportunity)

### Overall Assessment:
The tune is **safe and functional** but has opportunities for **power optimization** through conservative adjustments to fuel mixture and spark timing. The boost control issues should be addressed first to ensure consistent boost delivery.

---

**End of Recommendations**










