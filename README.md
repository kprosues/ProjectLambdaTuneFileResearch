# Project Lambda Tune File Research

## Overview

This project contains a comprehensive analysis and model of ECU (Engine Control Unit) tune files for a JDM Subaru WRX STi EJ207 engine. The documentation provides detailed information about how each data section and table interacts to form a complete ECU calibration.

## Contents

- **`ECU_TUNE_FILE_MODEL.md`** - Comprehensive documentation of the ECU tune file structure, including:
  - 28 functional sections covering all aspects of engine control
  - 157 unique maps/parameters documented
  - Table relationships and dependencies
  - Inter-table calculation flows
  - Spark timing, fuel delivery, boost control, and safety systems

- **`example_tune_files/`** - Example ECU tune files:
  - `AF041_base.tune` - Base/reference tune (v1.6.33.2 - Latest Schema)
  - `Keith Proseus_1999JDMSTI_DW740_VF28_21builtStroker_v3.tune` - Tuned example (v1.6.32.1)
  - `Keith Proseus_1999JDMSTI_DW740_VF28_21builtStroker_v7_keith_edit.tune` - Tuned example (v1.6.36.2)

## File Format

ECU tune files are JSON-formatted calibration files containing:
- **Metadata**: Calibration ID, car ID, ROM ID, version information
- **Maps Array**: All tuning tables and parameters organized by function

## Key Features Documented

- **Spark/Ignition Timing** - Base spark tables, learned spark corrections, IAM calculations
- **Fuel Delivery** - Base fuel maps, Power Enrichment (PE) mode, compensations
- **Boost Control** - Wastegate control, boost targets, error handling
- **Safety Systems** - Knock detection, rev limiting, load limiting, speed limiting
- **Sensor Calibrations** - MAF, MAP, IAT, ECT, wideband oxygen sensor
- **Idle Control** - Adaptive idle air valve management

## Usage

Refer to `ECU_TUNE_FILE_MODEL.md` for detailed documentation on:
- How each table functions
- Table relationships and dependencies
- Calculation flows for fuel, spark, and boost
- Open questions about system interactions

## Quick Start: Fueling Analysis Script

Use `fueling_analysis.py` to analyze datalogs against a tune file and optionally write updated `fuel_base` values.

From the project root (with `venv` activated and `numpy`/`pandas` installed):

```bash
python fueling_analysis.py ^
  --tune "example_tune_files\Keith Proseus_1999JDMSTI_DW740_VF28_21builtStroker_v8.tune" ^
  --logs "datalogs\tuner_log_25-11-27_1038_V8.csv" ^
  --min-samples 20 ^
  --change-limit 5.0 ^
  --output "reports\fueling_report_v8.md" ^
  --output-tune "tunes\v8_fueling_updated.tune"
```

- **`--tune`**: Source tune used for analysis and as the baseline for `fuel_base` and change limits.  
- **`--logs`**: One or more CSV datalogs to analyze.  
- **`--output`**: Optional Markdown fueling summary.  
- **`--output-tune`**: Optional tune file with updated `fuel_base`.  
- **`--modify-tune`** (optional): Template tune for non-fuel tables; fuel_base always comes from `--tune`.

## Notes

- The system is configured for **MAF-only mode** - Speed Density (SD) tables are ignored
- All Speed Density related tables are documented but marked as not applicable
- The documentation includes open questions where detailed ECU logic is proprietary or unavailable

## Version Information

This analysis is based on the latest schema version **v1.6.33.2** as found in the base tune file.

