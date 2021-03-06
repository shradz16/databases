from __future__ import print_function

import pymongo
import json
import boto3
import os
import time
import uuid
from datetime import datetime
from decimal import Decimal

from dynamodb_json import json_util as json

def lambda_handler(event, context):

    # read env variables for mongodb connection
    urlDb = os.environ['mongodburl']
    database = os.environ['database']
    table = os.environ['table']

    # configure pymongo connection
    myclient = pymongo.MongoClient(urlDb)
    mydb = myclient[database]
    mycol = mydb[table]

    count = 0

    with myclient.start_session() as session:

        for record in event['Records']:

            ddb = record['dynamodb']
  
            if (record['eventName'] == 'INSERT' or record['eventName'] == 'MODIFY'):

                newimage = ddb['NewImage']
                newimage_conv = json.loads(newimage)
            
                # create the explicit _id
                # newimage_conv['_id'] = newimage_conv['id']


                try:
                    #mycol.update_one({"_id":newimage_conv['_id']}, { "$set" : newimage_conv}, upsert=True, session=session)
                    mycol.update_one({"id":newimage_conv['id']}, { "$set" : newimage_conv}, upsert=True, session=session)
                    count = count + 1

                except Exception as e:
                    print(e)
                    #print("ERROR update id=",newimage_conv['id']," ",type(e),e)

            elif (record['eventName'] == 'REMOVE'):

                oldimage = ddb['OldImage']
                oldimage_conv = json.loads(oldimage)

                try:
                    mycol.delete_one({"id":oldimage_conv['id']}, session=session)
                    count = count + 1

                except Exception as e:
                    print("ERROR delete id",oldimage_conv['id']," ",type(e),e)

    session.end_session()

    myclient.close()

    # return response code to Lambda and log on CloudWatch
    if count == len(event['Records']):
        print('Successfully processed %s records.' % str(len(event['Records'])))
        return {
            'statusCode': 200,
            'body': json.dumps('OK')
        }
    else:
        print('Processed only ',str(count),' records on %s' % str(len(event['Records'])))
        return {
            'statusCode': 500,
            'body': json.dumps('ERROR') 
        }
