import json
import datetime
import string
import random
import boto3
from package import pymysql
import os

ENDPOINT = "serverlessdemo.ctsehct8fg1i.eu-west-3.rds.amazonaws.com"
PORT = 3306
USR = "admin"
PWD = "[SECRET]"
REGION = "eu-west-3"
DBNAME = "serverlessdemodb"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket = str(event["Records"][0]["s3"]["bucket"]["name"])
    key = str(event["Records"][0]["s3"]["object"]["key"])
    input_file = os.path.join(bucket, key)
    file_obj = s3.get_object(Bucket = bucket, Key = key)
    body_len = len(
        file_obj['Body']
            .read()
            .decode('utf-8')
            .split("\n")
    )

    try:
        connection = pymysql.connect(
            host = ENDPOINT,
            user = USR,
            passwd = PWD,
            port = PORT,
            database = DBNAME
        )

        with connection.cursor() as cursor:
            cursor.execute("""SELECT now()""")
            query_results = cursor.fetchall()
            print(query_results)

            cursor.execute(
                f'''
                create table if not exists `Lines` (
                  Id VARCHAR(255) NOT NULL,
                  ObjectPath VARCHAR(255) NOT NULL,
                  Date DATE NOT NULL,
                  AmountOfLines BIGINT(8) NOT NULL,
                  PRIMARY KEY (Id)
                )
                '''
            )
            result = cursor.fetchone()
            print(result)

            cursor.execute(
                f'''
                insert into
                  `Lines` (Id, ObjectPath, Date, AmountOfLines)
                values(
                    "{id_generator()}",
                    "{input_file}",
                    "{datetime.datetime.now()}",
                    {body_len}
                  )
                '''
            )
            result = cursor.fetchone()
            print(result)

        connection.commit()

        print(f'''
            insert into
              `Lines` (Id, ObjectPath, Date, AmountOfLines)
            values(
                "{id_generator()}",
                "{input_file}",
                "{datetime.datetime.now()}",
                {body_len}
              )
        ''')
    except Exception as e:
        print("Database connection failed due to {}".format(e))
    finally:
        connection.close()

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
