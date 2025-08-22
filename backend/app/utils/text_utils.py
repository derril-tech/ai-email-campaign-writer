"""
Text utility functions for content processing and analysis.
"""

import re
import string
from typing import List, Dict, Optional
from collections import Counter
import math


def clean_text(text: str) -> str:
    """
    Clean and normalize text content.
    
    Args:
        text: Raw text content
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?;:()\'"-]', '', text)
    
    # Normalize quotes and dashes
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace(''', "'").replace(''', "'")
    text = text.replace('–', '-').replace('—', '-')
    
    return text


def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """
    Extract keywords from text using frequency analysis.
    
    Args:
        text: Text content
        max_keywords: Maximum number of keywords to return
        
    Returns:
        List[str]: List of keywords
    """
    if not text:
        return []
    
    # Clean text
    text = clean_text(text.lower())
    
    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those',
        'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
        'my', 'your', 'his', 'her', 'its', 'our', 'their', 'mine', 'yours', 'hers',
        'ours', 'theirs', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being'
    }
    
    # Split into words and filter
    words = re.findall(r'\b\w+\b', text)
    words = [word for word in words if word not in stop_words and len(word) > 2]
    
    # Count frequency
    word_counts = Counter(words)
    
    # Return most common keywords
    return [word for word, count in word_counts.most_common(max_keywords)]


def calculate_readability_score(text: str) -> Dict[str, float]:
    """
    Calculate various readability scores for text.
    
    Args:
        text: Text content
        
    Returns:
        Dict[str, float]: Dictionary with readability scores
    """
    if not text:
        return {}
    
    # Clean text
    text = clean_text(text)
    
    # Count basic metrics
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    words = re.findall(r'\b\w+\b', text.lower())
    syllables = count_syllables(text)
    
    num_sentences = len(sentences)
    num_words = len(words)
    num_syllables = syllables
    
    if num_sentences == 0 or num_words == 0:
        return {}
    
    # Calculate scores
    avg_sentence_length = num_words / num_sentences
    avg_syllables_per_word = num_syllables / num_words
    
    # Flesch Reading Ease
    flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
    flesch_score = max(0, min(100, flesch_score))
    
    # Flesch-Kincaid Grade Level
    fk_grade = (0.39 * avg_sentence_length) + (11.8 * avg_syllables_per_word) - 15.59
    fk_grade = max(0, fk_grade)
    
    # Gunning Fog Index
    complex_words = count_complex_words(text)
    fog_index = 0.4 * ((num_words / num_sentences) + 100 * (complex_words / num_words))
    
    return {
        'flesch_reading_ease': round(flesch_score, 2),
        'flesch_kincaid_grade': round(fk_grade, 1),
        'gunning_fog_index': round(fog_index, 1),
        'avg_sentence_length': round(avg_sentence_length, 1),
        'avg_syllables_per_word': round(avg_syllables_per_word, 2),
        'complex_words_percentage': round((complex_words / num_words) * 100, 1)
    }


def count_syllables(text: str) -> int:
    """
    Count syllables in text.
    
    Args:
        text: Text content
        
    Returns:
        int: Number of syllables
    """
    text = text.lower()
    count = 0
    vowels = "aeiouy"
    on_vowel = False
    
    for char in text:
        is_vowel = char in vowels
        if is_vowel and not on_vowel:
            count += 1
        on_vowel = is_vowel
    
    # Adjust for words ending with 'e'
    if text.endswith('e'):
        count -= 1
    
    # Ensure at least one syllable per word
    return max(1, count)


def count_complex_words(text: str) -> int:
    """
    Count complex words (3+ syllables) in text.
    
    Args:
        text: Text content
        
    Returns:
        int: Number of complex words
    """
    words = re.findall(r'\b\w+\b', text.lower())
    complex_count = 0
    
    for word in words:
        if count_syllables(word) >= 3:
            complex_count += 1
    
    return complex_count


def generate_summary(text: str, max_length: int = 150) -> str:
    """
    Generate a summary of text content.
    
    Args:
        text: Text content
        max_length: Maximum length of summary
        
    Returns:
        str: Generated summary
    """
    if not text:
        return ""
    
    # Clean text
    text = clean_text(text)
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return ""
    
    # If text is already short enough, return as is
    if len(text) <= max_length:
        return text
    
    # Simple approach: take first few sentences
    summary = ""
    for sentence in sentences:
        if len(summary + sentence) <= max_length:
            summary += sentence + ". "
        else:
            break
    
    return summary.strip()


def extract_sentiment_words(text: str) -> Dict[str, List[str]]:
    """
    Extract positive and negative sentiment words from text.
    
    Args:
        text: Text content
        
    Returns:
        Dict[str, List[str]]: Dictionary with positive and negative words
    """
    # Simple sentiment word lists (in production, use more sophisticated NLP)
    positive_words = {
        'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
        'awesome', 'brilliant', 'outstanding', 'perfect', 'best', 'love',
        'like', 'enjoy', 'happy', 'pleased', 'satisfied', 'impressed'
    }
    
    negative_words = {
        'bad', 'terrible', 'awful', 'horrible', 'worst', 'disappointing',
        'poor', 'unhappy', 'angry', 'frustrated', 'annoyed', 'upset',
        'hate', 'dislike', 'terrible', 'awful', 'horrible'
    }
    
    words = re.findall(r'\b\w+\b', text.lower())
    
    positive_found = [word for word in words if word in positive_words]
    negative_found = [word for word in words if word in negative_words]
    
    return {
        'positive': list(set(positive_found)),
        'negative': list(set(negative_found))
    }


def calculate_text_statistics(text: str) -> Dict[str, any]:
    """
    Calculate comprehensive text statistics.
    
    Args:
        text: Text content
        
    Returns:
        Dict[str, any]: Dictionary with text statistics
    """
    if not text:
        return {}
    
    # Clean text
    text = clean_text(text)
    
    # Basic counts
    characters = len(text)
    characters_no_spaces = len(text.replace(' ', ''))
    words = len(re.findall(r'\b\w+\b', text))
    sentences = len(re.split(r'[.!?]+', text))
    paragraphs = len([p for p in text.split('\n\n') if p.strip()])
    
    # Word frequency
    word_counts = Counter(re.findall(r'\b\w+\b', text.lower()))
    unique_words = len(word_counts)
    
    # Average word length
    avg_word_length = sum(len(word) for word in re.findall(r'\b\w+\b', text)) / words if words > 0 else 0
    
    # Readability scores
    readability = calculate_readability_score(text)
    
    # Sentiment analysis
    sentiment = extract_sentiment_words(text)
    
    return {
        'characters': characters,
        'characters_no_spaces': characters_no_spaces,
        'words': words,
        'sentences': sentences,
        'paragraphs': paragraphs,
        'unique_words': unique_words,
        'avg_word_length': round(avg_word_length, 2),
        'readability': readability,
        'sentiment': sentiment,
        'estimated_reading_time': round(words / 200, 1)  # Average reading speed
    }


def normalize_text(text: str) -> str:
    """
    Normalize text for consistent processing.
    
    Args:
        text: Text content
        
    Returns:
        str: Normalized text
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove punctuation (optional, depending on use case)
    # text = text.translate(str.maketrans('', '', string.punctuation))
    
    return text.strip()


def extract_hashtags(text: str) -> List[str]:
    """
    Extract hashtags from text.
    
    Args:
        text: Text content
        
    Returns:
        List[str]: List of hashtags
    """
    hashtags = re.findall(r'#\w+', text)
    return [tag.lower() for tag in hashtags]


def extract_mentions(text: str) -> List[str]:
    """
    Extract mentions (@username) from text.
    
    Args:
        text: Text content
        
    Returns:
        List[str]: List of mentions
    """
    mentions = re.findall(r'@\w+', text)
    return [mention.lower() for mention in mentions]


def extract_urls(text: str) -> List[str]:
    """
    Extract URLs from text.
    
    Args:
        text: Text content
        
    Returns:
        List[str]: List of URLs
    """
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_pattern, text)
    return urls
