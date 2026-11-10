
from pathlib import Path
import pandas as pd

# Locate project files
PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_FILE = PROJECT_ROOT / "data" / "raw" / "patients.csv"
CLEANED_FILE = PROJECT_ROOT / "data" / "processed" / "patients_cleaned.csv"
REJECTED_FILE = PROJECT_ROOT / "data" / "processed" / "patients_rejected.csv"


def run_quality_checks():

    print("Starting healthcare data quality checks...\n")

    # Read source and transformed datasets
    raw = pd.read_csv(RAW_FILE)
    cleaned = pd.read_csv(CLEANED_FILE)
    rejected = pd.read_csv(REJECTED_FILE)

    results = {}

    # 1. Completeness check
    required_columns = ["patient_id", "first_name", "last_name"]

    results["Completeness"] = (
        cleaned[required_columns].notna().all().all()
    )

    # 2. Uniqueness check
    results["Uniqueness"] = (
        cleaned["patient_id"].is_unique
    )

    # 3. Date validity check
    date_columns = ["date_of_birth", "registration_date"]

    valid_dates = True

    for column in date_columns:
        parsed_dates = pd.to_datetime(
            cleaned[column],
            errors="coerce"
        )
        if parsed_dates.isna().any():
            valid_dates = False

    results["Date validity"] = valid_dates

    # 4. City consistency check
    valid_cities = (
        cleaned["city"].dropna()
        .eq(cleaned["city"].dropna().str.title())
        .all()
    )

    results["City consistency"] = valid_cities

    # 5. Email format check
    # Email is optional, but if provided it must be valid.
    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    provided_emails = cleaned["email"].dropna()

    results["Email validity"] = (
        provided_emails.str.fullmatch(email_pattern).all()
    )

    # 6. Business rule check
    dob = pd.to_datetime(cleaned["date_of_birth"], errors="coerce")
    registration = pd.to_datetime(
        cleaned["registration_date"],
        errors="coerce"
    )

    results["Business rules"] = (
        dob.notna().all()
        and registration.notna().all()
        and (dob <= registration).all()
    )

    # 7. Source-to-target reconciliation
    duplicate_count = raw.duplicated(
        subset=["patient_id"]
    ).sum()

    expected_count = (
        len(cleaned) + len(rejected) + duplicate_count
    )

    results["Record reconciliation"] = (
        len(raw) == expected_count
    )

    # Display results
    print("DATA QUALITY REPORT")
    print("-" * 40)

    for check_name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"{check_name}: {status}")

    print("-" * 40)

    print(f"Source records: {len(raw)}")
    print(f"Cleaned records: {len(cleaned)}")
    print(f"Rejected records: {len(rejected)}")
    print(f"Duplicate records: {duplicate_count}")

    passed_checks = sum(results.values())
    total_checks = len(results)

    print(f"\nChecks passed: {passed_checks}/{total_checks}")

    if all(results.values()):
        print("\nOverall result: ALL QUALITY CHECKS PASSED")
    else:
        print("\nOverall result: QUALITY ISSUES DETECTED")

        failed_checks = [
            name for name, passed in results.items() if not passed
        ]

        print("Failed checks:", failed_checks)


if __name__ == "__main__":
    run_quality_checks()
