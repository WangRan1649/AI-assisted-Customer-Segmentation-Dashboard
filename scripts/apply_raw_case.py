from pathlib import Path
import argparse
import shutil
import sys
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]

CASES_DIR = ROOT / "data" / "demo_cases"
TARGET_RAW = ROOT / "data" / "raw" / "ecommerce_user_behavior_dataset.csv"
BACKUP_DIR = ROOT / "_case_switch_backup"


def list_cases():
    if not CASES_DIR.exists():
        return []
    return sorted(
        p.name for p in CASES_DIR.iterdir()
        if p.is_dir() and (p / "raw.csv").exists()
    )


def print_cases():
    cases = list_cases()
    print("Available raw data cases:")
    if not cases:
        print("  No cases found.")
        print(f"  Expected folder: {CASES_DIR}")
        return

    for case in cases:
        print(f"  - {case}")

    print()
    print("Usage:")
    print(r"  .venv\Scripts\python.exe scripts\apply_raw_case.py baseline_original")
    print(r"  .venv\Scripts\python.exe scripts\apply_raw_case.py apparel_vip_shift")


def main():
    parser = argparse.ArgumentParser(
        description="Apply only the raw.csv of a demo case to the active raw data source."
    )
    parser.add_argument(
        "case_name",
        nargs="?",
        help="Demo case name under data/demo_cases, for example: apparel_vip_shift",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available demo cases.",
    )

    args = parser.parse_args()

    if args.list or not args.case_name:
        print_cases()
        return 0

    case_dir = CASES_DIR / args.case_name
    source_raw = case_dir / "raw.csv"

    if not case_dir.exists():
        print(f"ERROR: Case folder does not exist: {case_dir}")
        print()
        print_cases()
        return 1

    if not source_raw.exists():
        print(f"ERROR: raw.csv not found in case folder: {source_raw}")
        return 1

    if not TARGET_RAW.exists():
        print(f"ERROR: Target raw file does not exist: {TARGET_RAW}")
        return 1

    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_raw = BACKUP_DIR / f"raw_before_{args.case_name}_{timestamp}.csv"

    shutil.copy2(TARGET_RAW, backup_raw)
    shutil.copy2(source_raw, TARGET_RAW)

    print("Raw data source switched successfully.")
    print(f"Case name: {args.case_name}")
    print(f"Source raw: {source_raw}")
    print(f"Target raw: {TARGET_RAW}")
    print(f"Backup saved: {backup_raw}")
    print()
    print("Next step:")
    print(r"  .venv\Scripts\python.exe run_pipeline.py --provider mock")
    print()
    print("Then refresh Power BI:")
    print("  Home -> Refresh")

    return 0


if __name__ == "__main__":
    sys.exit(main())