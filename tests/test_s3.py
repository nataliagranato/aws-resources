"""Tests for S3 service functionality."""

import unittest
from unittest.mock import Mock, patch, MagicMock
from botocore.exceptions import ClientError

from aws_cli.services.s3 import S3Service


class TestS3Service(unittest.TestCase):
    """Test cases for S3Service."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.s3_service = S3Service(region='us-east-1')
    
    def test_init(self):
        """Test S3Service initialization."""
        service = S3Service('us-west-2')
        self.assertEqual(service.region, 'us-west-2')
        self.assertEqual(service.service_name, 's3')
    
    def test_validate_required_params_success(self):
        """Test successful parameter validation."""
        params = {'bucket_name': 'test-bucket'}
        required = ['bucket_name']
        # Should not raise any exception
        self.s3_service.validate_required_params(params, required)
    
    def test_validate_required_params_missing(self):
        """Test parameter validation with missing params."""
        params = {}
        required = ['bucket_name']
        with self.assertRaises(ValueError) as context:
            self.s3_service.validate_required_params(params, required)
        self.assertIn('Missing required parameters: bucket_name', str(context.exception))
    
    @patch('aws_cli.services.s3.boto3.client')
    def test_create_bucket_success_us_east_1(self, mock_boto_client):
        """Test successful bucket creation in us-east-1."""
        # Mock the S3 client
        mock_client = Mock()
        mock_boto_client.return_value = mock_client
        mock_client.create_bucket.return_value = {
            'Location': '/test-bucket'
        }
        
        result = self.s3_service.create_resource('test-bucket', 'us-east-1')
        
        self.assertTrue(result['success'])
        self.assertEqual(result['bucket_name'], 'test-bucket')
        self.assertEqual(result['region'], 'us-east-1')
        self.assertIn('Successfully created', result['message'])
        mock_client.create_bucket.assert_called_once_with(Bucket='test-bucket')
    
    @patch('aws_cli.services.s3.boto3.client')
    def test_create_bucket_success_other_region(self, mock_boto_client):
        """Test successful bucket creation in non-us-east-1 region."""
        # Mock the S3 client
        mock_client = Mock()
        mock_boto_client.return_value = mock_client
        mock_client.create_bucket.return_value = {
            'Location': '/test-bucket'
        }
        
        result = self.s3_service.create_resource('test-bucket', 'us-west-2')
        
        self.assertTrue(result['success'])
        self.assertEqual(result['bucket_name'], 'test-bucket')
        self.assertEqual(result['region'], 'us-west-2')
        mock_client.create_bucket.assert_called_once_with(
            Bucket='test-bucket',
            CreateBucketConfiguration={'LocationConstraint': 'us-west-2'}
        )
    
    @patch('aws_cli.services.s3.boto3.client')
    def test_create_bucket_already_exists(self, mock_boto_client):
        """Test bucket creation when bucket already exists."""
        # Mock the S3 client
        mock_client = Mock()
        mock_boto_client.return_value = mock_client
        
        # Mock ClientError for bucket already exists
        error_response = {
            'Error': {
                'Code': 'BucketAlreadyExists',
                'Message': 'The bucket already exists'
            }
        }
        mock_client.create_bucket.side_effect = ClientError(error_response, 'CreateBucket')
        
        result = self.s3_service.create_resource('test-bucket', 'us-east-1')
        
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'BucketAlreadyExists')
        self.assertIn('already exists and is owned by another account', result['message'])
    
    def test_create_bucket_missing_name(self):
        """Test bucket creation with missing bucket name."""
        with self.assertRaises(ValueError) as context:
            self.s3_service.create_resource(None)
        self.assertIn('Missing required parameters: bucket_name', str(context.exception))


if __name__ == '__main__':
    unittest.main()