import re
import nltk
from urllib.parse import urlparse
from typing import Dict, Any

# Download required NLTK data
nltk.download('punkt')
nltk.download('vader_lexicon')

class InputParser:
    @staticmethod
    def parse_text(text: str) -> Dict[Any, Any]:
        """Parse input text and extract key metadata."""
        # Basic text metrics
        word_count = len(text.split())
        sentences = nltk.sent_tokenize(text)
        sentence_count = len(sentences)
        
        # Tone analysis using NLTK's VADER
        sia = nltk.sentiment.SentimentIntensityAnalyzer()
        sentiment_scores = sia.polarity_scores(text)
        estimated_tone = "neutral"
        if sentiment_scores['compound'] >= 0.05:
            estimated_tone = "positive"
        elif sentiment_scores['compound'] <= -0.05:
            estimated_tone = "negative"
        
        # Keyword and hashtag frequency
        words = text.lower().split()
        hashtags = [word for word in words if word.startswith('#')]
        hashtag_frequency = len(hashtags)
        
        # CTA and link detection
        cta_patterns = [
            r'\b(buy|shop|get|order|download|subscribe|sign up|register|learn more|click|tap|swipe)\b',
            r'\b(limited time|act now|today only|exclusive offer)\b',
            r'!(^|\s)(DM|PM|contact)(\s|$)'
        ]
        
        cta_count = sum(len(re.findall(pattern, text.lower())) for pattern in cta_patterns)
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        
        return {
            "metadata": {
                "word_count": word_count,
                "sentence_count": sentence_count,
                "avg_sentence_length": word_count / sentence_count if sentence_count > 0 else 0
            },
            "tone": {
                "estimated_tone": estimated_tone,
                "sentiment_scores": sentiment_scores
            },
            "engagement": {
                "hashtag_count": hashtag_frequency,
                "hashtags": hashtags,
                "cta_count": cta_count,
                "link_count": len(urls)
            }
        } 