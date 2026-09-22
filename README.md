# Rule-based Complaint Routing Prototype (CFPB data)

## What This Is

A **complaint routing baseline** for the [CFPB Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/) that converts unstructured complaint text into structured outputs:

- **Category** (Product type: Credit Card, Mortgage, Student Loan, etc.)
- **Confidence** (0.0-1.0 score for quality assurance)
- **Severity** (1-10 urgency scale)
- **Sentiment** (Angry, Frustrated, Confused, Neutral)
- **Routing** (Suggested department assignment)

Includes a **human-in-the-loop gate** that flags low-confidence cases (<0.75) for manual review.

**Portfolio POC** demonstrating NLP-based classification with rule-based pattern matching on 284K+ real consumer complaints.

---

## 🎯 Problems It Solves

✅ **Slow Manual Triage** - Reduces processing time from 3-5 minutes to ~2 seconds per complaint  
✅ **Inconsistency** - Standardized classification logic eliminates reviewer variability  
✅ **Hidden Criticals** - Auto-flags fraud, identity theft, and high-severity cases for immediate escalation  
✅ **Auditability** - Confidence scores and structured outputs enable quality tracking  
✅ **Productization** - Clean JSON output ready for integration with ticketing/CRM systems  

---

## 📊 Problem Statement

### The Challenge
Financial institutions receive hundreds of thousands of consumer complaints annually. Manual classification and routing of these complaints is:

- **Time-Intensive**: Manual review is assumed at approximately 3 minutes per complaint
- **Error-Prone**: Human reviewers may misclassify complaints due to fatigue or inconsistency
- **Costly**: Manual labor costs for complaint processing run into millions annually
- **Slow Response**: Critical complaints (fraud, identity theft) may not receive immediate attention

### Business Impact
- **Average manual processing**: 3-5 minutes per complaint
- **Risk**: Delayed responses to critical issues can lead to regulatory penalties and customer churn

---

## 💡 Solution

A **rule-based classification system** that automatically:

1. **Classifies complaints** into product categories (Credit Card, Mortgage, Student Loan, etc.)
2. **Identifies issue types** (Fraud, Billing Error, Account Access, etc.)
3. **Assigns severity scores** (1-10 scale based on urgency and risk)
4. **Analyzes sentiment** (Angry, Frustrated, Confused, Neutral, Satisfied)
5. **Routes to appropriate teams** (Fraud Team, Legal, Escalation, Support, etc.)
6. **Provides confidence scores** (0.0-1.0) to flag cases needing manual review

### Key Features
✅ **2 seconds per complaint** (vs. 3-5 minutes manual)  
✅ **Automatic priority scoring** for critical cases  
✅ **Intelligent routing** based on issue type and severity  
✅ **Confidence flagging** for quality assurance  

---

## 📈 Results

### Performance Metrics

| Metric | Value |
|--------|-------|
| **Dataset Size** | 284,500 complaints (CFPB database) |
| **Test Sample** | 100 complaints |
| **Processing Speed** | ~2 seconds per complaint (illustrative; a 100-row demo ran in ~3.5 s total) |
| **Average Confidence** | 0.826 (82.6%) |

### Classification Distribution

![Complaint Categories](charts/complaint_categories.png)

**Top Categories:**
- Credit Reporting: 32%
- Debt Collection: 21%
- Credit Card: 17%
- Mortgage: 15%
- Bank Account: 9%

### Severity Analysis

![Severity Distribution](charts/severity_distribution.png)

**Severity Breakdown:**
- Critical (8-10): 9% - Immediate attention required
- High (6-7): 10% - Escalation needed
- Medium (4-5): 80% - Standard processing
- Low (1-3): 1% - Routine handling

### Routing Intelligence

![Routing Breakdown](charts/routing_breakdown.png)

**Department Routing:**
- Support: 48%
- Billing Dept: 27%
- Fraud Team: 8%
- Credit Dispute Team: 8%
- Escalation: 7%

### Quality Assurance

Confidence is a text-length heuristic, not a model probability.

![Confidence Distribution](charts/confidence_distribution.png)

**Confidence Levels:**
- High (>0.9): 42% - Ready for immediate processing
- Low (<0.75): 58% - Flagged for manual review

---

## 🔧 Tech Stack

### Core Technologies
- **Python 3.x** - Primary programming language
- **Pandas** - Data manipulation and analysis
- **OpenPyXL** - Excel file processing
- **JSON** - Structured data output

### NLP & Classification
- **Rule-based NLP** - Keyword matching and pattern recognition
- **Sentiment Analysis** - Emotion detection from text
- **Severity Scoring** - Risk assessment algorithm

### Visualization
- **Matplotlib** - Chart generation
- **Data visualization** - Business intelligence reporting

### Data Processing Pipeline
```
Raw Complaint → Text Cleaning → Feature Extraction → Classification → 
Severity Scoring → Sentiment Analysis → Routing Assignment → 
Confidence Calculation → Output (JSON/CSV)
```

---

## 🎯 Classification System

### 1. Product Classification
Identifies the financial product involved:
- Credit Card
- Mortgage  
- Student Loan
- Bank Account
- Debt Collection
- Credit Reporting
- Vehicle Loan
- Personal Loan

### 2. Issue Category
Determines the main problem:
- Fraud
- Billing Error
- Account Access
- Customer Service
- Harassment
- Account Ownership
- Fees/Charges
- Credit Reporting

### 3. Severity Score (1-10)
Risk-based urgency assessment:
- **10**: Critical fraud, identity theft, urgent legal action
- **8-9**: High-risk issues requiring immediate attention
- **6-7**: Significant problems needing escalation
- **4-5**: Standard complaints with moderate priority
- **1-3**: Routine inquiries or minor issues

### 4. Sentiment Analysis
Customer emotion detection:
- **Angry**: Strong negative language, threats, legal terms
- **Frustrated**: Repeated issues, dissatisfaction
- **Confused**: Questions, unclear situation
- **Neutral**: Factual reporting
- **Satisfied**: Positive resolution (rare in complaints)

### 5. Routing Recommendation
Intelligent department assignment:
- **Fraud Team**: Fraud, identity theft, unauthorized charges
- **Legal**: Harassment, threats, regulatory violations
- **Escalation**: High severity + negative sentiment
- **Billing Dept**: Billing errors, fee disputes
- **Credit Dispute Team**: Credit report issues
- **Account Services**: Account access, ownership issues
- **Support**: General inquiries, standard processing

### 6. Confidence Score (0.0-1.0)
Confidence is a text-length heuristic, not a model probability.

Quality assurance metric:
- **1.0**: Full complaint narrative available, high certainty
- **0.7**: No narrative, classification based on product/issue fields only
- **<0.75**: Flagged for manual review

---

## 📁 Project Structure

```
complaint-classifier/
├── README.md                          # This file
├── data/
│   ├── classified_sample.json         # 100 classified complaints (49KB)
│   └── validation_report.csv          # Validation checklist (10 samples)
├── charts/
│   ├── complaint_categories.png       # Product distribution
│   ├── severity_distribution.png      # Severity breakdown
│   ├── routing_breakdown.png          # Department routing
│   └── confidence_distribution.png    # Confidence levels
└── prompt_used.txt                    # Classification logic documentation
```

---

## Validation

Validation: 10-sample manual check, incomplete (see data/outputs/validation_report.csv). No accuracy claim is made.

---

## Illustrative cost model (assumptions only, not a measured saving)

Nothing in this section is a measured result. The figures below are extrapolated from timing assumptions and are provided only to show how a cost model for complaint triage could be framed.

### Worked example (assumptions only)

Assumptions, not measurements: 284,500 complaints per year, 3 minutes per manual review, ~2 seconds per automated classification, $30 per labor hour.

| Scenario | Hours per year | Labor cost per year |
|----------|----------------|---------------------|
| Manual (284,500 × 3 min) | approximately 14,250 | approximately $427,500 |
| Automated (284,500 × 2 sec) | approximately 158 | approximately $4,740 |

The difference between the two rows is an extrapolation from these assumptions, not a measured saving.

### Calculate Your Own Scenario

Use the built-in calculator to estimate time and cost under your own assumptions:

```bash
python3 scripts/roi.py --cases 100000 --auto-rate 0.5
```

**Sample Output:**

```
======================================================================
COMPLAINT CLASSIFIER ROI ANALYSIS
======================================================================

📊 INPUT PARAMETERS
----------------------------------------------------------------------
  Annual complaint volume:       100,000 cases
  Automation rate:               50%
  Manual processing time:        6.0 min/case
  Automated processing time:     3.0 sec/case
  Labor cost:                    $30.00/hour

📈 BASELINE (100% Manual Processing)
----------------------------------------------------------------------
  Total hours required:          10,000 hours/year
  Total cost:                    $300,000.00/year

⚡ WITH AUTOMATION
----------------------------------------------------------------------
  Automated cases:               50,000 cases
  Manual cases remaining:        50,000 cases
  Total hours required:          5,042 hours/year
  Total cost:                    $151,250.00/year

💰 ESTIMATED SAVINGS
----------------------------------------------------------------------
  Time saved:                    4,958 hours/year (49.6%)
  Cost saved:                    $148,750.00/year (49.6%)
  Equivalent FTE saved:          2.38 full-time employees

⚠️  NOTE: These are illustrative estimates based on assumptions.
    Actual results will vary based on implementation and workflows.
======================================================================
```

### Scenario Examples

**Conservative Estimate** (30% automation, 7 min/case):
```bash
python3 scripts/roi.py --cases 284500 --minutes 7 --auto-rate 0.3 --hourly-cost 30
```

**Optimistic Estimate** (70% automation, 5 min/case):
```bash
python3 scripts/roi.py --cases 284500 --minutes 5 --auto-rate 0.7 --hourly-cost 35
```

### Parameters

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `--cases` | *required* | any | Annual complaint volume |
| `--minutes` | 6.0 | 5-7 | Minutes per manual case |
| `--auto-rate` | 0.5 | 0.0-1.0 | Automation rate (0.5 = 50%) |
| `--hourly-cost` | 30.0 | any | Labor cost per hour (USD) |
| `--seconds-auto` | 3.0 | any | Seconds per automated case |

**Note:** These calculations provide illustrative estimates. Actual results depend on complaint complexity, team expertise, and implementation details.

---

## 🚀 Use Cases

### Financial Institutions
- Consumer complaint processing
- Regulatory compliance (CFPB reporting)
- Customer service optimization

### E-commerce Platforms
- Product review analysis
- Customer feedback routing
- Quality assurance automation

### Healthcare
- Patient complaint management
- HIPAA compliance monitoring
- Service quality improvement

### Government Agencies
- Citizen complaint processing
- Regulatory enforcement
- Public service optimization

---

## 🔄 Reproduce Charts

To regenerate all visualization charts from the classified data:

```bash
pip install -r requirements.txt
make charts
```

This will:
1. Install required dependencies (papermill, matplotlib, numpy, pandas)
2. Execute the `notebooks/generate_charts.ipynb` notebook via papermill
3. Generate all PNG charts in the `charts/` directory:
   - `complaint_categories.png`
   - `confidence_distribution.png`
   - `routing_breakdown.png`
   - `severity_distribution.png`

---

## 🚀 Run the API

To start the FastAPI server:

```bash
pip install -r requirements.txt
uvicorn src.app:app --reload
```

The API will be available at `http://localhost:8000` with:
- **Interactive docs**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc
- **Health check**: `GET /health`
- **Classification**: `POST /classify`

### Example API Usage

```bash
# Health check
curl http://localhost:8000/health

# Classify a complaint
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "I found unauthorized charges on my credit card. This is fraud!"}'
```

**Response:**
```json
{
  "category": "Credit Card",
  "confidence": 0.95,
  "severity": 9,
  "route": "Fraud Team",
  "issue_category": "Fraud",
  "sentiment": "Angry",
  "needs_review": false
}
```

### Run Tests

```bash
pytest tests/test_app.py -v
```

---

## 🐳 Run with Docker

The API can be containerized and run with Docker for consistent deployment across environments.

### Build the Docker Image

```bash
docker build -t complaint-classifier .
```

### Run the Container

```bash
docker run -p 8000:8000 complaint-classifier
```

The API will be available at `http://localhost:8000`

### Docker Compose (Optional)

Create a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    restart: unless-stopped
```

Run with:
```bash
docker-compose up
```

### Image Details

- **Base Image**: `python:3.11-slim`
- **Port**: 8000
- **Size**: ~200MB (optimized with slim base)
- **Includes**: All dependencies from `requirements.txt`

---

## LLM Assist (stub)

`src/llm_assist.py` is a stub; this version makes no LLM call. Classification is rule-based.

The stub only checks whether an `OPENAI_API_KEY` or Azure OpenAI environment variable is set and returns `None`; the API (`src/app.py`) uses `src/classifier.py`.

---

## 📊 Sample Output

```json
{
  "complaint_id": 1816726,
  "classification": {
    "product": "Credit Card",
    "issue_category": "Billing Error",
    "severity_score": 7,
    "sentiment": "Angry",
    "recommended_routing": "Escalation",
    "confidence": 1.0
  },
  "needs_review": false,
  "original_data": {
    "date_received": "2016-04-03",
    "company": "DISCOVER BANK",
    "state": "NV",
    "submitted_via": "Web"
  }
}
```

---

## 🎓 Key Insights

### Technical Learnings
1. **Narrative text is crucial** - Complaints with full narratives receive confidence 1.0
2. **Keyword-based NLP** works well for structured complaint data
3. **Severity scoring** requires domain expertise and continuous refinement
4. **Confidence flagging** enables quality assurance at scale

### Business Learnings
1. **Credit reporting** is the #1 complaint category (32%)
2. **Most complaints are medium severity** (80%) - allows focus on critical cases
3. **Less than 10% require escalation** - efficient resource allocation
4. **58% lack narratives** - opportunity to improve data collection

---

## ⚠️ Assumptions & Limitations

This is a **portfolio proof-of-concept** with the following scope:

### What Was Measured
- ✅ **100-row demo** processed in ~3.5 seconds (~0.035s per complaint)
- ✅ Confidence scoring correlates with narrative availability (1.0 = full text, 0.7 = metadata only)

### What Is Illustrative
- ROI numbers in the illustrative cost model are extrapolated from manual timing assumptions
- ⚠️ **Full-dataset timings** (284K complaints) were **not captured** in production conditions
- ⚠️ Rule-based classification may miss edge cases requiring ML models
- ⚠️ Sentiment detection is conservative (92% classified as "Neutral")

### Known Constraints
- 58% of complaints lack narrative text (limits classification depth)
- Issue categorization needs refinement (46% classified as "Other")
- Binary confidence scoring (0.7 or 1.0) lacks gradient
- No comparison with production complaint routing systems

**Intended Use**: Baseline demonstration for portfolio/interview discussions, not production deployment.

---

## 🔮 Future Enhancements

### Phase 2 Improvements
- [ ] Machine learning model (BERT, RoBERTa) as a comparison to the rule-based baseline
- [ ] Multi-language support (Spanish, Chinese, etc.)
- [ ] Real-time API for live complaint processing
- [ ] Dashboard for monitoring and analytics
- [ ] A/B testing framework for continuous improvement

### Advanced Features
- [ ] Duplicate complaint detection
- [ ] Trend analysis and anomaly detection
- [ ] Predictive resolution time estimation
- [ ] Automated response generation
- [ ] Customer satisfaction prediction

---

## 📞 Contact & Attribution

**Dataset Source**: Consumer Financial Protection Bureau (CFPB)  
**License**: Public Domain  
**Project Type**: Portfolio/Educational  

---

## 📝 Citation

If you use this project, please cite:

```
Rule-based Complaint Routing Prototype (CFPB data)
Rule-based complaint routing prototype
Processing: 2 sec/complaint (illustrative)
Dataset: CFPB Consumer Complaint Database (284,500 complaints)
```

---

## ⭐ Key Statistics Summary

| Metric | Value |
|--------|-------|
| 📊 Total Complaints | 284,500 |
| ⚡ Speed | 2 sec/complaint |
| 🎯 Confidence | 82.6% average |

---

**Built with Python. Rule-based NLP on CFPB public data.**
