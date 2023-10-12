# cresta-challenge

## Prereqs
Make sure you have all env vars set up in settings for Github runner or as `.env` file in folder

## How to run
1. `source .env` 
2. `pip3 install -r requirements.txt`
3. `python main.py`

## Assumptions
1. We are given an AWS_ACCESS_KEY and AWS_SECRET_KEY where we do not need to assume role to put to s3
2. All calls that end on the targeted date are exported. I.E if a call starts on 2023-10-12 and ends on 2023-10-13, then it is counted as a phone call that occured on 2023-10-13
3. `cresta-data-dump` bucket with correct permissions already exists on user AWS account(we should have a terraform module/cloudformation template for them to use)
4. IP addresses for github actions are whitelisted to Clickhouse DB



