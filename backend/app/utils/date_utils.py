"""
Date and time utility functions.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Union
import pytz


def format_date(
    date: Union[datetime, str],
    format_str: str = "%Y-%m-%d %H:%M:%S",
    timezone_name: Optional[str] = None
) -> str:
    """
    Format a date/datetime object or string.
    
    Args:
        date: Date/datetime object or string
        format_str: Format string for output
        timezone_name: Timezone name (e.g., 'UTC', 'America/New_York')
        
    Returns:
        str: Formatted date string
    """
    if isinstance(date, str):
        date = parse_date(date)
    
    if not date:
        return ""
    
    if timezone_name:
        tz = pytz.timezone(timezone_name)
        if date.tzinfo is None:
            date = pytz.utc.localize(date)
        date = date.astimezone(tz)
    
    return date.strftime(format_str)


def parse_date(
    date_string: str,
    format_str: Optional[str] = None
) -> Optional[datetime]:
    """
    Parse a date string into a datetime object.
    
    Args:
        date_string: Date string to parse
        format_str: Format string (if None, will try common formats)
        
    Returns:
        Optional[datetime]: Parsed datetime object or None if failed
    """
    if not date_string:
        return None
    
    # Common date formats to try
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y %H:%M",
        "%m/%d/%Y",
        "%B %d, %Y %H:%M:%S",
        "%B %d, %Y %H:%M",
        "%B %d, %Y",
        "%d %B %Y %H:%M:%S",
        "%d %B %Y %H:%M",
        "%d %B %Y",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%fZ"
    ]
    
    if format_str:
        formats.insert(0, format_str)
    
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    
    return None


def get_relative_time(
    date: Union[datetime, str],
    reference_date: Optional[Union[datetime, str]] = None
) -> str:
    """
    Get relative time description (e.g., "2 hours ago", "in 3 days").
    
    Args:
        date: Date to get relative time for
        reference_date: Reference date (defaults to current time)
        
    Returns:
        str: Relative time description
    """
    if isinstance(date, str):
        date = parse_date(date)
    
    if isinstance(reference_date, str):
        reference_date = parse_date(reference_date)
    
    if not date:
        return "Unknown"
    
    if not reference_date:
        reference_date = datetime.now()
    
    # Ensure both dates are timezone-aware
    if date.tzinfo is None:
        date = pytz.utc.localize(date)
    if reference_date.tzinfo is None:
        reference_date = pytz.utc.localize(reference_date)
    
    delta = reference_date - date
    
    # Handle future dates
    if delta.total_seconds() < 0:
        delta = abs(delta)
        future = True
    else:
        future = False
    
    seconds = delta.total_seconds()
    
    if seconds < 60:
        unit = "second"
        value = int(seconds)
    elif seconds < 3600:
        unit = "minute"
        value = int(seconds // 60)
    elif seconds < 86400:
        unit = "hour"
        value = int(seconds // 3600)
    elif seconds < 2592000:  # 30 days
        unit = "day"
        value = int(seconds // 86400)
    elif seconds < 31536000:  # 365 days
        unit = "month"
        value = int(seconds // 2592000)
    else:
        unit = "year"
        value = int(seconds // 31536000)
    
    # Pluralize
    if value != 1:
        unit += "s"
    
    if future:
        return f"in {value} {unit}"
    else:
        return f"{value} {unit} ago"


def is_business_day(
    date: Union[datetime, str],
    timezone_name: str = "UTC"
) -> bool:
    """
    Check if a date is a business day (Monday-Friday).
    
    Args:
        date: Date to check
        timezone_name: Timezone name
        
    Returns:
        bool: True if business day, False otherwise
    """
    if isinstance(date, str):
        date = parse_date(date)
    
    if not date:
        return False
    
    # Convert to specified timezone
    tz = pytz.timezone(timezone_name)
    if date.tzinfo is None:
        date = pytz.utc.localize(date)
    date = date.astimezone(tz)
    
    # Monday = 0, Sunday = 6
    return date.weekday() < 5


def add_business_days(
    date: Union[datetime, str],
    days: int,
    timezone_name: str = "UTC"
) -> datetime:
    """
    Add business days to a date.
    
    Args:
        date: Starting date
        days: Number of business days to add
        timezone_name: Timezone name
        
    Returns:
        datetime: Date with business days added
    """
    if isinstance(date, str):
        date = parse_date(date)
    
    if not date:
        raise ValueError("Invalid date")
    
    # Convert to specified timezone
    tz = pytz.timezone(timezone_name)
    if date.tzinfo is None:
        date = pytz.utc.localize(date)
    date = date.astimezone(tz)
    
    current_date = date
    business_days_added = 0
    
    while business_days_added < days:
        current_date += timedelta(days=1)
        if is_business_day(current_date, timezone_name):
            business_days_added += 1
    
    return current_date


def get_date_range(
    start_date: Union[datetime, str],
    end_date: Union[datetime, str],
    include_weekends: bool = True
) -> list:
    """
    Get a list of dates between start and end date.
    
    Args:
        start_date: Start date
        end_date: End date
        include_weekends: Whether to include weekends
        
    Returns:
        list: List of datetime objects
    """
    if isinstance(start_date, str):
        start_date = parse_date(start_date)
    if isinstance(end_date, str):
        end_date = parse_date(end_date)
    
    if not start_date or not end_date:
        return []
    
    dates = []
    current_date = start_date
    
    while current_date <= end_date:
        if include_weekends or is_business_day(current_date):
            dates.append(current_date)
        current_date += timedelta(days=1)
    
    return dates


def get_quarter_dates(year: int, quarter: int) -> tuple:
    """
    Get start and end dates for a quarter.
    
    Args:
        year: Year
        quarter: Quarter (1-4)
        
    Returns:
        tuple: (start_date, end_date)
    """
    if quarter not in [1, 2, 3, 4]:
        raise ValueError("Quarter must be 1, 2, 3, or 4")
    
    month = (quarter - 1) * 3 + 1
    start_date = datetime(year, month, 1)
    
    if quarter == 4:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, month + 3, 1) - timedelta(days=1)
    
    return start_date, end_date


def get_month_dates(year: int, month: int) -> tuple:
    """
    Get start and end dates for a month.
    
    Args:
        year: Year
        month: Month (1-12)
        
    Returns:
        tuple: (start_date, end_date)
    """
    if month not in range(1, 13):
        raise ValueError("Month must be 1-12")
    
    start_date = datetime(year, month, 1)
    
    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(days=1)
    
    return start_date, end_date


def get_week_dates(
    date: Union[datetime, str],
    start_of_week: int = 0
) -> tuple:
    """
    Get start and end dates for the week containing the given date.
    
    Args:
        date: Date within the week
        start_of_week: Day of week to start (0=Monday, 6=Sunday)
        
    Returns:
        tuple: (start_date, end_date)
    """
    if isinstance(date, str):
        date = parse_date(date)
    
    if not date:
        raise ValueError("Invalid date")
    
    # Calculate days to subtract to get to start of week
    days_to_subtract = (date.weekday() - start_of_week) % 7
    start_date = date - timedelta(days=days_to_subtract)
    end_date = start_date + timedelta(days=6)
    
    return start_date, end_date


def is_same_day(
    date1: Union[datetime, str],
    date2: Union[datetime, str]
) -> bool:
    """
    Check if two dates are on the same day.
    
    Args:
        date1: First date
        date2: Second date
        
    Returns:
        bool: True if same day, False otherwise
    """
    if isinstance(date1, str):
        date1 = parse_date(date1)
    if isinstance(date2, str):
        date2 = parse_date(date2)
    
    if not date1 or not date2:
        return False
    
    return date1.date() == date2.date()


def get_age(
    birth_date: Union[datetime, str],
    reference_date: Optional[Union[datetime, str]] = None
) -> int:
    """
    Calculate age from birth date.
    
    Args:
        birth_date: Birth date
        reference_date: Reference date (defaults to current date)
        
    Returns:
        int: Age in years
    """
    if isinstance(birth_date, str):
        birth_date = parse_date(birth_date)
    if isinstance(reference_date, str):
        reference_date = parse_date(reference_date)
    
    if not birth_date:
        raise ValueError("Invalid birth date")
    
    if not reference_date:
        reference_date = datetime.now()
    
    age = reference_date.year - birth_date.year
    
    # Adjust if birthday hasn't occurred yet this year
    if (reference_date.month, reference_date.day) < (birth_date.month, birth_date.day):
        age -= 1
    
    return age


def format_duration(
    seconds: Union[int, float],
    include_seconds: bool = True
) -> str:
    """
    Format duration in seconds to human-readable string.
    
    Args:
        seconds: Duration in seconds
        include_seconds: Whether to include seconds in output
        
    Returns:
        str: Formatted duration string
    """
    if seconds < 60:
        return f"{int(seconds)}s"
    
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    
    if minutes < 60:
        if include_seconds and remaining_seconds > 0:
            return f"{minutes}m {remaining_seconds}s"
        else:
            return f"{minutes}m"
    
    hours = int(minutes // 60)
    remaining_minutes = int(minutes % 60)
    
    if hours < 24:
        if include_seconds and remaining_seconds > 0:
            return f"{hours}h {remaining_minutes}m {remaining_seconds}s"
        elif remaining_minutes > 0:
            return f"{hours}h {remaining_minutes}m"
        else:
            return f"{hours}h"
    
    days = int(hours // 24)
    remaining_hours = int(hours % 24)
    
    if include_seconds and remaining_seconds > 0:
        return f"{days}d {remaining_hours}h {remaining_minutes}m {remaining_seconds}s"
    elif remaining_minutes > 0:
        return f"{days}d {remaining_hours}h {remaining_minutes}m"
    elif remaining_hours > 0:
        return f"{days}d {remaining_hours}h"
    else:
        return f"{days}d"
