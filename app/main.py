from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.api import api_router
import requests

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AutoTriage Server",
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root() -> dict[str, str]:
    """Health check endpoint."""
    return {"message": "Hello World"}


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}

posturl = 'https://candidate-ds-endpoint.onrender.com/get-category'

postdata = {
   "email_content": "a new email that is not spam!",
   "username": "eexuanen",
   "input_categories": ["SPAM", "IMPORTANT", "MARKETING"]
}

# Function to do a post message to to the url
def SendPost(data):
    response = requests.post(posturl, json = data)
    print(response.status_code)
    print(response.text)


SendPost(postdata)