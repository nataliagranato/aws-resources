# AWS Resources CLI Tool

A comprehensive command-line interface for creating various AWS resources including S3 buckets, EC2 instances, DynamoDB tables, RDS instances, Lambda functions, and SNS topics.

## Features

- **S3 Buckets**: Create S3 buckets in any AWS region
- **EC2 Instances**: Launch EC2 instances with customizable configurations
- **DynamoDB Tables**: Create DynamoDB tables with partition keys and optional sort keys
- **RDS Instances**: Create RDS database instances with various engines
- **Lambda Functions**: Create Lambda functions with different runtimes
- **SNS Topics**: Create SNS topics for messaging

## Prerequisites

- Python 3.6 or higher
- AWS credentials configured (via AWS CLI, environment variables, or IAM roles)
- Required Python packages (see requirements.txt)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/nataliagranato/aws-resources.git
cd aws-resources
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure AWS credentials (choose one method):
   - Using AWS CLI: `aws configure`
   - Using environment variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
   - Using IAM roles (if running on EC2)

## Usage

### General Syntax
```bash
python aws_cli.py <service> <action> [options]
```

### S3 Operations

Create an S3 bucket:
```bash
python aws_cli.py s3 create-bucket --name my-unique-bucket-name --region us-east-1
```

### EC2 Operations

Create an EC2 instance:
```bash
python aws_cli.py ec2 create-instance --image-id ami-0abcdef1234567890 --instance-type t2.micro --region us-east-1
```

With optional parameters:
```bash
python aws_cli.py ec2 create-instance --image-id ami-0abcdef1234567890 --instance-type t2.micro --region us-east-1 --key-name my-key-pair --security-groups default
```

### DynamoDB Operations

Create a simple table with partition key only:
```bash
python aws_cli.py dynamodb create-table --name my-table --partition-key id --region us-east-1
```

Create a table with both partition and sort keys:
```bash
python aws_cli.py dynamodb create-table --name my-table --partition-key userId --partition-key-type S --sort-key timestamp --sort-key-type N --region us-east-1
```

### RDS Operations

Create an RDS MySQL instance:
```bash
python aws_cli.py rds create-instance --identifier my-database --engine mysql --username admin --password mypassword123 --region us-east-1
```

With additional options:
```bash
python aws_cli.py rds create-instance --identifier my-database --engine postgres --instance-class db.t3.small --username admin --password mypassword123 --storage 50 --publicly-accessible --region us-east-1
```

### Lambda Operations

Create a Lambda function (with default Hello World code):
```bash
python aws_cli.py lambda create-function --name my-function --runtime python3.9 --role arn:aws:iam::123456789012:role/lambda-execution-role --region us-east-1
```

With custom code and settings:
```bash
python aws_cli.py lambda create-function --name my-function --runtime python3.9 --role arn:aws:iam::123456789012:role/lambda-execution-role --handler index.handler --code-file my-function.zip --timeout 60 --memory 256 --region us-east-1
```

### SNS Operations

Create an SNS topic:
```bash
python aws_cli.py sns create-topic --name my-topic --region us-east-1
```

With display name:
```bash
python aws_cli.py sns create-topic --name my-topic --display-name "My Notification Topic" --region us-east-1
```

## Command Reference

### Global Options
- `--region`: AWS region (required for all commands)

### S3 create-bucket
- `--name`: Bucket name (must be globally unique)

### EC2 create-instance
- `--image-id`: AMI ID to launch (required)
- `--instance-type`: Instance type (required, e.g., t2.micro)
- `--key-name`: EC2 Key Pair name (optional)
- `--security-groups`: Security group names (optional, space-separated)

### DynamoDB create-table
- `--name`: Table name (required)
- `--partition-key`: Partition key attribute name (required)
- `--partition-key-type`: Partition key type - S/N/B (default: S)
- `--sort-key`: Sort key attribute name (optional)
- `--sort-key-type`: Sort key type - S/N/B (default: S)

### RDS create-instance
- `--identifier`: DB instance identifier (required)
- `--engine`: Database engine - mysql/postgres/mariadb/oracle-ee/sqlserver-ex (required)
- `--username`: Master username (required)
- `--password`: Master password (required)
- `--instance-class`: DB instance class (default: db.t3.micro)
- `--storage`: Allocated storage in GB (default: 20)
- `--security-groups`: VPC security group IDs (optional, space-separated)
- `--publicly-accessible`: Make instance publicly accessible (flag)

### Lambda create-function
- `--name`: Function name (required)
- `--runtime`: Runtime environment (required) - python3.9/python3.10/python3.11/nodejs18.x/nodejs20.x/java11/dotnet6
- `--role`: IAM role ARN (required)
- `--handler`: Function handler (default: lambda_function.lambda_handler)
- `--code-file`: Path to code zip file (optional, creates Hello World if not provided)
- `--description`: Function description (optional)
- `--timeout`: Function timeout in seconds (optional)
- `--memory`: Memory size in MB (optional)

### SNS create-topic
- `--name`: Topic name (required)
- `--display-name`: Topic display name (optional)

## Error Handling

The tool provides clear error messages for common scenarios:
- Missing AWS credentials
- Resource already exists
- Invalid parameters
- AWS service errors

## Examples

For more examples, run:
```bash
python aws_cli.py --help
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Feito com ❤️ por [Natália Granato](https://github.com/nataliagranato).
