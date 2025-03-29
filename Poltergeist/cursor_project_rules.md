# Cursor Project Rules

This project is a private, invite-only persuasion intelligence tool designed for elite ghostwriting agencies. Its purpose is to provide qualitative feedback on writing based on persuasion strength, simulation-informed viewer profiles, and sentiment alignment. These rules must be followed on all tasks, file changes, and model logic implementations.

---

## Core Directives

1. **Never reference platform algorithms directly.**  
   We are not trying to reverse-engineer Twitter, Instagram, or any platform. We are simulating persuasive effectiveness based on known copywriting and psychological principles.

2. **Always frame output as qualitative insight, not guaranteed performance.**  
   No module or model should predict exact metrics like views, likes, or shares. Focus on persuasion scores, tone matching, and simulated reader response *likelihoods*.

3. **The tone of the tool should be expert, quiet, and exclusive.**  
   No onboarding for mass-market use. Do not add general help pages, tooltips, or FAQs unless explicitly requested.

4. **Use Eugene Schwartz’s levels of awareness to guide viewer personas.**  
   Simulation personas should follow:
   - Unaware
   - Problem-Aware
   - Solution-Aware
   - Product-Aware
   - Most Aware

5. **Scoring must be rooted in classic copywriting techniques.**  
   Scoring modules should evaluate clarity, urgency, credibility/social proof, CTA strength, stickiness, and tone resonance.

6. **Simulation must use weighted probabilities, not raw metrics.**  
   Monte Carlo simulations should be based on controlled variations of persuasive features, not engagement prediction.

7. **No new external libraries without approval.**  
   Core stack is Python, NLTK, NumPy, Flask. Any additional ML/NLP tools must be approved before use.

8. **Preserve stealth mode.**  
   Never expose internal methods or APIs to the public. All routes must be private, token-based, and invite-only.

9. **Feedback loop must be non-invasive and controlled.**  
   User-submitted data is optional and must be stored locally in `/data/` for private model refinement. Do not build any kind of automatic telemetry or cloud sync.

10. **Never use placeholder outputs or mock data in live endpoints.**  
    All outputs must reflect actual logic and computation. If something isn’t built yet, return a clean `"not implemented"` message.

---

## File-Specific Responsibilities

- `implementation-plan.md`: Follow it step-by-step, marking steps as `Done` only when complete. Never skip.
- `models/`: Simulation logic, scoring functions, persona definitions, tone/sentiment analysis all live here.
- `app/`: All Flask endpoints. Secure routing, input parsing, simulation trigger, output formatting.
- `templates/` and `static/`: Only used for lightweight MVP web interface. No JavaScript frameworks. Clean and minimal.
- `data/`: Sample user feedback, simulation logs, and calibration data must be stored here.

---

## Interaction Guidelines

- Do not apologize, speculate, or provide understanding statements.
- Only respond with code and execution necessary to complete the current step.
- Always reference this rules file and `implementation-plan.md` before making assumptions.
- If instructions are unclear, pause and request clarification before continuing.
