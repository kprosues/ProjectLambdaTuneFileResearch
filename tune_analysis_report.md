# Tune File Analysis Report

## Executive Summary

- **Long-Term Fuel Trim**: -0.32% (target: 0%)
- **Short-Term Fuel Trim**: -1.72% ± 5.48%
- **Boost Error**: -61.27kPa ± 20.66kPa
- **Problematic Fuel Regions**: 0

## Fuel Trim Analysis

### Overall Statistics

- STFT Mean: -1.72%
- STFT Std Dev: 5.48%
- STFT Max: 25.00%
- LTFT Mean: -0.32%
- LTFT Std Dev: 0.87%
- LTFT Max: 3.12%

## Boost Control Analysis

- Boost Error Mean: -61.27 kPa
- Boost Error Std Dev: 20.66 kPa
- Boost Error Max: 81.00 kPa

### Wastegate Duty Cycle

- Mean: 7.5%
- Min: 0.0%
- Max: 80.1%

## Recommendations

### 1. Fuel Trim - Medium Priority

**Issue**: Short-term fuel trim has high variability (std=5.5%)

**Recommendation**: Review fuel_base table for smoothness and consistency

### 2. Boost Control - High Priority

**Issue**: Boost control has high variability (std=20.66kPa)

**Recommendation**: Review wastegate control parameters (wg_overboost_step, wg_underboost_step) and boost_target table

### 3. Boost Control - High Priority

**Issue**: Frequent overboost events (75.8% of boost samples)

**Recommendation**: Increase wg_overboost_step values or reduce boost_target in affected regions

### 4. Boost Control - High Priority

**Issue**: Frequent underboost events (14.8% of boost samples)

**Recommendation**: Increase wg_underboost_step values or adjust wg_base table to increase wastegate duty
