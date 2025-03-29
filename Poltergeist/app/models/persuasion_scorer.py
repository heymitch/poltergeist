import re
from typing import Dict, Any, List
import nltk
from statistics import mean

class PersuasionScorer:
    def __init__(self):
        self.clarity_indicators = {
            'simple_words': r'\b\w{1,6}\b',  # Short words are clearer
            'complex_words': r'\b\w{13,}\b',  # Very long words reduce clarity
            'transition_words': r'\b(therefore|because|however|moreover|furthermore|consequently)\b',
            'bullet_points': r'[•\-\*]',
        }
        
        self.urgency_indicators = {
            'time_limited': r'\b(limited time|ends soon|last chance|closing soon|deadline|expires|today only)\b',
            'scarcity': r'\b(only|exclusive|limited|rare|few remaining|while supplies last)\b',
            'immediate': r'\b(now|instantly|immediately|today|tonight|asap)\b',
        }
        
        self.social_proof_indicators = {
            'testimonial': r'["\'](.*?)[\"\']',  # Quoted text often indicates testimonials
            'numbers': r'\b\d+(\+|\s*k)?\s*(customers|clients|people|users)\b',
            'social_validation': r'\b(trusted|proven|recommended|popular|leading|top-rated)\b',
            'endorsements': r'\b(verified|certified|endorsed|approved|backed by)\b',
        }
        
        self.cta_patterns = {
            'action_verbs': r'\b(get|buy|shop|order|download|subscribe|sign up|register|learn more|discover)\b',
            'imperative': r'\b(start|begin|try|see|find|check out|click|tap|swipe)\b',
            'value_props': r'\b(free|bonus|extra|save|discount|special)\b',
            'urgency_cta': r'\b(now|today|instantly|immediately)\b',
        }

    def score_clarity(self, text: str) -> float:
        """Score text clarity on a scale of 1-10."""
        text_lower = text.lower()
        
        # Analyze sentence structure
        sentences = nltk.sent_tokenize(text)
        avg_sentence_length = mean([len(s.split()) for s in sentences])
        sentence_length_score = max(0, 10 - (abs(15 - avg_sentence_length) / 2))
        
        # Count clarity indicators
        simple_words = len(re.findall(self.clarity_indicators['simple_words'], text_lower))
        complex_words = len(re.findall(self.clarity_indicators['complex_words'], text_lower))
        transitions = len(re.findall(self.clarity_indicators['transition_words'], text_lower))
        bullets = len(re.findall(self.clarity_indicators['bullet_points'], text))
        
        # Calculate composite score
        word_ratio_score = min(10, (simple_words - complex_words * 2) / max(len(text.split()), 1) * 10)
        structure_score = min(10, (transitions + bullets * 2) / max(len(sentences), 1) * 10)
        
        return round(mean([sentence_length_score, word_ratio_score, structure_score]), 2)

    def score_urgency(self, text: str) -> float:
        """Score urgency on a scale of 1-10."""
        text_lower = text.lower()
        
        scores = []
        total_words = len(text_lower.split())
        
        for pattern_type, pattern in self.urgency_indicators.items():
            matches = len(re.findall(pattern, text_lower))
            if pattern_type == 'time_limited':
                scores.append(min(10, matches * 3))
            elif pattern_type == 'scarcity':
                scores.append(min(10, matches * 2.5))
            elif pattern_type == 'immediate':
                scores.append(min(10, matches * 2))
        
        # Penalize overuse
        if sum(scores) / len(scores) > 8:
            scores.append(7)  # Add a lower score to balance extreme urgency
            
        return round(mean(scores), 2)

    def score_social_proof(self, text: str) -> float:
        """Score social proof on a scale of 1-10."""
        text_lower = text.lower()
        
        scores = []
        
        # Weight different types of social proof
        testimonials = len(re.findall(self.social_proof_indicators['testimonial'], text))
        numbers = len(re.findall(self.social_proof_indicators['numbers'], text_lower))
        validation = len(re.findall(self.social_proof_indicators['social_validation'], text_lower))
        endorsements = len(re.findall(self.social_proof_indicators['endorsements'], text_lower))
        
        scores.append(min(10, testimonials * 3))  # Testimonials are strong
        scores.append(min(10, numbers * 4))       # Specific numbers are very strong
        scores.append(min(10, validation * 2))    # General validation terms
        scores.append(min(10, endorsements * 2.5)) # Endorsements are good
        
        return round(mean(scores), 2)

    def score_cta_strength(self, text: str) -> float:
        """Score call-to-action strength on a scale of 1-10."""
        text_lower = text.lower()
        
        scores = []
        
        for pattern_type, pattern in self.cta_patterns.items():
            matches = len(re.findall(pattern, text_lower))
            if pattern_type == 'action_verbs':
                scores.append(min(10, matches * 2.5))
            elif pattern_type == 'imperative':
                scores.append(min(10, matches * 2))
            elif pattern_type == 'value_props':
                scores.append(min(10, matches * 1.5))
            elif pattern_type == 'urgency_cta':
                scores.append(min(10, matches * 2))
        
        # Ensure at least one strong CTA exists
        if max(scores) < 5:
            scores.append(3)  # Penalize weak CTAs
            
        return round(mean(scores), 2)

    def calculate_influence_score(self, scores: Dict[str, float]) -> float:
        """Calculate composite influence score from individual metrics."""
        weights = {
            'clarity': 0.3,
            'urgency': 0.2,
            'social_proof': 0.25,
            'cta_strength': 0.25
        }
        
        weighted_score = sum(scores[metric] * weight for metric, weight in weights.items())
        return round(weighted_score, 2)

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze text and return comprehensive persuasion scores."""
        scores = {
            'clarity': self.score_clarity(text),
            'urgency': self.score_urgency(text),
            'social_proof': self.score_social_proof(text),
            'cta_strength': self.score_cta_strength(text)
        }
        
        influence_score = self.calculate_influence_score(scores)
        
        return {
            'category_scores': scores,
            'influence_score': influence_score
        } 