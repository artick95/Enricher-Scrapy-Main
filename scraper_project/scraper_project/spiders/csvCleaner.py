import pandas as pd
import re

def is_valid_email(email):
    """Check if the email is valid and doesn't contain invalid patterns"""
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False

    invalid_patterns = [
        r"\.\w+@",  # Emails starting with a dot followed by word characters
        r"sentry",  # Emails containing the word "sentry"
        r"calendar|google",  # Emails containing the words "calendar" or "google"
        r"amazon",  # Emails containing the word "amazon"
        r"@\w+\.\w+\.\w+\.\w+"  # Emails with more than 3 dots after '@'
    ]

    for pattern in invalid_patterns:
        if re.search(pattern, email):
            return False

    return True

def best_email(emails):
    """Select the best email based on certain criteria"""
    emails = [email for email in emails if is_valid_email(email)]
    return emails[0] if emails else None

def email_cleaning_logic(emails):
    """Main logic for cleaning and prioritizing emails"""
    # Get the best email
    best_email_addr = best_email(emails)
    output = {'best_email': best_email_addr}
    
    # Get up to 6 additional emails
    additional_emails = [email for email in emails if email != best_email_addr and is_valid_email(email)]
    for idx, email in enumerate(additional_emails[:6], 1):
        output[f'email{idx}'] = email

    return output

# Test
if __name__ == "__main__":
    emails = [
        "test1@example.com", 
        "sentry@example.com", 
        "calendar@google.com", 
        "amazon@example.com", 
        "test2@example.com", 
        "test3@example.com", 
        "test4@example.com", 
        "test5@example.com", 
        "test6@example.com", 
        "test7@example.com"
    ]
    print(email_cleaning_logic(emails))
