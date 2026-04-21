# Causal Analysis of Obesity and Type 2 Diabetes
Artificial Intelligence in Medicine - project

This project investigates whether obesity causally increases the probability of Type 2 Diabetes (T2D) using NHANES data and the `DoWhy` causal inference framework.

The workflow has two main stages:

1. Clean and merge multiple NHANES source files into a single analysis-ready dataset.
2. Estimate the causal effect of obesity on T2D using a backdoor-adjusted causal model.

## Project Overview

The analysis uses obesity as the treatment variable and T2D as the outcome:

- Treatment: `Obese` (`BMI >= 30`)
- Outcome: `T2D`
- Confounders: `Age`, `Sex`, `PA` (physical activity), `Diet`

The project builds a directed acyclic graph (DAG), estimates the Average Treatment Effect (ATE), runs a placebo refutation test, and saves both the graph and the numerical results.

## Repository Structure

```text
AIM/
├── README.md
└── AIM/
    ├── AIM.py
    ├── Data Cleaning Code.py
    ├── causal_dag.png
    ├── causal_results.txt
    ├── nhanes_cleaned.csv
    ├── DEMO_L.xpt
    ├── BMX_L.xpt
    ├── DIQ_L.xpt
    ├── PAQ_L.xpt
    ├── GHB_L.xpt
    ├── GLU_L.xpt
    └── DR1TOT_L.xpt
```

## Data Sources

The project uses NHANES `.xpt` files:

- `DEMO_L.xpt`: demographics
- `BMX_L.xpt`: body measures, including BMI
- `DIQ_L.xpt`: diabetes questionnaire
- `PAQ_L.xpt`: physical activity
- `GHB_L.xpt`: glycated hemoglobin (HbA1c)
- `GLU_L.xpt`: blood glucose
- `DR1TOT_L.xpt`: dietary intake / total calories

These files are merged on `SEQN`, the participant identifier.

## Data Preparation

The cleaning script is [Data Cleaning Code.py](d:/MASTER/Semester%202/Artificial%20Intelligence%20in%20Medicine/AIM%20project/AIM/AIM/Data%20Cleaning%20Code.py).

It performs the following steps:

- Loads the seven NHANES source files
- Merges them into one dataframe
- Creates analysis variables:
  - `BMI` from `BMXBMI`
  - `Obese` from `BMI >= 30`
  - `Age` from `RIDAGEYR`
  - `Sex` from `RIAGENDR`
  - `PA` from `PAD800`
  - `Diet` from `DR1TKCAL`
- Defines `T2D` as positive if any of the following are true:
  - self-reported diabetes (`DIQ010 == 1`)
  - HbA1c >= 6.5
  - fasting glucose >= 126
- Drops rows with missing values in the main analysis columns
- Saves the cleaned dataset as `nhanes_cleaned.csv`

## Causal Analysis

The main analysis script is [AIM.py](d:/MASTER/Semester%202/Artificial%20Intelligence%20in%20Medicine/AIM%20project/AIM/AIM/AIM.py).

It:

- Loads `nhanes_cleaned.csv`
- Recreates `Obese` as a binary treatment variable
- Defines the causal DAG:
  - `Obese -> T2D`
  - `Age -> Obese`, `Age -> T2D`
  - `Sex -> Obese`, `Sex -> T2D`
  - `PA -> Obese`, `PA -> T2D`
  - `Diet -> Obese`, `Diet -> T2D`
- Estimates the ATE using `backdoor.propensity_score_weighting`
- Runs a placebo treatment refutation test
- Saves:
  - `causal_dag.png`
  - `causal_results.txt`

## Current Result

From [causal_results.txt](d:/MASTER/Semester%202/Artificial%20Intelligence%20in%20Medicine/AIM%20project/AIM/AIM/causal_results.txt):

- Estimated ATE: `0.1390`
- Interpretation: obesity is associated with an approximately 13.9 percentage-point increase in T2D probability in this model
- Placebo refutation p-value: `0.98`

This supports that the estimated effect is not reproduced by a random placebo treatment.

## Requirements

Install the required Python packages:

```bash
pip install pandas matplotlib networkx dowhy
```

Depending on your environment, `dowhy` may also install additional scientific Python dependencies automatically.

## How to Run

Run the scripts from inside the `AIM/` subfolder, because the file paths in the code are relative to that directory.

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

After running the pipeline, the main generated outputs are:

- `nhanes_cleaned.csv`: cleaned analysis dataset
- `causal_dag.png`: visual representation of the assumed causal structure
- `causal_results.txt`: estimated causal effect and refutation results

## Notes and Limitations

- The analysis assumes no important unmeasured confounders beyond `Age`, `Sex`, `PA`, and `Diet`.
- The validity of the causal estimate depends on the correctness of the DAG and variable definitions.
- The scripts currently use local relative paths and are designed for a simple folder-based workflow rather than a packaged application.

## Academic Context

This repository appears structured as a course project for Artificial Intelligence in Medicine, focused on applying causal inference methods to a real biomedical dataset.
