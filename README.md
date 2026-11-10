# Healthcare ETL Data Pipeline

## Project Overview

This project demonstrates an end-to-end ETL (Extract, Transform, Load) pipeline built using Python, Pandas, and PostgreSQL.

The pipeline processes healthcare data, performs data cleaning and quality validation, and loads the transformed data into a PostgreSQL database.

## Project Objectives

- Extract healthcare data from CSV files.
- Clean and transform raw datasets using Python and Pandas.
- Perform data quality checks to identify missing values and duplicate records.
- Load validated data into PostgreSQL.
- Implement logging and error handling for pipeline monitoring.

## Technologies Used

- **Programming Language:** Python
- **Data Processing:** Pandas
- **Database:** PostgreSQL
- **Database Connectivity:** SQLAlchemy / Psycopg
- **Development Environment:** Visual Studio Code
- **Version Control:** Git and GitHub

## ETL Pipeline Workflow

1. **Extract:** Read healthcare records from CSV files.
2. **Transform:** Clean, standardize, and prepare the data.
3. **Data Quality:** Validate records and identify data issues.
4. **Load:** Insert processed records into PostgreSQL.
5. **Logging:** Track pipeline execution and errors.

## Data Quality Checks

- Check for missing values.
- Identify duplicate records.
- Validate required columns.
- Verify data consistency before loading.

## Project Structure

```text
healthcare-etl-data-pipeline/
├── data/
│   ├── raw/
│   │   └── patients.csv
│   └── processed/
│       ├── clean_patients.csv
│       └── rejected_patients.csv
├── src/
│   ├── transform_patients.py
│   └── load_patients_to_db.py
├── tests/
├── sql/
├── logs/
├── requirements.txt
├── .gitignore
└── README.md
```

## How to Run the Project

1. Clone the GitHub repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the data transformation script:

   ```bash
   python src/transform_patients.py
   ```

5. Run the PostgreSQL loading script:

   ```bash
   python src/load_patients_to_db.py
   ```

6. Verify the loaded records in PostgreSQL.

## Key Learning Outcomes

- Building ETL pipelines using Python.
- Extracting and transforming healthcare datasets.
- Implementing data quality validation.
- Loading processed data into PostgreSQL.
- Implementing logging and error handling.
- Managing source code using Git and GitHub.