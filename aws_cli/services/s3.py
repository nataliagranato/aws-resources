"""S3 service implementation for bucket management."""

import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any
from .base import BaseService


class S3Service(BaseService):
    """Service for managing S3 buckets."""
    
    def __init__(self, region: str = None):
        """Initialize S3 service.
        
        Args:
            region: AWS region name (e.g., 'us-east-1')
        """
        super().__init__(region)
        self.service_name = 's3'
    
    def create_resource(self, bucket_name: str, region: str = None) -> Dict[str, Any]:
        """Create an S3 bucket.
        
        Args:
            bucket_name: Name of the S3 bucket to create
            region: AWS region for the bucket (overrides instance region)
            
        Returns:
            Dictionary containing bucket creation result
            
        Raises:
            ValueError: If bucket_name is not provided
            ClientError: If AWS API call fails
        """
        # Use provided region or fall back to instance region
        target_region = region or self.region
        
        # Validate required parameters
        self.validate_required_params(
            {'bucket_name': bucket_name}, 
            ['bucket_name']
        )
        
        try:
            # Get S3 client for the target region
            s3_client = self.get_client(self.service_name) if not target_region else \
                       boto3.client(self.service_name, region_name=target_region)
            
            # Create bucket configuration
            create_bucket_config = {}
            
            # For regions other than us-east-1, we need to specify the location constraint
            if target_region and target_region != 'us-east-1':
                create_bucket_config['CreateBucketConfiguration'] = {
                    'LocationConstraint': target_region
                }
            
            # Create the bucket
            if create_bucket_config:
                response = s3_client.create_bucket(
                    Bucket=bucket_name,
                    **create_bucket_config
                )
            else:
                response = s3_client.create_bucket(Bucket=bucket_name)
            
            return {
                'success': True,
                'bucket_name': bucket_name,
                'region': target_region or 'us-east-1',
                'location': response.get('Location', ''),
                'message': f"Successfully created S3 bucket '{bucket_name}' in region '{target_region or 'us-east-1'}'"
            }
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            
            if error_code == 'BucketAlreadyExists':
                return {
                    'success': False,
                    'error': 'BucketAlreadyExists',
                    'message': f"Bucket '{bucket_name}' already exists and is owned by another account"
                }
            elif error_code == 'BucketAlreadyOwnedByYou':
                return {
                    'success': False,
                    'error': 'BucketAlreadyOwnedByYou',
                    'message': f"Bucket '{bucket_name}' already exists and is owned by you"
                }
            else:
                return {
                    'success': False,
                    'error': error_code,
                    'message': f"Failed to create bucket: {error_message}"
                }
        except Exception as e:
            return {
                'success': False,
                'error': 'UnexpectedError',
                'message': f"Unexpected error creating bucket: {str(e)}"
            }