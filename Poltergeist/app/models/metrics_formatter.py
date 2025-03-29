from typing import Dict, Any, List
from datetime import datetime

class MetricsFormatter:
    @staticmethod
    def format_metrics(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format and structure all analysis metrics into a clean, focused output."""
        
        # Extract core metrics
        influence_metrics = {
            "overall_influence_score": analysis_data['persuasion']['influence_score'],
            "persuasion_category_scores": analysis_data['persuasion']['category_scores'],
        }
        
        # Format simulation results
        simulation_metrics = {
            "most_receptive_persona": analysis_data['simulation']['most_receptive_persona'],
            "persona_breakdown": {}
        }
        
        for persona_key, data in analysis_data['simulation']['persona_responses'].items():
            simulation_metrics["persona_breakdown"][persona_key] = {
                "name": data["name"],
                "response_likelihood": data["response_likelihood"],
                "weighted_score": data["weighted_score"]
            }
            
        # Format sentiment and tone metrics
        sentiment_metrics = {
            "primary_sentiment": analysis_data['sentiment']['sentiment']['primary'],
            "sentiment_scores": analysis_data['sentiment']['sentiment']['scores'],
            "dominant_tone": analysis_data['sentiment']['tone_analysis']['dominant_tone'],
            "formality_level": analysis_data['sentiment']['tone_analysis']['formality_level']
        }
        
        # Format alignment insights
        alignment_metrics = {
            "resonance_score": analysis_data['tone_alignment']['resonance_score'],
            "overall_assessment": analysis_data['tone_alignment']['overall_assessment'],
            "category_alignment": analysis_data['tone_alignment']['alignment_scores']
        }
        
        # Compile key insights
        key_insights = []
        
        # Add persuasion insights
        for category, score in influence_metrics['persuasion_category_scores'].items():
            if score >= 8:
                key_insights.append(f"Strong {category} score at {score}")
            elif score <= 4:
                key_insights.append(f"Consider improving {category}, currently at {score}")
                
        # Add persona insights
        best_persona = max(
            simulation_metrics['persona_breakdown'].items(),
            key=lambda x: x[1]['response_likelihood']
        )
        key_insights.append(
            f"Content resonates best with {best_persona[1]['name']} persona "
            f"({best_persona[1]['response_likelihood']}% response likelihood)"
        )
        
        # Add tone alignment insights
        if alignment_metrics['resonance_score'] >= 7:
            key_insights.append("Strong tone-persuasion alignment")
        elif alignment_metrics['resonance_score'] <= 4:
            key_insights.append("Significant tone-persuasion misalignment detected")
            
        # Add sentiment insights
        if sentiment_metrics['primary_sentiment'] != 'neutral':
            key_insights.append(
                f"Strong {sentiment_metrics['primary_sentiment']} sentiment detected"
            )
            
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "influence_metrics": influence_metrics,
            "simulation_metrics": simulation_metrics,
            "sentiment_metrics": sentiment_metrics,
            "alignment_metrics": alignment_metrics,
            "key_insights": key_insights,
            "metadata": {
                "word_count": analysis_data['metadata']['word_count'],
                "sentence_count": analysis_data['metadata']['sentence_count'],
                "avg_sentence_length": analysis_data['metadata']['avg_sentence_length']
            }
        } 