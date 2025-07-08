from fastapi import FastAPI, Request
from app.core.config import settings
from app.api.v1.api import api_router
import requests
import re

# send messages
posturl = 'https://candidate-ds-endpoint.onrender.com/get-category'

postdata = {
   "email_content": "",
   "username": "eexuanen",
   "input_categories": ["SPAM", "IMPORTANT", "MARKETING", "Security", "Account", "Not Important"]
}

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


# create frontend client endpoint
@app.post("/email")
async def getPost(request: Request) -> dict[str, str]:
    data = await request.json()
    print(data)
    postdata["email_content"] = data["email_content"]
    response = sendPost(postdata);
    return response;


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}


def removeImage(data):
    imagePattern = r"\n\s*data:image/"
    match = re.match(imagePattern, data)
    if(match):
        result = re.sub(imagePattern, "", text)
        nextNL = result.find("\n")
        result = result[nextNL:]
        return result

    return data

def removeReply(data):
    replyPattern = r"> From:"
    match = re.match(replyPattern, data)
    if(match):
        result = re.sub(replyPattern, "", text)
        i = result.rfind("> > > > >")
        result = result[i:]
        nl = result.find("\n");
        result = result[nl:]
        return result

    return data

# Function to do a post message to to the url
def sendPost(data):
    data = removeImage(data)
    data = removeReply(data)
    response = requests.post(posturl, json = data)
    return response.text
