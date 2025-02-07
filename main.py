"""Mailserver API"""

import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.email_routes import email_router

WEB_API_KEY = os.getenv("WEB_API_KEY")
WEB_API_WHITELISTED_IPS = os.getenv("WEB_API_WHITELISTED_IPS", "127.0.0.1").split(',')
WEB_API_FAIL2BAN_SQLITE_PATH = "/var/lib/fail2ban/fail2ban.sqlite3"

origins = [
    "http://localhost",
    "http://localhost:3000"
]

app = FastAPI(root_path="/api/v1", title="Mailserver API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(email_router)


@app.get("/", response_model=dict[str, str])
async def root_api():
    """Root API.

    Returns:
        dict[str, str]: HelloWorld!
    """
    return {"message": "Hello World !"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
