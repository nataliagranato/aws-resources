"""EC2 service implementation for instance management."""

import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any
from .base import BaseService


class EC2Service(BaseService):
    """Service for managing EC2 instances."""
    
    def __init__(self, region: str = None):
        """Initialize EC2 service.
        
        Args:
            region: AWS region name (e.g., 'us-east-1')
        """
        super().__init__(region)
        self.service_name = 'ec2'
    
    def create_resource(self, image_id: str, instance_type: str, key_name: str, 
                       count: int = 1, region: str = None) -> Dict[str, Any]:
        """Create EC2 instances.
        
        Args:
            image_id: AMI ID to launch the instance from (e.g., 'ami-12345678')
            instance_type: EC2 instance type (e.g., 't2.micro', 't3.small')
            key_name: Name of the EC2 Key Pair for SSH access
            count: Number of instances to launch (default: 1)
            region: AWS region for the instances (overrides instance region)
            
        Returns:
            Dictionary containing instance creation result
            
        Raises:
            ValueError: If required parameters are not provided
            ClientError: If AWS API call fails
        """
        # Use provided region or fall back to instance region
        target_region = region or self.region
        
        # Validate required parameters
        self.validate_required_params(
            {
                'image_id': image_id,
                'instance_type': instance_type,
                'key_name': key_name
            }, 
            ['image_id', 'instance_type', 'key_name']
        )
        
        # Validate count parameter
        if count < 1:
            raise ValueError("Count must be at least 1")
        
        try:
            # Get EC2 client for the target region
            ec2_client = self.get_client(self.service_name) if not target_region else \
                        boto3.client(self.service_name, region_name=target_region)
            
            # Launch instances
            response = ec2_client.run_instances(
                ImageId=image_id,
                MinCount=count,
                MaxCount=count,
                InstanceType=instance_type,
                KeyName=key_name
            )
            
            # Extract instance information
            instances = response.get('Instances', [])
            instance_ids = [instance['InstanceId'] for instance in instances]
            
            return {
                'success': True,
                'instance_ids': instance_ids,
                'count': len(instance_ids),
                'image_id': image_id,
                'instance_type': instance_type,
                'key_name': key_name,
                'region': target_region,
                'message': f"Successfully launched {len(instance_ids)} EC2 instance(s) in region '{target_region}'"
            }
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            
            if error_code == 'InvalidAMIID.NotFound':
                return {
                    'success': False,
                    'error': 'InvalidAMIID',
                    'message': f"AMI '{image_id}' not found in region '{target_region}'"
                }
            elif error_code == 'InvalidKeyPair.NotFound':
                return {
                    'success': False,
                    'error': 'InvalidKeyPair',
                    'message': f"Key pair '{key_name}' not found in region '{target_region}'"
                }
            elif error_code == 'InvalidInstanceType':
                return {
                    'success': False,
                    'error': 'InvalidInstanceType',
                    'message': f"Instance type '{instance_type}' is not valid or not available in region '{target_region}'"
                }
            elif error_code == 'InsufficientInstanceCapacity':
                return {
                    'success': False,
                    'error': 'InsufficientCapacity',
                    'message': f"Insufficient capacity for instance type '{instance_type}' in region '{target_region}'"
                }
            elif error_code == 'UnauthorizedOperation':
                return {
                    'success': False,
                    'error': 'UnauthorizedOperation',
                    'message': "You are not authorized to perform this operation. Check your AWS permissions."
                }
            else:
                return {
                    'success': False,
                    'error': error_code,
                    'message': f"Failed to launch instances: {error_message}"
                }
        except Exception as e:
            return {
                'success': False,
                'error': 'UnexpectedError',
                'message': f"Unexpected error launching instances: {str(e)}"
            }