
"""Scholarship screening system with input validation."""

import json

# Global configuration
results = {}
INCOME_LIMIT = 800000
CUTOFF = 85


def calculate_merit_score(gpa, credit_count):
    """Calculate the merit score using the fixed formula."""
    return gpa * 10 + credit_count * 2


def evaluate_applicant(student_id, test_scores, logs=None):
    """Evaluate an applicant and record scholarship eligibility."""
    if logs is None:
        logs = []

    gpa = test_scores.get("gpa")
    credit_count = test_scores.get("credits", 0)
    income = test_scores.get("income", 0)

    # Validate GPA.
    if (
        not isinstance(gpa, (int, float))
        or isinstance(gpa, bool)
        or not 0 <= gpa <= 10
    ):
        raise ValueError("GPA must be between 0 and 10.")

    # Validate credits.
    if (
        not isinstance(credit_count, int)
        or isinstance(credit_count, bool)
        or credit_count < 0
    ):
        raise ValueError("Credits must be a non-negative integer.")

    # Validate income.
    if (
        not isinstance(income, (int, float))
        or isinstance(income, bool)
        or income < 0
    ):
        raise ValueError("Income must be a non-negative number.")

    score = calculate_merit_score(gpa, credit_count)
    eligible = score >= CUTOFF and income < INCOME_LIMIT

    results[student_id] = {
        "score": score,
        "eligible": eligible,
    }

    # Use an f-string for logging.
    logs.append(f"{student_id} scored {score}")

    return eligible


def persist_results(file="scholarships.json"):
    """Save scholarship results to a JSON file."""
    with open(file, "w", encoding="utf-8") as output_file:
        json.dump(results, output_file, indent=4)


def load_results(file="scholarships.json"):
    """Load saved results and handle expected file errors."""
    try:
        with open(file, "r", encoding="utf-8") as input_file:
            loaded_results = json.load(input_file)
    except (OSError, json.JSONDecodeError):
        loaded_results = {}

    # Update the existing dictionary without using 'global'.
    results.clear()
    results.update(loaded_results)


def print_shortlist():
    """Print applicants who meet the scholarship cutoff."""
    print("Shortlisted applicants:")

    for student_id, applicant in results.items():
        if applicant["eligible"]:
            print(f"  {student_id} score = {applicant['score']}")


def main():
    """Run the scholarship screening program."""
    applicants = [
        ("U001", {"gpa": 9.1, "credits": 4, "income": 450000}),
        ("U002", {"gpa": 7.2, "credits": 1, "income": 300000}),
        ("U003", {"gpa": 12.5, "credits": -3, "income": -1}),
        ("U004", {"gpa": 6.5}),
        ("U005", {"gpa": 8.4, "credits": 3, "income": 600000}),
    ]

    # Validate applicants and skip invalid records.
    for student_id, scores in applicants:
        try:
            evaluate_applicant(student_id, scores)
        except ValueError as error:
            print(f"Skipping {student_id}: {error}")

    persist_results()
    load_results()
    print_shortlist()


if __name__ == "__main__":
    main()
