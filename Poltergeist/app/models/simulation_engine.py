import numpy as np
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class PersonaProfile:
    name: str
    description: str
    # Weights for how much each persuasion factor matters to this persona
    clarity_weight: float
    urgency_weight: float
    social_proof_weight: float
    cta_weight: float
    # Base response rate and variance
    base_response_rate: float
    variance: float

class SimulationEngine:
    def __init__(self):
        # Define personas based on Eugene Schwartz's levels of awareness
        self.personas = {
            "unaware": PersonaProfile(
                name="Unaware",
                description="No knowledge of the product or problem",
                clarity_weight=0.5,      # Needs very clear problem explanation
                urgency_weight=0.1,      # Low urgency impact (doesn't know the problem)
                social_proof_weight=0.3,  # Moderate social proof impact
                cta_weight=0.1,          # Low CTA impact
                base_response_rate=0.01,  # Very low base response
                variance=0.005
            ),
            "problem_aware": PersonaProfile(
                name="Problem-Aware",
                description="Knows the problem but not the solution",
                clarity_weight=0.4,      # Needs clear solution explanation
                urgency_weight=0.2,      # Growing urgency impact
                social_proof_weight=0.3,  # Moderate social proof impact
                cta_weight=0.1,          # Low CTA impact
                base_response_rate=0.05,  # Low base response
                variance=0.02
            ),
            "solution_aware": PersonaProfile(
                name="Solution-Aware",
                description="Knows solutions exist but not your product",
                clarity_weight=0.3,      # Moderate clarity needs
                urgency_weight=0.2,      # Moderate urgency impact
                social_proof_weight=0.3,  # High social proof impact
                cta_weight=0.2,          # Growing CTA impact
                base_response_rate=0.10,  # Moderate base response
                variance=0.04
            ),
            "product_aware": PersonaProfile(
                name="Product-Aware",
                description="Knows your product but hasn't bought",
                clarity_weight=0.2,      # Lower clarity needs
                urgency_weight=0.3,      # High urgency impact
                social_proof_weight=0.2,  # Moderate social proof impact
                cta_weight=0.3,          # High CTA impact
                base_response_rate=0.15,  # Higher base response
                variance=0.06
            ),
            "most_aware": PersonaProfile(
                name="Most-Aware",
                description="Knows and wants your product",
                clarity_weight=0.1,      # Low clarity needs
                urgency_weight=0.4,      # Highest urgency impact
                social_proof_weight=0.1,  # Low social proof impact
                cta_weight=0.4,          # Highest CTA impact
                base_response_rate=0.25,  # Highest base response
                variance=0.08
            )
        }
        
        self.iterations = 1000  # Number of Monte Carlo iterations

    def calculate_weighted_score(self, scores: Dict[str, float], persona: PersonaProfile) -> float:
        """Calculate weighted persuasion score for a specific persona."""
        return (
            scores['clarity'] * persona.clarity_weight +
            scores['urgency'] * persona.urgency_weight +
            scores['social_proof'] * persona.social_proof_weight +
            scores['cta_strength'] * persona.cta_weight
        ) / 10  # Normalize to 0-1 scale

    def simulate_response(self, base_rate: float, weighted_score: float, variance: float) -> float:
        """Simulate response rate using Monte Carlo method."""
        # Base response rate modified by persuasion score
        modified_rate = base_rate * (1 + weighted_score)
        
        # Generate random variations
        responses = np.random.normal(
            loc=modified_rate,
            scale=variance,
            size=self.iterations
        )
        
        # Ensure responses are between 0 and 1
        responses = np.clip(responses, 0, 1)
        
        return float(np.mean(responses))

    def run_simulation(self, persuasion_scores: Dict[str, float]) -> Dict[str, Any]:
        """Run Monte Carlo simulation for each persona."""
        results = {}
        
        for persona_key, persona in self.personas.items():
            # Calculate weighted score for this persona
            weighted_score = self.calculate_weighted_score(persuasion_scores, persona)
            
            # Run simulation
            response_likelihood = self.simulate_response(
                persona.base_response_rate,
                weighted_score,
                persona.variance
            )
            
            results[persona_key] = {
                "name": persona.name,
                "description": persona.description,
                "response_likelihood": round(response_likelihood * 100, 2),  # Convert to percentage
                "weighted_score": round(weighted_score, 2)
            }
        
        return {
            "persona_responses": results,
            "simulation_iterations": self.iterations,
            "most_receptive_persona": max(
                results.items(),
                key=lambda x: x[1]["response_likelihood"]
            )[1]["name"]
        } 