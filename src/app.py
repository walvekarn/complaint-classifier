"""
FastAPI application for complaint classification.
Author: Nikita Walvekar (walvekarn)
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import logging

from src.classifier import classify_complaint

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Complaint Classifier API",
    description="AI-powered complaint classification and routing system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


class ComplaintRequest(BaseModel):
    """Request model for complaint classification."""
    text: str = Field(..., description="The complaint text to classify", min_length=1)
    
    class Config:
        schema_extra = {
            "example": {
                "text": "I found unauthorized charges on my credit card statement. This is fraud!"
            }
        }


class ClassificationResponse(BaseModel):
    """Response model for classification results."""
    category: str = Field(..., description="Product category (e.g., Credit Card, Mortgage)")
    confidence: float = Field(..., description="Classification confidence score (0.0-1.0)")
    severity: int = Field(..., description="Severity score (1-10)")
    route: str = Field(..., description="Recommended routing department")
    issue_category: Optional[str] = Field(None, description="Issue type (e.g., Fraud, Billing Error)")
    sentiment: Optional[str] = Field(None, description="Customer sentiment (e.g., Angry, Neutral)")
    needs_review: bool = Field(..., description="Whether manual review is recommended")
    
    class Config:
        schema_extra = {
            "example": {
                "category": "Credit Card",
                "confidence": 0.95,
                "severity": 9,
                "route": "Fraud Team",
                "issue_category": "Fraud",
                "sentiment": "Angry",
                "needs_review": False
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    message: str


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Health status of the API
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "message": "Complaint Classifier API is running"
    }


@app.post("/classify", response_model=ClassificationResponse, tags=["Classification"])
async def classify(request: ComplaintRequest):
    """
    Classify a complaint and recommend routing.
    
    Args:
        request: ComplaintRequest containing the complaint text
        
    Returns:
        ClassificationResponse with category, confidence, severity, and routing
        
    Raises:
        HTTPException: If classification fails
    """
    try:
        logger.info(f"Classifying complaint: {request.text[:100]}...")
        
        # Run classification
        result = classify_complaint(request.text)
        
        logger.info(f"Classification complete: category={result['category']}, "
                   f"confidence={result['confidence']}, severity={result['severity']}")
        
        return result
        
    except Exception as e:
        logger.error(f"Classification error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Classification failed: {str(e)}"
        )


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        API information and links
    """
    return {
        "name": "Complaint Classifier API",
        "version": "1.0.0",
        "author": "Nikita Walvekar (walvekarn)",
        "description": "Rule-based complaint classification and intelligent routing",
        "endpoints": {
            "health": "/health",
            "classify": "/classify",
            "docs": "/docs",
            "redoc": "/redoc"
        },
        "usage": {
            "POST /classify": {
                "body": {"text": "Your complaint text here"},
                "returns": "Classification results with category, confidence, severity, and routing"
            }
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

