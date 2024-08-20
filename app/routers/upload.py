from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import io
from ..db.db import User, FileStorage, UserFile
from ..utils.ipfs_utils import connect_to_ipfs, save_file_to_disk, upload_file_to_ipfs
from ..utils.jwt_token import get_api_key

router = APIRouter()
##https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/


@router.post("/upload/put")
async def upload_ipfs(files: List[UploadFile], api_key: str = Depends(get_api_key)):
    client = connect_to_ipfs()
    ipfs_hashes = []
    
    for file in files:
        try:
            # Read the file's content directly
            file_content = await file.read()
            
            # Wrap the file content in a BytesIO object
            file_like_object = io.BytesIO(file_content)
            
            # Upload the file content directly to IPFS
            ipfs_hash_info = client.add(file_like_object)
            ipfs_hashes.append(ipfs_hash_info)
            
            # Store file metadata in the database
            file_storage = FileStorage(
                cid=ipfs_hash_info['Hash'],  # 'Hash' key from IPFS response
                file_name=file.filename,
                file_size=len(file_content),
                file_type=file.content_type,
                file_date="2024-08-06"  # Example date, adjust as needed
            )
            user_file_storage = UserFile(
                cid=ipfs_hash_info['Hash'],  # 'Hash' key from IPFS response
                user_id=1  # Adjust user_id as needed
            )

            await file_storage.save()
            await user_file_storage.save()

        except HTTPException as e:
            # Handle exceptions for each file
            return JSONResponse(content={"detail": str(e)}, status_code=e.status_code)

    return JSONResponse(content={"ipfs_hashes": ipfs_hashes})

@router.get("/upload/get/{user_id}")
async def get_ipfs(user_id: int):
    user_files = await UserFile.objects.select_related("cid").filter(user_id=user_id).all()
    if not user_files:
        raise HTTPException(status_code=404, detail="User not found or no files uploaded by user")
    return {"cids": [file.cid for file in user_files]}

@router.get("/upload/get/{user_id}/{content_cid}")
async def get_ipfs(user_id: int, content_cid: str):
    user_files = await UserFile.objects.select_related("cid").filter(user_id=user_id).all()
    for content in user_files['cids']:
        if content_cid == content['cid']:
            if not user_files:
                raise HTTPException(status_code=404, detail="User not found or no files uploaded by user")
            return {"data": "/ipfs/"+content_cid }
    return JSONResponse(content={"error": "no data available"})

@router.get("/upload/delete/{cid}")
async def delete_ipfs(cid: str):
    return {"username": username}