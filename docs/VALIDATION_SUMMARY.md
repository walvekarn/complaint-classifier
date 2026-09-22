# Classification Validation Summary

## Overview
Rule-based classification run on the first 100 complaints from 312,628 total complaints.

Validation: 10-sample manual check, incomplete (see data/outputs/validation_report.csv). No accuracy claim is made.

---

## Validation Status (First 10 Complaints)

### Status
- **Manual check**: 10 complaints selected; all 10 rows in data/outputs/validation_report.csv are marked validation_status=Pending
- **High Confidence Cases**: 6/10 (60%)
- **Low Confidence Cases**: 4/10 (40%)

### What the 10-sample check compares
For each complaint, the form lists:
1. Original complaint text
2. Rule-based classification (6 fields)
3. Confidence score (a text-length heuristic, not a model probability)
4. The original product/issue fields, for comparison

---

## 📊 Distribution Analysis (100 Complaints)

### 1. Product Distribution
| Product | Count | Percentage |
|---------|-------|------------|
| Credit Reporting | 32 | 32.0% |
| Debt Collection | 21 | 21.0% |
| Credit Card | 17 | 17.0% |
| Mortgage | 15 | 15.0% |
| Bank Account | 9 | 9.0% |
| Student Loan | 5 | 5.0% |
| Other | 1 | 1.0% |

### 2. Severity Score Distribution
| Severity Level | Count | Percentage |
|----------------|-------|------------|
| **Critical (8-10)** 🚨 | 9 | 9.0% |
| **High (6-7)** ⚠️ | 10 | 10.0% |
| **Medium (4-5)** ⚡ | 80 | 80.0% |
| **Low (1-3)** ℹ️ | 1 | 1.0% |

**Average Severity**: 5.46/10

### 3. Routing to Escalation
- **Escalation Team**: 7 complaints (7%)
- **Other Routing**: 93 complaints (93%)

**All Routing Destinations**:
- Support: 48%
- Billing Dept: 27%
- Fraud Team: 8%
- Credit Dispute Team: 8%
- Escalation: 7%
- Account Services: 1%
- Legal: 1%

### 4. Confidence Score Analysis
- **High confidence (>0.9)**: 42 complaints (42%) ✓
- **Medium confidence (0.75-0.9)**: 0 complaints (0%)
- **Low confidence (<0.75)**: 58 complaints (58%) ⚠️

**Statistics**:
- Average: 0.826
- Min: 0.70
- Max: 1.00

**Binary Distribution**: 
- Complaints WITH narratives: 1.00 confidence
- Complaints WITHOUT narratives: 0.70 confidence

Confidence is a text-length heuristic, not a model probability.

---

## Validation Examples (status: Pending)

The three rows below show what the check compares. None has been marked correct or wrong yet.

### Example 1: High Confidence Case
**Complaint ID**: 1816726
- **Company**: DISCOVER BANK
- **Original Product**: Credit card
- **Classifier Product**: Credit Card
- **Classifier Issue**: Billing Error
- **Severity**: 7/10
- **Sentiment**: Angry
- **Routing**: Escalation
- **Confidence**: 1.0
- **Validation status**: Pending

### Example 2: Low Confidence Case
**Complaint ID**: 1509954
- **Company**: Experian Information Solutions Inc.
- **Original Product**: Credit reporting
- **Classifier Product**: Credit Reporting
- **Classifier Issue**: Billing Error
- **Severity**: 5/10
- **Sentiment**: Neutral
- **Routing**: Billing Dept
- **Confidence**: 0.7
- **Narrative**: [NONE PROVIDED]
- **Validation status**: Pending

### Example 3: Fraud Keyword Case
**Complaint ID**: 1786527
- **Company**: CITIBANK, N.A.
- **Original Issue**: Identity theft / Fraud / Embezzlement
- **Classifier Product**: Credit Card
- **Classifier Issue**: Fraud
- **Severity**: 7/10
- **Routing**: Fraud Team
- **Confidence**: 0.7
- **Validation status**: Pending

---

## 🎯 Pattern Analysis

### Observed behaviour of the rules
1. **Fraud keyword mapping**: "Identity theft" in the original issue field maps to the "Fraud" category by rule
2. **Routing logic**: High severity routes to Escalation or Fraud Team by rule
3. **Confidence correlation**: High confidence = narrative available (text-length heuristic)

### Potential Issues ⚠️
1. **Issue categorization**: 46% classified as "Other" (too generic)
2. **Sentiment detection**: 92% neutral (may be under-detecting frustration)
3. **Narrative dependency**: 58% lack narratives (limits classification depth)
4. **Binary confidence**: Only 0.7 or 1.0 (no gradient)

---

## 📈 Confidence Score Reliability

### High Confidence Cases (1.0)
- **Count**: 42 complaints
- **Characteristic**: All have full complaint narratives
- **Accuracy**: Not established (validation pending)

### Low Confidence Cases (0.7)
- **Count**: 58 complaints  
- **Characteristic**: No complaint narratives
- **Accuracy**: Not established (relies only on product/issue fields)
- **Handling**: Flagged for manual review

---

## 🎓 Key Insights

### Strengths
- Fraud keywords detected by rule
- Severity scoring follows logical patterns (fraud = high severity)
- Routing recommendations align with issue type

### Limitations
- 58% of complaints lack narrative text
- Sentiment analysis appears conservative
- Issue categorization needs more granularity
- Confidence scoring is binary (0.7 or 1.0 only)

### Recommendations
1. **Complete the manual check** in validation_form.txt before reporting any accuracy figure
2. **Manual review** all "Other" issue categories to improve classification
3. **Enhance sentiment** analysis to catch subtle frustration/anger
4. **Validate severity** scoring with domain experts
5. **Refine confidence** calculation to provide gradient (not binary)
6. **Focus on narratives** - consider processing only complaints with full text

---

## 📁 Output Files Created

1. **classified_sample_100.json** (49 KB)
   - Full structured classification data
   - All 6 classification fields per complaint
   - JSON format for easy integration

2. **classification_report.txt** (3.3 KB)
   - Human-readable summary report
   - Statistics and visualizations
   - Action items

3. **validation_form.txt**
   - Manual validation checklist for first 10 complaints
   - Space to mark ✓/✗ for each field
   - Summary scoring section

4. **metrics_summary.txt**
   - Detailed statistical analysis
   - Distribution breakdowns
   - Recommendations

5. **VALIDATION_SUMMARY.md** (this file)
   - Validation status
   - Pattern analysis
   - Key findings

---

## 📋 Manual Validation Checklist Status

**Instructions**: Review validation_form.txt and mark each classification as ✓ (Correct) or ✗ (Wrong)

**Current status** (data/outputs/validation_report.csv):
- Product: Pending manual review
- Issue: Pending manual review
- Severity: Pending manual review
- Sentiment: Pending manual review
- Routing: Pending manual review

**Next Step**: Complete manual validation in validation_form.txt before any accuracy metric is reported.

---

## 📞 Questions to Answer Through Manual Validation

1. **Are product classifications accurate?** Pending manual review
2. **Are issue categories appropriate?** Pending manual review
3. **Are severity scores reasonable?** Pending manual review  
4. **Is sentiment accurately detected?** Pending manual review (92% neutral suggests conservative detection)
5. **Is routing logical?** Pending manual review
6. **Which confidence scores are reliable?** Pending manual review; confidence is a text-length heuristic, not a model probability

---

*Validation Date: 2025-11-05*  
*Dataset: First 100 of 312,628 total complaints*  
*Classification System: Rule-based NLP with keyword matching*
