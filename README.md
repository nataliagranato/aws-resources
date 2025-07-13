# AWS Resources CLI

A command-line tool for managing AWS resources using boto3. This CLI provides an easy-to-use interface for creating and managing various AWS services.

## Features

- **S3 Bucket Management**: Create S3 buckets with region specification
- **EC2 Instance Management**: Launch EC2 instances with customizable configuration
- **Extensible Architecture**: Designed to support future services (DynamoDB, RDS, Lambda, SNS)
- **Comprehensive Error Handling**: Clear error messages and validation
- **Verbose Output**: Optional detailed information about operations

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

3. Install the package:
```bash
pip install -e .
```

## AWS Configuration

Before using this tool, ensure your AWS credentials are configured. You can use any of these methods:

- AWS CLI: `aws configure`
- Environment variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
- IAM roles (for EC2 instances)
- AWS credentials file

## Usage

### S3 Bucket Creation

Create a new S3 bucket:

```bash
aws-resources s3 create-bucket --bucket-name my-unique-bucket --region us-west-2
```

**Parameters:**
- `--bucket-name`: Name of the S3 bucket (must be globally unique)
- `--region`: AWS region for the bucket (e.g., us-east-1, us-west-2)

### EC2 Instance Creation

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

### Global Options

- `-v, --verbose`: Enable verbose output for detailed information

### Help

Get help for any command:

```bash
aws-resources --help
aws-resources s3 --help
aws-resources ec2 create-instances --help
```

## Examples

### Create an S3 bucket in us-east-1:
```bash
aws-resources s3 create-bucket --bucket-name my-app-logs-2024 --region us-east-1
```

### Launch a single t2.micro instance:
```bash
aws-resources ec2 create-instances \
  --image-id ami-0abcdef1234567890 \
  --instance-type t2.micro \
  --key-name my-keypair \
  --region us-west-2
```

### Launch multiple instances with verbose output:
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

## Future Services

The CLI is designed to support additional AWS services:

- **DynamoDB**: Table creation and management
- **RDS**: Database instance management  
- **Lambda**: Function deployment and management
- **SNS**: Topic creation and message publishing

## Requirements

- Python 3.8+
- boto3 >= 1.26.0
- Valid AWS credentials

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feito com ❤️ por [Natália Granato](https://github.com/nataliagranato).
