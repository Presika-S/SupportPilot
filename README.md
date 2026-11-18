
# SupportPilot – AI Ticket Resolution Agent

## Overview
SupportPilot is an AI-powered support ticket management system that automatically classifies support tickets, predicts issue severity, and assigns priority to improve IT support workflows.

## Key Features
- Ticket submission and management
- AI-based ticket category classification
- Automated severity prediction
- Priority assignment based on severity and business impact
- SQLite database integration
- Ticket history and detailed ticket tracking
- REST API integration

## Technology Stack
- **Backend:** Python, Flask
- **Machine Learning:** Scikit-learn, TF-IDF, Logistic Regression
- **Database:** SQLite
- **Frontend:** HTML, CSS, Bootstrap, JavaScript

## Model Performance
- Dataset: 47,834 support ticket records
- Classification Accuracy: 86.73% (Logistic Regression benchmark)
- Classification Method: TF-IDF with Logistic Regression

*Severity prediction uses rule-based keyword matching and has not yet been independently accuracy-validated.*

## Installation

```bash
git clone https://github.com/Presika-S/SupportPilot.git
cd SupportPilot
pip install flask pandas scikit-learn
```

## Run the Application

```bash
python app.py
```

Open: http://127.0.0.1:5000

## Project Structure

```text
SupportPilot/
├── app.py
├── classifier.py
├── database.py
├── severity.py
├── priority.py
├── train_model.py
├── models/
├── templates/
└── README.md
```

## Project Status
Milestone 1 prototype implemented with ticket submission, AI classification, severity prediction, priority assignment, and ticket tracking.
