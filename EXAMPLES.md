# AWS CLI Examples

This document provides practical examples of using the AWS CLI tool.

## Prerequisites
Ensure you have AWS credentials configured before running these commands.

## Example Commands

### 1. Create an S3 Bucket
```bash
python aws_cli.py s3 create-bucket --name my-company-data-bucket-2024 --region us-west-2
```

### 2. Launch an EC2 Instance
```bash
# Basic instance
python aws_cli.py ec2 create-instance --image-id ami-0abcdef1234567890 --instance-type t2.micro --region us-east-1

# With key pair and security groups
python aws_cli.py ec2 create-instance --image-id ami-0abcdef1234567890 --instance-type t2.small --region us-east-1 --key-name my-keypair --security-groups web-servers ssh-access
```

### 3. Create DynamoDB Tables
```bash
# Simple table with partition key only
python aws_cli.py dynamodb create-table --name UserProfiles --partition-key userId --region us-east-1

# Table with partition and sort keys
python aws_cli.py dynamodb create-table --name OrderHistory --partition-key customerId --sort-key orderDate --sort-key-type N --region us-east-1
```

### 4. Create RDS Database Instances
```bash
# MySQL database
python aws_cli.py rds create-instance --identifier my-mysql-db --engine mysql --username admin --password SecurePass123! --region us-east-1

# PostgreSQL with custom settings
python aws_cli.py rds create-instance --identifier my-postgres-db --engine postgres --instance-class db.t3.small --username dbadmin --password SecurePass123! --storage 50 --publicly-accessible --region us-west-2
```

### 5. Create Lambda Functions
```bash
# Simple function with default Hello World code
python aws_cli.py lambda create-function --name my-api-function --runtime python3.9 --role arn:aws:iam::123456789012:role/lambda-execution-role --region us-east-1

# Function with custom settings
python aws_cli.py lambda create-function --name data-processor --runtime python3.11 --role arn:aws:iam::123456789012:role/lambda-role --handler process.main --timeout 300 --memory 512 --description "Processes incoming data files" --region us-east-1
```

### 6. Create SNS Topics
```bash
# Simple topic
python aws_cli.py sns create-topic --name user-notifications --region us-east-1

# Topic with display name
python aws_cli.py sns create-topic --name system-alerts --display-name "Critical System Alerts" --region us-east-1
```

## Complete Workflow Example

Here's an example of setting up a complete infrastructure:

```bash
# 1. Create S3 bucket for data storage
python aws_cli.py s3 create-bucket --name myapp-data-store-2024 --region us-east-1

# 2. Create DynamoDB table for user data
python aws_cli.py dynamodb create-table --name Users --partition-key email --region us-east-1

# 3. Create RDS database for transactions
python aws_cli.py rds create-instance --identifier myapp-transactions --engine postgres --username dbadmin --password SecureDBPass123! --region us-east-1

# 4. Create Lambda function for API
python aws_cli.py lambda create-function --name api-handler --runtime python3.9 --role arn:aws:iam::123456789012:role/lambda-execution-role --region us-east-1

# 5. Create SNS topic for notifications
python aws_cli.py sns create-topic --name app-notifications --display-name "App Notifications" --region us-east-1

# 6. Launch EC2 instance for additional processing
python aws_cli.py ec2 create-instance --image-id ami-0abcdef1234567890 --instance-type t2.small --region us-east-1 --key-name my-keypair
```

## Tips

- Always specify the correct region for your resources
- Use strong passwords for RDS instances
- Ensure IAM roles have proper permissions for Lambda functions
- S3 bucket names must be globally unique
- Consider security groups and network configuration for EC2 and RDS instances