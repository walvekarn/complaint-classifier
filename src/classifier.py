"""
Rule-based classification logic for complaints.
Replicates the baseline classification system.
"""

import re
from typing import Dict, Any


def clean_text(text: str) -> str:
    """Clean and normalize text for classification."""
    if not text:
        return ""
    return text.lower().strip()


def contains_keywords(text: str, keywords: list) -> bool:
    """Check if text contains any of the keywords."""
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in keywords)


def classify_product(text: str) -> str:
    """Classify the financial product type."""
    if not text:
        return "Other"
    
    if contains_keywords(text, ['credit card', 'discover card', 'mastercard', 'visa', 'amex']):
        return "Credit Card"
    elif contains_keywords(text, ['mortgage', 'home loan', 'foreclosure', 'refinance']):
        return "Mortgage"
    elif contains_keywords(text, ['student loan', 'navient', 'sallie mae', 'education loan']):
        return "Student Loan"
    elif contains_keywords(text, ['checking', 'savings', 'bank account', 'deposit']):
        return "Bank Account"
    elif contains_keywords(text, ['debt collect', 'collection agency', 'collector']):
        return "Debt Collection"
    elif contains_keywords(text, ['credit report', 'credit bureau', 'experian', 'equifax', 'transunion']):
        return "Credit Reporting"
    elif contains_keywords(text, ['auto loan', 'car loan', 'vehicle']):
        return "Vehicle Loan"
    elif contains_keywords(text, ['payday', 'personal loan', 'installment']):
        return "Personal Loan"
    elif contains_keywords(text, ['prepaid card', 'prepaid']):
        return "Prepaid Card"
    else:
        return "Other"


def classify_issue(text: str) -> str:
    """Classify the main issue category."""
    if not text:
        return "Other"
    
    # Priority order matters (fraud checked first)
    if contains_keywords(text, ['fraud', 'fraudulent', 'identity theft', 'stolen', 'unauthorized']):
        return "Fraud"
    elif contains_keywords(text, ['incorrect', 'wrong', 'error', 'mistake', 'inaccurate', 'dispute']):
        return "Billing Error"
    elif contains_keywords(text, ['cannot access', 'locked out', 'account closed', 'denied access']):
        return "Account Access"
    elif contains_keywords(text, ['rude', 'poor service', 'no response', 'ignored', 'customer service']):
        return "Customer Service"
    elif contains_keywords(text, ['harass', 'calling', 'threatening', 'abusive']):
        return "Harassment"
    elif contains_keywords(text, ['not mine', 'not my', "don't owe", 'never opened']):
        return "Account Ownership"
    elif contains_keywords(text, ['fee', 'charge', 'overcharge']):
        return "Fees/Charges"
    elif contains_keywords(text, ['reporting', 'credit report', 'credit score']):
        return "Credit Reporting"
    else:
        return "Other"


def calculate_severity(text: str, issue_category: str) -> int:
    """Calculate severity score (1-10)."""
    score = 5  # Base score
    
    if not text:
        return score
    
    # High severity indicators
    if contains_keywords(text, ['fraud', 'stolen', 'identity theft', 'unauthorized']):
        score += 4
    if contains_keywords(text, ['foreclosure', 'eviction', 'legal action', 'lawsuit']):
        score += 3
    if contains_keywords(text, ['emergency', 'urgent', 'immediate', 'critical']):
        score += 2
    if contains_keywords(text, ['harass', 'threatening', 'abusive']):
        score += 2
    
    # Medium severity indicators
    if contains_keywords(text, ['dispute', 'incorrect', 'error', 'wrong']):
        score += 1
    if contains_keywords(text, ['multiple', 'repeated', 'several times']):
        score += 1
    
    # Low severity indicators
    if contains_keywords(text, ['question', 'inquiry', 'wondering', 'clarify']):
        score -= 2
    
    # Adjust by issue category
    if issue_category in ["Fraud", "Identity Theft"]:
        score += 2
    elif issue_category == "Customer Service":
        score -= 1
    
    # Cap between 1-10
    return max(1, min(10, score))


def analyze_sentiment(text: str) -> str:
    """Analyze customer sentiment."""
    if not text or len(text) < 20:
        return "Neutral"
    
    angry_words = ['outraged', 'disgusted', 'unacceptable', 'ridiculous', 
                   'furious', 'appalled', 'scam', 'theft', 'illegal', 'violated']
    frustrated_words = ['frustrated', 'disappointed', 'dissatisfied', 'unhappy', 
                        'repeatedly', 'still waiting', 'no response', 'ignored']
    confused_words = ['confused', 'unclear', "don't understand", 'wondering', 
                      'not sure', 'help', 'explain', 'question']
    
    text_lower = text.lower()
    angry_count = sum(1 for word in angry_words if word in text_lower)
    frustrated_count = sum(1 for word in frustrated_words if word in text_lower)
    confused_count = sum(1 for word in confused_words if word in text_lower)
    
    exclamation_count = text.count('!')
    caps_words = sum(1 for word in text.split() if word.isupper() and len(word) > 2)
    
    if angry_count >= 2 or exclamation_count >= 3 or caps_words >= 3:
        return "Angry"
    elif angry_count >= 1:
        return "Angry"
    elif frustrated_count >= 2:
        return "Frustrated"
    elif frustrated_count >= 1:
        return "Frustrated"
    elif confused_count >= 2:
        return "Confused"
    else:
        return "Neutral"


def recommend_routing(issue_category: str, severity: int, sentiment: str) -> str:
    """Recommend department for routing."""
    if issue_category == "Fraud" or severity >= 9:
        return "Fraud Team"
    elif severity >= 8 or sentiment == "Angry":
        return "Escalation"
    elif issue_category in ["Billing Error", "Fees/Charges"]:
        return "Billing Dept"
    elif issue_category == "Harassment":
        return "Legal"
    elif issue_category in ["Account Access", "Account Ownership"]:
        return "Account Services"
    elif issue_category == "Credit Reporting":
        return "Credit Dispute Team"
    else:
        return "Support"


def calculate_confidence(text: str) -> float:
    """Calculate confidence score (0.0-1.0)."""
    confidence = 0.5
    
    # Narrative availability
    if text and len(text) > 50:
        confidence += 0.3
    elif text and len(text) > 0:
        confidence += 0.15
    
    # Text quality indicators
    if text and len(text) > 100:
        confidence += 0.1
    
    return min(1.0, confidence)


def classify_complaint(text: str) -> Dict[str, Any]:
    """
    Main classification function - combines all classification logic.
    
    Args:
        text: The complaint text to classify
        
    Returns:
        Dictionary with classification results
    """
    if not text or not text.strip():
        return {
            "category": "Other",
            "confidence": 0.5,
            "severity": 5,
            "route": "Support",
            "issue_category": "Other",
            "sentiment": "Neutral",
            "needs_review": True
        }
    
    # Run all classifiers
    category = classify_product(text)
    issue_category = classify_issue(text)
    severity = calculate_severity(text, issue_category)
    sentiment = analyze_sentiment(text)
    route = recommend_routing(issue_category, severity, sentiment)
    confidence = calculate_confidence(text)
    
    return {
        "category": category,
        "confidence": round(confidence, 2),
        "severity": severity,
        "route": route,
        "issue_category": issue_category,
        "sentiment": sentiment,
        "needs_review": confidence < 0.75
    }

