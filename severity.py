
def predict_severity(description):

    text = str(description).lower()

    critical_keywords = [
        "server down",
        "server is down",
        "production server",
        "production down",
        "system outage",
        "complete outage",
        "business stopped",
        "employees cannot access the system",
        "entire system unavailable",
        "critical infrastructure failure"
    ]

    high_keywords = [
        "network down",
        "vpn not working",
        "unable to access",
        "system unavailable",
        "multiple users affected",
        "laptop completely unusable",
        "cannot access critical application",
        "database unavailable",
        "security breach"
    ]

    medium_keywords = [
        "slow performance",
        "error",
        "not responding",
        "connection issue",
        "application issue",
        "laptop not starting",
        "software crashing",
        "printer not working"
    ]

    low_keywords = [
        "installation request",
        "software request",
        "general enquiry",
        "minor issue",
        "information request",
        "password reset request"
    ]

    if any(word in text for word in critical_keywords):
        return "Critical"

    elif any(word in text for word in high_keywords):
        return "High"

    elif any(word in text for word in medium_keywords):
        return "Medium"

    elif any(word in text for word in low_keywords):
        return "Low"

    return "Medium"


if __name__ == "__main__":

    test_tickets = [
        "Production server down completely",
        "VPN not working for employees",
        "Application showing an error",
        "General enquiry about software",
        "Laptop not starting"
    ]

    for ticket in test_tickets:
        print("Ticket:", ticket)
        print("Severity:", predict_severity(ticket))
        print("-" * 50)
