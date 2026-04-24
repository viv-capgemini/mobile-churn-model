# DVC — Data Version Control

Data files and the trained model are versioned with DVC and stored in S3.

## Initialise DVC

```bash
dvc init
git add .dvc .dvcignore
git commit -m "Initialise DVC"
```

## Configure S3 Remote

```bash
dvc remote add -d s3remote s3://your-bucket-name/mobile-churn-model
dvc remote modify s3remote region eu-west-2   # update to your bucket's region
git add .dvc/config
git commit -m "Add DVC S3 remote"
```

## Authenticate with AWS

```bash
# Option 1 — AWS CLI (recommended)
aws configure

# Option 2 — environment variables
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=eu-west-2
```

## Run the Pipeline

```bash
# Run all stages (generate data → build features → train model)
dvc repro

# Check pipeline status
dvc status
```

## Push Files to S3

```bash
# Push all DVC-tracked files (CSV data + model)
dvc push

# Push a specific file
dvc push data/raw/customers.csv
dvc push models/churn_model.pkl
```

## Pull Files from S3

```bash
# Pull all tracked files
dvc pull

# Pull a specific file
dvc pull data/raw/customers.csv
dvc pull models/churn_model.pkl
```

## Upload Directly with AWS CLI (without DVC)

```bash
# Upload data files
aws s3 cp data/raw/customers.csv s3://your-bucket-name/mobile-churn-model/data/raw/customers.csv
aws s3 cp data/features/features.csv s3://your-bucket-name/mobile-churn-model/data/features/features.csv

# Upload model
aws s3 cp models/churn_model.pkl s3://your-bucket-name/mobile-churn-model/models/churn_model.pkl

# Sync entire data and models directories
aws s3 sync data/ s3://your-bucket-name/mobile-churn-model/data/
aws s3 sync models/ s3://your-bucket-name/mobile-churn-model/models/
```

> **Note:** `dvc push`/`dvc pull` is preferred over direct AWS CLI uploads as it keeps file versions in sync with Git commits.
