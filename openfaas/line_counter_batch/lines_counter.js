"use strict";
const fetch = require("node-fetch");
const { v4: uuidv4 } = require('uuid');
const AWS = require('aws-sdk');
const s3 = new AWS.S3();
const MongoClient = require('mongodb').MongoClient;

module.exports = async (event, context) => {
    context.callbackWaitsForEmptyEventLoop = false;
    console.log('event: ', event);
    
    // CONNECT TO S3 AND RUN BATCH
    const bucket = event.Records[0].s3.bucket.name;
    const key = event.Records[0].s3.object.key;
    const fileObject = await s3.getObject({Bucket: bucket, Key: key}).promise();
    const fileContent = fileObject['Body'].toString('utf-8');
    
    const result = await fetchVaultCreds();
    const DB_PASS = result['data']['pass']
    const DB_NAME = result['data']['dbname']
    const uri = `mongodb+srv://admin:${DB_PASS}@cluster0.14ono.mongodb.net/${DB_NAME}?retryWrites=true&w=majority`;
    const client = new MongoClient(uri, {
        useNewUrlParser: true,
        useUnifiedTopology: true
    });
    
    await client.connect(async (err, client) => {
        if (err) throw err;
        let db = client.db(DB_NAME);
        let collection = db.collection("Lines");
        
        await collection.insertOne({
            Id: uuidv4(),
            ObjectPath: `${bucket}/${key}`,
            Date: new Date(),
            AmountOfLines: fileContent.split("\n")
        })
        
        client.close();
    });
};


`
curl --header "X-Vault-Token: s.A946lZFDo7WOrX9v39d5Gf6h" \
     --request GET 'http://127.0.0.1:8200/v1/kv-v1/db'
`
async function fetchVaultCreds() {
    const response = await fetch(
        'http://127.0.0.1:8200/v1/kv-v1/db',
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Vault-Token': 's.A946lZFDo7WOrX9v39d5Gf6h'
            }
        })
    
    return response.json();
}
