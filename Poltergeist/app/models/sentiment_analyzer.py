import nltk
from typing import Dict, Any
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from collections import Counter

class SentimentAnalyzer:
    def __init__(self):
        # Download required NLTK data
        nltk.download('vader_lexicon')
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        
        self.sia = SentimentIntensityAnalyzer()
        
        # Define tone indicators
        self.tone_indicators = {
            'professional': set(['therefore', 'consequently', 'furthermore', 'moreover', 'thus', 'hence']),
            'friendly': set(['hey', 'hi', 'thanks', 'please', 'appreciate', 'welcome', 'glad']),
            'authoritative': set(['must', 'need', 'require', 'essential', 'crucial', 'critical', 'important']),
            'empathetic': set(['understand', 'feel', 'know', 'relate', 'imagine', 'realize']),
            'urgent': set(['now', 'immediately', 'quickly', 'urgent', 'limited', 'hurry', 'soon']),
            'confident': set(['guarantee', 'proven', 'certainly', 'definitely', 'absolutely', 'undoubtedly'])
        }

    def analyze_sentiment_and_tone(self, text: str) -> Dict[str, Any]:
        """Perform comprehensive sentiment and tone analysis."""
        # Basic sentiment analysis
        sentiment_scores = self.sia.polarity_scores(text)
        
        # Determine primary sentiment
        if sentiment_scores['compound'] >= 0.05:
            primary_sentiment = 'positive'
        elif sentiment_scores['compound'] <= -0.05:
            primary_sentiment = 'negative'
        else:
            primary_sentiment = 'neutral'
            
        # Analyze tone presence
        words = word_tokenize(text.lower())
        tone_presence = {}
        
        for tone, indicators in self.tone_indicators.items():
            matches = sum(1 for word in words if word in indicators)
            tone_presence[tone] = round(matches / len(words) * 10, 2)  # Scale to 0-10
            
        # Determine dominant tone
        dominant_tone = max(tone_presence.items(), key=lambda x: x[1])[0]
        
        # Analyze sentence structure for additional tone indicators
        sentences = nltk.sent_tokenize(text)
        avg_sentence_length = sum(len(word_tokenize(s)) for s in sentences) / len(sentences)
        
        # Tag parts of speech for deeper analysis
        pos_tags = nltk.pos_tag(words)
        pos_counts = Counter(tag for word, tag in pos_tags)
        
        # Calculate formality score (higher ratio of nouns and prepositions to pronouns and adverbs)
        formality_indicators = pos_counts.get('NN', 0) + pos_counts.get('NNP', 0) + pos_counts.get('IN', 0)
        informality_indicators = pos_counts.get('PRP', 0) + pos_counts.get('RB', 0)
        formality_score = round(formality_indicators / (informality_indicators + 1) * 5, 2)  # Scale to 0-10
        
        return {
            "sentiment": {
                "primary": primary_sentiment,
                "scores": {
                    "positive": round(sentiment_scores['pos'] * 10, 2),
                    "neutral": round(sentiment_scores['neu'] * 10, 2),
                    "negative": round(sentiment_scores['neg'] * 10, 2),
                    "compound": round(sentiment_scores['compound'] * 10, 2)
                }
            },
            "tone_analysis": {
                "dominant_tone": dominant_tone,
                "tone_scores": tone_presence,
                "formality_level": formality_score
            },
            "structure": {
                "avg_sentence_length": round(avg_sentence_length, 2),
                "sentence_count": len(sentences)
            }
        }
        
    def assess_persuasion_alignment(self, sentiment_data: Dict[str, Any], persuasion_scores: Dict[str, float]) -> Dict[str, Any]:
        """Assess how well sentiment and tone align with persuasion goals."""
        alignment_scores = {}
        
        # Check if tone matches persuasion strategy
        tone_scores = sentiment_data['tone_analysis']['tone_scores']
        
        # Clarity alignment
        alignment_scores['clarity'] = {
            'score': round((tone_scores['professional'] + tone_scores['confident']) / 2, 2),
            'suggestion': "Tone is professional and clear" if tone_scores['professional'] > 5 
                        else "Consider using more professional language for clarity"
        }
        
        # Urgency alignment
        alignment_scores['urgency'] = {
            'score': tone_scores['urgent'],
            'suggestion': "Urgency is well-conveyed" if tone_scores['urgent'] > 5
                        else "Consider strengthening urgency in tone"
        }
        
        # Social proof alignment
        alignment_scores['social_proof'] = {
            'score': round((tone_scores['authoritative'] + tone_scores['confident']) / 2, 2),
            'suggestion': "Authority is well-established" if tone_scores['authoritative'] > 5
                        else "Consider adding more authoritative tone elements"
        }
        
        # CTA alignment
        cta_tone_score = (tone_scores['confident'] + tone_scores['urgent']) / 2
        alignment_scores['cta'] = {
            'score': round(cta_tone_score, 2),
            'suggestion': "CTA tone is strong" if cta_tone_score > 5
                        else "Consider strengthening call-to-action tone"
        }
        
        # Overall resonance score
        resonance_score = sum(
            abs(alignment_scores[key]['score'] - persuasion_scores[key])
            for key in ['clarity', 'urgency']
        ) / 2
        
        return {
            "alignment_scores": alignment_scores,
            "resonance_score": round(10 - resonance_score, 2),  # Convert to 0-10 scale where 10 is perfect alignment
            "overall_assessment": "Strong tone-persuasion alignment" if resonance_score < 3
                                else "Moderate tone-persuasion alignment" if resonance_score < 5
                                else "Weak tone-persuasion alignment"
        } 