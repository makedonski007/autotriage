from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx

router = APIRouter()

# Request model
class ClassifyRequest(BaseModel):
    email_content: str
    username: str

# Response model
class ClassifyResponse(BaseModel):
    category: str

@router.post("/classify", response_model=ClassifyResponse)
async def classify_email(request: ClassifyRequest):
    try:
        async with httpx.AsyncClient() as client:
            # Call the external DS API to classify the email
          response = await client.post(
            "https://candidate-ds-endpoint.onrender.com/get-category",
            json={
                "username": request.username,
                "email_content": request.email_content,
                "input_categories": ["SPAM", "IMPORTANT", "MARKETING"]
            }
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DS API error: {str(e)}")
