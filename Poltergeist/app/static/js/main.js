// Utility functions
const showElement = (elementId) => {
    document.getElementById(elementId).classList.remove('hidden');
};

const hideElement = (elementId) => {
    document.getElementById(elementId).classList.add('hidden');
};

const displayError = (message) => {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    showElement('errorMessage');
    setTimeout(() => hideElement('errorMessage'), 5000);
};

// Analysis form handling
document.addEventListener('DOMContentLoaded', () => {
    const analysisForm = document.getElementById('analysisForm');
    if (analysisForm) {
        analysisForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const content = document.getElementById('content').value.trim();
            if (!content) {
                displayError('Please enter some content to analyze');
                return;
            }

            // Show loading state
            hideElement('results');
            showElement('loading');

            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ content }),
                });

                if (!response.ok) {
                    throw new Error('Analysis request failed');
                }

                const data = await response.json();
                
                // Update results
                document.getElementById('overallScore').textContent = 
                    `${(data.overall_score * 100).toFixed(1)}%`;
                document.getElementById('bestPersona').textContent = 
                    data.best_performing_persona;

                // Update key insights
                const insightsList = document.getElementById('keyInsights');
                insightsList.innerHTML = data.key_insights
                    .map(insight => `<li>${insight}</li>`)
                    .join('');

                // Update detailed scores
                const detailedScores = document.getElementById('detailedScores');
                detailedScores.innerHTML = Object.entries(data.detailed_scores)
                    .map(([metric, score]) => `
                        <div class="p-4 bg-gray-50 rounded-md">
                            <h3 class="font-medium text-gray-900">${metric}</h3>
                            <p class="text-xl font-bold text-blue-600">${(score * 100).toFixed(1)}%</p>
                        </div>
                    `).join('');

                // Update persona breakdown
                const personaBreakdown = document.getElementById('personaBreakdown');
                personaBreakdown.innerHTML = Object.entries(data.persona_responses)
                    .map(([persona, likelihood]) => `
                        <div class="flex items-center">
                            <span class="w-32 text-gray-700">${persona}</span>
                            <div class="flex-1 h-4 bg-gray-200 rounded-full overflow-hidden">
                                <div class="h-full bg-blue-600" style="width: ${likelihood * 100}%"></div>
                            </div>
                            <span class="ml-4 text-gray-700">${(likelihood * 100).toFixed(1)}%</span>
                        </div>
                    `).join('');

                // Show results
                hideElement('loading');
                showElement('results');

            } catch (error) {
                hideElement('loading');
                displayError('Failed to analyze content. Please try again.');
                console.error('Analysis error:', error);
            }
        });
    }

    // Feedback form handling
    const feedbackForm = document.getElementById('feedbackForm');
    if (feedbackForm) {
        feedbackForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const formData = {
                content: document.getElementById('campaignContent').value.trim(),
                engagement_rate: parseFloat(document.getElementById('engagementRate').value),
                conversion_rate: parseFloat(document.getElementById('conversionRate').value),
                target_persona: document.getElementById('targetPersona').value,
                campaign_type: document.getElementById('campaignType').value,
                notes: document.getElementById('notes').value.trim()
            };

            // Validation
            if (!formData.content) {
                displayError('Please enter campaign content');
                return;
            }
            if (isNaN(formData.engagement_rate) || formData.engagement_rate < 0 || formData.engagement_rate > 100) {
                displayError('Please enter a valid engagement rate (0-100)');
                return;
            }
            if (isNaN(formData.conversion_rate) || formData.conversion_rate < 0 || formData.conversion_rate > 100) {
                displayError('Please enter a valid conversion rate (0-100)');
                return;
            }
            if (!formData.target_persona) {
                displayError('Please select a target persona');
                return;
            }
            if (!formData.campaign_type) {
                displayError('Please select a campaign type');
                return;
            }

            try {
                const response = await fetch('/feedback', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData),
                });

                if (!response.ok) {
                    throw new Error('Feedback submission failed');
                }

                // Show success message
                showElement('successMessage');
                feedbackForm.reset();
                setTimeout(() => hideElement('successMessage'), 5000);

            } catch (error) {
                displayError('Failed to submit feedback. Please try again.');
                console.error('Feedback submission error:', error);
            }
        });
    }
}); 