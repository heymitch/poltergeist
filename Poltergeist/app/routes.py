from flask import Flask, request, jsonify, render_template, session
from .models.input_parser import InputParser
from .models.persuasion_scorer import PersuasionScorer
from .models.simulation_engine import SimulationEngine
from .models.sentiment_analyzer import SentimentAnalyzer
from .models.metrics_formatter import MetricsFormatter
from .models.feedback_processor import FeedbackProcessor
from .models.analyzer import TextAnalyzer
from .auth import auth, login_required

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key in production
app.register_blueprint(auth, url_prefix='/auth')

analyzer = TextAnalyzer()
feedback_processor = FeedbackProcessor()

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/feedback')
@login_required
def feedback_page():
    return render_template('feedback.html')

@app.route('/analyze', methods=['POST'])
@login_required
def analyze():
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({'error': 'No content provided'}), 400

    content = data['content']
    try:
        analysis_results = analyzer.analyze_text(content)
        return jsonify(analysis_results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/feedback', methods=['POST'])
@login_required
def submit_feedback():
    data = request.get_json()
    required_fields = ['content', 'engagement_rate', 'conversion_rate', 'target_persona', 'campaign_type']
    
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        feedback_processor.process_feedback(
            content=data['content'],
            engagement_rate=float(data['engagement_rate']) / 100,  # Convert from percentage
            conversion_rate=float(data['conversion_rate']) / 100,  # Convert from percentage
            target_persona=data['target_persona'],
            campaign_type=data['campaign_type'],
            notes=data.get('notes', '')
        )
        return jsonify({'message': 'Feedback processed successfully'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 