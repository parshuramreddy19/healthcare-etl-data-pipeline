
from pathlib import Path
import pandas as pd

# Define project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_FILE = PROJECT_ROOT / "data" / "raw" / "patients.csv"
PROCESSED_FILE = PROJECT_ROOT / "data" / "processed" / "patients_cleaned.csv"
REJECTED_FILE = PROJECT_ROOT / "data" / "processed" / "patients_rejected.csv"


def extract_data():
    """Extract patient records from the raw CSV file."""
    print("Extracting patient data...")

    df = pd.read_csv(RAW_FILE)

    print(f"Records extracted: {len(df)}")
    return df


def transform_data(df):
    """Clean and validate patient records."""

    print("\nStarting data transformation...")

    initial_count = len(df)

    # Remove leading and trailing spaces
    for column in df.select_dtypes(include=["object"]).columns:
        df[column] = df[column].str.strip()

    # Convert empty strings into missing values
    df = df.replace("", pd.NA)

    # Standardize city names
    df["city"] = df["city"].str.title()

    # Remove duplicate patient IDs
    before_deduplication = len(df)

    df = df.drop_duplicates(
        subset=["patient_id"],
        keep="first"
    ).copy()

    duplicates_removed = before_deduplication - len(df)

    # Validate mandatory fields
    required_columns = [
        "patient_id",
        "first_name",
        "last_name"
    ]

    rejected = df[df[required_columns].isna().any(axis=1)].copy()

    # Keep only valid records
    cleaned = df.drop(index=rejected.index).copy()

    # Convert dates into standard format
    date_columns = [
        "date_of_birth",
        "registration_date"
    ]

    for column in date_columns:
        cleaned[column] = pd.to_datetime(
            cleaned[column],
            errors="coerce"
        ).dt.strftime("%Y-%m-%d")

    print(f"Original records: {initial_count}")
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Rejected records: {len(rejected)}")
    print(f"Clean records: {len(cleaned)}")

    return cleaned, rejected


def load_data(cleaned, rejected):
    """Save cleaned and rejected records."""

    PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)

    cleaned.to_csv(PROCESSED_FILE, index=False)
    rejected.to_csv(REJECTED_FILE, index=False)

    print("\nData loading completed!")
    print(f"Cleaned data saved to: {PROCESSED_FILE}")
    print(f"Rejected data saved to: {REJECTED_FILE}")


def main():
    raw_data = extract_data()

    cleaned_data, rejected_data = transform_data(raw_data)

    load_data(cleaned_data, rejected_data)


if __name__ == "__main__":
    main()
