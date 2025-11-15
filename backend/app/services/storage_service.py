"""
Jukeyman Autonomous Media Station (JAMS) - Cloudflare R2 Storage Service
"""
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
import os
import uuid
import mimetypes
from typing import Optional
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class R2StorageService:
    """
    Service for uploading and managing files in Cloudflare R2 (S3-compatible storage)
    """
    
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=settings.R2_ENDPOINT_URL,
            aws_access_key_id=settings.R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
            config=Config(signature_version='s3v4'),
            region_name='auto'  # Cloudflare R2 uses 'auto'
        )
        self.bucket_name = settings.R2_BUCKET_NAME
        self.public_url = settings.R2_PUBLIC_URL
    
    def upload_file(
        self,
        file_path: str,
        tenant_id: str,
        filename: Optional[str] = None,
        content_type: Optional[str] = None
    ) -> str:
        """
        Upload a file to R2 and return the public URL
        
        Args:
            file_path: Local path to the file
            tenant_id: Tenant ID for organization
            filename: Optional custom filename (defaults to UUID)
            content_type: Optional MIME type (auto-detected if not provided)
            
        Returns:
            Public URL of the uploaded file
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Generate filename if not provided
        if not filename:
            ext = os.path.splitext(file_path)[1]
            filename = f"{uuid.uuid4()}{ext}"
        
        # Auto-detect content type if not provided
        if not content_type:
            content_type, _ = mimetypes.guess_type(file_path)
            if not content_type:
                content_type = "application/octet-stream"
        
        # Construct S3 key with tenant isolation
        key = f"{tenant_id}/{filename}"
        
        try:
            # Upload file
            with open(file_path, 'rb') as f:
                self.s3_client.upload_fileobj(
                    f,
                    self.bucket_name,
                    key,
                    ExtraArgs={
                        'ContentType': content_type,
                        'ACL': 'public-read'  # Make publicly accessible
                    }
                )
            
            # Construct public URL
            public_url = f"{self.public_url}/{key}"
            logger.info(f"Uploaded file to R2: {public_url}")
            
            return public_url
        
        except ClientError as e:
            logger.error(f"Failed to upload file to R2: {e}")
            raise Exception(f"Failed to upload file: {str(e)}")
    
    def upload_bytes(
        self,
        file_bytes: bytes,
        tenant_id: str,
        filename: str,
        content_type: str = "application/octet-stream"
    ) -> str:
        """
        Upload bytes directly to R2
        
        Args:
            file_bytes: File content as bytes
            tenant_id: Tenant ID for organization
            filename: Filename with extension
            content_type: MIME type
            
        Returns:
            Public URL of the uploaded file
        """
        key = f"{tenant_id}/{filename}"
        
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=file_bytes,
                ContentType=content_type,
                ACL='public-read'
            )
            
            public_url = f"{self.public_url}/{key}"
            logger.info(f"Uploaded bytes to R2: {public_url}")
            
            return public_url
        
        except ClientError as e:
            logger.error(f"Failed to upload bytes to R2: {e}")
            raise Exception(f"Failed to upload bytes: {str(e)}")
    
    def delete_file(self, url: str) -> bool:
        """
        Delete a file from R2 given its public URL
        
        Args:
            url: Public URL of the file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Extract key from URL
            key = url.replace(f"{self.public_url}/", "")
            
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=key
            )
            
            logger.info(f"Deleted file from R2: {url}")
            return True
        
        except ClientError as e:
            logger.error(f"Failed to delete file from R2: {e}")
            return False
    
    def get_file_url(self, tenant_id: str, filename: str) -> str:
        """
        Get the public URL for a file
        
        Args:
            tenant_id: Tenant ID
            filename: Filename
            
        Returns:
            Public URL
        """
        key = f"{tenant_id}/{filename}"
        return f"{self.public_url}/{key}"
    
    def file_exists(self, url: str) -> bool:
        """
        Check if a file exists in R2
        
        Args:
            url: Public URL of the file
            
        Returns:
            True if file exists, False otherwise
        """
        try:
            key = url.replace(f"{self.public_url}/", "")
            self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=key
            )
            return True
        except ClientError:
            return False
    
    def list_files(self, tenant_id: str, prefix: str = "") -> list:
        """
        List files for a tenant
        
        Args:
            tenant_id: Tenant ID
            prefix: Optional prefix to filter files
            
        Returns:
            List of file URLs
        """
        try:
            full_prefix = f"{tenant_id}/{prefix}" if prefix else tenant_id
            
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=full_prefix
            )
            
            if 'Contents' not in response:
                return []
            
            files = [
                f"{self.public_url}/{obj['Key']}"
                for obj in response['Contents']
            ]
            
            return files
        
        except ClientError as e:
            logger.error(f"Failed to list files from R2: {e}")
            return []


# Global instance
storage_service = R2StorageService()

