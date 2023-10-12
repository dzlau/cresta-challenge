import boto3
import os
import clickhouse_connect
import csv
from datetime import datetime, timedelta
# check env vars
try:
    AWS_ACCESS_KEY=os.environ["AWS_ACCESS_KEY"]
    AWS_SECRET_KEY=os.environ["AWS_SECRET_KEY"]
    CLICKBASE_HOST=os.environ["CLICKBASE_HOST"]
    CLICKBASE_USER=os.environ["CLICKBASE_USER"]
    CLICKBASE_PASSWORD=os.environ["CLICKBASE_PASSWORD"]
    CLICKBASE_PORT=os.environ["CLICKBASE_PORT"]
except Exception as e:
    print("Make sure to set proper env vars")
    raise
print(CLICKBASE_HOST)
# quantile 0.9 means "value should over-predict 90% of the times"
query="""SELECT agent_id,AVG(call_duration_sec),quantile(0.9)(call_duration_sec) 
        FROM conversations where toDate(call_end)=toDate(yesterday()) 
        AND call_status='Answered' 
        GROUP BY agent_id"""

# Connect to DB
client = clickhouse_connect.get_client(host=CLICKBASE_HOST,port=8443, 
                                 username=CLICKBASE_USER, password=CLICKBASE_PASSWORD)
# query results
results = client.query(query)
# clean data into list of dict
data = [{'uuid':result[0],'avg_time':result[1], '90th_percentile':result[2]} for result in results.result_rows]

# connect to boto3
s3 = boto3.resource('s3',aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY)

bucket = "cresta-daily-dump"
yesterday = datetime.now() - timedelta(days=1)
filename = f"{yesterday.strftime('%Y-%m-%d')}.csv"

# generate csv for boto upload
with open(filename, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
# upload to boto3
s3.meta.client.upload_file(Filename = filename, Bucket= bucket, Key = filename)
