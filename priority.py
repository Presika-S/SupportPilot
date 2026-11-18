
def calculate_priority(severity, business_impact):

    severity = str(severity).lower().strip()
    business_impact = str(business_impact).lower().strip()

    if severity == "critical":
        return "P1"

    elif severity == "high" and business_impact == "high":
        return "P1"

    elif severity == "high":
        return "P2"

    elif severity == "medium" and business_impact == "high":
        return "P2"

    elif severity == "medium":
        return "P3"

    elif severity == "low" and business_impact == "high":
        return "P3"

    elif severity == "low":
        return "P4"

    return "P3"


if __name__ == "__main__":

    test_cases = [
        ("Critical", "High"),
        ("High", "High"),
        ("High", "Medium"),
        ("Medium", "High"),
        ("Medium", "Low"),
        ("Low", "High"),
        ("Low", "Low")
    ]

    for severity, impact in test_cases:
        priority = calculate_priority(severity, impact)

        print(
            f"Severity: {severity} | "
            f"Impact: {impact} | "
            f"Priority: {priority}"
        )
