# AWS Resources CLI Tool

A comprehensive command-line interface for creating various AWS resources including S3 buckets, EC2 instances, DynamoDB tables, RDS instances, Lambda functions, and SNS topics.

## Features

This CLI tool provides two complementary interfaces for AWS resource management:

### Modern Package-based CLI (S3 & EC2 - Production Ready)
- **S3 Bucket Management**: Create S3 buckets with region specification
- **EC2 Instance Management**: Launch EC2 instances with customizable configuration
- **Package Installation**: Install as `pip install -e .` and use `aws-resources` command
- **Advanced Error Handling**: Comprehensive AWS error handling and user-friendly messages
- **Hierarchical Commands**: Professional CLI experience with argparse subcommands

### Extended Service Support (All AWS Services)
- **DynamoDB Tables**: Create DynamoDB tables with partition keys and optional sort keys
- **RDS Instances**: Create RDS database instances with various engines
- **Lambda Functions**: Create Lambda functions with different runtimes
- **SNS Topics**: Create SNS topics for messaging
- **Direct Python Execution**: Use `python aws_cli.py` for broader service access

## Prerequisites

- Python 3.8 or higher
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

3. Install the package for modern CLI experience:
```bash
pip install -e .
```

4. Configure AWS credentials (choose one method):
   - Using AWS CLI: `aws configure`
   - Using environment variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
   - Using IAM roles (if running on EC2)

## Usage

### Modern Package-based CLI (Recommended for S3 & EC2)

#### S3 Bucket Creation

Create a new S3 bucket:

```bash
aws-resources s3 create-bucket --bucket-name my-unique-bucket --region us-west-2
```

**Parameters:**
- `--bucket-name`: Name of the S3 bucket (must be globally unique)
- `--region`: AWS region for the bucket (e.g., us-east-1, us-west-2)

#### EC2 Instance Creation

Launch new EC2 instances:

```bash
aws-resources ec2 create-instances \
  --image-id ami-12345678 \
  --instance-type t2.micro \
  --key-name my-ec2-key \
  --count 2 \
  --region us-east-1
```

**Parameters:**
- `--image-id`: AMI ID to launch the instance from (required)
- `--instance-type`: EC2 instance type like t2.micro, t3.small (required)
- `--key-name`: Name of the EC2 Key Pair for SSH access (required)
- `--count`: Number of instances to launch (default: 1)
- `--region`: AWS region for the instances (required)

#### Global Options

- `-v, --verbose`: Enable verbose output for detailed information

#### Help

Get help for any command:

```bash
aws-resources --help
aws-resources s3 --help
aws-resources ec2 create-instances --help
```

### Extended Service CLI (All AWS Services)

#### General Syntax
```bash
python aws_cli.py <service> <action> [options]
```

#### S3 Operations

Create an S3 bucket:
```bash
python aws_cli.py s3 create-bucket --name my-unique-bucket-name --region us-east-1
```

#### EC2 Operations

Create an EC2 instance:
```bash
python aws_cli.py ec2 create-instance --image-id ami-0abcdef1234567890 --instance-type t2.micro --region us-east-1
```

With optional parameters:
```bash
python aws_cli.py ec2 create-instance --image-id ami-0abcdef1234567890 --instance-type t2.micro --region us-east-1 --key-name my-key-pair --security-groups default
```

#### DynamoDB Operations

Create a simple table with partition key only:
```bash
python aws_cli.py dynamodb create-table --name my-table --partition-key id --region us-east-1
```

Create a table with both partition and sort keys:
```bash
python aws_cli.py dynamodb create-table --name my-table --partition-key userId --partition-key-type S --sort-key timestamp --sort-key-type N --region us-east-1
```

#### RDS Operations

Create an RDS MySQL instance:
```bash
python aws_cli.py rds create-instance --identifier my-database --engine mysql --username admin --password mypassword123 --region us-east-1
```

With additional options:
```bash
python aws_cli.py rds create-instance --identifier my-database --engine postgres --instance-class db.t3.small --username admin --password mypassword123 --storage 50 --publicly-accessible --region us-east-1
```

#### Lambda Operations

Create a Lambda function (with default Hello World code):
```bash
python aws_cli.py lambda create-function --name my-function --runtime python3.9 --role arn:aws:iam::123456789012:role/lambda-execution-role --region us-east-1
```

With custom code and settings:
```bash
python aws_cli.py lambda create-function --name my-function --runtime python3.9 --role arn:aws:iam::123456789012:role/lambda-execution-role --handler index.handler --code-file my-function.zip --timeout 60 --memory 256 --region us-east-1
```

#### SNS Operations

Create an SNS topic:
```bash
python aws_cli.py sns create-topic --name my-topic --region us-east-1
```

With display name:
```bash
python aws_cli.py sns create-topic --name my-topic --display-name "My Notification Topic" --region us-east-1
```

## Examples

### Modern CLI Examples

#### Create an S3 bucket in us-east-1:
```bash
aws-resources s3 create-bucket --bucket-name my-app-logs-2024 --region us-east-1
```

#### Launch a single t2.micro instance:
```bash
aws-resources ec2 create-instances \
  --image-id ami-0abcdef1234567890 \
  --instance-type t2.micro \
  --key-name my-keypair \
  --region us-west-2
```

#### Launch multiple instances with verbose output:
```bash
aws-resources -v ec2 create-instances \
  --image-id ami-0abcdef1234567890 \
  --instance-type t3.small \
  --key-name production-key \
  --count 3 \
  --region eu-west-1
```

## Architecture

The CLI is built with extensibility in mind:

- **Base Service Class**: Common functionality for all AWS services
- **Service-Specific Modules**: Dedicated modules for each AWS service
- **Argument Parsing**: Hierarchical subcommands using argparse
- **Error Handling**: Comprehensive error handling with user-friendly messages
## Command Reference (Extended CLI)

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

## Requirements

- Python 3.8+
- boto3 >= 1.26.0
- Valid AWS credentials

## Error Handling

The tool provides clear error messages for common scenarios:
- Missing AWS credentials
- Resource already exists
- Invalid parameters
- AWS service errors

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

---

Feito com ❤️ por [Natália Granato](https://github.com/nataliagranato).
