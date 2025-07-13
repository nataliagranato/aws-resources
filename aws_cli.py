#!/usr/bin/env python3
"""
AWS Resources CLI Tool

This CLI tool provides commands to create various AWS resources including:
- S3 buckets
- EC2 instances  
- DynamoDB tables
- RDS instances
- Lambda functions
- SNS topics

Usage:
    python aws_cli.py s3 create-bucket --name my-bucket --region us-east-1
    python aws_cli.py ec2 create-instance --image-id ami-12345 --instance-type t2.micro --region us-east-1
    python aws_cli.py dynamodb create-table --name my-table --region us-east-1
    python aws_cli.py rds create-instance --identifier my-db --engine mysql --region us-east-1
    python aws_cli.py lambda create-function --name my-function --runtime python3.9 --region us-east-1
    python aws_cli.py sns create-topic --name my-topic --region us-east-1

Requirements:
    - boto3
    - AWS credentials configured (via AWS CLI, environment variables, or IAM roles)
"""

import argparse
import boto3
import sys
from botocore.exceptions import ClientError, NoCredentialsError


def create_s3_bucket(args):
    """Create an S3 bucket."""
    try:
        s3_client = boto3.client('s3', region_name=args.region)
        
        if args.region == 'us-east-1':
            # us-east-1 doesn't need LocationConstraint
            s3_client.create_bucket(Bucket=args.name)
        else:
            s3_client.create_bucket(
                Bucket=args.name,
                CreateBucketConfiguration={'LocationConstraint': args.region}
            )
        
        print(f"Successfully created S3 bucket: {args.name} in region {args.region}")
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'BucketAlreadyExists':
            print(f"Error: Bucket '{args.name}' already exists")
        elif error_code == 'BucketAlreadyOwnedByYou':
            print(f"Error: Bucket '{args.name}' already owned by you")
        else:
            print(f"Error creating S3 bucket: {e}")
        sys.exit(1)
    except NoCredentialsError:
        print("Error: AWS credentials not found. Please configure your credentials.")
        sys.exit(1)


def create_ec2_instance(args):
    """Create an EC2 instance."""
    try:
        ec2_client = boto3.client('ec2', region_name=args.region)
        
        run_params = {
            'ImageId': args.image_id,
            'MinCount': 1,
            'MaxCount': 1,
            'InstanceType': args.instance_type
        }
        
        if args.key_name:
            run_params['KeyName'] = args.key_name
        if args.security_groups:
            run_params['SecurityGroups'] = args.security_groups
        
        response = ec2_client.run_instances(**run_params)
        instance_id = response['Instances'][0]['InstanceId']
        
        print(f"Successfully created EC2 instance: {instance_id} in region {args.region}")
        print(f"Instance type: {args.instance_type}")
        print(f"Image ID: {args.image_id}")
        
    except ClientError as e:
        print(f"Error creating EC2 instance: {e}")
        sys.exit(1)
    except NoCredentialsError:
        print("Error: AWS credentials not found. Please configure your credentials.")
        sys.exit(1)


def create_dynamodb_table(args):
    """Create a DynamoDB table."""
    try:
        dynamodb_client = boto3.client('dynamodb', region_name=args.region)
        
        table_params = {
            'TableName': args.name,
            'KeySchema': [
                {
                    'AttributeName': args.partition_key,
                    'KeyType': 'HASH'
                }
            ],
            'AttributeDefinitions': [
                {
                    'AttributeName': args.partition_key,
                    'AttributeType': args.partition_key_type
                }
            ],
            'BillingMode': 'PAY_PER_REQUEST'
        }
        
        if args.sort_key:
            table_params['KeySchema'].append({
                'AttributeName': args.sort_key,
                'KeyType': 'RANGE'
            })
            table_params['AttributeDefinitions'].append({
                'AttributeName': args.sort_key,
                'AttributeType': args.sort_key_type
            })
        
        response = dynamodb_client.create_table(**table_params)
        
        print(f"Successfully created DynamoDB table: {args.name} in region {args.region}")
        print(f"Partition key: {args.partition_key} ({args.partition_key_type})")
        if args.sort_key:
            print(f"Sort key: {args.sort_key} ({args.sort_key_type})")
        print("Billing mode: PAY_PER_REQUEST")
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ResourceInUseException':
            print(f"Error: Table '{args.name}' already exists")
        else:
            print(f"Error creating DynamoDB table: {e}")
        sys.exit(1)
    except NoCredentialsError:
        print("Error: AWS credentials not found. Please configure your credentials.")
        sys.exit(1)


def create_rds_instance(args):
    """Create an RDS instance."""
    try:
        rds_client = boto3.client('rds', region_name=args.region)
        
        create_params = {
            'DBInstanceIdentifier': args.identifier,
            'DBInstanceClass': args.instance_class,
            'Engine': args.engine,
            'MasterUsername': args.username,
            'MasterUserPassword': args.password,
            'AllocatedStorage': args.storage,
            'VpcSecurityGroupIds': [],
            'PubliclyAccessible': args.publicly_accessible
        }
        
        if args.security_groups:
            create_params['VpcSecurityGroupIds'] = args.security_groups
        
        response = rds_client.create_db_instance(**create_params)
        
        print(f"Successfully initiated RDS instance creation: {args.identifier} in region {args.region}")
        print(f"Engine: {args.engine}")
        print(f"Instance class: {args.instance_class}")
        print(f"Allocated storage: {args.storage} GB")
        print("Note: Instance creation may take several minutes to complete")
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'DBInstanceAlreadyExists':
            print(f"Error: RDS instance '{args.identifier}' already exists")
        else:
            print(f"Error creating RDS instance: {e}")
        sys.exit(1)
    except NoCredentialsError:
        print("Error: AWS credentials not found. Please configure your credentials.")
        sys.exit(1)


def create_lambda_function(args):
    """Create a Lambda function."""
    try:
        lambda_client = boto3.client('lambda', region_name=args.region)
        
        # Create a simple Hello World function if no code is provided
        if not args.code_file:
            code_content = '''
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }
'''
            code_bytes = code_content.encode('utf-8')
        else:
            with open(args.code_file, 'rb') as f:
                code_bytes = f.read()
        
        function_params = {
            'FunctionName': args.name,
            'Runtime': args.runtime,
            'Role': args.role,
            'Handler': args.handler,
            'Code': {'ZipFile': code_bytes},
            'Description': args.description or f'Lambda function {args.name}'
        }
        
        if args.timeout:
            function_params['Timeout'] = args.timeout
        if args.memory:
            function_params['MemorySize'] = args.memory
        
        response = lambda_client.create_function(**function_params)
        
        print(f"Successfully created Lambda function: {args.name} in region {args.region}")
        print(f"Runtime: {args.runtime}")
        print(f"Handler: {args.handler}")
        print(f"Role: {args.role}")
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ResourceConflictException':
            print(f"Error: Lambda function '{args.name}' already exists")
        else:
            print(f"Error creating Lambda function: {e}")
        sys.exit(1)
    except NoCredentialsError:
        print("Error: AWS credentials not found. Please configure your credentials.")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Code file '{args.code_file}' not found")
        sys.exit(1)


def create_sns_topic(args):
    """Create an SNS topic."""
    try:
        sns_client = boto3.client('sns', region_name=args.region)
        
        topic_params = {
            'Name': args.name
        }
        
        if args.display_name:
            topic_params['Attributes'] = {
                'DisplayName': args.display_name
            }
        
        response = sns_client.create_topic(**topic_params)
        topic_arn = response['TopicArn']
        
        print(f"Successfully created SNS topic: {args.name} in region {args.region}")
        print(f"Topic ARN: {topic_arn}")
        if args.display_name:
            print(f"Display name: {args.display_name}")
        
    except ClientError as e:
        print(f"Error creating SNS topic: {e}")
        sys.exit(1)
    except NoCredentialsError:
        print("Error: AWS credentials not found. Please configure your credentials.")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='AWS Resources CLI Tool - Create various AWS resources',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s s3 create-bucket --name my-bucket --region us-east-1
  %(prog)s ec2 create-instance --image-id ami-12345 --instance-type t2.micro --region us-east-1
  %(prog)s dynamodb create-table --name my-table --partition-key id --region us-east-1
  %(prog)s rds create-instance --identifier my-db --engine mysql --username admin --password secret123 --region us-east-1
  %(prog)s lambda create-function --name my-function --runtime python3.9 --role arn:aws:iam::123456789012:role/lambda-role --region us-east-1
  %(prog)s sns create-topic --name my-topic --region us-east-1
        """
    )
    
    subparsers = parser.add_subparsers(dest='service', help='AWS service')
    subparsers.required = True
    
    # S3 subcommand
    s3_parser = subparsers.add_parser('s3', help='S3 operations')
    s3_subparsers = s3_parser.add_subparsers(dest='s3_action', help='S3 actions')
    s3_subparsers.required = True
    
    s3_create_bucket = s3_subparsers.add_parser('create-bucket', help='Create S3 bucket')
    s3_create_bucket.add_argument('--name', required=True, help='Bucket name (must be globally unique)')
    s3_create_bucket.add_argument('--region', required=True, help='AWS region')
    s3_create_bucket.set_defaults(func=create_s3_bucket)
    
    # EC2 subcommand
    ec2_parser = subparsers.add_parser('ec2', help='EC2 operations')
    ec2_subparsers = ec2_parser.add_subparsers(dest='ec2_action', help='EC2 actions')
    ec2_subparsers.required = True
    
    ec2_create_instance = ec2_subparsers.add_parser('create-instance', help='Create EC2 instance')
    ec2_create_instance.add_argument('--image-id', required=True, help='AMI ID to launch')
    ec2_create_instance.add_argument('--instance-type', required=True, help='Instance type (e.g., t2.micro)')
    ec2_create_instance.add_argument('--region', required=True, help='AWS region')
    ec2_create_instance.add_argument('--key-name', help='EC2 Key Pair name')
    ec2_create_instance.add_argument('--security-groups', nargs='+', help='Security group names')
    ec2_create_instance.set_defaults(func=create_ec2_instance)
    
    # DynamoDB subcommand
    dynamodb_parser = subparsers.add_parser('dynamodb', help='DynamoDB operations')
    dynamodb_subparsers = dynamodb_parser.add_subparsers(dest='dynamodb_action', help='DynamoDB actions')
    dynamodb_subparsers.required = True
    
    dynamodb_create_table = dynamodb_subparsers.add_parser('create-table', help='Create DynamoDB table')
    dynamodb_create_table.add_argument('--name', required=True, help='Table name')
    dynamodb_create_table.add_argument('--partition-key', required=True, help='Partition key attribute name')
    dynamodb_create_table.add_argument('--partition-key-type', default='S', choices=['S', 'N', 'B'], 
                                     help='Partition key type (S=String, N=Number, B=Binary)')
    dynamodb_create_table.add_argument('--sort-key', help='Sort key attribute name (optional)')
    dynamodb_create_table.add_argument('--sort-key-type', default='S', choices=['S', 'N', 'B'],
                                     help='Sort key type (S=String, N=Number, B=Binary)')
    dynamodb_create_table.add_argument('--region', required=True, help='AWS region')
    dynamodb_create_table.set_defaults(func=create_dynamodb_table)
    
    # RDS subcommand
    rds_parser = subparsers.add_parser('rds', help='RDS operations')
    rds_subparsers = rds_parser.add_subparsers(dest='rds_action', help='RDS actions')
    rds_subparsers.required = True
    
    rds_create_instance = rds_subparsers.add_parser('create-instance', help='Create RDS instance')
    rds_create_instance.add_argument('--identifier', required=True, help='DB instance identifier')
    rds_create_instance.add_argument('--engine', required=True, 
                                   choices=['mysql', 'postgres', 'mariadb', 'oracle-ee', 'sqlserver-ex'],
                                   help='Database engine')
    rds_create_instance.add_argument('--instance-class', default='db.t3.micro', help='DB instance class')
    rds_create_instance.add_argument('--username', required=True, help='Master username')
    rds_create_instance.add_argument('--password', required=True, help='Master password')
    rds_create_instance.add_argument('--storage', type=int, default=20, help='Allocated storage in GB')
    rds_create_instance.add_argument('--region', required=True, help='AWS region')
    rds_create_instance.add_argument('--security-groups', nargs='+', help='VPC security group IDs')
    rds_create_instance.add_argument('--publicly-accessible', action='store_true', 
                                   help='Make instance publicly accessible')
    rds_create_instance.set_defaults(func=create_rds_instance)
    
    # Lambda subcommand
    lambda_parser = subparsers.add_parser('lambda', help='Lambda operations')
    lambda_subparsers = lambda_parser.add_subparsers(dest='lambda_action', help='Lambda actions')
    lambda_subparsers.required = True
    
    lambda_create_function = lambda_subparsers.add_parser('create-function', help='Create Lambda function')
    lambda_create_function.add_argument('--name', required=True, help='Function name')
    lambda_create_function.add_argument('--runtime', required=True,
                                      choices=['python3.9', 'python3.10', 'python3.11', 'nodejs18.x', 'nodejs20.x', 'java11', 'dotnet6'],
                                      help='Runtime environment')
    lambda_create_function.add_argument('--role', required=True, help='IAM role ARN for the function')
    lambda_create_function.add_argument('--handler', default='lambda_function.lambda_handler', 
                                      help='Function handler (default: lambda_function.lambda_handler)')
    lambda_create_function.add_argument('--code-file', help='Path to code zip file (optional, creates Hello World if not provided)')
    lambda_create_function.add_argument('--description', help='Function description')
    lambda_create_function.add_argument('--timeout', type=int, help='Function timeout in seconds')
    lambda_create_function.add_argument('--memory', type=int, help='Memory size in MB')
    lambda_create_function.add_argument('--region', required=True, help='AWS region')
    lambda_create_function.set_defaults(func=create_lambda_function)
    
    # SNS subcommand
    sns_parser = subparsers.add_parser('sns', help='SNS operations')
    sns_subparsers = sns_parser.add_subparsers(dest='sns_action', help='SNS actions')
    sns_subparsers.required = True
    
    sns_create_topic = sns_subparsers.add_parser('create-topic', help='Create SNS topic')
    sns_create_topic.add_argument('--name', required=True, help='Topic name')
    sns_create_topic.add_argument('--display-name', help='Topic display name')
    sns_create_topic.add_argument('--region', required=True, help='AWS region')
    sns_create_topic.set_defaults(func=create_sns_topic)
    
    # Parse arguments and execute appropriate function
    args = parser.parse_args()
    
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()