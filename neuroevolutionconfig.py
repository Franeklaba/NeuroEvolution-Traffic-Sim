from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(frozen=True)
class NeuroevolutionConfig:
    population_size: int = 200
    generations: int = 2
    base_mutation_rate: float = 0.3
    base_mutation_strength: float = 0.3
    num_elites: int = 3
    simulation_time: int = 1400

    stability_penalty_weight:float = 0.5
    target_score: float = 100000.0
    
NEURO_EVOLUTION_CONFIG = NeuroevolutionConfig()