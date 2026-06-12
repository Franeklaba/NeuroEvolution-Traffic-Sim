from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(frozen=True)
class NeuroevolutionConfig:

    ml_input_type:int = 5

    generations: int = 10
    base_mutation_rate: float = 0.3
    base_mutation_strength: float = 0.3
    stability_penalty_weight:float = 0.6
    target_score: float = 100.0

    
    _population_sizes: dict[int, int] = field(default_factory=lambda: {
        1: 120,
        2: 170,
        3: 260,
        4: 400,
        5: 170
    })
    @property
    def population_size(self) -> int:
        return self._population_sizes[self.ml_input_type]
    
    _num_of_elites: dict[int, int] = field(default_factory=lambda: {
        1: 3,   
        2: 5,   
        3: 8,   
        4: 12,  
        5: 5    
    })

    @property
    def num_of_elites(self) -> int:
        return self._num_of_elites[self.ml_input_type]
    
    _result_files_names: dict[int, str] = field(default_factory=lambda: {
        1: "ml_input_1_results.csv",
        2: "ml_input_2_results.csv",
        3: "ml_input_3_results.csv",
        4: "ml_input_4_results.csv",
        5: "ml_input_5_results.csv"
        })
    _weights_files_names: dict[int, str]  = field(default_factory=lambda: {
        1: "ml_input_1_weights.npy",
        2: "ml_input_2_weights.npy",
        3: "ml_input_3_weights.npy",
        4: "ml_input_4_weights.npy",
        5: "ml_input_5_weights.npy"
        })
    _best_weights_files_names: dict[int, str] = field(default_factory=lambda: {
        1: "ml_input_1_best_weights.npy",
        2: "ml_input_2_best_weights.npy",
        3: "ml_input_3_best_weights.npy",
        4: "ml_input_4_best_weights.npy",
        5: " ml_input_5_best_weights.npy"
        })

    @property
    def result_file_path(self) -> str:
        return 'genes_and_results_in_training/results/' + self._result_files_names[self.ml_input_type]
    @property
    def weights_file_path(self) -> str:
        return 'genes_and_results_in_training/population_weights/' + self._weights_files_names[self.ml_input_type]
    @property
    def best_weights_file_path(self) -> str:
        return 'genes_and_results_in_training/best_genes/' + self._best_weights_files_names[self.ml_input_type]
    

    

    
NEURO_EVOLUTION_CONFIG = NeuroevolutionConfig()