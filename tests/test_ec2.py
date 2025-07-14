"""Tests for EC2 service functionality."""

import unittest
from unittest.mock import Mock, patch, MagicMock
from botocore.exceptions import ClientError

from aws_cli.services.ec2 import EC2Service


class TestEC2Service(unittest.TestCase):
    """Test cases for EC2Service."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ec2_service = EC2Service(region='us-east-1')
    
    def test_init(self):
        """Test EC2Service initialization."""
        service = EC2Service('us-west-2')
        self.assertEqual(service.region, 'us-west-2')
        self.assertEqual(service.service_name, 'ec2')
    
    def test_validate_required_params_success(self):
        """Test successful parameter validation."""
        params = {
            'image_id': 'ami-12345678',
            'instance_type': 't2.micro',
            'key_name': 'test-key'
        }
        required = ['image_id', 'instance_type', 'key_name']
        # Should not raise any exception
        self.ec2_service.validate_required_params(params, required)
    
    def test_validate_required_params_missing(self):
        """Test parameter validation with missing params."""
        params = {'image_id': 'ami-12345678'}
        required = ['image_id', 'instance_type', 'key_name']
        with self.assertRaises(ValueError) as context:
            self.ec2_service.validate_required_params(params, required)
        self.assertIn('Missing required parameters:', str(context.exception))
    
    @patch('aws_cli.services.ec2.boto3.client')
    def test_create_instances_success(self, mock_boto_client):
        """Test successful EC2 instance creation."""
        # Mock the EC2 client
        mock_client = Mock()
        mock_boto_client.return_value = mock_client
        mock_client.run_instances.return_value = {
            'Instances': [
                {'InstanceId': 'i-1234567890abcdef0'},
                {'InstanceId': 'i-0987654321fedcba0'}
            ]
        }
        
        result = self.ec2_service.create_resource(
            image_id='ami-12345678',
            instance_type='t2.micro',
            key_name='test-key',
            count=2,
            region='us-east-1'
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(len(result['instance_ids']), 2)
        self.assertEqual(result['count'], 2)
        self.assertEqual(result['image_id'], 'ami-12345678')
        self.assertEqual(result['instance_type'], 't2.micro')
        self.assertEqual(result['key_name'], 'test-key')
        self.assertIn('Successfully launched', result['message'])
        
        mock_client.run_instances.assert_called_once_with(
            ImageId='ami-12345678',
            MinCount=2,
            MaxCount=2,
            InstanceType='t2.micro',
            KeyName='test-key'
        )
    
    @patch('aws_cli.services.ec2.boto3.client')
    def test_create_instances_invalid_ami(self, mock_boto_client):
        """Test EC2 instance creation with invalid AMI."""
        # Mock the EC2 client
        mock_client = Mock()
        mock_boto_client.return_value = mock_client
        
        # Mock ClientError for invalid AMI
        error_response = {
            'Error': {
                'Code': 'InvalidAMIID.NotFound',
                'Message': 'The image id ami-invalid does not exist'
            }
        }
        mock_client.run_instances.side_effect = ClientError(error_response, 'RunInstances')
        
        result = self.ec2_service.create_resource(
            image_id='ami-invalid',
            instance_type='t2.micro',
            key_name='test-key',
            region='us-east-1'
        )
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'InvalidAMIID')
        self.assertIn('not found in region', result['message'])
    
    @patch('aws_cli.services.ec2.boto3.client')
    def test_create_instances_invalid_keypair(self, mock_boto_client):
        """Test EC2 instance creation with invalid key pair."""
        # Mock the EC2 client
        mock_client = Mock()
        mock_boto_client.return_value = mock_client
        
        # Mock ClientError for invalid key pair
        error_response = {
            'Error': {
                'Code': 'InvalidKeyPair.NotFound',
                'Message': 'The key pair invalid-key does not exist'
            }
        }
        mock_client.run_instances.side_effect = ClientError(error_response, 'RunInstances')
        
        result = self.ec2_service.create_resource(
            image_id='ami-12345678',
            instance_type='t2.micro',
            key_name='invalid-key',
            region='us-east-1'
        )
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'InvalidKeyPair')
        self.assertIn('Key pair', result['message'])
        self.assertIn('not found', result['message'])
    
    def test_create_instances_invalid_count(self):
        """Test EC2 instance creation with invalid count."""
        with self.assertRaises(ValueError) as context:
            self.ec2_service.create_resource(
                image_id='ami-12345678',
                instance_type='t2.micro',
                key_name='test-key',
                count=0
            )
        self.assertIn('Count must be at least 1', str(context.exception))
    
    def test_create_instances_missing_params(self):
        """Test EC2 instance creation with missing parameters."""
        with self.assertRaises(ValueError) as context:
            self.ec2_service.create_resource(
                image_id=None,
                instance_type='t2.micro',
                key_name='test-key'
            )
        self.assertIn('Missing required parameters', str(context.exception))


if __name__ == '__main__':
    unittest.main()