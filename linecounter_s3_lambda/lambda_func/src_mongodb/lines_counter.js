"use strict";
const AWS = require('aws-sdk');
const s3 = new AWS.S3();
const { v4: uuidv4 } = require('uuid');
const MONGODB_URI = process.env.MONGODB_URI; // or Atlas connection string

let cachedDb = null;

function connectToDatabase(uri) {
    console.log(`=> connect to database`);
    if (cachedDb) {
        console.log(`=> using cached database instance`);
        return Promise.resolve(cachedDb);

    }
    
    return MongoClient.connect(uri)
        .then(db => {
            cachedDb = db;
            return cachedDb;
        });
}

function queryDatabase(db) {
    console.log('=> query database');

    return db.collection('items').find({}).toArray()
        .then(() => {
            return { statusCode: 200, body: 'success' };
        })
        .catch(err => {
            console.log('=> an error occurred: ', err);
            return { statusCode: 500, body: 'error' };
        });
}

exports.handler = async (event, context, callback) => {
    context.callbackWaitsForEmptyEventLoop = false;
    console.log('event: ', event);
    
    const bucket = event.Records[0].s3.bucket.name;
    const key = event.Records[0].s3.object.key;]
    const fileObject = await s3.getObject({
        Bucket: bucket,
        Key: key
    }).promise();
    
    const getObjectResult = await s3.getObject(params).promise() // await the promise
    const fileContent = getObjectResult.Body.toString('utf-8');
    
    connectToDatabase(MONGODB_URI)
        .then(async db => {
            await db.insertRow({
                Id: uuidv4(),
                ObjectPath: `${bucket}/${key}`,
                Date: new Date(),
                AmountOfLines: fileContent.split("\n")
            })
            return queryDatabase(db)
        })
        .then(result => {
            console.log('=> returning result: ', result);
            
            callback(null, result);
        })
        .catch(err => {
            console.log('=> an error occurred: ', err);
            callback(err);
        });
};
