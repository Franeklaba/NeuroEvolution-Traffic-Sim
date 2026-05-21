from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(frozen=True)
class MlInputNormConfig:
    max_nav_distance: float = 2000.0       # Maximum distance for normalization
    nav_distance_exponent: float = 0.5     # Exponent to emphasize close targets
    
@dataclass(frozen=True)
class SensorConfig: 
    base_range: int = 200  # Warto nieznacznie zwiększyć bazowy zasięg, skoro nie ma już bonusu od prędkości
    angle_range_multiplier: float = 0.7

@dataclass(frozen=True)
class CarScoreConfig:
    no_collision_reward: float = 300.0
    min_distance_score: float = 1.0
    win_base_reward: float = 2000.0
    win_distance_multiplier: float = 5.0
    time_penalty_multiplier: float = 0.5
    collision_penalty: float = 100.0 

@dataclass(frozen=True)
class CarConfig:
    angle_change: int = 2
    max_speed: int = 3
    acceleration: float = 0.05
    sensors_angle: tuple[int, ...] = (0, 20, 45, 90, 270, 315, 340)
    # sensors_angle: tuple[int, ...] = (0, 33, -33)

    dest_point_rect: tuple[int, int]= (40, 40)

    sensor: SensorConfig = field(default_factory=SensorConfig)
    ml_input_norm: MlInputNormConfig = field(default_factory=MlInputNormConfig)
    score: CarScoreConfig = field(default_factory=CarScoreConfig)
    @property
    def num_of_sensors(self) -> int:
        return len(self.sensors_angle)


@dataclass(frozen=True)
class SimulationConfig:
    window_width: int = 1900
    window_height: int = 1000
    num_of_cars: int = 15
    background_color: tuple[int, int, int] = (30, 30, 30)
    clock_tick: int = 120
    car: CarConfig = field(default_factory=CarConfig)
    
    _city_positions_and_angles: list[tuple[tuple[int, int], int]] = field(default_factory=lambda: [
        # (Start pos, angle)
        ((100, 100), 342),    # 1. Dest: (1300, 500)
        ((400, 100), 344),    # 2. Dest: (1800, 500)
        ((700, 100), 233),    # 3. Dest: (100, 900)
        ((1000, 100), 233),   # 4. Dest: (400, 900)
        ((1300, 100), 233),   # 5. Dest: (700, 900)
        ((1800, 100), 225),   # 6. Dest: (1000, 900)
        ((100, 500), 347),    # 7. Dest: (1800, 900)
        ((700, 500), 146),    # 8. Dest: (100, 100)
        ((1300, 500), 156),   # 9. Dest: (400, 100)
        ((1800, 500), 160),   # 10. Dest: (700, 100)
        ((100, 900), 42),     # 11. Dest: (1000, 100)
        ((400, 900), 42),     # 12. Dest: (1300, 100)
        ((700, 900), 36),     # 13. Dest: (1800, 100)
        ((1000, 900), 156),   # 14. Dest: (100, 500)
        ((1800, 900), 160),   # 15. Dest: (700, 500)
    ], repr=False, hash=False, compare=False)
    _city_destination_points: list[tuple[int, int]] = field(default_factory=lambda: [
        (1300, 500), (1800, 500), (100, 900), (400, 900), (700, 900),
        (1000, 900), (1800, 900), (100, 100), (400, 100), (700, 100),
        (1000, 100), (1300, 100), (1800, 100), (100, 500), (700, 500)
    ], repr=False, hash=False, compare=False)

    def cars_position_and_angle(self, map_type="slalom") -> list[tuple[tuple[int, int], int]]:
        if map_type == "slalom":
            return [((self.window_width - 100, self.window_height / 2 + (i - self.num_of_cars // 2)* 70), 180) for i in range(self.num_of_cars )]
        elif map_type == "city":
            return self._city_positions_and_angles[:self.num_of_cars]
        elif map_type == "bottleneck":
            return [((self.window_width / 2 + (i - self.num_of_cars // 2) * 100, 100), 270) for i in range(self.num_of_cars)]
        elif map_type == "track":
            return [((100, self.window_height / 2 + (i - self.num_of_cars // 2)* 70), 0) for i in range(self.num_of_cars)]
        else:
            return [(((70, self.window_height / 2)), 0) for _ in range(self.num_of_cars)]
    @property 
    def map_types(self) -> list[str]:
        return ["slalom", "city", "bottleneck", "track"]
    
    def obsticles_pos(self, map_type="slalom") -> list[tuple[int, int, int, int]]:
        # Stałe ramki ekranu - wspólne dla każdej mapy
        borders = [
            (0, 0, self.window_width, 10),
            (0, self.window_height - 10, self.window_width, 10),
            (0, 0, 10, self.window_height),
            (self.window_width - 10, 0, 10, self.window_height),
        ]
        if map_type == "slalom":
            inner_obstacles = [
                (300, 0, 100, 500),      # Ściana z góry
                (700, 400, 100, 500),    # Ściana z dołu
                (1100, 0, 100, 500),     # Ściana z góry
                (1500, 400, 100, 500),   # Ściana z dołu
            ]
        elif map_type == "city":
            inner_obstacles = [
                (200, 200, 400, 200),
                (200, 600, 400, 200),
                (800, 200, 400, 200),
                (800, 600, 400, 200),
                (1400, 200, 300, 600),
            ]
        elif map_type == "bottleneck":
            inner_obstacles = [
                (0, 400, 750, 100),       # Lewa zapora
                (950, 400, 970, 100),     # Prawa zapora (zostawia 200px przerwy)
                (400, 700, 800, 50),      # Dodatkowa belka do ominięcia po przejechaniu gardła
            ]
        elif map_type == "track":
            inner_obstacles = [
                (300, 150, 100, 170),   # Blok pionowy (lewa góra)
                (250, 550, 170, 80),    # Blok poziomy (lewy środek)
                (550, 750, 100, 120),   # Kwadratowy blok (lewy dół)
                (700, 150, 220, 100),   # Szeroka belka (środek góra)
                (750, 500, 80, 80),     # Mała kostka (centrum)
                (800, 750, 100, 100),   # Mniejszy blok (środek dół)
                (1150, 150, 60, 120),   # Wąski wpust (prawa góra)
                (1050, 420, 160, 200),   # Wysoki słupek (środek dół)
                (1150, 800, 120, 60),   # Niska belka (prawa dół)
                (1400, 150, 120, 120),  # Masywny blok (skrajna prawa góra)
                (1450, 750, 170, 100),  # Pozioma przeszkoda (skrajna prawa dół)
            ]
            
        else:
            inner_obstacles = []

        return borders + inner_obstacles
    def cars_destination_points_and_color(self, map_type="slalom") -> list[tuple[tuple[int, int], tuple[int, int, int]]]:
    # Stała paleta 15 kolorów dla wszystkich aut
        colors = [
            (255, 0, 0), (0, 255, 0), (0, 150, 255),       # Czerwony, Zielony, Jasnoniebieski
            (255, 255, 0), (0, 255, 255), (255, 0, 255),   # Żółty, Cyjan, Magenta
            (255, 165, 0), (255, 105, 180), (50, 205, 50), # Pomarańczowy, Różowy, Limonkowy
            (255, 215, 0), (255, 99, 71), (64, 224, 208),  # Złoty, Pomidorowy, Turkusowy
            (238, 130, 238), (255, 127, 80), (100, 149, 237) # Fioletowy, Koralowy, Chabrowy
        ]

        if map_type == "slalom":
            # Wszystkie cele na początku toru (po lewej stronie, przed pierwszą ścianą)
            points = [
                (200, 100), (200, 250), (200, 400), (200, 550), (200, 700),
                (100, 150), (100, 300), (100, 450), (100, 600), (100, 750),
                (250, 150), (250, 350), (250, 650), (250, 850), (150, 850)
            ]

        elif map_type == "city":
            points = self._city_destination_points[:self.num_of_cars]

        elif map_type == "bottleneck":
            points = [
                (100, 850), (300, 850), (500, 850), (700, 850), (900, 850),
                (1100, 850), (1300, 850), (1500, 850), (1700, 850),
                (200, 950), (400, 950), (600, 950), (800, 950), (1000, 950), (1200, 950)
            ]

        elif map_type == "track":
            points = [
                (950, 100),        # Czerwony
                (1300, 100),        # Zielony
                (1600, 100),     # Jasnoniebieski
                
                # Środkowa strefa (wyżej)
                (1000, 300),      # Żółty
                (1300, 350),      # Cyjan (Jasnobłękitny)
                (1600, 350),      # Magenta (Fuksja)
                
                # Środkowa strefa (niżej)
                (950, 600),       # Pomarańczowy
                (1300, 550),   # Różowy (Hot Pink)
                (1600, 550),     # Limonkowy
                
                # Dolna strefa
                (950, 900),      # Złoty
                (1350, 920),     # Pomidorowy
                (1650, 950),    # Turkusowy
                
                # Dodatkowe zakamarki
                (1250, 700),   # Fioletowy
                (1550, 200),    # Koralowy
                (1100, 750),   # Chabrowy
            ]
                

        else:
            points = [(100 + i*50, 100) for i in range(15)] 

        return list(zip(points, colors))


SIMULATION_CONFIG = SimulationConfig()
CAR_CONFIG = CarConfig()
ML_INPUT_NORM_CONFIG = MlInputNormConfig()
SENSOR_CONFIG = SensorConfig()
