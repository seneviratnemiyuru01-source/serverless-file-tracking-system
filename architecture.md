flowchart TD
    Client --> API_Gateway
    API_Gateway --> Lambda
    Lambda --> S3
    Lambda --> DynamoDB
    Lambda --> CloudWatch_Logs
    CloudFormation --> API_Gateway
    CloudFormation --> Lambda
    CloudFormation --> S3
    CloudFormation --> DynamoDB
