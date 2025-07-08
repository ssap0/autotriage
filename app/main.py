from fastapi import FastAPI, Request
from app.core.config import settings
from app.api.v1.api import api_router
import requests
import re

# send messages
posturl = 'https://candidate-ds-endpoint.onrender.com/get-category'

postdata = {
   "email_content": "Dear Accounts Team,\n\nPlease find attached invoice BG-2024-447 for bakery supply delivery completed on March 13, 2024.\n\nInvoice Details:\n- Invoice #BG-2024-447\n- Amount: $15,680.45\n- Payment terms: 30 days\n- Delivery date: March 13, 2024\n\nInvoice and delivery confirmation images:\n\ndata:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k=\n\nPlease process at your earliest convenience.\n\nBest regards,\nAnna Wilson\nBilling Department\n\n-- \nAnna Wilson | Billing Coordinator\nBaking Goods Australia Pty Ltd\nPhone: +61 2 6543 2109\nEmail: anna.wilson@bakinggoods.com.au",
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
    imagePattern = r"\ndata:image/"
    match = re.search(imagePattern, data)
    if(match):
        result = re.sub(imagePattern, "", data)
        prevhalf = result[:match.start()]
        nexthalf = result[match.start():]
        nl = nexthalf.find("\n")
        result = prevhalf + nexthalf[nl:]
        print(result)
        return result

    return data

def removeReply(data):
    replyPattern = r"> From:"
    match = re.search(replyPattern, data)
    if(match):
        result = re.sub(replyPattern, "", data)
        i = result.rfind("> > > > >")
        result = result[i:]
        nl = result.find("\n");
        result = result[nl:]
        return result

    return data

# Function to do a post message to to the url
def sendPost(data):
    data["email_content"] = removeImage(data["email_content"])
    data["email_content"] = removeReply(data["email_content"])
    print(data["email_content"])
    response = requests.post(posturl, json = data)
    print(response.text)
    return response.text

sendPost(postdata)