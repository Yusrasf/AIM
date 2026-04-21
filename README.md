# AIM: Causal Analysis of Obesity and Type 2 Diabetes

This project studies whether obesity causally increases the probability of Type 2 Diabetes (T2D) using NHANES data and the `DoWhy` causal inference framework.

The workflow has two main stages:

1. Merge and clean multiple NHANES source files into one analysis-ready dataset.
2. Estimate the causal effect of obesity on T2D using a backdoor-adjusted causal model.

## Project Overview

The analysis is built around:

- Treatment: `Obese` where `BMI >= 30`
- Outcome: `T2D`
- Confounders: `Age`, `Sex`, `PA` (physical activity), `Diet`

The repository includes data preparation, causal graph definition, effect estimation, a placebo refutation test, and saved outputs for both the graph and the causal estimate.

## Repository Structure

```text
AIM/
|-- README.md
`-- AIM/
    |-- AIM.py
    |-- Data Cleaning Code.py
    |-- causal_dag.png
    |-- causal_results.txt
    |-- nhanes_cleaned.csv
    |-- DEMO_L.xpt
    |-- BMX_L.xpt
    |-- DIQ_L.xpt
    |-- PAQ_L.xpt
    |-- GHB_L.xpt
    |-- GLU_L.xpt
    `-- DR1TOT_L.xpt
```

## Data Sources

The project uses the following NHANES `.xpt` files:

- `DEMO_L.xpt`: demographic data
- `BMX_L.xpt`: body measurements, including BMI
- `DIQ_L.xpt`: diabetes questionnaire data
- `PAQ_L.xpt`: physical activity data
- `GHB_L.xpt`: HbA1c laboratory values
- `GLU_L.xpt`: blood glucose laboratory values
- `DR1TOT_L.xpt`: dietary intake / total calorie data

All files are merged on `SEQN`, the participant identifier.

## Data Preparation

The cleaning script is [Data Cleaning Code.py](d:/MASTER/Semester%202/Artificial%20Intelligence%20in%20Medicine/AIM%20project/AIM/AIM/Data%20Cleaning%20Code.py).

It:

- Loads the seven NHANES source files
- Merges them into a single dataframe
- Creates the main variables used in the analysis
- Defines `T2D` as positive when at least one of these is true:
  - `DIQ010 == 1`
  - `LBXGH >= 6.5`
  - `LBXGLU >= 126`
- Removes rows with missing values in the main analysis columns
- Saves the cleaned dataset as `nhanes_cleaned.csv`

Main derived variables:

- `BMI` from `BMXBMI`
- `Obese` from `BMI >= 30`
- `Age` from `RIDAGEYR`
- `Sex` from `RIAGENDR`
- `PA` from `PAD800`
- `Diet` from `DR1TKCAL`

## Causal Analysis

The main analysis script is [AIM.py](d:/MASTER/Semester%202/Artificial%20Intelligence%20in%20Medicine/AIM%20project/AIM/AIM/AIM.py).

It:

- Loads `nhanes_cleaned.csv`
- Recreates `Obese` as the binary treatment variable
- Defines a causal DAG with:
  - `Obese -> T2D`
  - `Age -> Obese`, `Age -> T2D`
  - `Sex -> Obese`, `Sex -> T2D`
  - `PA -> Obese`, `PA -> T2D`
  - `Diet -> Obese`, `Diet -> T2D`
- Estimates the Average Treatment Effect using `backdoor.propensity_score_weighting`
- Runs a placebo treatment refutation test
- Saves:
  - `causal_dag.png`
  - `causal_results.txt`

## Current Result

From [causal_results.txt](d:/MASTER/Semester%202/Artificial%20Intelligence%20in%20Medicine/AIM%20project/AIM/AIM/causal_results.txt):

- Estimated ATE: `0.1390`
- Interpretation: obesity is associated with an approximate 13.9 percentage-point increase in T2D probability in this model
- Placebo refutation p-value: `0.98`

This indicates the observed effect is not reproduced by a randomly permuted placebo treatment.

## Requirements

Install the required packages with:

```bash
pip install pandas matplotlib networkx dowhy
```

Depending on your Python environment, `dowhy` may pull in additional scientific dependencies.

## How to Run

Run the scripts from inside the `AIM/` subfolder because both scripts use local relative file paths.

### 1. Generate the cleaned dataset

```bash
cd AIM
python "Data Cleaning Code.py"
```

### 2. Run the causal analysis

```bash
python AIM.py
```

## Outputs

Running the full pipeline produces:

- `nhanes_cleaned.csv`: cleaned analysis dataset
- `causal_dag.png`: saved visualization of the causal DAG
- `causal_results.txt`: saved causal estimate and refutation output

## Notes and Limitations

- The causal estimate depends on the assumed DAG being appropriate.
- The model only adjusts for the observed confounders included in the scripts: `Age`, `Sex`, `PA`, and `Diet`.
- Any unmeasured confounding may bias the result.
- The repository is structured as a course-style analysis project rather than a packaged software application.

## Academic Context

This repository appears to be an Artificial Intelligence in Medicine course project focused on applying causal inference methods to biomedical data.
