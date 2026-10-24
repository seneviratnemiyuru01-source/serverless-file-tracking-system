flowchart TD
    Client[Client] -->|POST /files or GET /status/fileId| API[Amazon API Gateway]
    API --> Lambda[AWS Lambda]
    Lambda -->|Store uploaded file| S3[Amazon S3]
    Lambda -->|Save tracking record| DDB[Amazon DynamoDB]
    Lambda --> Logs[Amazon CloudWatch Logs]
    CF[AWS CloudFormation] -.->|Deploys infrastructure| API
    CF -.-> Lambda
    CF -.-> S3
    CF -.-> DDB
