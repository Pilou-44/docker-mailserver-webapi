"""Mailserver API"""

import os

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from routes.alias_routes import alias_router
from routes.email_routes import email_router
from routes.fail2ban_routes import fail2ban_router
from routes.quota_routes import quota_router
from routes.restriction_routes import restriction_router

WEB_API_KEY = os.getenv("WEB_API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key")


def get_db(apikey_header: str = Security(api_key_header)):
    """API Key check."""
    if WEB_API_KEY and apikey_header == WEB_API_KEY:
        return True
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid API key")


app = FastAPI(root_path="/api/v1", title="Mailserver API")

app.include_router(email_router, dependencies=[Depends(get_db)])
app.include_router(alias_router, dependencies=[Depends(get_db)])
app.include_router(quota_router, dependencies=[Depends(get_db)])
app.include_router(restriction_router, dependencies=[Depends(get_db)])
app.include_router(fail2ban_router, dependencies=[Depends(get_db)])


@app.get("/", response_model=dict[str, str])
async def root_api():
    """Root API.

    Returns:
        dict[str, str]: HelloWorld!
    """
    return {"message": "Hello World !"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
