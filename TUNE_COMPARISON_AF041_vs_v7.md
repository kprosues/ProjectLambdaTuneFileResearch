# Tune File Comparison: AF041_base.tune vs v7_keith_edit.tune

## File Information

**Base File (AF041_base.tune):**
- Version: 1.6.33.2
- Schema: Latest standard schema
- Comments: None

**Tuned File (v7_keith_edit.tune):**
- Version: 1.6.36.2
- Schema: Extended performance tuning schema
- Comments: "10/19 removed 10% from the load comp table; added 10% to the base inj pulse crank\r\nv6 leaned power target by 5%\r\n"

---

## Summary of Major Changes

The v7 tune is a **performance-oriented modification** with significant changes to:
1. **Extended load range** (supports higher engine loads up to 2.74 g/rev vs 2.16 g/rev)
2. **More aggressive spark timing** (up to 48° advance vs 44° in base)
3. **Higher boost targets** (up to 199.5 kPa vs 208.0 kPa peak, but more aggressive across the table)
4. **Richer fuel mixture** in high-load regions
5. **More aggressive wastegate control**
6. **Extended MAF calibration** (up to 280 g/s vs 250 g/s)
7. **Higher load limits** (5.00 g/rev vs 2.54 g/rev max)

---

## 1. SPARK TIMING (Base Spark Tables)

### Base Spark AT (Automatic Transmission)
**Base File:**
- Conservative timing: 30-44° advance
- High-load regions: 1-22° advance
- Smooth, conservative curve

**v7 Tune:**
- **More aggressive timing**: Up to 48° advance in mid-load regions
- **Significant changes in high-load areas**:
  - Row 8 (3600 rpm): Base has 2-22°, v7 has -7° to 13° (more conservative at high load)
  - Row 9 (4000 rpm): Base has 1-23°, v7 has -7° to 14° (more conservative at high load)
  - Row 10 (4400 rpm): Base has 1-24°, v7 has -7° to 15° (more conservative at high load)
  - Row 11 (4800 rpm): Base has 1-30°, v7 has -7° to 16° (more conservative at high load)
  - Row 12 (5200 rpm): Base has 1-31°, v7 has -7° to 17° (more conservative at high load)
  - Row 13 (5600 rpm): Base has 1-32°, v7 has -7° to 18° (more conservative at high load)
  - Row 14 (6000 rpm): Base has 1-31°, v7 has -7° to 19° (more conservative at high load)
  - Row 15 (6400 rpm): Base has 1-31°, v7 has -7° to 20° (more conservative at high load)
  - Row 16 (6800 rpm): Base has 1-31°, v7 has -7° to 21° (more conservative at high load)

**Analysis**: v7 uses more aggressive timing in mid-load regions (up to 48°) but is **more conservative (retarded) at high loads** to prevent knock under boost.

### Base Spark MT (Manual Transmission)
Similar pattern to AT table - more aggressive in mid-load, more conservative at high load.

### Load Index (base_spark_map_index)
**Base File:**
- Range: 0.13, 0.27, 0.40, 0.54, 0.67, 0.81, 0.94, 1.08, 1.21, 1.35, 1.48, 1.62, 1.75, 1.89, 2.02, 2.16 g/rev

**v7 Tune:**
- **Extended range**: 0.13, 0.27, 0.40, 0.54, 0.67, 0.81, 0.94, 1.08, 1.21, 1.35, 1.48, **1.75, 2.02, 2.24, 2.51, 2.74** g/rev
- **Note**: Missing 1.62 breakpoint, adds higher load points (1.75, 2.02, 2.24, 2.51, 2.74)

**Impact**: Allows tuning at higher engine loads beyond stock limits.

---

## 2. FUEL DELIVERY

### Fuel Base Table (fuel_base)
**Base File:**
- Range: 98.4% to 137.5% (mostly 100% with some enrichment in high-load areas)
- Conservative fueling

**v7 Tune:**
- **Significantly richer**: Range: 60.2% to 87.5%
- **Note**: Lower percentages indicate richer mixture (these are correction factors)
- More aggressive enrichment in high-load regions
- Values are generally 10-20% richer across the table

**Analysis**: v7 provides richer fuel mixture to support higher boost and more aggressive spark timing.

### Power Enrichment (PE) Lambda Targets

#### PE Initial (pe_initial)
**Base File:**
- Range: 0.921 to 1.000 λ (richer under power)
- Conservative enrichment

**v7 Tune:**
- **Much richer**: Range: 0.667 to 0.892 λ
- **Significantly more aggressive enrichment** (lower lambda = richer)
- High-load, high-RPM regions: 0.667-0.749 λ (very rich for safety)

**Analysis**: v7 uses much richer PE targets, especially at high load/RPM, to prevent detonation.

#### PE Safe (pe_safe)
**Base File:**
- Range: 0.831 to 1.000 λ
- Safety enrichment when IAM is low

**v7 Tune:**
- **Even richer**: Range: 0.667 to 0.892 λ
- More aggressive safety enrichment
- High-load regions: 0.667-0.734 λ (very rich)

**Analysis**: v7 provides more aggressive safety enrichment when knock is detected (low IAM).

#### PE Enable Thresholds
**Base File:**
- `pe_enable_load`: 11.45 to 0.00 g/rev (high threshold at low RPM)
- `pe_enable_tps`: 99.61% to 0.00% (very high threshold at low RPM)

**v7 Tune:**
- `pe_enable_load`: **1.48 to 0.00 g/rev** (lower threshold - PE activates earlier)
- `pe_enable_tps`: **99.60% to 0.00%** (similar, but different values in mid-range)

**Analysis**: v7 allows PE mode to activate at lower loads, providing enrichment earlier.

### Fuel Acceleration Enrichment (fuel_accel_enrich)
**Base File:**
- Mostly 0.0% except high rate-of-change: 398.4%

**v7 Tune:**
- **More aggressive**: 20.3% to 398.4% (enrichment at lower rate-of-change)
- Better throttle response with enrichment starting earlier

### Fuel Acceleration Enrichment Decay (fuel_accel_enrich_decay)
**Base File:**
- All 0.0% (no decay configured)

**v7 Tune:**
- **25.0% decay rate** (enrichment decays more slowly, providing better transient response)

### Injector Calibration

#### Injector Latency (inj_latency_offset, inj_latency_slope)
**Base File:**
- Offset: 2.03 ms
- Slope: 0.11 ms

**v7 Tune:**
- Offset: **3.30 ms** (increased by 62.6%)
- Slope: **0.17 ms** (increased by 54.5%)

**Analysis**: v7 accounts for different injector characteristics (likely larger/higher-flow injectors).

#### Cranking Fuel (inj_pw_cranking)
**Base File:**
- Range: 3.33 to 56.40 ms

**v7 Tune:**
- Range: **3.04 to 40.61 ms** (generally lower, but comment says "added 10% to base inj pulse crank")
- **Note**: Comment may refer to a different version or different interpretation

#### Cranking Throttle Factor (inj_pw_cranking_throttle_factor)
**Base File:**
- 0.0% to 50.0%

**v7 Tune:**
- 0.0% to **99.2%** (much higher compensation at high throttle during cranking)

---

## 3. BOOST CONTROL

### Boost Target (boost_target)
**Base File:**
- Range: 60.8 to 208.0 kPa
- Conservative boost curve

**v7 Tune:**
- Range: 60.8 to **199.5 kPa** (slightly lower peak, but more aggressive across the table)
- **Key differences**:
  - Row 1 (0 rpm): Same
  - Row 2 (2800 rpm): Base peaks at 208.0, v7 peaks at **199.5 kPa**
  - Row 3 (2900 rpm): Base peaks at 208.0, v7 peaks at **199.5 kPa**
  - Row 4 (3000 rpm): Base peaks at 208.0, v7 peaks at **199.5 kPa**
  - Row 5 (3100 rpm): Base peaks at 208.0, v7 peaks at **199.5 kPa**
  - Row 6 (3300 rpm): Base peaks at 208.0, v7 peaks at **199.5 kPa**
  - Row 7 (5400 rpm): Base peaks at 200.5, v7 peaks at **199.5 kPa**
  - Row 8 (6200 rpm): Base peaks at 200.5, v7 peaks at **199.5 kPa**

**Analysis**: v7 uses a more consistent, slightly lower peak boost target (199.5 kPa vs 208.0 kPa) but maintains higher boost across more of the RPM/TPS range.

### Boost Target Barometric Compensation (boost_target_baro_comp)
**Base File:**
- Range: -44.5% to 0.0% (active compensation)

**v7 Tune:**
- **All 0.0%** (compensation disabled - as noted in model doc, zero values = disabled)

**Analysis**: v7 disables barometric compensation, likely for consistent boost regardless of altitude.

### Boost Target TPS Index (boost_target_tps_index)
**Base File:**
- 0.00, 18.75, 21.88, 28.12, 34.38, 43.75, 53.12, 62.50%

**v7 Tune:**
- 0.00, **18.80, 21.90, 28.10, 34.40, 43.80, 53.10, 80.10%**
- **Extended TPS range** (last breakpoint: 80.10% vs 62.50%)

**Analysis**: v7 allows boost control at higher throttle positions.

---

## 4. WASTEGATE CONTROL

### Wastegate Base Duty (wg_base)
**Base File:**
- All 0.0% (wastegate fully closed at base)

**v7 Tune:**
- **0.0% to 80.5%** (aggressive wastegate control)
- Row 1 (0 rpm): 0.0% to 80.5%
- Rows 2-8: 0.0% to 7.0% at low TPS, up to 50.0% at high TPS

**Analysis**: v7 uses active wastegate control to achieve boost targets, while base relies on mechanical wastegate spring pressure.

### Wastegate Max Duty (wg_max)
**Base File:**
- Range: 0.0% to 90.6%

**v7 Tune:**
- Range: **0.0% to 90.6%** (same peak, but different distribution)
- Row 1: 0.0% to 90.6% (same)
- Rows 2-8: **10.2% to 60.2%** (more aggressive than base's 39.1-62.5%)

**Analysis**: v7 allows higher wastegate duty at lower RPM/TPS combinations.

### Wastegate IAT Compensation (wg_max_iat_comp)
**Base File:**
- Range: -10.2% to 1.6%

**v7 Tune:**
- Range: **-29.7% to 1.6%** (more aggressive compensation at low IAT)

**Analysis**: v7 reduces wastegate duty more aggressively at low intake temperatures.

### Wastegate Overboost/Underboost Steps
**Base File:**
- Overboost step: 3.1, 1.6, 0.8, 0.4%
- Underboost step: 3.1, 1.6, 0.8, 0.4%

**v7 Tune:**
- Overboost step: **4.3, 2.7, 2.0, 1.6%** (larger steps - more aggressive correction)
- Underboost step: **2.7, 1.2, 0.4, 0.0%** (smaller steps - less aggressive correction)

**Analysis**: v7 corrects overboost more aggressively but is gentler on underboost recovery.

### Wastegate Frequency (wg_freq)
**Base File:**
- 14.46 Hz

**v7 Tune:**
- **14.50 Hz** (slightly higher PWM frequency)

---

## 5. MAF SENSOR CALIBRATION

### MAF Scale (maf_scale)
**Base File:**
- 64 points: 0.00 to 250.00 g/s (clamped at 250 g/s)

**v7 Tune:**
- **64 points: 0.00 to 280.00 g/s** (extended range)
- Extended calibration points: 236.80, 242.97, 249.15, 255.31, 261.49, 267.65, 273.83, 280.00 g/s

**Analysis**: v7 supports higher airflow readings (likely for larger turbo or intake modifications).

### MAF Limit (maf_limit)
**Base File:**
- 250.00 g/s

**v7 Tune:**
- **500.00 g/s** (doubled limit)

**Analysis**: v7 allows much higher MAF readings before limiting.

---

## 6. LOAD MANAGEMENT

### Load Max (load_max)
**Base File:**
- Range: 1.28 to 2.54 g/rev (increases with RPM)

**v7 Tune:**
- **All 5.00 g/rev** (constant, very high limit)

**Analysis**: v7 allows much higher engine loads (nearly 2x the base maximum) to support higher power output.

---

## 7. KNOCK DETECTION

### Knock Retard Attack (knock_retard_attack)
**Base File:**
- -1.0° per event

**v7 Tune:**
- **-4.0° per event** (4x more aggressive retard when knock detected)

**Analysis**: v7 responds more aggressively to knock events for better protection.

### Knock Retard Decay (knock_retard_decay)
**Base File:**
- 0.2° per recovery

**v7 Tune:**
- **0.1° per recovery** (slower recovery - more conservative)

**Analysis**: v7 recovers spark advance more slowly after knock events.

---

## 8. LEARNED SPARK

### Learned Spark AT (learned_spark_at)
**Base File:**
- Range: 0.0° to 11.0° (moderate learning range)

**v7 Tune:**
- Range: **0.0° to 8.0°** (slightly reduced learning range)
- More conservative learned corrections

**Analysis**: v7 allows less learned spark advance, keeping timing more conservative.

### Learned Spark MT (learned_spark_mt)
Similar pattern - v7 has slightly reduced learning range (0-8° vs 0-11°).

---

## 9. IDLE CONTROL

### Idle Target (idle_target_at, idle_target_mt)
**Base File:**
- Range: 750-1700 rpm (varies by ECT and AC state)

**v7 Tune:**
- **850 rpm minimum** (higher idle speed)
- Many cells changed to 850 rpm (simplified, higher idle)

**Analysis**: v7 uses higher idle speed, likely for better stability with larger cams or other modifications.

### Idle Target Min AC (idle_target_min_ac_at, idle_target_min_ac_mt)
**Base File:**
- AT: 800, 0 rpm
- MT: 800 rpm

**v7 Tune:**
- AT: **850, 850 rpm**
- MT: **850 rpm**

**Analysis**: v7 maintains higher minimum idle with AC on.

---

## 10. WIDEBAND OXYGEN SENSOR

### Wideband Calibration (wideband_cal)
**Base File:**
- Range: 0.680 to 1.367 λ (16 points)

**v7 Tune:**
- Range: **0.500 to 1.523 λ** (extended range, different calibration)
- Different sensor or calibration curve

**Analysis**: v7 uses a different wideband sensor or calibration.

### Wideband Enable (wideband_enable)
**Base File:**
- 0 (disabled)

**v7 Tune:**
- **1 (enabled)**

**Analysis**: v7 enables wideband sensor for closed-loop fuel control.

### Wideband Filter (wideband_filter)
**Base File:**
- 100.0%

**v7 Tune:**
- **90.2%** (less filtering, faster response)

---

## 11. SPEED LIMITING

### Speed Limit (speed_limit)
**Base File:**
- 180, 182, 184, 186, 188 km/h (by gear)

**v7 Tune:**
- **180, 220, 230, 236, 240 km/h** (much higher limits in higher gears)

**Analysis**: v7 allows much higher speeds in gears 2-5.

### Speed Limit Boost (speed_limit_boost)
**Base File:**
- 236, 230, 220 km/h

**v7 Tune:**
- **250, 240, 230 km/h** (higher limits during boost)

---

## 12. CYLINDER-SPECIFIC SPARK

### Spark Cylinder Throttle (spark_cyl_throttle)
**Base File:**
- 0.78, 0.39%

**v7 Tune:**
- **0.80, 0.40%** (slightly different thresholds)

---

## 13. VDC TORQUE RATIO INDEX

### VDC Torque Ratio Index (vdc_torque_ratio_index)
**Base File:**
- 0.000 to 99.609 (16 points)

**v7 Tune:**
- **0.000 to 99.600** (slightly different last value: 99.600 vs 99.609)

---

## Summary of Tuning Philosophy

The v7 tune represents a **performance-oriented calibration** with the following characteristics:

1. **Extended Operating Range**: Supports higher loads (up to 2.74 g/rev), higher airflow (280 g/s), and higher speeds
2. **Aggressive Mid-Load Timing**: Up to 48° advance in mid-load regions for power
3. **Conservative High-Load Timing**: Retarded timing at high loads to prevent knock
4. **Richer Fueling**: More aggressive enrichment, especially in PE mode (0.667-0.892 λ vs 0.831-1.000 λ)
5. **Higher Boost Targets**: Consistent 199.5 kPa peak (slightly lower than base's 208.0 kPa peak, but more aggressive across the table)
6. **Active Wastegate Control**: Uses wastegate duty cycle control vs base's mechanical spring pressure
7. **More Aggressive Knock Response**: 4x faster retard on knock detection
8. **Higher Load Limits**: 5.00 g/rev vs 2.54 g/rev maximum
9. **Wideband Enabled**: Uses wideband O2 sensor for closed-loop control
10. **Higher Idle**: 850 rpm minimum vs 750-800 rpm in base

**Overall Assessment**: This is a **high-performance street/track tune** designed for a modified engine with:
- Larger turbocharger (higher airflow capacity)
- Larger injectors (higher latency values)
- Possibly larger cams (higher idle speed)
- Performance-oriented modifications requiring richer fueling and more conservative high-load timing

The tune prioritizes **power in mid-load regions** while maintaining **safety through conservative high-load timing and aggressive knock response**.

