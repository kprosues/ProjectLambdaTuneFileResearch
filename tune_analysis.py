#!/usr/bin/env python3
"""
Analyze datalog against tune file to identify areas for improvement.
Focuses on fuel trimming and boost control.
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path

def load_tune_file(tune_path):
    """Load and parse tune file."""
    with open(tune_path, 'r') as f:
        return json.load(f)

def get_map_value(tune_data, map_id):
    """Extract map data from tune file."""
    for map_entry in tune_data.get('maps', []):
        if map_entry.get('id') == map_id:
            return map_entry.get('data', [])
    return None

def analyze_datalog(datalog_path, tune_data):
    """Analyze datalog for fuel trim and boost control issues."""
    
    # Load datalog
    print(f"Loading datalog: {datalog_path}")
    df = pd.read_csv(datalog_path)
    
    print(f"Total data points: {len(df)}")
    print(f"Time span: {df['Time (s)'].min():.1f}s to {df['Time (s)'].max():.1f}s")
    
    # Filter out invalid data
    df = df[df['Engine Speed (rpm)'] > 0]
    df = df[df['Load (MAF) (g/rev)'] > 0]
    
    # Calculate boost error
    df['Boost Error (kPa)'] = df['Manifold Air Pressure - Filtered (kPa)'] - df['Boost Target (kPa)']
    
    # Identify operating regions
    df['Power Mode'] = df['Power Mode - Fuel Ratio Target (λ)'] < 1.0
    df['Closed Loop'] = ~df['Power Mode']
    
    # Analysis results
    results = {
        'fuel_trim_analysis': {},
        'boost_control_analysis': {},
        'lambda_analysis': {},
        'recommendations': []
    }
    
    # ===== FUEL TRIM ANALYSIS =====
    print("\n=== FUEL TRIM ANALYSIS ===")
    
    # Overall fuel trim stats
    stft_mean = df['Fuel Trim - Short Term (%)'].mean()
    stft_std = df['Fuel Trim - Short Term (%)'].std()
    stft_max = df['Fuel Trim - Short Term (%)'].abs().max()
    
    ltft_mean = df['Fuel Trim - Long Term (%)'].mean()
    ltft_std = df['Fuel Trim - Long Term (%)'].std()
    ltft_max = df['Fuel Trim - Long Term (%)'].abs().max()
    
    results['fuel_trim_analysis']['overall'] = {
        'stft_mean': float(stft_mean),
        'stft_std': float(stft_std),
        'stft_max': float(stft_max),
        'ltft_mean': float(ltft_mean),
        'ltft_std': float(ltft_std),
        'ltft_max': float(ltft_max)
    }
    
    print(f"STFT: Mean={stft_mean:.2f}%, Std={stft_std:.2f}%, Max Abs={stft_max:.2f}%")
    print(f"LTFT: Mean={ltft_mean:.2f}%, Std={ltft_std:.2f}%, Max Abs={ltft_max:.2f}%")
    
    # Analyze by RPM/Load bins
    rpm_bins = [0, 2000, 3000, 4000, 5000, 6000, 7000, 8000]
    load_bins = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    
    df['RPM_Bin'] = pd.cut(df['Engine Speed (rpm)'], bins=rpm_bins, labels=['0-2k', '2-3k', '3-4k', '4-5k', '5-6k', '6-7k', '7-8k'])
    df['Load_Bin'] = pd.cut(df['Load (MAF) (g/rev)'], bins=load_bins, labels=['0-0.5', '0.5-1.0', '1.0-1.5', '1.5-2.0', '2.0-2.5', '2.5-3.0'])
    
    # Find problematic areas
    trim_by_region = df.groupby(['RPM_Bin', 'Load_Bin']).agg({
        'Fuel Trim - Short Term (%)': ['mean', 'std', 'count'],
        'Fuel Trim - Long Term (%)': ['mean', 'std'],
        'Load (MAF) (g/rev)': 'mean',
        'Engine Speed (rpm)': 'mean'
    }).round(2)
    
    # Filter regions with significant trimming (>5% STFT or >3% LTFT)
    problematic_regions = []
    for idx, row in trim_by_region.iterrows():
        stft_mean = row[('Fuel Trim - Short Term (%)', 'mean')]
        ltft_mean = row[('Fuel Trim - Long Term (%)', 'mean')]
        count = row[('Fuel Trim - Short Term (%)', 'count')]
        
        if count > 50 and (abs(stft_mean) > 5 or abs(ltft_mean) > 3):
            problematic_regions.append({
                'rpm_bin': idx[0],
                'load_bin': idx[1],
                'stft_mean': float(stft_mean),
                'ltft_mean': float(ltft_mean),
                'sample_count': int(count),
                'avg_rpm': float(row[('Engine Speed (rpm)', 'mean')]),
                'avg_load': float(row[('Load (MAF) (g/rev)', 'mean')])
            })
    
    results['fuel_trim_analysis']['problematic_regions'] = problematic_regions
    
    print(f"\nFound {len(problematic_regions)} regions with significant fuel trimming:")
    for region in problematic_regions[:10]:  # Show top 10
        print(f"  {region['rpm_bin']} RPM, {region['load_bin']} Load: STFT={region['stft_mean']:.1f}%, LTFT={region['ltft_mean']:.1f}% (n={region['sample_count']})")
    
    # ===== BOOST CONTROL ANALYSIS =====
    print("\n=== BOOST CONTROL ANALYSIS ===")
    
    # Overall boost error stats
    boost_error_mean = df['Boost Error (kPa)'].mean()
    boost_error_std = df['Boost Error (kPa)'].std()
    boost_error_max = df['Boost Error (kPa)'].abs().max()
    
    results['boost_control_analysis']['overall'] = {
        'boost_error_mean': float(boost_error_mean),
        'boost_error_std': float(boost_error_std),
        'boost_error_max': float(boost_error_max)
    }
    
    print(f"Boost Error: Mean={boost_error_mean:.2f}kPa, Std={boost_error_std:.2f}kPa, Max Abs={boost_error_max:.2f}kPa")
    
    # Analyze boost control in boost regions (MAP > 100 kPa)
    boost_df = df[df['Manifold Air Pressure - Filtered (kPa)'] > 100].copy()
    
    if len(boost_df) > 0:
        print(f"\nBoost regions (MAP > 100kPa): {len(boost_df)} samples")
        
        # Boost error by RPM
        rpm_bins_boost = [0, 3000, 4000, 5000, 6000, 7000, 8000]
        boost_df['RPM_Bin_Boost'] = pd.cut(boost_df['Engine Speed (rpm)'], bins=rpm_bins_boost)
        
        boost_by_rpm = boost_df.groupby('RPM_Bin_Boost').agg({
            'Boost Error (kPa)': ['mean', 'std', 'count'],
            'Wastegate Duty Cycle (%)': ['mean', 'min', 'max'],
            'Boost Target (kPa)': 'mean',
            'Manifold Air Pressure - Filtered (kPa)': 'mean'
        }).round(2)
        
        print("\nBoost Error by RPM Range:")
        for idx, row in boost_by_rpm.iterrows():
            if pd.notna(idx):
                error_mean = row[('Boost Error (kPa)', 'mean')]
                wg_duty = row[('Wastegate Duty Cycle (%)', 'mean')]
                count = row[('Boost Error (kPa)', 'count')]
                print(f"  {idx}: Error={error_mean:.2f}kPa, WG Duty={wg_duty:.1f}%, Samples={int(count)}")
        
        # Identify overboost/underboost issues
        overboost = boost_df[boost_df['Boost Error (kPa)'] > 5]
        underboost = boost_df[boost_df['Boost Error (kPa)'] < -5]
        
        results['boost_control_analysis']['overboost_samples'] = len(overboost)
        results['boost_control_analysis']['underboost_samples'] = len(underboost)
        
        print(f"\nOverboost (>5kPa error): {len(overboost)} samples ({100*len(overboost)/len(boost_df):.1f}%)")
        print(f"Underboost (<-5kPa error): {len(underboost)} samples ({100*len(underboost)/len(boost_df):.1f}%)")
        
        # Wastegate duty cycle analysis
        wg_duty_mean = boost_df['Wastegate Duty Cycle (%)'].mean()
        wg_duty_max = boost_df['Wastegate Duty Cycle (%)'].max()
        wg_duty_min = boost_df['Wastegate Duty Cycle (%)'].min()
        
        results['boost_control_analysis']['wastegate'] = {
            'duty_mean': float(wg_duty_mean),
            'duty_max': float(wg_duty_max),
            'duty_min': float(wg_duty_min)
        }
        
        print(f"\nWastegate Duty: Mean={wg_duty_mean:.1f}%, Min={wg_duty_min:.1f}%, Max={wg_duty_max:.1f}%")
    
    # ===== LAMBDA ANALYSIS =====
    print("\n=== LAMBDA ANALYSIS ===")
    
    # Compare actual lambda to target
    df['Lambda Error'] = df['Air/Fuel Sensor #1 (λ)'] - df['Power Mode - Fuel Ratio Target (λ)']
    
    # Only analyze where we have a target (not 1.000 in power mode)
    power_mode_df = df[df['Power Mode']].copy()
    
    if len(power_mode_df) > 0:
        lambda_error_mean = power_mode_df['Lambda Error'].mean()
        lambda_error_std = power_mode_df['Lambda Error'].std()
        lambda_error_max = power_mode_df['Lambda Error'].abs().max()
        
        results['lambda_analysis']['power_mode'] = {
            'lambda_error_mean': float(lambda_error_mean),
            'lambda_error_std': float(lambda_error_std),
            'lambda_error_max': float(lambda_error_max),
            'samples': len(power_mode_df)
        }
        
        print(f"Power Mode Lambda Error: Mean={lambda_error_mean:.3f}, Std={lambda_error_std:.3f}, Max Abs={lambda_error_max:.3f}")
        print(f"Power Mode Samples: {len(power_mode_df)}")
    
    # Closed loop lambda (should be near 1.0)
    closed_loop_df = df[df['Closed Loop']].copy()
    if len(closed_loop_df) > 0:
        lambda_mean = closed_loop_df['Air/Fuel Sensor #1 (λ)'].mean()
        lambda_std = closed_loop_df['Air/Fuel Sensor #1 (λ)'].std()
        
        results['lambda_analysis']['closed_loop'] = {
            'lambda_mean': float(lambda_mean),
            'lambda_std': float(lambda_std),
            'samples': len(closed_loop_df)
        }
        
        print(f"Closed Loop Lambda: Mean={lambda_mean:.3f}, Std={lambda_std:.3f}")
        print(f"Closed Loop Samples: {len(closed_loop_df)}")
    
    # ===== GENERATE RECOMMENDATIONS =====
    print("\n=== GENERATING RECOMMENDATIONS ===")
    
    recommendations = []
    
    # Fuel trim recommendations
    if abs(ltft_mean) > 2:
        recommendations.append({
            'category': 'Fuel Trim',
            'priority': 'High',
            'issue': f'Long-term fuel trim is {ltft_mean:.1f}%, indicating systematic fueling error',
            'recommendation': 'Adjust fuel_base table in problematic regions to reduce LTFT toward 0%'
        })
    
    if stft_std > 3:
        recommendations.append({
            'category': 'Fuel Trim',
            'priority': 'Medium',
            'issue': f'Short-term fuel trim has high variability (std={stft_std:.1f}%)',
            'recommendation': 'Review fuel_base table for smoothness and consistency'
        })
    
    # Add specific region recommendations
    for region in problematic_regions[:5]:
        recommendations.append({
            'category': 'Fuel Trim',
            'priority': 'High',
            'issue': f'High fuel trimming at {region["avg_rpm"]:.0f} RPM, {region["avg_load"]:.2f} g/rev: STFT={region["stft_mean"]:.1f}%, LTFT={region["ltft_mean"]:.1f}%',
            'recommendation': f'Adjust fuel_base table at {region["avg_rpm"]:.0f} RPM, {region["avg_load"]:.2f} g/rev by approximately {-(region["stft_mean"] + region["ltft_mean"]):.1f}%'
        })
    
    # Boost control recommendations
    if len(boost_df) > 0:
        if boost_error_std > 3:
            recommendations.append({
                'category': 'Boost Control',
                'priority': 'High',
                'issue': f'Boost control has high variability (std={boost_error_std:.2f}kPa)',
                'recommendation': 'Review wastegate control parameters (wg_overboost_step, wg_underboost_step) and boost_target table'
            })
        
        if len(overboost) > len(boost_df) * 0.1:  # More than 10% overboost
            recommendations.append({
                'category': 'Boost Control',
                'priority': 'High',
                'issue': f'Frequent overboost events ({100*len(overboost)/len(boost_df):.1f}% of boost samples)',
                'recommendation': 'Increase wg_overboost_step values or reduce boost_target in affected regions'
            })
        
        if len(underboost) > len(boost_df) * 0.1:  # More than 10% underboost
            recommendations.append({
                'category': 'Boost Control',
                'priority': 'High',
                'issue': f'Frequent underboost events ({100*len(underboost)/len(boost_df):.1f}% of boost samples)',
                'recommendation': 'Increase wg_underboost_step values or adjust wg_base table to increase wastegate duty'
            })
        
        if wg_duty_max > 90:
            recommendations.append({
                'category': 'Boost Control',
                'priority': 'Medium',
                'issue': f'Wastegate duty cycle reaching maximum ({wg_duty_max:.1f}%)',
                'recommendation': 'Review wg_max table - may need higher limits or mechanical wastegate adjustment'
            })
    
    # Lambda recommendations
    if len(power_mode_df) > 0:
        if abs(lambda_error_mean) > 0.02:
            recommendations.append({
                'category': 'Lambda Control',
                'priority': 'High',
                'issue': f'Power mode lambda error: {lambda_error_mean:.3f} (target vs actual)',
                'recommendation': 'Adjust pe_initial and pe_safe tables to better match actual lambda'
            })
    
    results['recommendations'] = recommendations
    
    return results, df

def generate_report(results, tune_data, output_path):
    """Generate markdown report with recommendations."""
    
    report = []
    report.append("# Tune File Analysis Report")
    report.append("")
    report.append("## Executive Summary")
    report.append("")
    
    # Summary stats
    ft = results['fuel_trim_analysis']['overall']
    bc = results['boost_control_analysis'].get('overall', {})
    
    report.append(f"- **Long-Term Fuel Trim**: {ft['ltft_mean']:.2f}% (target: 0%)")
    report.append(f"- **Short-Term Fuel Trim**: {ft['stft_mean']:.2f}% ± {ft['stft_std']:.2f}%")
    report.append(f"- **Boost Error**: {bc.get('boost_error_mean', 0):.2f}kPa ± {bc.get('boost_error_std', 0):.2f}kPa")
    report.append(f"- **Problematic Fuel Regions**: {len(results['fuel_trim_analysis']['problematic_regions'])}")
    report.append("")
    
    # Fuel Trim Analysis
    report.append("## Fuel Trim Analysis")
    report.append("")
    report.append("### Overall Statistics")
    report.append("")
    report.append(f"- STFT Mean: {ft['stft_mean']:.2f}%")
    report.append(f"- STFT Std Dev: {ft['stft_std']:.2f}%")
    report.append(f"- STFT Max: {ft['stft_max']:.2f}%")
    report.append(f"- LTFT Mean: {ft['ltft_mean']:.2f}%")
    report.append(f"- LTFT Std Dev: {ft['ltft_std']:.2f}%")
    report.append(f"- LTFT Max: {ft['ltft_max']:.2f}%")
    report.append("")
    
    if results['fuel_trim_analysis']['problematic_regions']:
        report.append("### Problematic Regions")
        report.append("")
        report.append("| RPM Range | Load Range | STFT Mean | LTFT Mean | Samples |")
        report.append("|-----------|------------|-----------|-----------|---------|")
        for region in results['fuel_trim_analysis']['problematic_regions'][:10]:
            report.append(f"| {region['rpm_bin']} | {region['load_bin']} | {region['stft_mean']:.1f}% | {region['ltft_mean']:.1f}% | {region['sample_count']} |")
        report.append("")
    
    # Boost Control Analysis
    report.append("## Boost Control Analysis")
    report.append("")
    if bc:
        report.append(f"- Boost Error Mean: {bc.get('boost_error_mean', 0):.2f} kPa")
        report.append(f"- Boost Error Std Dev: {bc.get('boost_error_std', 0):.2f} kPa")
        report.append(f"- Boost Error Max: {bc.get('boost_error_max', 0):.2f} kPa")
        report.append("")
        
        wg = results['boost_control_analysis'].get('wastegate', {})
        if wg:
            report.append("### Wastegate Duty Cycle")
            report.append("")
            report.append(f"- Mean: {wg.get('duty_mean', 0):.1f}%")
            report.append(f"- Min: {wg.get('duty_min', 0):.1f}%")
            report.append(f"- Max: {wg.get('duty_max', 0):.1f}%")
            report.append("")
    
    # Recommendations
    report.append("## Recommendations")
    report.append("")
    
    for i, rec in enumerate(results['recommendations'], 1):
        report.append(f"### {i}. {rec['category']} - {rec['priority']} Priority")
        report.append("")
        report.append(f"**Issue**: {rec['issue']}")
        report.append("")
        report.append(f"**Recommendation**: {rec['recommendation']}")
        report.append("")
    
    # Write report
    with open(output_path, 'w') as f:
        f.write('\n'.join(report))
    
    print(f"\nReport written to: {output_path}")

if __name__ == '__main__':
    import sys
    
    tune_file = "example_tune_files/Keith Proseus_1999JDMSTI_DW740_VF28_21builtStroker_v10_20251203_155625.tune"
    datalog_file = "datalogs/tuner_log_25-12-03_1610_v10.csv"
    output_report = "tune_analysis_report.md"
    
    print("Loading tune file...")
    tune_data = load_tune_file(tune_file)
    
    print("Analyzing datalog...")
    results, df = analyze_datalog(datalog_file, tune_data)
    
    print("Generating report...")
    generate_report(results, tune_data, output_report)
    
    print("\nAnalysis complete!")

