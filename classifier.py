

import pickle
import re

from severity import predict_severity
from priority import calculate_priority
from database import create_table, save_ticket


# Keep preprocessing consistent with train_model.py
def clean_text(text):
    text = str(text).lower()

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Remove email addresses
    text = re.sub(
        r"\b[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}\b",
        " ",
        text
    )

    # Remove URLs
    text = re.sub(
        r"https?://\S+|www\.\S+",
        " ",
        text
    )

    # Remove common greetings and sign-offs
    patterns = [
        r"\bdear\s+(sir|madam|team|all|colleague)\b",
        r"\bkind regards\b",
        r"\bbest regards\b",
        r"\bthanks and regards\b",
        r"\bthank you and regards\b",
        r"\byours sincerely\b",
        r"\byours faithfully\b"
    ]

    for pattern in patterns:
        text = re.sub(pattern, " ", text)

    return re.sub(r"\s+", " ", text).strip()


# Load the existing Logistic Regression model
with open("models/ticket_classifier.pkl", "rb") as f:
    model = pickle.load(f)


def process_ticket(
    employee_name,
    email,
    title,
    description,
    business_impact="Medium",
    department=""
):
    # Clean ticket description
    cleaned_description = clean_text(description)

    # Predict ticket category
    category = model.predict([cleaned_description])[0]

    # Calculate AI confidence
    probabilities = model.predict_proba(
        [cleaned_description]
    )[0]

    confidence = float(max(probabilities))

    # Predict severity
    severity = predict_severity(description)

    # Calculate priority
    priority = calculate_priority(
        severity,
        business_impact
    )

    # Ensure database table exists
    create_table()

    # Save ticket
    ticket_id = save_ticket(
        employee_name=employee_name,
        email=email,
        title=title,
        description=description,
        category=category,
        severity=severity,
        priority=priority,
        confidence=confidence,
        department=department
    )

    # Prepare response
    return {
        "ticket_id": ticket_id,
        "employee_name": employee_name,
        "email": email,
        "department": department,
        "title": title,
        "description": description,
        "category": category,
        "severity": severity,
        "business_impact": business_impact,
        "priority": priority,
        "confidence": round(confidence, 4)
    }
