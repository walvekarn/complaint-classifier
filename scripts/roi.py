#!/usr/bin/env python3
"""
ROI Calculator for Complaint Classification System
Author: Nikita Walvekar (walvekarn)

Calculates time and cost savings from automating complaint classification.
Uses realistic ranges to provide illustrative impact estimates.
"""

import argparse
import sys


def calculate_roi(
    cases_per_year: int,
    minutes_per_manual_case: float = 6.0,
    hourly_cost: float = 30.0,
    auto_rate: float = 0.5,
    seconds_per_case_auto: float = 3.0
):
    """
    Calculate ROI metrics for complaint classification automation.
    
    Args:
        cases_per_year: Number of complaints processed annually
        minutes_per_manual_case: Time per manual classification (5-7 minutes typical)
        hourly_cost: Labor cost per hour (USD)
        auto_rate: Percentage of cases automated (0.0-1.0)
        seconds_per_case_auto: Processing time per automated case
        
    Returns:
        Dictionary with ROI metrics
    """
    
    # Manual processing (baseline)
    manual_hours_total = (cases_per_year * minutes_per_manual_case) / 60
    manual_cost_total = manual_hours_total * hourly_cost
    
    # Automated processing
    automated_cases = int(cases_per_year * auto_rate)
    manual_cases_remaining = cases_per_year - automated_cases
    
    auto_hours = (automated_cases * seconds_per_case_auto) / 3600
    manual_hours_remaining = (manual_cases_remaining * minutes_per_manual_case) / 60
    
    total_hours_with_automation = auto_hours + manual_hours_remaining
    total_cost_with_automation = total_hours_with_automation * hourly_cost
    
    # Savings
    hours_saved = manual_hours_total - total_hours_with_automation
    cost_saved = manual_cost_total - total_cost_with_automation
    
    # Percentages
    hours_saved_pct = (hours_saved / manual_hours_total) * 100 if manual_hours_total > 0 else 0
    cost_saved_pct = (cost_saved / manual_cost_total) * 100 if manual_cost_total > 0 else 0
    
    return {
        "cases_per_year": cases_per_year,
        "automated_cases": automated_cases,
        "automation_rate": auto_rate * 100,
        "manual_hours_baseline": manual_hours_total,
        "manual_cost_baseline": manual_cost_total,
        "hours_with_automation": total_hours_with_automation,
        "cost_with_automation": total_cost_with_automation,
        "hours_saved": hours_saved,
        "cost_saved": cost_saved,
        "hours_saved_pct": hours_saved_pct,
        "cost_saved_pct": cost_saved_pct,
        "hourly_cost": hourly_cost,
        "minutes_per_manual": minutes_per_manual_case,
        "seconds_per_auto": seconds_per_case_auto
    }


def print_roi_report(metrics: dict):
    """Print a formatted ROI report."""
    
    print("\n" + "=" * 70)
    print("COMPLAINT CLASSIFIER ROI ANALYSIS")
    print("=" * 70)
    
    print("\n📊 INPUT PARAMETERS")
    print("-" * 70)
    print(f"  Annual complaint volume:       {metrics['cases_per_year']:,} cases")
    print(f"  Automation rate:               {metrics['automation_rate']:.0f}%")
    print(f"  Manual processing time:        {metrics['minutes_per_manual']:.1f} min/case")
    print(f"  Automated processing time:     {metrics['seconds_per_auto']:.1f} sec/case")
    print(f"  Labor cost:                    ${metrics['hourly_cost']:.2f}/hour")
    
    print("\n📈 BASELINE (100% Manual Processing)")
    print("-" * 70)
    print(f"  Total hours required:          {metrics['manual_hours_baseline']:,.0f} hours/year")
    print(f"  Total cost:                    ${metrics['manual_cost_baseline']:,.2f}/year")
    
    print("\n⚡ WITH AUTOMATION")
    print("-" * 70)
    print(f"  Automated cases:               {metrics['automated_cases']:,} cases")
    print(f"  Manual cases remaining:        {metrics['cases_per_year'] - metrics['automated_cases']:,} cases")
    print(f"  Total hours required:          {metrics['hours_with_automation']:,.0f} hours/year")
    print(f"  Total cost:                    ${metrics['cost_with_automation']:,.2f}/year")
    
    print("\n💰 ESTIMATED SAVINGS")
    print("-" * 70)
    print(f"  Time saved:                    {metrics['hours_saved']:,.0f} hours/year ({metrics['hours_saved_pct']:.1f}%)")
    print(f"  Cost saved:                    ${metrics['cost_saved']:,.2f}/year ({metrics['cost_saved_pct']:.1f}%)")
    
    # FTE calculation (assuming 2080 work hours per year)
    fte_saved = metrics['hours_saved'] / 2080
    print(f"  Equivalent FTE saved:          {fte_saved:.2f} full-time employees")
    
    print("\n⚠️  NOTE: These are illustrative estimates based on assumptions.")
    print("    Actual results will vary based on implementation and workflows.")
    print("=" * 70 + "\n")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Calculate ROI for complaint classification automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Calculate for 100k cases/year at 50% automation
  python scripts/roi.py --cases 100000 --auto-rate 0.5

  # Conservative estimate (7 min/case, 30% automation)
  python scripts/roi.py --cases 284500 --minutes 7 --auto-rate 0.3

  # Optimistic estimate (5 min/case, 70% automation)
  python scripts/roi.py --cases 284500 --minutes 5 --auto-rate 0.7 --hourly-cost 35

Typical ranges:
  - Manual time: 5-7 minutes per case
  - Automation rate: 30-70% (depends on complaint complexity)
  - Hourly cost: $25-50 (depends on location and seniority)
        """
    )
    
    parser.add_argument(
        "--cases",
        type=int,
        required=True,
        help="Number of complaints processed per year"
    )
    
    parser.add_argument(
        "--minutes",
        type=float,
        default=6.0,
        help="Minutes per manual case (typical range: 5-7, default: 6.0)"
    )
    
    parser.add_argument(
        "--hourly-cost",
        type=float,
        default=30.0,
        help="Labor cost per hour in USD (default: 30.0)"
    )
    
    parser.add_argument(
        "--auto-rate",
        type=float,
        default=0.5,
        help="Automation rate as decimal (0.0-1.0, default: 0.5 for 50%%)"
    )
    
    parser.add_argument(
        "--seconds-auto",
        type=float,
        default=3.0,
        help="Seconds per automated case (default: 3.0)"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    
    args = parser.parse_args()
    
    # Validation
    if args.minutes < 1 or args.minutes > 60:
        print("Error: --minutes must be between 1 and 60", file=sys.stderr)
        sys.exit(1)
    
    if args.auto_rate < 0 or args.auto_rate > 1:
        print("Error: --auto-rate must be between 0.0 and 1.0", file=sys.stderr)
        sys.exit(1)
    
    if args.hourly_cost <= 0:
        print("Error: --hourly-cost must be positive", file=sys.stderr)
        sys.exit(1)
    
    # Calculate ROI
    metrics = calculate_roi(
        cases_per_year=args.cases,
        minutes_per_manual_case=args.minutes,
        hourly_cost=args.hourly_cost,
        auto_rate=args.auto_rate,
        seconds_per_case_auto=args.seconds_auto
    )
    
    # Output
    if args.json:
        import json
        print(json.dumps(metrics, indent=2))
    else:
        print_roi_report(metrics)


if __name__ == "__main__":
    main()

