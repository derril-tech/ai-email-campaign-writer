"""
Email utility functions for validation and processing.
"""

import re
import hashlib
from typing import Optional, List
from email_validator import validate_email as validate_email_address, EmailNotValidError


def validate_email(email: str) -> bool:
    """
    Validate email address format and basic structure.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        validate_email_address(email)
        return True
    except EmailNotValidError:
        return False


def extract_domain(email: str) -> Optional[str]:
    """
    Extract domain from email address.
    
    Args:
        email: Email address
        
    Returns:
        Optional[str]: Domain name or None if invalid
    """
    if not validate_email(email):
        return None
    
    return email.split('@')[1].lower()


def is_disposable_email(email: str) -> bool:
    """
    Check if email is from a disposable email service.
    
    Args:
        email: Email address to check
        
    Returns:
        bool: True if disposable, False otherwise
    """
    domain = extract_domain(email)
    if not domain:
        return False
    
    # List of common disposable email domains
    disposable_domains = {
        '10minutemail.com', 'guerrillamail.com', 'mailinator.com',
        'tempmail.org', 'throwaway.email', 'yopmail.com',
        'temp-mail.org', 'sharklasers.com', 'getairmail.com',
        'mailnesia.com', 'maildrop.cc', 'mailcatch.com',
        'dispostable.com', 'mailnull.com', 'spam4.me',
        'bccto.me', 'chacuo.net', 'dispostable.com',
        'fakeinbox.com', 'fakemailgenerator.com'
    }
    
    return domain in disposable_domains


def generate_email_hash(email: str) -> str:
    """
    Generate a hash for email address (for privacy).
    
    Args:
        email: Email address
        
    Returns:
        str: SHA-256 hash of email
    """
    return hashlib.sha256(email.lower().encode()).hexdigest()


def normalize_email(email: str) -> str:
    """
    Normalize email address (lowercase, trim whitespace).
    
    Args:
        email: Email address
        
    Returns:
        str: Normalized email address
    """
    return email.lower().strip()


def extract_email_parts(email: str) -> dict:
    """
    Extract parts of email address.
    
    Args:
        email: Email address
        
    Returns:
        dict: Dictionary with local_part and domain
    """
    if not validate_email(email):
        return {}
    
    local_part, domain = email.split('@')
    return {
        'local_part': local_part,
        'domain': domain.lower(),
        'full_email': email.lower()
    }


def is_business_email(email: str) -> bool:
    """
    Check if email appears to be from a business domain.
    
    Args:
        email: Email address to check
        
    Returns:
        bool: True if business email, False otherwise
    """
    domain = extract_domain(email)
    if not domain:
        return False
    
    # Common personal email providers
    personal_domains = {
        'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
        'aol.com', 'icloud.com', 'protonmail.com', 'tutanota.com',
        'zoho.com', 'yandex.com', 'mail.ru', 'qq.com'
    }
    
    return domain not in personal_domains


def validate_email_list(emails: List[str]) -> dict:
    """
    Validate a list of email addresses.
    
    Args:
        emails: List of email addresses
        
    Returns:
        dict: Validation results with valid and invalid emails
    """
    results = {
        'valid': [],
        'invalid': [],
        'disposable': [],
        'business': [],
        'personal': []
    }
    
    for email in emails:
        normalized_email = normalize_email(email)
        
        if not validate_email(normalized_email):
            results['invalid'].append(normalized_email)
            continue
        
        results['valid'].append(normalized_email)
        
        if is_disposable_email(normalized_email):
            results['disposable'].append(normalized_email)
        elif is_business_email(normalized_email):
            results['business'].append(normalized_email)
        else:
            results['personal'].append(normalized_email)
    
    return results


def sanitize_email(email: str) -> str:
    """
    Sanitize email address for safe storage/display.
    
    Args:
        email: Email address
        
    Returns:
        str: Sanitized email address
    """
    if not validate_email(email):
        return ""
    
    # Remove any potentially dangerous characters
    sanitized = re.sub(r'[^\w@.-]', '', email.lower().strip())
    return sanitized


def get_email_provider(email: str) -> Optional[str]:
    """
    Get email provider name from email address.
    
    Args:
        email: Email address
        
    Returns:
        Optional[str]: Provider name or None
    """
    domain = extract_domain(email)
    if not domain:
        return None
    
    # Map common domains to provider names
    providers = {
        'gmail.com': 'Gmail',
        'yahoo.com': 'Yahoo',
        'hotmail.com': 'Hotmail',
        'outlook.com': 'Outlook',
        'aol.com': 'AOL',
        'icloud.com': 'iCloud',
        'protonmail.com': 'ProtonMail',
        'tutanota.com': 'Tutanota',
        'zoho.com': 'Zoho',
        'yandex.com': 'Yandex',
        'mail.ru': 'Mail.ru',
        'qq.com': 'QQ Mail'
    }
    
    return providers.get(domain, domain)


def is_valid_email_format(email: str) -> bool:
    """
    Check if email has valid format using regex.
    
    Args:
        email: Email address to check
        
    Returns:
        bool: True if format is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def extract_emails_from_text(text: str) -> List[str]:
    """
    Extract email addresses from text.
    
    Args:
        text: Text to search for emails
        
    Returns:
        List[str]: List of found email addresses
    """
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(pattern, text)
    
    # Filter valid emails
    valid_emails = []
    for email in emails:
        if validate_email(email):
            valid_emails.append(normalize_email(email))
    
    return list(set(valid_emails))  # Remove duplicates
