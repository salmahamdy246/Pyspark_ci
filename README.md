## Project Overview

Processing incoming user transaction data using PySpark by filtering invalid records and calculating derived business metrics.
The project adheres to software engineering best practices by maintaining an automated unit test suite (`pytest`) and executing CI checks on pull requests targeting the `main` branch.

## Repository Structure

```text
Pyspark_ci/
│
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI workflow configuration
│
├── pyspark_job.py             # PySpark data transformation & cleaning job
├── test_pyspark_job.py        # Automated test suite using PyTest and PySpark
├── requirements.txt           # Python project dependencies
└── README.md                  # Project documentation
```

## Components & Business Logic

### 1. PySpark Data Job (`pyspark_job.py`)

The main processing function, `clean_data(df)`, executes the following operations:

* **Positive Amount Validation:** Drops records where `amount <= 0`.
* **Missing Value Handling:** Drops records where `name` is `NULL`.
* **Metric Calculation:** Adds an `amount_with_tax` column calculating a 20% tax (`amount * 1.20`).

### 2. Unit Testing Suite (`test_pyspark_job.py`)

The testing suite utilizes a localized PySpark session fixture to validate transformation logic:

* Verifies record filtering accuracy (`amount` and `name` checks).
* Validates output schema and row counts.
* Asserts exact float calculations for derived tax metrics using `pytest.approx`.

### 3. Continuous Integration Workflow (`.github/workflows/ci.yml`)

Automated pipeline triggered on pull requests targeting `main`. Workflow steps include:

1. Code checkout (`actions/checkout@v3`).
2. Setting up Java JDK 17 (`actions/setup-java@v3`) required by Apache Spark.
3. Setting up Python 3.10 (`actions/setup-python@v4`).
4. Installing project dependencies from `requirements.txt`.
5. Executing the `pytest` test suite.

## Implementation Guide

### Step 1: Local Development & Setup

1. Clone the repository:
   ```cmd
   git clone https://github.com/salmahamdy246/Pyspark_ci.git
   cd Pyspark_ci
   ```

2. Create virtual environment and install dependencies:
   ```cmd
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run local unit tests:
   ```cmd
   pytest test_pyspark_job.py
   ```

### Step 2: Triggering and Verifying the CI Pipeline

Because the GitHub Actions workflow is configured to trigger on `pull_request` events targeting `main`, the following feature-branch workflow was executed:

1. **Create and switch to a feature branch:**
   ```cmd
   git checkout -b feature/test-ci
   ```

2. **Commit changes and push to GitHub:**
   ```cmd
   git add .
   git commit -m "PySpark data pipeline with CI workflow"
   git push -u origin feature/test-ci
   ```

3. **Open a Pull Request:**
   * Navigate to the repository on GitHub.
   * Open a Pull Request from `feature/test-ci` into `main`.

4. **Automated Pipeline Execution:**
   * GitHub Actions automatically kicks off the `PySpark CI Testing Pipeline`.
   * Checks complete with a green pass status once all unit tests pass.

5. **Merge Pull Request:**
   * Merge `feature/test-ci` into `main` and clean up the feature branch.
