import json
from datetime import datetime
import string
import random
import mysql.connector
import boto3
import os

ENDPOINT = "eg-serverlessdemo.ctsehct8fg1i.eu-west-3.rds.amazonaws.com"
PORT = "3306"
USR = "admin"
REGION = "eu-west-3"
DBNAME = "serverlessdemo"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

# gets the credentials from .aws/credentials
session = boto3.session.Session(profile_name='RDSCreds')
client = boto3.client('rds')
token = client.generate_db_auth_token(
    DBHostname=ENDPOINT, Port=PORT,
    DBUsername=USR,
    Region=REGION
)

try:
    conn = mysql.connector.connect(
        host=ENDPOINT,
        user=USR,
        passwd=token,
        port=PORT,
        database=DBNAME
    )
    cur = conn.cursor()
    cur.execute("""SELECT now()""")
    query_results = cur.fetchall()
    print(query_results)
except Exception as e:
    print("Database connection failed due to {}".format(e))


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket = str(event["Records"][0]["s3"]["bucket"]["name"])
    key = str(event["Records"][0]["s3"]["object"]["key"])
    input_file = os.path.join(bucket, key)
    obj = s3.get_object(Bucket=bucket, Key=key)
    body_len = len(obj['Body'].read().decode('utf-8').split("\n"))

    cur.execute(
        '''
        create table if not exists Lines
        (
            ID string NOT NULL,
            ObjectPath varchar(255) NOT NULL,
            Date DATETIME NOT NULL,
            AmountOfLines int NOT NULL,
            PRIMARY KEY (ID))
        )
        '''
    )

    cur.execute(
        f'''
        insert into Lines (ID, ObjectPath, Date, AmountOfLines) 
        values("{id_generator()}", "{input_file}","{datetime.now()}","{body_len}")
        '''
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
