from datetime import datetime, timedelta
from dateutil.tz import tzutc
import boto3
import requests
import pymongo


'''
curl --header "X-Vault-Token: s.A946lZFDo7WOrX9v39d5Gf6h" \
     --request GET 'http://127.0.0.1:8200/v1/kv-v1/db'
'''
vault_header = {'X-Vault-Token': 's.A946lZFDo7WOrX9v39d5Gf6h'}
response = requests.get(
    'http://127.0.0.1:8200/v1/kv-v1/db',
    headers= vault_header
)
result = response.json()
DB_PASS = result['data']['pass']
DB_NAME = result['data']['dbname']
client = pymongo.MongoClient(
    f"mongodb+srv://admin:{DB_PASS}@cluster0.14ono.mongodb.net/{DB_NAME}?retryWrites=true&w=majority",
    ssl=True,
    ssl_cert_reqs='CERT_NONE'
)

REGION = "eu-west-3"
BUCKET_NAME = "bpserverlessdemo"
s3 = boto3.resource(
    's3',
    region_name=REGION
)

for s3object in s3.Bucket(BUCKET_NAME).objects.all():
    # TODO change to '>' before creating cron
    if s3object.last_modified < datetime.now(tzutc()) - timedelta(hours=24):
        # <download the file> ?? --> bucket.download_file(s3object.key, s3object.key)
        # <send it to words counter in openfaas>
        # <save to database>
        response = requests.post(
            'http://127.0.0.1:8080/function/word-counter.openfaas-fn',
            data=s3object.get()['Body'].read()
        )
        numOfWords = response.json()
        db = client.serverlessdemodb
        db.Words.insert_one({
            "ObjectPath": f'''{s3object.bucket_name}/{s3object.key}''',
            "Date": datetime.now(),
            "AmountOfWords": numOfWords
        })
        print(f'''
            S3 FILE ({s3object.key}) 
            WORDS COUNT ({numOfWords}) 
            HAS BEEN SUCCESSFULLY PERSISTED TO MONGODB
        ''')
