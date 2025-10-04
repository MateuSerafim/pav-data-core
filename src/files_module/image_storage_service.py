from azure.storage.blob.aio import BlobServiceClient
import os
from ..utils.result import ErrorCode, Result

class AzureStorageService():
    def __init__(self):
        self.blob_service = \
            BlobServiceClient.from_connection_string(os.getenv("STORAGE_CONNECTION_STRING"))
        
    async def upload_file(self, container_name: str, file_data: str, file_name: str) -> Result:
        try:
            container_client = self.blob_service.get_container_client(container_name)
            blob_client = container_client.get_blob_client(file_name)
            
            await blob_client.upload_blob(file_data)

            return Result.success()
        
        except Exception as ex:
            return Result.failure(str(ex), ErrorCode.CRITICAL_ERROR)