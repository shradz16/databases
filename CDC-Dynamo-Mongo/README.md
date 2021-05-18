# Real-Time Replication/ CDC

Setting up Data pipeline using Python Lambda function

###### Steps:

## Create Role

Create an IAM role(dynamo-lambda-role) for Lambda to have DynamoDB access and assign below policies

- *AWSLambdaDynamoDBExecutionRole*

- *AWSLambdaBasicExecutionRole*

## Python Script

`replicatory.py` is the python script to read a record from DynamoDB stream and update in Mongo Atlas

## Create a deployment package

I have used virtualenv to install and package the requirements

#Install virtualenv
>
>sudo pip install virtualenv
>
#create env named Project
>
>virtualenv -p /usr/bin/python3.6 Project
>
#Activate the env
>
>source Project/bin/activate
>
#Install required packages
>
> pip install pymongo
> 
> pip install dynamodb_json
> 
> pip install dnspython
> 
#go to site-packages where packages are installed
> 
> cd Project/lin/python3.6/site-packages/
> 
#add the python script here as replicator.py and zip the package
> 
> vi replicator.py
> 
> zip -r9 ~/repl_function.zip .
> 
#Deactivate the env
>
>deactivate

## Create a Lambda function

`aws lambda create-function --function-name dy-mongo-replicator \\
--handler replicator.lambda_handler \\
--zip-file fileb://repl_function.zip \\
--runtime python3.6 \\
--timeout 15 \\
--role arn:aws:iam::XXXXXXXXXXX:role/dynamo-lambda-role \\
--environment 'Variables={mongodburl="mongodb+srv://user:password@clusterX.XXXXX.mongodb.net/test?retryWrites=true&w=majority",database="test",table="User_profile"}'`

## Add a trigger & Enable DynamoDB stream

- On the function page, go to Add Trigger and enter the info below
- Click on "Enable trigger" to enable DynamoDB streams.


## Execution:

Any changes in the DynamoDB are captured by the DynamoDB stream and stored in the form of events. DynamoDB Stream can store the events for 24 hours after which it flushes out. As soon as any insert, modify, or delete action is done on the DynamoDB table, a Lambda function is invoked and a python script is executed which performs upsert/ delete action on the MongoDB and replicates the changes record by record in seconds.
Mongo has _id as a primary key and if not defined, an arbitrary value gets assigned. We haven't assigned any value to _id since we will use "id" as a primary key and will create an index later on.
