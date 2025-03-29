from .input_parser import InputParser
from .persuasion_scorer import PersuasionScorer
from .simulation_engine import SimulationEngine
from .sentiment_analyzer import SentimentAnalyzer
from .metrics_formatter import MetricsFormatter

class TextAnalyzer:
    def __init__(self):
        self.parser = InputParser()
        self.scorer = PersuasionScorer()
        self.simulator = SimulationEngine()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.metrics_formatter = MetricsFormatter()

    def analyze_text(self, content):
        """
        Performs comprehensive analysis on the provided text content.
        Returns formatted results suitable for the web interface.
        """
        try:
            # Get base analysis
            base_analysis = self.parser.parse_text(content)
            
            # Get persuasion scores
            persuasion_analysis = self.scorer.analyze_text(content)
            
            # Run simulation
            simulation_results = self.simulator.run_simulation(
                persuasion_analysis['category_scores']
            )
            
            # Analyze sentiment and tone
            sentiment_data = self.sentiment_analyzer.analyze_sentiment_and_tone(content)
            alignment_data = self.sentiment_analyzer.assess_persuasion_alignment(
                sentiment_data,
                persuasion_analysis['category_scores']
            )
            
            # Combine all analysis results
            full_analysis = {
                **base_analysis,
                'persuasion': persuasion_analysis,
                'simulation': simulation_results,
                'sentiment': sentiment_data,
                'tone_alignment': alignment_data
            }
            
            # Format for web display
            return {
                'overall_score': simulation_results['overall_effectiveness'],
                'best_performing_persona': simulation_results['best_persona'],
                'key_insights': [
                    f"Overall persuasion effectiveness: {simulation_results['overall_effectiveness']*100:.1f}%",
                    f"Best performing persona: {simulation_results['best_persona']}",
                    f"Dominant tone: {sentiment_data['dominant_tone']}",
                    f"Sentiment alignment: {alignment_data['overall_alignment']*100:.1f}% match with intent"
                ],
                'detailed_scores': {
                    'Logical Appeal': persuasion_analysis['category_scores']['logical'],
                    'Emotional Appeal': persuasion_analysis['category_scores']['emotional'],
                    'Credibility': persuasion_analysis['category_scores']['credibility'],
                    'Clarity': base_analysis['clarity_score'],
                    'Tone Alignment': alignment_data['overall_alignment']
                },
                'persona_responses': simulation_results['persona_responses']
            }
            
        except Exception as e:
            raise Exception(f"Analysis failed: {str(e)}") 