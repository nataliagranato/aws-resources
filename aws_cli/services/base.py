"""Base service class for AWS resource management."""

import boto3
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseService(ABC):
    """Base class for AWS service implementations."""
    
    def __init__(self, region: str = None):
        """Initialize base service with AWS region.
        
        Args:
            region: AWS region name (e.g., 'us-east-1')
        """
        self.region = region
        self.session = boto3.Session()
    
    def get_client(self, service_name: str):
        """Get AWS service client.
        
        Args:
            service_name: Name of the AWS service (e.g., 's3', 'ec2')
            
        Returns:
            boto3 client for the specified service
        """
        if self.region:
            return self.session.client(service_name, region_name=self.region)
        return self.session.client(service_name)
    
    @abstractmethod
    def create_resource(self, **kwargs) -> Dict[str, Any]:
        """Create AWS resource.
        
        Args:
            **kwargs: Service-specific parameters
            
        Returns:
            Dictionary containing creation result
        """
        pass
    
    def validate_required_params(self, params: Dict[str, Any], required: list):
        """Validate that required parameters are provided.
        
        Args:
            params: Dictionary of parameters
            required: List of required parameter names
            
        Raises:
            ValueError: If any required parameter is missing
        """
        missing = [param for param in required if param not in params or params[param] is None]
        if missing:
            raise ValueError(f"Missing required parameters: {', '.join(missing)}")