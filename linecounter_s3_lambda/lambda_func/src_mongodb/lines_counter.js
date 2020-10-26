"use strict";
const AWS = require('aws-sdk');
const s3 = new AWS.S3();
const { v4: uuidv4 } = require('uuid');


`
curl --header "X-Vault-Token: s.A946lZFDo7WOrX9v39d5Gf6h" \
     --request GET 'http://127.0.0.1:8200/v1/kv-v1/db'
`

const DB_PASS = result['data']['pass']
const DB_NAME = result['data']['dbname']
const MongoClient = require('mongodb').MongoClient;
const uri = `mongodb+srv://admin:${DB_PASS}@cluster0.14ono.mongodb.net/${DB_NAME}?retryWrites=true&w=majority`;
const client = new MongoClient(uri, { useNewUrlParser: true });


exports.handler = async (event, context, callback) => {
    context.callbackWaitsForEmptyEventLoop = false;
    console.log('event: ', event);
    
    const bucket = event.Records[0].s3.bucket.name;
    const key = event.Records[0].s3.object.key;
    const fileObject = await s3.getObject({
        Bucket: bucket,
        Key: key
    }).promise();
    
    const getObjectResult = await s3.getObject(params).promise()
    const fileContent = getObjectResult['Body'].toString('utf-8');
    
    client.connect(async err => {
        const collection = client.db("test").collection("Words");
        await db.insertRow({
            Id: uuidv4(),
            ObjectPath: `${bucket}/${key}`,
            Date: new Date(),
            AmountOfLines: fileContent.split("\n")
        })
        
        client.close();
    });
};

handler();