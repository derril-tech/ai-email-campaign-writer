"""
Validation utility functions for input sanitization and validation.
"""

import re
import urllib.parse
from typing import Optional, List, Dict, Any
import mimetypes


def validate_phone_number(phone: str, country_code: str = "US") -> bool:
    """
    Validate phone number format.
    
    Args:
        phone: Phone number to validate
        country_code: Country code for validation rules
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not phone:
        return False
    
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    
    # Basic validation for US phone numbers
    if country_code == "US":
        # US phone numbers should be 10 or 11 digits
        if len(digits_only) == 10:
            return True
        elif len(digits_only) == 11 and digits_only.startswith('1'):
            return True
    
    # International format (E.164)
    if digits_only.startswith('+'):
        digits_only = digits_only[1:]
    
    # Most international numbers are 7-15 digits
    if 7 <= len(digits_only) <= 15:
        return True
    
    return False


def validate_url(url: str, allowed_schemes: Optional[List[str]] = None) -> bool:
    """
    Validate URL format and scheme.
    
    Args:
        url: URL to validate
        allowed_schemes: List of allowed URL schemes (default: http, https)
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not url:
        return False
    
    if allowed_schemes is None:
        allowed_schemes = ['http', 'https']
    
    try:
        parsed = urllib.parse.urlparse(url)
        
        # Check if scheme is allowed
        if parsed.scheme not in allowed_schemes:
            return False
        
        # Check if netloc (domain) is present
        if not parsed.netloc:
            return False
        
        # Basic domain validation
        domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
        if not re.match(domain_pattern, parsed.netloc):
            return False
        
        return True
        
    except Exception:
        return False


def sanitize_input(
    text: str,
    max_length: Optional[int] = None,
    allowed_tags: Optional[List[str]] = None,
    strip_html: bool = True
) -> str:
    """
    Sanitize user input text.
    
    Args:
        text: Text to sanitize
        max_length: Maximum length allowed
        allowed_tags: List of allowed HTML tags (if strip_html=False)
        strip_html: Whether to strip HTML tags
        
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    
    # Convert to string if needed
    text = str(text)
    
    # Strip HTML tags if requested
    if strip_html:
        text = re.sub(r'<[^>]+>', '', text)
    elif allowed_tags:
        # Only allow specific HTML tags
        allowed_pattern = '|'.join(allowed_tags)
        text = re.sub(rf'<(?!\/?(?:{allowed_pattern})\b)[^>]+>', '', text)
    
    # Remove null bytes and control characters
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # Truncate if max length specified
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text


def validate_file_type(
    filename: str,
    allowed_extensions: Optional[List[str]] = None,
    allowed_mime_types: Optional[List[str]] = None
) -> bool:
    """
    Validate file type based on extension and MIME type.
    
    Args:
        filename: Name of the file
        allowed_extensions: List of allowed file extensions
        allowed_mime_types: List of allowed MIME types
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not filename:
        return False
    
    # Get file extension
    extension = filename.lower().split('.')[-1] if '.' in filename else ''
    
    # Check extension if specified
    if allowed_extensions and extension not in allowed_extensions:
        return False
    
    # Check MIME type if specified
    if allowed_mime_types:
        mime_type, _ = mimetypes.guess_type(filename)
        if mime_type not in allowed_mime_types:
            return False
    
    return True


def validate_email_list(emails: List[str]) -> Dict[str, List[str]]:
    """
    Validate a list of email addresses.
    
    Args:
        emails: List of email addresses
        
    Returns:
        Dict[str, List[str]]: Validation results
    """
    results = {
        'valid': [],
        'invalid': [],
        'duplicates': []
    }
    
    seen_emails = set()
    
    for email in emails:
        email = email.strip().lower()
        
        # Check for duplicates
        if email in seen_emails:
            results['duplicates'].append(email)
            continue
        
        seen_emails.add(email)
        
        # Basic email validation
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            results['valid'].append(email)
        else:
            results['invalid'].append(email)
    
    return results


def validate_password_strength(password: str) -> Dict[str, Any]:
    """
    Validate password strength.
    
    Args:
        password: Password to validate
        
    Returns:
        Dict[str, Any]: Password strength analysis
    """
    if not password:
        return {
            'valid': False,
            'score': 0,
            'issues': ['Password is empty']
        }
    
    issues = []
    score = 0
    
    # Length check
    if len(password) < 8:
        issues.append('Password must be at least 8 characters long')
    else:
        score += 1
    
    if len(password) >= 12:
        score += 1
    
    # Character variety checks
    if re.search(r'[a-z]', password):
        score += 1
    else:
        issues.append('Password must contain at least one lowercase letter')
    
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        issues.append('Password must contain at least one uppercase letter')
    
    if re.search(r'\d', password):
        score += 1
    else:
        issues.append('Password must contain at least one number')
    
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        issues.append('Password must contain at least one special character')
    
    # Common password check (simplified)
    common_passwords = {
        'password', '123456', '123456789', 'qwerty', 'abc123',
        'password123', 'admin', 'letmein', 'welcome', 'monkey'
    }
    
    if password.lower() in common_passwords:
        issues.append('Password is too common')
        score -= 1
    
    # Determine strength level
    if score >= 5:
        strength = 'strong'
    elif score >= 3:
        strength = 'medium'
    else:
        strength = 'weak'
    
    return {
        'valid': len(issues) == 0,
        'score': score,
        'strength': strength,
        'issues': issues
    }


def validate_json_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Basic JSON schema validation.
    
    Args:
        data: Data to validate
        schema: Schema definition
        
    Returns:
        Dict[str, Any]: Validation results
    """
    errors = []
    
    for field, rules in schema.items():
        if field not in data:
            if rules.get('required', False):
                errors.append(f"Missing required field: {field}")
            continue
        
        value = data[field]
        
        # Type validation
        expected_type = rules.get('type')
        if expected_type:
            if expected_type == 'string' and not isinstance(value, str):
                errors.append(f"Field {field} must be a string")
            elif expected_type == 'integer' and not isinstance(value, int):
                errors.append(f"Field {field} must be an integer")
            elif expected_type == 'number' and not isinstance(value, (int, float)):
                errors.append(f"Field {field} must be a number")
            elif expected_type == 'boolean' and not isinstance(value, bool):
                errors.append(f"Field {field} must be a boolean")
            elif expected_type == 'array' and not isinstance(value, list):
                errors.append(f"Field {field} must be an array")
            elif expected_type == 'object' and not isinstance(value, dict):
                errors.append(f"Field {field} must be an object")
        
        # Length validation for strings
        if isinstance(value, str):
            min_length = rules.get('minLength')
            max_length = rules.get('maxLength')
            
            if min_length and len(value) < min_length:
                errors.append(f"Field {field} must be at least {min_length} characters")
            
            if max_length and len(value) > max_length:
                errors.append(f"Field {field} must be at most {max_length} characters")
        
        # Pattern validation for strings
        pattern = rules.get('pattern')
        if pattern and isinstance(value, str):
            if not re.match(pattern, value):
                errors.append(f"Field {field} does not match required pattern")
        
        # Enum validation
        enum_values = rules.get('enum')
        if enum_values and value not in enum_values:
            errors.append(f"Field {field} must be one of: {enum_values}")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe storage.
    
    Args:
        filename: Original filename
        
    Returns:
        str: Sanitized filename
    """
    if not filename:
        return ""
    
    # Remove or replace dangerous characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove control characters
    filename = re.sub(r'[\x00-\x1f\x7f]', '', filename)
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        max_name_length = 255 - len(ext) - 1 if ext else 255
        filename = name[:max_name_length] + ('.' + ext if ext else '')
    
    return filename or "unnamed_file"


def validate_ip_address(ip: str, ipv6: bool = True) -> bool:
    """
    Validate IP address format.
    
    Args:
        ip: IP address to validate
        ipv6: Whether to allow IPv6 addresses
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not ip:
        return False
    
    # IPv4 validation
    ipv4_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    if re.match(ipv4_pattern, ip):
        return True
    
    # IPv6 validation
    if ipv6:
        ipv6_pattern = r'^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'
        if re.match(ipv6_pattern, ip):
            return True
    
    return False


def validate_credit_card(card_number: str) -> Dict[str, Any]:
    """
    Validate credit card number using Luhn algorithm.
    
    Args:
        card_number: Credit card number
        
    Returns:
        Dict[str, Any]: Validation results
    """
    if not card_number:
        return {
            'valid': False,
            'type': 'unknown',
            'error': 'Empty card number'
        }
    
    # Remove spaces and dashes
    card_number = re.sub(r'[\s-]', '', card_number)
    
    # Check if all characters are digits
    if not card_number.isdigit():
        return {
            'valid': False,
            'type': 'unknown',
            'error': 'Card number must contain only digits'
        }
    
    # Check length
    if len(card_number) < 13 or len(card_number) > 19:
        return {
            'valid': False,
            'type': 'unknown',
            'error': 'Invalid card number length'
        }
    
    # Luhn algorithm
    total = 0
    is_even = False
    
    for digit in reversed(card_number):
        digit = int(digit)
        
        if is_even:
            digit *= 2
            if digit > 9:
                digit -= 9
        
        total += digit
        is_even = not is_even
    
    if total % 10 != 0:
        return {
            'valid': False,
            'type': 'unknown',
            'error': 'Invalid card number'
        }
    
    # Determine card type
    card_type = 'unknown'
    if card_number.startswith('4'):
        card_type = 'visa'
    elif card_number.startswith(('51', '52', '53', '54', '55')):
        card_type = 'mastercard'
    elif card_number.startswith(('34', '37')):
        card_type = 'amex'
    elif card_number.startswith('6'):
        card_type = 'discover'
    
    return {
        'valid': True,
        'type': card_type,
        'masked': '*' * (len(card_number) - 4) + card_number[-4:]
    }
