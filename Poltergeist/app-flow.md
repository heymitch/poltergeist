# 5. App Flow Document

## 5.1. User Journey

1. **Entry Point:**
    - **Invitation & Login:**
        - User receives an invitation and signs up with a referral code, agreeing to NDA terms.
2. **Dashboard:**
    - **Overview:**
        - Upon logging in, the user lands on a confidential dashboard showing summary persuasion scores and simulation snapshots.
3. **Creating a New Post:**
    - **Input Page:**
        - User drafts or pastes the post in a secure text editor.
        - The Input Parser extracts and displays key persuasive features in real time.
4. **Running the Simulation:**
    - **Trigger Analysis:**
        - User clicks “Analyze.”
        - The Persuasion Scoring Model evaluates the text.
        - The Simulation Engine runs controlled Monte Carlo iterations based on defined viewer profiles.
        - The Sentiment & Tone Analyzer provides additional qualitative feedback.
5. **Viewing Results:**
    - **Results Page:**
        - Display of composite “Influence Score,” detailed qualitative feedback, and simulated response likelihoods for each viewer persona.
        - Graphs and charts highlight strengths and areas for improvement.
6. **Feedback Integration:**
    - **Performance Feedback:**
        - After running live campaigns, the user inputs actual performance data (revenue, conversion, etc.) via the Feedback Loop interface.
        - The backend recalibrates the simulation and persuasion scoring models.
7. **Iterative Improvement:**
    - **Ongoing Refinement:**
        - Users can compare historical simulation outputs with real-world results, adjusting their approach for future campaigns.
        - Continuous learning and refinement improve model accuracy and personalization over time.

## 5.2. System Flow

1. **User Request:**
    - Secure HTTP requests (over TLS) are received by the Flask backend.
2. **Data Processing:**
    - The Input Parser and Sentiment Analyzer process the submitted text.
    - The Persuasion Scoring Model assigns qualitative scores based on internal heuristics.
3. **Simulation:**
    - The Monte Carlo Simulation Engine uses NumPy to run controlled iterations with viewer profiles based on sales funnel archetypes.
    - Simulation outputs are aggregated into qualitative “response likelihood” metrics.
4. **Response Generation:**
    - The Output Metrics module formats numerical insights and visual data.
    - A secure response is sent to the user’s Dashboard/Results page.
5. **Feedback Loop:**
    - User-submitted performance data is incorporated.
    - Regression-based recalibration adjusts model parameters, improving future predictions.