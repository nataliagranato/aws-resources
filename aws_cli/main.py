"""Main CLI application for AWS resource management."""

import argparse
import sys
import json
from typing import Dict, Any

from .services.s3 import S3Service
from .services.ec2 import EC2Service


def create_s3_bucket(args) -> None:
    """Create an S3 bucket.
    
    Args:
        args: Parsed command line arguments
    """
    try:
        s3_service = S3Service(args.region)
        result = s3_service.create_resource(
            bucket_name=args.bucket_name,
            region=args.region
        )
        
        if result['success']:
            print(f"✅ {result['message']}")
            if args.verbose:
                print(f"   Bucket: {result['bucket_name']}")
                print(f"   Region: {result['region']}")
                if result.get('location'):
                    print(f"   Location: {result['location']}")
        else:
            print(f"❌ {result['message']}")
            if args.verbose:
                print(f"   Error: {result.get('error', 'Unknown')}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


def create_ec2_instances(args) -> None:
    """Create EC2 instances.
    
    Args:
        args: Parsed command line arguments
    """
    try:
        ec2_service = EC2Service(args.region)
        result = ec2_service.create_resource(
            image_id=args.image_id,
            instance_type=args.instance_type,
            key_name=args.key_name,
            count=args.count,
            region=args.region
        )
        
        if result['success']:
            print(f"✅ {result['message']}")
            if args.verbose:
                print(f"   Instance IDs: {', '.join(result['instance_ids'])}")
                print(f"   Count: {result['count']}")
                print(f"   AMI: {result['image_id']}")
                print(f"   Instance Type: {result['instance_type']}")
                print(f"   Key Pair: {result['key_name']}")
                print(f"   Region: {result['region']}")
        else:
            print(f"❌ {result['message']}")
            if args.verbose:
                print(f"   Error: {result.get('error', 'Unknown')}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser.
    
    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        prog='aws-resources',
        description='AWS Resources CLI - A command-line tool for managing AWS resources',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create an S3 bucket
  aws-resources s3 create-bucket --bucket-name my-bucket --region us-west-2
  
  # Create EC2 instances
  aws-resources ec2 create-instances --image-id ami-12345678 --instance-type t2.micro \\
                                   --key-name my-key --count 2 --region us-east-1
        """
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    # Create subparsers for different services
    subparsers = parser.add_subparsers(
        dest='service',
        help='AWS service to manage',
        required=True
    )
    
    # S3 subcommands
    s3_parser = subparsers.add_parser(
        's3',
        help='Manage S3 buckets',
        description='S3 bucket management operations'
    )
    s3_subparsers = s3_parser.add_subparsers(
        dest='s3_action',
        help='S3 operations',
        required=True
    )
    
    # S3 create-bucket command
    s3_create_parser = s3_subparsers.add_parser(
        'create-bucket',
        help='Create a new S3 bucket',
        description='Create a new S3 bucket in the specified region'
    )
    s3_create_parser.add_argument(
        '--bucket-name',
        required=True,
        help='Name of the S3 bucket to create (must be globally unique)'
    )
    s3_create_parser.add_argument(
        '--region',
        required=True,
        help='AWS region where the bucket will be created (e.g., us-east-1, us-west-2)'
    )
    s3_create_parser.set_defaults(func=create_s3_bucket)
    
    # EC2 subcommands
    ec2_parser = subparsers.add_parser(
        'ec2',
        help='Manage EC2 instances',
        description='EC2 instance management operations'
    )
    ec2_subparsers = ec2_parser.add_subparsers(
        dest='ec2_action',
        help='EC2 operations',
        required=True
    )
    
    # EC2 create-instances command
    ec2_create_parser = ec2_subparsers.add_parser(
        'create-instances',
        help='Launch new EC2 instances',
        description='Launch new EC2 instances with specified configuration'
    )
    ec2_create_parser.add_argument(
        '--image-id',
        required=True,
        help='AMI ID to launch the instance from (e.g., ami-12345678)'
    )
    ec2_create_parser.add_argument(
        '--instance-type',
        required=True,
        help='EC2 instance type (e.g., t2.micro, t3.small, m5.large)'
    )
    ec2_create_parser.add_argument(
        '--key-name',
        required=True,
        help='Name of the EC2 Key Pair for SSH access'
    )
    ec2_create_parser.add_argument(
        '--count',
        type=int,
        default=1,
        help='Number of instances to launch (default: 1)'
    )
    ec2_create_parser.add_argument(
        '--region',
        required=True,
        help='AWS region where instances will be launched (e.g., us-east-1, us-west-2)'
    )
    ec2_create_parser.set_defaults(func=create_ec2_instances)
    
    # Future service placeholders (for extensibility)
    # These will show in help but are not yet implemented
    
    # DynamoDB placeholder
    dynamodb_parser = subparsers.add_parser(
        'dynamodb',
        help='Manage DynamoDB tables (coming soon)',
        description='DynamoDB table management operations (not yet implemented)'
    )
    
    # RDS placeholder  
    rds_parser = subparsers.add_parser(
        'rds',
        help='Manage RDS databases (coming soon)',
        description='RDS database management operations (not yet implemented)'
    )
    
    # Lambda placeholder
    lambda_parser = subparsers.add_parser(
        'lambda',
        help='Manage Lambda functions (coming soon)',
        description='Lambda function management operations (not yet implemented)'
    )
    
    # SNS placeholder
    sns_parser = subparsers.add_parser(
        'sns',
        help='Manage SNS topics (coming soon)',
        description='SNS topic management operations (not yet implemented)'
    )
    
    return parser


def main():
    """Main entry point for the CLI application."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Check if this is one of the implemented services
    if args.service in ['s3', 'ec2'] and hasattr(args, 'func'):
        args.func(args)
    elif args.service in ['dynamodb', 'rds', 'lambda', 'sns']:
        print(f"❌ {args.service.upper()} service is not yet implemented.")
        print("Currently supported services: s3, ec2")
        sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()