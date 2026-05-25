from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(frozen=True)
class NeuroevolutionConfig:
    population_size: int = 200
    generations: int = 10
    base_mutation_rate: float = 0.3
    base_mutation_strength: float = 0.3
    num_elites: int = 3
    simulation_time: int = 1400

    stability_penalty_weight:float = 0.5
    target_score: float = 100000.0

    ml_input_type:int = 1

    
    _result_files_names:list[str] = field(default_factory=lambda: ["ml_input_1_results.csv", "ml_input_2_results.csv", "ml_input_3_results.csv", "ml_input_4_results.csv", "ml_input_5_results.csv"])
    _weights_files_names: list[str]  = field(default_factory=lambda: ["ml_input_1_weights.npy", "ml_input_2_weights.npy", "ml_input_3_weights.npy", "ml_input_4_weights.npy", "ml_input_5_weights.npy"])
    _best_weights_files_names: list[str] = field(default_factory=lambda: ["ml_input_1_best_weights.npy", "ml_input_2_best_weights.npy", "ml_input_3_best_weights.npy", "ml_input_4_best_weights.npy", " ml_input_5_best_weights.npy"])

    @property
    def result_file_path(self) -> str:
        return 'genes_and_results/results/' + self._result_files_names[self.ml_input_type - 1]
    @property
    def weights_file_path(self) -> str:
        return 'genes_and_results/population_weights/' + self._weights_files_names[self.ml_input_type - 1]
    @property
    def best_weights_file_path(self) -> str:
        return 'genes_and_results/best_genes/' + self._best_weights_files_names[self.ml_input_type - 1]
    
    
    

    
NEURO_EVOLUTION_CONFIG = NeuroevolutionConfig()