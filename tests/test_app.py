"""
Tests for FastAPI complaint classifier.
Author: Nikita Walvekar (walvekarn)
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app

# Create test client
client = TestClient(app)


def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "healthy"
    assert "version" in data
    assert "message" in data
    assert "Complaint Classifier" in data["message"]


def test_classify_endpoint():
    """Test the classify endpoint with a sample complaint."""
    complaint_text = "I found unauthorized charges on my credit card. This is fraud!"
    
    response = client.post(
        "/classify",
        json={"text": complaint_text}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Check required fields exist
    assert "category" in data
    assert "confidence" in data
    assert "severity" in data
    assert "route" in data
    assert "needs_review" in data
    
    # Check data types
    assert isinstance(data["category"], str)
    assert isinstance(data["confidence"], (int, float))
    assert isinstance(data["severity"], int)
    assert isinstance(data["route"], str)
    assert isinstance(data["needs_review"], bool)
    
    # Check value ranges
    assert 0.0 <= data["confidence"] <= 1.0
    assert 1 <= data["severity"] <= 10
    
    # For this fraud complaint, expect high severity
    assert data["severity"] >= 7


def test_classify_empty_text():
    """Test classify endpoint with empty text."""
    response = client.post(
        "/classify",
        json={"text": ""}
    )
    
    # Should fail validation
    assert response.status_code == 422


def test_classify_mortgage_complaint():
    """Test classification of a mortgage-related complaint."""
    complaint_text = "My mortgage lender is refusing to process my refinance application."
    
    response = client.post(
        "/classify",
        json={"text": complaint_text}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Should detect mortgage category
    assert "Mortgage" in data["category"] or data["category"] == "Other"
    assert data["confidence"] > 0


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "name" in data
    assert "version" in data
    assert "endpoints" in data

