# lambda-data-exporter

## Description
This project has all components to deploy an application in AWS.
- **app:** This directory contains the application code. Here is the documentation [README.md](./app/README.md)
- **iac:** This directory contains the CloudFormation templates. Here is the documentation [README.md](./iac/README.md)

### What it is created?
Using this project, you will create this itens:

- Two S3 Bucket
- One Lambda Function
- One EventRule scheduled in EventBridge Scheduler
- All Rules and Policies
- An Python application, used to export data from DynamoDB Table to S3 Bucket.

---
## How to use
There is a shell scrit in this repo, create to help the creation and deploy.

First, you have configure the AWS Cli and give execution permissions to this script.

```bash
root@ubuntu:lambda-data-exporter$ chmod +x deploy
```

### To create all Stacks and deploy the application:
This option will create all infraestructure, upload and deploy the Python application.
```bash
root@ubuntu:lambda-data-exporter$ ./deploy all
```

### To deploy/update the application:
This option will crate a zip file of the Python application, upload to S3 Bucket and update the Lambda function with the new code.
```bash
root@ubuntu:lambda-data-exporter$ ./deploy update-app
```

### Other options:
This script has another options, if you desire to change a especific item.
```bash
root@ubuntu:lambda-data-exporter$ ./deploy
You can use:
        deploy all: To create the AWS components and deploy the application.

        deploy update-app: To upload and update your application.

        deploy update-s3: To update only the S3 Stack

        deploy update-lambda-configuration: To update only the Lambda Stack
```

## Manual deploy
You can deploy without the script, using *aws cloudformation* command line. Follow the instructions:

### Create the S3 Stack:
```bash
root@ubuntu:lambda-data-exporter$ aws cloudformation deploy \
    --template-file iac/iac-s3.yml \
    --stack-name s3-data-exporter
```

### Upload the Python application to S3:
```bash
root@ubuntu:lambda-data-exporter$ cd app

root@ubuntu:lambda-data-exporter/app$ zipname="latest-"$(date +'%Y%m%d%H%M%S')

root@ubuntu:lambda-data-exporter/app$ echo "S3Key=production/python/$zipname.zip" > ../iac/application.parameter

root@ubuntu:lambda-data-exporter/app$ zip -r $zipname.zip lambda_function.py

root@ubuntu:lambda-data-exporter/app$ aws s3 cp $zipname.zip s3://lambda-data-exporter/production/python/

root@ubuntu:lambda-data-exporter/app$ cd ..
```

### Create the Lambda Stack:
```bash
root@ubuntu:lambda-data-exporter$ param=$(cat iac/application.parameter)

root@ubuntu:lambda-data-exporter$ aws cloudformation deploy \
    --capabilities CAPABILITY_NAMED_IAM \
    --template-file iac/iac-lambda.yml --stack-name lambda-data-exporter \
    --parameter-overrides $param
```