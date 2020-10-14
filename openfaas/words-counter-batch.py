from datetime import datetime, timedelta
from dateutil.tz import tzutc, UTC
import boto3

REGION = "eu-west-3"
BUCKET_NAME = "bpserverlessdemo"

s3 = boto3.resource(
    's3',
    region_name = REGION
)
bucket = s3.Bucket(BUCKET_NAME)

for object in bucket.objects.all():
    if object.last_modified > datetime.now(tzutc()) - timedelta(hours = 24):
        # <download the file>
        # <send it to words counter in openfaas>
        # <save to database>