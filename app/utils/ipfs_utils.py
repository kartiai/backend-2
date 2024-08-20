import ipfsApi
import aiofiles
from fastapi import UploadFile, HTTPException
from typing import List, Dict

def connect_to_ipfs() -> ipfsApi.Client:
    """Connect to the local IPFS node."""
    try:
        client = ipfsApi.Client('host.docker.internal', 5001)
        return client
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to IPFS: {e}")

async def save_file_to_disk(file: UploadFile) -> str:
    """Save the uploaded file to disk asynchronously."""
    try:
        async with aiofiles.open(file.filename, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        return file.filename
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file {file.filename} to disk: {e}")

def upload_file_to_ipfs(client: ipfsApi.Client, file_path: str) -> Dict[str, str]:
    """Upload the file to IPFS and return the IPFS hash."""
    try:
        res = client.add(file_path)
        return {"filename": file_path, "ipfs_hash": res['Hash']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload {file_path} to IPFS: {e}")
