# Exhaust Burble Tuning Guide
## Progressive Tuning Methodology for Subaru WRX STi EJ207

---

## 📋 TABLE OF CONTENTS
1. [Prerequisites & Safety](#prerequisites--safety)
2. [Understanding Burble Mechanics](#understanding-burble-mechanics)
3. [Tuning Strategy Overview](#tuning-strategy-overview)
4. [Step-by-Step Tuning Process](#step-by-step-tuning-process)
5. [Fine-Tuning Parameters](#fine-tuning-parameters)
6. [Troubleshooting Guide](#troubleshooting-guide)
7. [Datalog Monitoring](#datalog-monitoring)
8. [Safety Limits & Red Flags](#safety-limits--red-flags)

---

## PREREQUISITES & SAFETY

### ⚠️ MANDATORY REQUIREMENTS

#### **1. Exhaust System**
- ✅ **REQUIRED**: Catless downpipe or test pipe
- ❌ **DO NOT PROCEED** if catalytic converters are installed
- **Why**: Unburned fuel will destroy catalytic converters within hours

#### **2. Monitoring Equipment**
- **REQUIRED**:
  - Wideband O2 sensor (AFR monitoring)
  - ECU datalogger capability
  - Laptop/tablet for real-time monitoring
- **HIGHLY RECOMMENDED**:
  - EGT (Exhaust Gas Temperature) sensor
  - EGT gauge or logging capability
  - Boost gauge

#### **3. Tuning Software**
- ECU flashing/tuning software compatible with your ROM
- Ability to edit and reflash tune files
- Backup of original/current tune file

#### **4. Testing Environment**
- Safe, empty road or private property
- Dry conditions (no rain/snow)
- Daylight visibility
- No traffic or pedestrians nearby

#### **5. Skills & Knowledge**
- Basic understanding of ECU tuning concepts
- Ability to recognize engine knock/detonation
- Experience with datalogging
- Understanding of AFR readings

---

## UNDERSTANDING BURBLE MECHANICS

### How Burbles Work

**Normal Deceleration:**
```
Throttle Closed → DFCO Activates → Fuel Cut → Silent Decel
```

**Burble Mode:**
```
Throttle Closed → Fuel Continues → Spark Retarded → Combustion in Exhaust → POP/BANG
```

### The Three Critical Elements

#### **1. Fuel Delivery (DFCO Control)**
- **Goal**: Keep fuel injecting during deceleration
- **Method**: Delay or disable DFCO (Deceleration Fuel Cut-Off)
- **Effect**: Unburned fuel enters exhaust system

#### **2. Ignition Timing (Spark Retard)**
- **Goal**: Ignite fuel late in combustion cycle
- **Method**: Heavily retard spark timing on closed throttle
- **Effect**: Combustion occurs as exhaust valves open
- **Key Range**: -10° to -30° retard creates burbles

#### **3. Air-Fuel Ratio (Mixture Control)**
- **Goal**: Rich mixture for reliable ignition
- **Method**: Enrich low-load fuel cells
- **Effect**: More unburned fuel = louder burbles
- **Target AFR**: 11.5:1 to 12.5:1 (λ 0.80-0.87)

---

## TUNING STRATEGY OVERVIEW

### Progressive Approach (Recommended)

**Phase 1: Foundation** → Enable basic burble conditions
**Phase 2: Refinement** → Adjust intensity and RPM range
**Phase 3: Optimization** → Fine-tune for best sound/safety balance
**Phase 4: Validation** → Extended testing and monitoring

### Tuning Philosophy

✅ **DO:**
- Start conservative, increase gradually
- Test one change at a time
- Monitor EGT constantly
- Log every test run
- Stop immediately if issues arise

❌ **DON'T:**
- Make multiple changes simultaneously
- Skip monitoring/datalogging
- Tune in traffic or unsafe conditions
- Ignore warning signs (knock, high EGT)
- Rush the process

---

## STEP-BY-STEP TUNING PROCESS

---

## PHASE 1: FOUNDATION SETUP

### **STAGE 1.1: Baseline Datalog**

**Objective**: Establish current behavior before modifications

**Steps:**
1. Load current tune into ECU
2. Configure datalogger to monitor:
   - RPM
   - TPS (Throttle Position)
   - Closed Throttle Flag (if available)
   - Vehicle Speed
   - AFR/Lambda
   - Fuel Injector Duty Cycle
   - Ignition Timing
   - Load (g/rev)
   - EGT (if equipped)

3. Perform test run:
   - Warm engine to operating temperature (80-90°C)
   - Accelerate to 4000 RPM in 2nd gear (50% throttle)
   - Lift throttle completely (closed throttle decel)
   - Coast down to 2000 RPM
   - Repeat 3-5 times

4. Review datalog:
   - Note RPM when DFCO activates (fuel duty drops to 0%)
   - Note AFR when DFCO active (should be >18:1 or "lean")
   - Note ignition timing during decel
   - Save this log as **"BASELINE_BEFORE_BURBLE.log"**

**Expected Baseline Observations:**
- DFCO activates at ~3000-3400 RPM (your current settings)
- AFR goes very lean (18:1+) when DFCO active
- Ignition timing advances on decel (normal operation)
- No exhaust pops/burbles

---

### **STAGE 1.2: DFCO Delay Configuration**

**Objective**: Delay fuel cut-off to allow burble window

**Files to Edit:**
- `dfco_delay`
- `dfco_delay_rpm`

**Current Values (from your v10 tune):**
```json
dfco_delay: "4, 4, 4, 0", "4, 4, 4, 0"
dfco_delay_rpm: "1600, 2400, 4000"
```

**Step-by-Step Changes:**

**Iteration 1.2a - Conservative Delay:**
```json
dfco_delay: "10, 10, 10, 5", "10, 10, 10, 5"
```
- **Effect**: Delays DFCO by ~1.2 seconds
- **Flash tune → Test → Datalog**
- **Expected**: Fuel continues longer on throttle lift

**Iteration 1.2b - Moderate Delay:**
```json
dfco_delay: "15, 15, 15, 10", "15, 15, 15, 10"
```
- **Effect**: Delays DFCO by ~1.8 seconds
- **Flash tune → Test → Datalog**
- **Expected**: Noticeable fuel flow during decel

**Iteration 1.2c - Aggressive Delay:**
```json
dfco_delay: "20, 20, 20, 15", "20, 20, 20, 15"
```
- **Effect**: Delays DFCO by ~2.4 seconds
- **Flash tune → Test → Datalog**
- **Expected**: Extended fuel delivery on decel

**Test Procedure for Each Iteration:**
1. Flash updated tune
2. Warm engine
3. Accelerate to 4000 RPM, lift throttle
4. Monitor datalog:
   - Does fuel injector duty stay above 0% longer?
   - Does AFR stay rich (12-14:1) longer during decel?
   - Note RPM where DFCO finally activates
5. Listen for any exhaust changes (may hear slight popping)

**Stop Criteria:**
- If engine stumbles/hesitates during decel
- If AFR goes excessively rich (<10:1)
- If EGT rises above 900°C

**Recommendation**: Start with **Iteration 1.2b (15 delay)** for most setups

---

### **STAGE 1.3: DFCO RPM Threshold Adjustment**

**Objective**: Raise RPM thresholds so DFCO activates only at lower RPM

**Files to Edit:**
- `dfco_enable_rpm_a`
- `dfco_enable_rpm_b`
- `dfco_disable_rpm`

**Current Values:**
```json
dfco_enable_rpm_a (row 1): "3400, 3400, 3400, 3275, 3150, 3000, 2925, 2900, 2750, 2550, 2475, 2325, 2100, 2100, 2100, 2100"
dfco_enable_rpm_a (row 2): "3700, 3700, 3700, 3575, 3450, 3300, 3225, 3200, 3050, 2750, 2675, 2475, 2250, 2250, 2250, 2250"
```

**Iteration 1.3a - Conservative Increase (+1000 RPM):**

Create new values by **adding 1000 to each value**:
```json
dfco_enable_rpm_a (row 1): "4400, 4400, 4400, 4275, 4150, 4000, 3925, 3900, 3750, 3550, 3475, 3325, 3100, 3100, 3100, 3100"
dfco_enable_rpm_a (row 2): "4700, 4700, 4700, 4575, 4450, 4300, 4225, 4200, 4050, 3750, 3675, 3475, 3250, 3250, 3250, 3250"

dfco_enable_rpm_b (row 1): "4100, 4100, 4100, 4000, 3875, 3750, 3650, 3600, 3475, 3250, 3150, 2700, 2300, 2300, 2300, 2300"
dfco_enable_rpm_b (row 2): "4400, 4400, 4400, 4300, 4175, 4050, 3950, 3900, 3775, 3450, 3300, 3050, 2700, 2700, 2700, 2700"

dfco_disable_rpm (row 1): "3900, 3900, 3900, 3800, 3675, 3550, 3450, 3400, 3275, 3050, 2700, 2500, 2100, 2100, 2100, 2100"
dfco_disable_rpm (row 2): "3900, 3900, 3900, 3800, 3675, 3550, 3450, 3400, 3275, 3050, 2700, 2500, 2100, 2100, 2100, 2100"
```

**Iteration 1.3b - Moderate Increase (+1500 RPM):**

Add 1500 to each original value:
```json
dfco_enable_rpm_a (row 1): "4900, 4900, 4900, 4775, 4650, 4500, 4425, 4400, 4250, 4050, 3975, 3825, 3600, 3600, 3600, 3600"
dfco_enable_rpm_a (row 2): "5200, 5200, 5200, 5075, 4950, 4800, 4725, 4700, 4550, 4250, 4175, 3975, 3750, 3750, 3750, 3750"
[...continue pattern...]
```

**Iteration 1.3c - Aggressive Increase (+2000 RPM):**

Add 2000 to each original value (maximum recommended):
```json
dfco_enable_rpm_a (row 1): "5400, 5400, 5400, 5275, 5150, 5000, 4925, 4900, 4750, 4550, 4475, 4325, 4100, 4100, 4100, 4100"
dfco_enable_rpm_a (row 2): "5700, 5700, 5700, 5575, 5450, 5300, 5225, 5200, 5050, 4750, 4675, 4475, 4250, 4250, 4250, 4250"

dfco_enable_rpm_b (row 1): "5100, 5100, 5100, 5000, 4875, 4750, 4650, 4600, 4475, 4250, 4150, 3700, 3300, 3300, 3300, 3300"
dfco_enable_rpm_b (row 2): "5400, 5400, 5400, 5300, 5175, 5050, 4950, 4900, 4775, 4450, 4300, 4050, 3700, 3700, 3700, 3700"

dfco_disable_rpm (row 1): "4900, 4900, 4900, 4800, 4675, 4550, 4450, 4400, 4275, 4050, 3700, 3500, 3100, 3100, 3100, 3100"
dfco_disable_rpm (row 2): "4900, 4900, 4900, 4800, 4675, 4550, 4450, 4400, 4275, 4050, 3700, 3500, 3100, 3100, 3100, 3100"
```

**Test Procedure:**
1. Flash updated tune with DFCO delay AND RPM threshold changes
2. Warm engine
3. Test at different RPM ranges:
   - Accelerate to 5000 RPM, lift throttle → Note when fuel cuts
   - Accelerate to 4000 RPM, lift throttle → Note when fuel cuts
   - Accelerate to 3000 RPM, lift throttle → Note when fuel cuts
4. Datalog should show:
   - Fuel continues flowing down to lower RPM than before
   - AFR stays in 12-14:1 range longer during decel
   - DFCO activates at lower RPM threshold

**Recommendation**: Start with **Iteration 1.3b (+1500 RPM)** for most setups

**⚠️ Warning Signs:**
- Engine bogs or stumbles during decel
- Excessive fuel smell (rich condition)
- Engine stalls when coming to stop
- Check engine light (lean/rich fault codes)

If any occur, reduce RPM increase by 500 RPM increments

---

### **STAGE 1.4: Initial Closed Throttle Spark Retard**

**Objective**: Introduce spark retard to create exhaust ignition

**File to Edit:**
- `closed_throttle_spark`

**Current Values:**
```json
"5.0, 5.0, 8.0, 12.0, 12.0, 12.0, 13.0, 14.0, 15.0, 16.0, 18.0, 22.0, 24.0, 28.0, 32.0, 36.0"
```

**RPM Index (for reference):**
```
800, 1200, 1600, 2000, 2400, 2800, 3200, 3600, 4000, 4400, 4800, 5200, 5600, 6000, 6400, 6800
```

**Understanding the Concept:**
- **Positive values** (current) = Spark advance BTDC (Before Top Dead Center)
- **Negative values** (burble mode) = Spark retard (delayed ignition)
- More negative = Later ignition = More burble intensity
- **Target zone**: 2000-5200 RPM (indices 3-11)

---

**Iteration 1.4a - Mild Retard (-10° to -12°):**

**Strategy**: Introduce modest retard in mid-range

```json
"5.0, 5.0, -10.0, -12.0, -12.0, -12.0, -12.0, -12.0, -12.0, -10.0, -10.0, -8.0, -6.0, -4.0, 0.0, 0.0"
```

**Breakdown by RPM:**
- 800-1200 RPM: Keep at 5° advance (idle stability)
- 1600 RPM: -10° retard (burble starts)
- 2000-4400 RPM: -12° retard (burble zone)
- 4800-5200 RPM: -10° to -8° (reduce for EGT)
- 5600-6800 RPM: -6° to 0° (minimize high-RPM retard)

**Expected Result**: Soft pops/burbles, subtle effect

---

**Iteration 1.4b - Moderate Retard (-15° to -18°):**

**Strategy**: Increase retard for noticeable burbles

```json
"5.0, 5.0, -15.0, -18.0, -18.0, -18.0, -18.0, -18.0, -18.0, -16.0, -14.0, -12.0, -10.0, -8.0, -4.0, 0.0"
```

**Breakdown by RPM:**
- 800-1200 RPM: 5° advance (idle)
- 1600-4400 RPM: -15° to -18° retard (strong burble zone)
- 4800-6000 RPM: -16° to -8° progressive reduction
- 6400-6800 RPM: -4° to 0° (minimal retard)

**Expected Result**: Distinct pops and crackles, clearly audible

---

**Iteration 1.4c - Aggressive Retard (-20° to -25°):**

**Strategy**: Maximum burble intensity

```json
"5.0, 5.0, -20.0, -25.0, -25.0, -25.0, -24.0, -22.0, -20.0, -18.0, -16.0, -14.0, -12.0, -10.0, -6.0, -4.0"
```

**Breakdown by RPM:**
- 800-1200 RPM: 5° advance (idle)
- 1600-3200 RPM: -20° to -25° retard (maximum burble)
- 3600-4800 RPM: -22° to -16° (aggressive but controlled)
- 5200-6800 RPM: -14° to -4° progressive reduction

**Expected Result**: LOUD pops, bangs, flames possible

⚠️ **WARNING**: High EGT risk - monitor closely!

---

**Iteration 1.4d - Custom "Sweet Spot" Tuning:**

**Strategy**: Target specific RPM range for optimal sound

**Example - Focus on 2500-4500 RPM:**
```json
"5.0, 5.0, -12.0, -18.0, -22.0, -24.0, -24.0, -22.0, -20.0, -16.0, -12.0, -8.0, -6.0, -4.0, 0.0, 0.0"
```

**Breakdown:**
- Peak burble at 2800-3200 RPM (-24°)
- Tapers off above and below
- Allows targeting specific gear/RPM scenarios

---

**Test Procedure for Each Iteration:**

1. **Flash tune** with DFCO settings + new spark timing
2. **Warm engine** to 80-90°C coolant temp
3. **Test run sequence:**

   **Test A - Low Speed (2nd gear, 2500-3500 RPM):**
   - Accelerate to 3500 RPM (30-40 mph)
   - Lift throttle completely
   - Coast down listening/monitoring
   - Note: Sound, AFR, EGT

   **Test B - Mid Speed (3rd gear, 3000-4500 RPM):**
   - Accelerate to 4500 RPM (50-60 mph)
   - Lift throttle completely
   - Coast down listening/monitoring
   - Note: Sound intensity, frequency

   **Test C - Higher Speed (3rd gear, 4000-5500 RPM):**
   - Accelerate to 5500 RPM (65-75 mph)
   - Lift throttle completely
   - Monitor EGT closely (danger zone!)
   - Note: Sound, heat buildup

4. **Datalog Analysis:**
   - Ignition timing drops to negative values ✓
   - AFR stays rich 11-13:1 during burbles ✓
   - EGT remains below 950°C ✓
   - No engine hesitation or stumble ✓

5. **Sound Evaluation:**
   - Rate burble intensity: 1-10 scale
   - Note frequency (pops per second)
   - Note tone (sharp pops vs deep rumbles)
   - Record audio/video for reference

**Recommendation Progression:**
- Day 1: Test **Iteration 1.4a** (mild -10/-12°)
- Day 2: If safe, test **Iteration 1.4b** (moderate -15/-18°)
- Day 3+: If desired, test **Iteration 1.4c** (aggressive -20/-25°)

**Never skip steps - progressive testing is critical for safety!**

---

### **STAGE 1.5: Closed Throttle Speed Limit Adjustment**

**Objective**: Allow burbles at higher vehicle speeds

**File to Edit:**
- `closed_throttle_spark_vss_max`

**Current Value:**
```json
"60" (km/h)
```

**Why This Matters:**
- Current setting limits closed throttle spark modifications to 60 km/h
- Burbles won't work above 60 km/h with current setting
- Most spirited driving occurs above 60 km/h

**Iteration 1.5a - Conservative (100 km/h):**
```json
"100"
```
- Allows burbles up to ~62 mph
- Safe for street use
- Limits highway burbles

**Iteration 1.5b - Moderate (150 km/h):**
```json
"150"
```
- Allows burbles up to ~93 mph
- Good for most street/backroad driving
- **RECOMMENDED** for street cars

**Iteration 1.5c - Aggressive (200 km/h):**
```json
"200"
```
- Allows burbles up to ~124 mph
- Track/unrestricted use
- Maximum flexibility

**Test Procedure:**
1. Flash tune with updated VSS limit
2. Test at progressively higher speeds:
   - 50 km/h decel test (baseline)
   - 80 km/h decel test (above old limit)
   - 120 km/h decel test (higher speeds)
3. Verify burbles occur at all speed ranges
4. Monitor for any speed-related issues

**Recommendation**: Start with **150 km/h** for street use

---

### **STAGE 1.6: Closed Throttle Coolant Compensation Removal**

**Objective**: Ensure spark retard applies regardless of coolant temp

**File to Edit:**
- `closed_throttle_spark_coolant_comp`

**Current Value:**
```json
"5.0, 5.0, 5.0, 5.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0"
```

**Problem**: These values ADD to closed throttle spark when engine is cold
- At cold temps, adds +5° reducing retard effectiveness
- Example: -20° retard becomes -15° when cold
- Burbles won't work properly until fully warmed up

**Solution - Zero Out Compensation:**
```json
"0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0"
```

**Effect**: 
- Spark retard applies consistently at all temps
- Burbles work from cold start
- More predictable behavior

**Test Procedure:**
1. Flash tune with zeroed compensation
2. Test cold start burbles (60-70°C coolant)
3. Test warm burbles (80-90°C coolant)
4. Verify consistent behavior at all temps

**Recommendation**: **Always zero out this compensation** for burble tunes

---

## 🎯 PHASE 1 COMPLETION CHECKLIST

Before proceeding to Phase 2, verify:

✅ **DFCO Settings Tuned:**
- [ ] DFCO delay increased (15-20 counts recommended)
- [ ] DFCO RPM thresholds raised (+1500-2000 RPM)
- [ ] Datalog confirms fuel continues during decel
- [ ] No engine stumbling or stalling

✅ **Spark Retard Configured:**
- [ ] Closed throttle spark retarded (-15° to -20° minimum)
- [ ] Tested at multiple RPM ranges
- [ ] Datalog confirms negative timing on decel
- [ ] Burbles audible and consistent

✅ **Supporting Parameters Adjusted:**
- [ ] VSS max increased (150+ km/h recommended)
- [ ] Coolant compensation zeroed
- [ ] Burbles work at all speeds and temps

✅ **Safety Monitoring:**
- [ ] EGT stays below 950°C during burbles
- [ ] AFR stays in 11-13:1 range during burbles
- [ ] No check engine lights or fault codes
- [ ] No excessive exhaust smell or smoke

✅ **Documentation:**
- [ ] Baseline datalog saved
- [ ] All test datalogs saved and labeled
- [ ] Current tune file backed up
- [ ] Notes on behavior at each setting

**If all checkboxes complete → Proceed to Phase 2**

**If any issues → Return to troubleshooting section**

---

## PHASE 2: REFINEMENT & OPTIMIZATION

### **STAGE 2.1: Fuel Enrichment for Enhanced Burbles**

**Objective**: Enrich low-load fueling to increase burble intensity

**File to Edit:**
- `fuel_base` (16x16 table)

**Current Strategy:**
- Your current fuel_base table is already performance-tuned
- For burbles, need to enrich LOW LOAD cells at MID/HIGH RPM
- Target: First 4-5 columns, Rows 4-11 (2000-5200 RPM)

**Understanding the Table:**
- 16 rows (RPM): 800, 1200, 1600, 2000, 2400, 2800, 3200, 3600, 4000, 4400, 4800, 5200, 5600, 6000, 6400, 6800
- 16 columns (Load): 0.13, 0.27, 0.40, 0.54, 0.67, 0.81, 0.94, 1.08, 1.21, 1.35, 1.48, 1.75, 2.02, 2.24, 2.51, 2.74
- Values are % corrections (100 = baseline, >100 = richer)

**Target Cells for Burble Enrichment:**
```
                LOW LOAD (closed throttle zone)
                ↓↓↓↓↓
RPM     0.13  0.27  0.40  0.54  0.67 | 0.81  0.94  1.08 ... (higher loads)
--------|-------|-------|-------|-------|---------
800     (skip) (skip) (skip) (skip)    | no change
1200    (skip) (skip) (skip) (skip)    | no change
1600    +5%   +5%   +5%   +5%   +3%  | no change
2000    +8%   +8%   +8%   +7%   +5%  | no change ← BURBLE ZONE
2400    +10%  +10%  +10%  +8%   +5%  | no change ← BURBLE ZONE
2800    +12%  +12%  +10%  +8%   +5%  | no change ← BURBLE ZONE
3200    +12%  +12%  +10%  +8%   +5%  | no change ← BURBLE ZONE
3600    +12%  +12%  +10%  +8%   +5%  | no change ← BURBLE ZONE
4000    +10%  +10%  +10%  +8%   +5%  | no change ← BURBLE ZONE
4400    +10%  +10%  +10%  +8%   +5%  | no change ← BURBLE ZONE
4800    +8%   +8%   +8%   +7%   +5%  | no change ← BURBLE ZONE
5200    +8%   +8%   +8%   +7%   +5%  | no change ← BURBLE ZONE
5600    +5%   +5%   +5%   +5%   +3%  | no change
6000    +3%   +3%   +3%   +3%   0%   | no change
6400+   (no change across all loads)
```

**Iteration 2.1a - Conservative Enrichment (+5-8%):**

**Example Row 4 (2000 RPM) Modification:**
```
CURRENT: "67.1, 62.2, 66.3, 69.9, 68.8, 68.8, ..."
CHANGE TO: "72.5, 67.1, 71.6, 75.4, 72.2, 68.8, ..." (add ~8%)
```

**Calculation Method:**
- Original value × 1.08 = New value (8% increase)
- Example: 67.1 × 1.08 = 72.5

**Iteration 2.1b - Moderate Enrichment (+10-15%):**

**Example Row 5 (2400 RPM):**
```
CURRENT: "68.8, 65.1, 65.3, 71.6, 71.1, 70.3, ..."
CHANGE TO: "75.7, 71.6, 71.8, 78.8, 74.7, 70.3, ..." (add ~10-12%)
```

**Iteration 2.1c - Aggressive Enrichment (+15-20%):**

**For maximum burble intensity** (⚠️ **RICH AFR WARNING**):
```
Apply +15-20% to first 4 columns, +10% to column 5
Monitor AFR closely - should not go below 10.5:1
```

---

**Step-by-Step Enrichment Process:**

**Step 1: Calculate New Values**

Create a spreadsheet or use calculator:
```
For each cell in burble zone:
New Value = Current Value × Multiplier

Example multipliers:
Conservative: 1.05-1.08 (5-8%)
Moderate: 1.10-1.12 (10-12%)
Aggressive: 1.15-1.20 (15-20%)
```

**Step 2: Update Tune File**

Modify `fuel_base` table rows 4-11 (RPM 2000-5200):
- Update columns 1-4 with calculated values
- Update column 5 with smaller increase
- Leave columns 6-16 unchanged
- Leave rows 1-3 and 12-16 unchanged

**Step 3: Test & Datalog**

1. Flash modified tune
2. Warm engine
3. Test burble conditions
4. Monitor datalog:
   - **AFR during burbles**: Should be 11.5-13:1
   - **Fuel injector duty**: Should increase in low-load cells
   - **Burble intensity**: Should increase
   - **EGT**: Watch for increases (danger!)

**Step 4: Evaluate Results**

**Successful Enrichment Indicators:**
- ✅ Louder, more frequent burbles
- ✅ AFR stays in 11-13:1 during burbles
- ✅ No excessive black smoke
- ✅ EGT remains safe (<950°C)

**Over-Enrichment Warning Signs:**
- ❌ AFR below 10.5:1 during burbles
- ❌ Black smoke from exhaust
- ❌ Strong fuel smell
- ❌ Engine bogging or misfiring
- ❌ Fouled spark plugs

**If over-enriched:** Reduce enrichment by 3-5% and retest

---

### **STAGE 2.2: RPM Range Targeting**

**Objective**: Fine-tune which RPM ranges produce burbles

**Method**: Selective spark retard adjustment

**Common Scenarios:**

**Scenario A: "Low-End Burbles" (2000-3500 RPM)**
- Good for: City driving, 2nd gear pulls
- Configuration:
```json
closed_throttle_spark:
"5.0, 5.0, -12.0, -20.0, -22.0, -22.0, -18.0, -12.0, -8.0, -6.0, -4.0, -2.0, 0.0, 0.0, 0.0, 0.0"
```
- Peak retard at 2000-3200 RPM
- Tapers off above 3600 RPM

**Scenario B: "Mid-Range Burbles" (3000-5000 RPM)**
- Good for: 3rd gear pulls, backroad driving
- Configuration:
```json
closed_throttle_spark:
"5.0, 5.0, -10.0, -14.0, -18.0, -22.0, -24.0, -24.0, -22.0, -18.0, -14.0, -10.0, -6.0, 0.0, 0.0, 0.0"
```
- Peak retard at 3200-4000 RPM
- Smooth taper both sides

**Scenario C: "High-End Burbles" (4000-6000 RPM)**
- Good for: Highway pulls, track use
- Configuration:
```json
closed_throttle_spark:
"5.0, 5.0, -8.0, -10.0, -12.0, -14.0, -16.0, -18.0, -20.0, -22.0, -20.0, -18.0, -14.0, -10.0, -6.0, -4.0"
```
- ⚠️ **WARNING**: High EGT risk!
- Peak retard at 4400-5200 RPM
- Requires close EGT monitoring

**Scenario D: "Wide Range Burbles" (2500-5500 RPM)**
- Good for: All-around performance
- Configuration:
```json
closed_throttle_spark:
"5.0, 5.0, -15.0, -20.0, -22.0, -24.0, -24.0, -24.0, -22.0, -20.0, -18.0, -16.0, -12.0, -8.0, -4.0, 0.0"
```
- Broad plateau of retard
- Consistent burbles across wide RPM range

**Test Procedure for RPM Targeting:**

1. Choose scenario based on driving style
2. Flash tune with selected profile
3. Test at various RPMs:
   - Low: 2500 RPM decel
   - Mid: 4000 RPM decel
   - High: 5500 RPM decel
4. Note where burbles are loudest/most frequent
5. Adjust retard curve to emphasize desired range

**Fine-Tuning Tips:**

- **To increase burbles in specific RPM range:**
  - Add -2° to -4° more retard in that zone
  
- **To reduce burbles in specific range:**
  - Reduce retard by +2° to +4° in that zone
  
- **To shift burble range higher:**
  - Move peak retard values to higher RPM indices
  
- **To shift burble range lower:**
  - Move peak retard values to lower RPM indices

---

### **STAGE 2.3: Burble Intensity Adjustment**

**Objective**: Fine-tune "loudness" and aggressiveness

**Three Control Levers:**

#### **Lever 1: Spark Retard Amount**
- **More negative** = Louder burbles, more flames
- **Less negative** = Softer burbles, less dramatic
- Adjust in **2° increments**

#### **Lever 2: Fuel Enrichment**
- **Richer** = More frequent burbles, louder pops
- **Leaner** = Sporadic burbles, quieter
- Adjust in **5% increments**

#### **Lever 3: DFCO Delay**
- **Longer delay** = Extended burble duration
- **Shorter delay** = Brief burble window
- Adjust in **5 count increments**

---

**Intensity Tuning Matrix:**

| Desired Effect | Spark Retard | Fuel Enrich | DFCO Delay |
|---------------|--------------|-------------|------------|
| **Subtle Pops** | -10° to -12° | +5% | 10 counts |
| **Moderate Burbles** | -15° to -18° | +8-10% | 15 counts |
| **Loud Crackling** | -20° to -24° | +12-15% | 20 counts |
| **Extreme/Flames** | -25° to -30° | +15-20% | 25 counts |

---

**Tuning Process:**

**Step 1: Establish Baseline**
- Record current burble intensity (1-10 scale)
- Note current settings for all three levers

**Step 2: Choose ONE Lever to Adjust**
- Never adjust multiple parameters simultaneously
- Make small incremental changes

**Step 3: Test & Evaluate**
- Perform standard decel test
- Rate new intensity (1-10 scale)
- Compare to baseline

**Step 4: Iterate**
- If too aggressive: Reduce parameter
- If too subtle: Increase parameter
- If just right: Document and move to next lever

**Example Progression:**

**Starting Point:**
- Spark: -15°
- Fuel: +8%
- Delay: 15 counts
- Result: 5/10 intensity

**Iteration 1 (increase spark retard):**
- Spark: -18° ← CHANGED
- Fuel: +8%
- Delay: 15 counts
- Result: 7/10 intensity (better!)

**Iteration 2 (increase fuel enrichment):**
- Spark: -18°
- Fuel: +12% ← CHANGED
- Delay: 15 counts
- Result: 8/10 intensity (louder!)

**Iteration 3 (increase DFCO delay):**
- Spark: -18°
- Fuel: +12%
- Delay: 20 counts ← CHANGED
- Result: 9/10 intensity (perfect!)

---

### **STAGE 2.4: Gear-Specific Optimization**

**Objective**: Tune burbles for specific gear scenarios

**Why Gear Matters:**
- Different gears = different load characteristics
- 2nd gear decel ≠ 4th gear decel at same RPM
- Load affects fuel delivery and combustion

**Test Each Gear:**

**2nd Gear Decel (Most Common):**
- RPM range: 2500-4500 typical
- Load: Light to moderate
- Focus tuning here for street driving

**3rd Gear Decel:**
- RPM range: 3000-5500 typical
- Load: Moderate
- Good for backroad/canyon driving

**4th+ Gear Decel:**
- RPM range: 3500-6000+ typical
- Load: Moderate to high
- ⚠️ Higher EGT risk

**Tuning Approach:**

1. **Record baseline in each gear:**
   - 2nd gear 3000 RPM decel
   - 3rd gear 4000 RPM decel
   - 4th gear 5000 RPM decel

2. **Note differences:**
   - Which gear has best burbles?
   - Which gear lacks burbles?
   - EGT comparison across gears

3. **Adjust for weak points:**
   - If 4th gear burbles are weak → add -2° retard in 4500-5500 RPM range
   - If 2nd gear is too aggressive → reduce -2° retard in 2500-3500 RPM range

---

## PHASE 3: ADVANCED OPTIMIZATION

### **STAGE 3.1: Temperature-Dependent Tuning**

**Objective**: Optimize burble behavior at different operating temps

**Temperature Factors:**

#### **Cold Engine (60-75°C)**
- Slower combustion
- May need MORE retard (-2° to -4°)
- Richer mixture naturally
- Burbles may be inconsistent

#### **Normal Operating (80-95°C)**
- Optimal combustion
- Baseline tuning applies
- Most consistent burbles

#### **Hot Engine (95-105°C)**
- Faster combustion
- May need LESS retard (+2° to +4°)
- Leaner mixture naturally
- EGT climbs faster

**Tuning Strategy:**

Since `closed_throttle_spark_coolant_comp` was zeroed (recommended), burbles work consistently at all temps. However, you may notice:

- **Cold engine**: Burbles quieter/less frequent
  - **Solution**: Accept it, or add +2-3% fuel enrichment
  
- **Hot engine**: Burbles louder/more aggressive
  - **Solution**: Monitor EGT closely, reduce retard if needed

**Alternative (Advanced):**
Re-enable coolant compensation with custom curve:
```json
closed_throttle_spark_coolant_comp:
"2.0, 2.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0"
```
- Adds +2° when cold (reduces retard slightly)
- Subtracts -2° when hot (increases retard slightly)
- Balances burble intensity across temps

---

### **STAGE 3.2: Exhaust System Matching**

**Objective**: Optimize for your specific exhaust setup

**Different Exhausts = Different Tuning:**

#### **Stock Exhaust (Catless)**
- Quieter, muffled sound
- May need MORE retard for audible burbles
- Recommendation: -22° to -28° range

#### **Cat-Back Exhaust**
- Moderate volume
- Good burble tone
- Recommendation: -18° to -24° range

#### **Turbo-Back Exhaust**
- Loud, aggressive
- Excellent burble projection
- Recommendation: -15° to -22° range

#### **Straight Pipe**
- VERY loud
- Maximum burble projection
- Recommendation: -12° to -20° range (less retard needed)
- ⚠️ May be TOO loud for some

**Tuning Process:**

1. Start with recommended range for your exhaust
2. Adjust based on desired loudness:
   - Too quiet? Add -3° to -5° retard
   - Too loud? Reduce -3° to -5° retard
3. Consider neighbors/local noise ordinances

---

### **STAGE 3.3: Fail-Safe and Safety Tuning**

**Objective**: Build in protections to prevent damage

**Safety Parameter: Spark Min**

**File to Edit:**
- `spark_min`

**Current Value:**
```json
"0.0, 0.0"
```

**Purpose**: Defines minimum allowed spark advance

**Problem with Burble Tuning:**
- With heavy retard (-25°), approaching spark_min limit
- If spark_min is 0°, ECU may clamp timing
- Burbles may not work, or work inconsistently

**Solution: Adjust Spark Min for Burbles:**

```json
"-30.0, -30.0"
```

**Effect**: Allows spark timing as low as -30° BTDC

**⚠️ Trade-off**: 
- Allows desired burble retard
- Removes safety limit that prevents extreme retard
- YOU must monitor EGT to ensure safety

**Recommendation**: 
- Set spark_min to -5° below your maximum retard value
- Example: If max retard is -24°, set spark_min to -30°

---

### **STAGE 3.4: Rev Limiter Burbles (Advanced)**

**Objective**: Create burbles when hitting rev limit

**Current Setup:**
- `rev_limit`: 6000, 7800, 8000, 8000, 8117 (by gear)
- `rev_limit_spark`: -6.0°

**How Rev Limit Works:**
- Engine hits RPM limit
- Fuel cut momentarily (hard rev limit)
- OR spark retarded (soft rev limit)

**Enabling Rev Limit Burbles:**

**Option A: Increase Rev Limit Spark Retard**
```json
rev_limit_spark: "-20.0"
```
- Changes from -6° to -20° retard at limit
- Creates pops/burbles when bouncing off limiter
- Less harsh than fuel cut

**Option B: Combine with DFCO Settings**
- Rev limiter uses same spark retard logic
- If closed_throttle_spark is already -20°, limiter will burble
- No additional changes needed

**Test Procedure:**
1. In safe environment, hold throttle to rev limit
2. Listen for burbles as limiter activates
3. Monitor EGT (will spike!)
4. Adjust retard amount for desired effect

**⚠️ WARNING:**
- Rev limit burbles create VERY high EGT
- Only use for brief moments (2-3 seconds max)
- Turbo damage risk is high
- Not recommended for daily driving

---

## PHASE 4: VALIDATION & DOCUMENTATION

### **STAGE 4.1: Extended Testing**

**Objective**: Validate tune reliability over extended period

**Test Plan:**

**Week 1: Daily Driving**
- Drive normally for 7 days
- Note burble consistency
- Monitor for any issues
- Log AFR, EGT daily

**Week 2: Spirited Driving**
- Canyon runs, backroads
- Multiple decel cycles
- Various RPM ranges
- Extended EGT monitoring

**Week 3: Mixed Conditions**
- Cold starts
- Hot weather
- Traffic driving
- Highway cruising

**Week 4: Validation**
- Review all datalogs
- Check spark plugs
- Inspect exhaust (cracks, damage)
- Final adjustments if needed

**Documentation Checklist:**

✅ **Performance Logs:**
- [ ] 10+ datalogs from various scenarios
- [ ] Peak EGT recorded
- [ ] AFR range documented
- [ ] No fault codes

✅ **Physical Inspection:**
- [ ] Spark plugs condition (should be tan/brown)
- [ ] Exhaust visual inspection (no cracks)
- [ ] Turbo no unusual noises
- [ ] Engine no leaks or issues

✅ **Final Tune Documentation:**
- [ ] All table values recorded
- [ ] Baseline comparison documented
- [ ] Known issues/limitations noted
- [ ] Recommended maintenance interval

---

### **STAGE 4.2: Creating Tune Variants**

**Objective**: Build multiple tunes for different scenarios

**Recommended Variants:**

#### **Variant 1: "Daily Driver" Burble**
- Conservative settings
- -15° to -18° retard
- +8% fuel enrichment
- Good for street use

#### **Variant 2: "Weekend Warrior" Burble**
- Aggressive settings
- -20° to -24° retard
- +12% fuel enrichment
- Spirited driving, backroads

#### **Variant 3: "Show Mode" Burble**
- Maximum aggression
- -25° to -30° retard
- +15% fuel enrichment
- Car shows, brief use only

#### **Variant 4: "Stealth Mode" (No Burble)**
- Stock DFCO settings
- Normal spark timing
- Use in noise-sensitive areas

**File Naming Convention:**
```
[Your Name]_[Car]_[Version]_[Variant]_[Date].tune

Examples:
Keith_JDMSTI_v10_DailyBurble_20251207.tune
Keith_JDMSTI_v10_WeekendBurble_20251207.tune
Keith_JDMSTI_v10_ShowMode_20251207.tune
Keith_JDMSTI_v10_StealthMode_20251207.tune
```

---

## TROUBLESHOOTING GUIDE

### Problem: No Burbles at All

**Symptoms:**
- Silence during decel
- No pops or crackles
- AFR goes lean during decel

**Diagnosis Steps:**

1. **Check Datalog:**
   - Is ignition timing going negative? 
     - NO → Spark retard not applying
     - YES → Continue diagnosis
   
2. **Check Fuel Delivery:**
   - Does injector duty stay above 0% during decel?
     - NO → DFCO still cutting fuel
     - YES → Continue diagnosis
   
3. **Check AFR:**
   - Is AFR rich (11-14:1) during decel?
     - NO → Not enough fuel
     - YES → Continue diagnosis

**Solutions:**

**If spark not retarding:**
- Verify `closed_throttle_spark` has negative values
- Check `closed_throttle_spark_vss_max` is high enough
- Ensure tune flashed successfully

**If fuel cutting:**
- Increase `dfco_delay` further (try 25-30 counts)
- Increase `dfco_enable_rpm_a/b` thresholds more (+500 RPM)
- OR disable DFCO entirely (`dfco_enable: 0`)

**If not enough fuel:**
- Increase fuel enrichment in low-load cells (+5-10%)
- Check fuel pump voltage/pressure
- Verify MAF sensor is reading correctly

---

### Problem: Burbles Too Quiet/Weak

**Symptoms:**
- Faint pops, barely audible
- Inconsistent burbles
- Only burbles at specific RPM

**Solutions:**

1. **Increase Spark Retard:**
   - Add -3° to -5° more retard
   - Current: -18° → Try: -22° to -24°

2. **Increase Fuel Enrichment:**
   - Add +5% more fuel in low-load cells
   - Richer mixture = louder burbles

3. **Extend DFCO Delay:**
   - Current 15 counts → Try 20-25 counts
   - Longer fuel delivery = more burbles

4. **Expand RPM Range:**
   - Apply retard to wider RPM band
   - More indices with -20°+ retard

5. **Check Exhaust System:**
   - Mufflers dampen sound significantly
   - Consider less restrictive exhaust

---

### Problem: Burbles Too Loud/Aggressive

**Symptoms:**
- Deafening pops, startles neighbors
- Flames from exhaust
- Complaints from passengers

**Solutions:**

1. **Reduce Spark Retard:**
   - Reduce by -3° to -5°
   - Current: -24° → Try: -18° to -20°

2. **Reduce Fuel Enrichment:**
   - Reduce by -5% in low-load cells
   - Leaner = quieter burbles

3. **Narrow RPM Range:**
   - Apply heavy retard to smaller band
   - Reduce retard at extremes

4. **Shorten DFCO Delay:**
   - Current 20 counts → Try 15 counts
   - Shorter burble duration

5. **Consider Resonator:**
   - Add resonator to exhaust
   - Tames volume without eliminating burbles

---

### Problem: High EGT (>950°C)

**Symptoms:**
- EGT gauge in danger zone
- Smell of hot metal
- Loss of power
- Blue/glowing exhaust components

**⚠️ IMMEDIATE ACTION:**
1. Stop aggressive driving immediately
2. Allow engine to cool down
3. Do NOT continue with current tune

**Solutions:**

1. **Reduce Spark Retard:**
   - Less retard = cooler exhaust
   - Reduce by -5° in problem RPM range

2. **Narrow Burble RPM Range:**
   - Remove retard from high-RPM indices (5200+)
   - Focus burbles in lower RPM range (2500-4500)

3. **Reduce Fuel Enrichment:**
   - Less fuel = less combustion = lower EGT
   - Reduce by -5% to -10%

4. **Limit Burble Duration:**
   - Reduce DFCO delay (15 → 10 counts)
   - Shorter burbles = less heat buildup

5. **Driving Habit Modification:**
   - Limit consecutive decel burbles
   - Allow cooldown between pulls
   - Don't abuse burbles in stop-go traffic

6. **Hardware Upgrades:**
   - Upgrade turbo to one with better heat tolerance
   - Add exhaust wrap (carefully, can trap heat)
   - Improve cooling system

**Safe EGT Limits:**
- **Normal Operation**: 650-750°C
- **Spirited Driving**: 750-850°C
- **Peak (Brief)**: 850-950°C
- **⚠️ DANGER ZONE**: 950°C+
- **🔥 DAMAGE IMMINENT**: 1000°C+

---

### Problem: Engine Stumbles or Bogs on Decel

**Symptoms:**
- Engine hesitates when closing throttle
- RPM drops erratically
- Nearly stalls during decel
- Rough idle after decel

**Diagnosis:**

Check datalog for:
- AFR going too rich (<10:1)
- RPM dropping too fast
- Load values

**Solutions:**

1. **Reduce Fuel Enrichment:**
   - Over-fueling causing bog
   - Reduce by -10% in low-load cells

2. **Reduce DFCO Delay:**
   - Too much fuel delivery time
   - Current 20 → Try 15 counts

3. **Moderate Spark Retard:**
   - Excessive retard = poor combustion
   - Reduce by -3° to -5°

4. **Check Idle Air Control:**
   - May need idle air adjustment
   - Review `idle_air_base_mt` table
   - Increase slightly if stalling occurs

5. **Verify MAF Sensor:**
   - Clean MAF sensor
   - Check for intake leaks
   - Ensure proper MAF scaling

---

### Problem: Check Engine Light / Fault Codes

**Common Codes with Burble Tunes:**

#### **P0171/P0172 - System Too Lean/Rich**
- Cause: Extreme AFR swings during burbles
- Solution: 
  - Reduce fuel enrichment magnitude
  - Shorten DFCO delay
  - May need to disable code monitoring (advanced)

#### **P0300-P0304 - Misfire Codes**
- Cause: Late ignition causing incomplete combustion
- Solution:
  - Reduce spark retard by -3° to -5°
  - Check spark plugs (may be fouled)
  - Verify coil pack health

#### **P0420/P0430 - Catalyst Efficiency**
- Cause: Unburned fuel damaging O2 sensors
- Solution:
  - Should not have cats with burble tune!
  - If cats present, STOP immediately
  - Remove cats or revert to stock tune

#### **P0101 - MAF Sensor Range**
- Cause: Erratic airflow during burbles
- Solution:
  - Clean MAF sensor
  - Check MAF scaling
  - May be false code - clear and monitor

**Code Management:**
1. Note all codes and conditions when they occurred
2. Clear codes
3. Test again to see if codes return
4. If persistent, address root cause
5. Do NOT ignore codes - they indicate problems

---

### Problem: Fouled Spark Plugs

**Symptoms:**
- Loss of power
- Rough idle
- Misfires
- Black soot on plugs

**Cause:**
- Rich mixture during burbles
- Incomplete combustion
- Carbon buildup

**Solutions:**

**Immediate:**
1. Remove and inspect spark plugs
2. Clean or replace plugs (recommend replace)
3. Use colder heat range plugs (1-2 steps colder)

**Tuning Adjustments:**
1. Reduce fuel enrichment (-5% to -10%)
2. Moderate spark retard (-3° less)
3. Shorten burble duration (less DFCO delay)

**Preventive Maintenance:**
- Inspect plugs every 3,000 miles
- Use high-quality plugs (NGK, Denso)
- Consider iridium or platinum plugs
- Run "Italian Tune-Up" periodically (high-RPM cruise to burn carbon)

---

### Problem: Excessive Fuel Consumption

**Symptoms:**
- MPG drops significantly (>20%)
- Fuel tank empties quickly
- Constant fuel smell

**Expected:**
- 10-15% fuel consumption increase is normal with burbles

**If excessive (>20%):**

**Solutions:**

1. **Reduce DFCO Delay:**
   - Shorter fuel delivery during decel
   - Current 20 → Try 10-12 counts

2. **Reduce Fuel Enrichment:**
   - Only enrich cells used during burbles
   - Remove enrichment from high-load cells

3. **Create "Eco Mode" Variant:**
   - Stock DFCO settings
   - Flash for highway trips
   - Flash burble tune for fun

4. **Driving Habits:**
   - Limit burble usage
   - Use burbles selectively
   - Coast in gear without burbles more often

---

## DATALOG MONITORING

### Essential Parameters to Log

**Tier 1 (Critical - Always Log):**
- RPM
- TPS (Throttle Position %)
- Ignition Timing (Final)
- AFR / Lambda
- Vehicle Speed
- Engine Load (g/rev)
- Coolant Temperature
- Fuel Injector Duty Cycle %

**Tier 2 (Important - Log Often):**
- EGT (if equipped)
- Boost Pressure
- MAF Sensor (g/s)
- Knock Count
- IAM (Ignition Advance Multiplier)
- Closed Throttle Flag
- DFCO Active Flag
- Fuel Pressure

**Tier 3 (Supplementary - Log Occasionally):**
- Intake Air Temperature
- Battery Voltage
- O2 Sensor Voltage
- Fuel Trim (Short & Long)
- Idle Air Control Valve %

---

### Datalog Analysis - What to Look For

#### **Successful Burble Datalog:**

**During Decel (Throttle Lift):**
```
Time  | RPM  | TPS | Timing | AFR  | Load | Fuel% | Notes
------|------|-----|--------|------|------|-------|--------
0.0s  | 4500 | 65% |  15°   | 11.8 | 1.95 | 85%   | WOT
0.5s  | 4400 | 0%  | -18°   | 12.1 | 0.54 | 42%   | Lift!
1.0s  | 4100 | 0%  | -20°   | 12.5 | 0.40 | 38%   | Burbles
1.5s  | 3800 | 0%  | -20°   | 12.8 | 0.35 | 35%   | Burbles
2.0s  | 3500 | 0%  | -18°   | 13.2 | 0.30 | 32%   | Burbles
2.5s  | 3200 | 0%  | -15°   | 14.5 | 0.25 | 15%   | Winding
3.0s  | 2900 | 0%  |  10°   | 18.2 | 0.20 | 0%    | DFCO On
```

**Key Indicators:**
- ✅ Timing goes negative immediately on throttle lift
- ✅ AFR stays 11.5-13.5:1 during burbles (rich)
- ✅ Fuel duty stays above 0% for 1.5-2.5 seconds
- ✅ Load drops to low values (closed throttle)
- ✅ DFCO doesn't activate until later in decel

---

#### **Problem Datalog Examples:**

**Problem: DFCO Activating Too Early**
```
Time  | RPM  | TPS | Timing | AFR  | Fuel% | Problem
------|------|-----|--------|------|-------|--------
0.5s  | 4400 | 0%  | -18°   | 12.1 | 42%   | Lift
1.0s  | 4100 | 0%  | -20°   | 18.5 | 0%    | ← DFCO! Too early!
```
**Solution**: Increase DFCO delay and/or RPM thresholds

---

**Problem: Spark Not Retarding**
```
Time  | RPM  | TPS | Timing | AFR  | Problem
------|------|-----|--------|------|--------
0.5s  | 4400 | 0%  |  22°   | 18.8 | ← Still advance!
1.0s  | 4100 | 0%  |  20°   | 18.5 | ← No retard!
```
**Solution**: Verify closed_throttle_spark table has negative values

---

**Problem: Excessive EGT**
```
Time  | RPM  | TPS | Timing | EGT   | Problem
------|------|-----|--------|-------|--------
0.5s  | 5500 | 0%  | -24°   | 850°C | Starting high
1.5s  | 5100 | 0%  | -24°   | 975°C | ← DANGER!
2.0s  | 4800 | 0%  | -24°   | 1025°C| ← TOO HOT!
```
**Solution**: Reduce retard at high RPM, narrow burble range

---

### Creating a Datalog Library

**Organization:**
```
/Datalogs/
  /Baseline/
    baseline_before_burble_001.csv
    baseline_before_burble_002.csv
  
  /Phase1_Testing/
    phase1_iter1_mild_retard_001.csv
    phase1_iter2_moderate_retard_001.csv
  
  /Phase2_Refinement/
    phase2_fuel_enrich_test_001.csv
    phase2_rpm_targeting_001.csv
  
  /Final_Validation/
    final_daily_drive_001.csv
    final_spirited_001.csv
    final_highway_001.csv
```

**Datalog Naming Convention:**
```
[Phase]_[Test Description]_[Iteration].csv

Examples:
baseline_stock_tune_001.csv
phase1_dfco_delay15_spark18_001.csv
phase2_fuel_plus10pct_001.csv
final_weekend_burble_tune_001.csv
```

**Log Retention:**
- Keep ALL logs during tuning process
- Archive successful iterations
- Keep "problem" logs for reference
- Back up to cloud storage

---

## SAFETY LIMITS & RED FLAGS

### Absolute Safety Limits

**DO NOT EXCEED:**

| Parameter | Safe Limit | Danger Zone | Stop Immediately |
|-----------|-----------|-------------|------------------|
| **EGT** | <900°C | 900-975°C | >975°C |
| **AFR (Burbles)** | 11.5-14:1 | 10.5-11.5 or >14.5 | <10.5 or >15 |
| **AFR (WOT)** | 11.0-12.5:1 | <10.5 or >13 | <10.0 or >13.5 |
| **Knock Count** | 0-2 | 3-5 | >5 |
| **IAM** | >0.75 | 0.50-0.75 | <0.50 |
| **Coolant Temp** | <100°C | 100-105°C | >105°C |
| **Oil Temp** | <120°C | 120-130°C | >130°C |
| **Boost (Peak)** | <200kPa | 200-210kPa | >210kPa |

---

### Red Flags - Stop Tuning Immediately

🚩 **Mechanical Issues:**
- Unusual engine noises (knocking, pinging, rattling)
- Smoke from engine bay
- Coolant or oil leaks
- Burning smell (not exhaust)
- Loss of power
- Turbo whine or grinding

🚩 **Exhaust System Issues:**
- Glowing exhaust components (visible red)
- Exhaust leaks or hissing
- Cracked exhaust manifold
- Melted heat shields
- Flames entering engine bay (!)

🚩 **Performance Issues:**
- Engine will not start
- Stalling frequently
- Misfires at all RPM
- Limp mode activation
- Multiple fault codes

🚩 **Safety Issues:**
- Brakes affected (bogging interferes with braking)
- Throttle response delayed
- Inability to control vehicle
- Passenger complaints of illness (CO leak?)

---

### When to Seek Professional Help

**Scenarios requiring professional tuner:**

1. **Persistent knock** despite reducing timing
2. **Misfires** that don't resolve with plug/coil changes
3. **AFR issues** that can't be corrected with fuel adjustments
4. **Excessive EGT** even with conservative settings
5. **Multiple fault codes** related to engine management
6. **Physical damage** to engine or exhaust components
7. **Uncertainty** about any tuning parameter

**Finding a good tuner:**
- Look for Subaru-specific experience
- Ask for references/portfolio
- Discuss burble tune goals upfront
- Ensure they have dyno and EGT monitoring
- Get written estimate before work

---

## FINAL RECOMMENDATIONS

### Conservative "Safe Street" Burble Setup

**Recommended for daily drivers, first-time tuners:**

```
DFCO Settings:
- dfco_delay: 15, 15, 15, 10
- dfco_enable_rpm_a/b: +1500 RPM across all values
- dfco_disable_rpm: +1000 RPM across all values

Spark Settings:
- closed_throttle_spark: -15° to -18° in 2400-4800 RPM range
- closed_throttle_spark_vss_max: 150 km/h
- closed_throttle_spark_coolant_comp: all 0.0

Fuel Settings:
- fuel_base low-load enrichment: +8% in columns 1-4
- Apply to rows 4-11 (2000-5200 RPM)

Safety:
- spark_min: -25.0
- Monitor EGT constantly
- Limit consecutive burbles
```

**Expected Result:**
- Moderate burble intensity (6-7/10)
- Safe EGT levels (<900°C)
- Good reliability
- Minimal maintenance impact

---

### Aggressive "Weekend Warrior" Setup

**Recommended for experienced tuners, performance builds:**

```
DFCO Settings:
- dfco_delay: 20, 20, 20, 15
- dfco_enable_rpm_a/b: +2000 RPM across all values
- OR dfco_enable: 0 (full disable)

Spark Settings:
- closed_throttle_spark: -20° to -24° in 2400-5200 RPM range
- Targeted retard curve for specific RPM emphasis
- closed_throttle_spark_vss_max: 200 km/h
- closed_throttle_spark_coolant_comp: all 0.0

Fuel Settings:
- fuel_base low-load enrichment: +12-15% in columns 1-4
- Apply to rows 4-11 (2000-5200 RPM)
- Consider slight high-RPM enrichment

Safety:
- spark_min: -30.0
- EGT sensor REQUIRED
- Upgraded turbo recommended
- Accept shorter component lifespan
```

**Expected Result:**
- Loud, aggressive burbles (8-9/10)
- Higher EGT (850-950°C)
- More maintenance required
- Spectacular sound and flames

---

## APPENDIX: Quick Reference Tables

### Tuning Parameter Quick Reference

| Want More: | Adjust: | Direction: |
|-----------|---------|------------|
| Burble Volume | Spark Retard | More negative (-3° to -5°) |
| Burble Duration | DFCO Delay | Increase (+5 counts) |
| Burble Frequency | Fuel Enrichment | Increase (+5%) |
| Safety Margin | All Parameters | Reduce (less aggressive) |
| High RPM Burbles | Spark Retard @ High RPM | Extend to 5200+ RPM |
| Low RPM Burbles | Spark Retard @ Low RPM | Start at 1600-2000 RPM |

---

### Problem Solving Matrix

| Symptom | Most Likely Cause | Quick Fix |
|---------|-------------------|-----------|
| No burbles | Spark not retarding | Check closed_throttle_spark values |
| Weak burbles | Not enough retard | Add -5° more retard |
| Too loud | Too much retard | Reduce -5° retard |
| High EGT | Retard at high RPM | Remove retard above 5200 RPM |
| Engine bogs | Too much fuel | Reduce enrichment -10% |
| Fouled plugs | Over-fueling | Reduce enrichment, colder plugs |
| Stumbles | Extreme retard | Reduce retard -5° |

---

### Datalog Target Values

| Parameter | During Burbles | Notes |
|-----------|---------------|-------|
| RPM | 2500-5500 | Sweet spot for most setups |
| TPS | 0-2% | Closed throttle |
| Timing | -15° to -25° | More negative = louder |
| AFR | 11.5-13.5:1 | Rich but not excessive |
| EGT | <900°C | <850°C ideal |
| Load | 0.20-0.60 g/rev | Low load, decel |
| Fuel Duty | 25-50% | Continuing to inject |

---

## MAINTENANCE SCHEDULE

### Burble Tune-Specific Maintenance

**Every 1,000 Miles:**
- Inspect spark plugs
- Check for exhaust leaks
- Review datalogs for anomalies

**Every 3,000 Miles:**
- Replace spark plugs
- Inspect turbo for damage
- Check exhaust hangers/mounts
- Oil change (more frequent due to fuel dilution)

**Every 6,000 Miles:**
- Inspect exhaust manifold (cracks)
- Check turbo bearings (play test)
- Inspect downpipe welds
- Deep clean MAF sensor

**Every 12,000 Miles:**
- Compression test
- Leak-down test
- Turbo inspection/rebuild if needed
- Full exhaust inspection

**Annual:**
- Full exhaust system inspection
- Turbo replacement consideration (if aggressive tune)
- Engine bay inspection for heat damage

---

## CONCLUSION

Burble tuning is an iterative process requiring patience, careful monitoring, and respect for safety limits. 

**Key Takeaways:**
- Start conservative, increase gradually
- Monitor EGT religiously
- One change at a time
- Document everything
- Listen to your engine

**Most Important:**
- If something doesn't feel right, STOP
- Burbles are fun, but engine health comes first
- Be prepared for increased maintenance
- Accept shorter component lifespan

**Enjoy your burbles responsibly! 🔥**

---

*Document Version: 1.0*
*Created: December 7, 2025*
*For: 1999 JDM Subaru WRX STi EJ207*
*Based on: Tune File v10_20251203*

---

## REVISION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-07 | Initial comprehensive guide |

---

**END OF GUIDE**
