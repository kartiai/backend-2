from fastapi import Depends,Header, HTTPException


# Define the authentication dependency
async def get_api_key(api_key: str = Header(None)) -> str:
    print(api_key)
    if api_key != "your_secret_key":  # Replace with actual API key checking
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key
