from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(frozen=True)
class MlInputNormConfig:
    dead_zone_base: float = 15.0           # Base value of the dead zone
    dead_zone_speed_weight: float = 2.0    # Speed weight multiplier
    dead_zone_range_weight: float = 0.1    # Sensor range weight multiplier
    dead_zone_margin: float = 1.0          # Margin when dead_zone >= sensor_range
    sensor_data_exponent: float = 1.2      # Exponent to emphasize close objects
    max_nav_distance: float = 1400.0       # Maximum distance for normalization
    max_nav_angle: float = 180.0           # Maximum angle for normalization

@dataclass(frozen=True)
class SensorConfig: 
    base_range: int = 170
    angle_range_multiplier: float = 0.7 #range_multiplier = 1.0 - (abs_angle / 90.0) * ange_range_muliplayer
    speed_range_multiplier: float = 40.0 # raycas_range = (self.BASE_RANGE + speed * speed_range_multiplayer) * range_multiplier


@dataclass(frozen=True)
class CarScoreConfig:
    no_collision_reward: int = 300
    min_distance_score: int = 1
    win_base_reward: int = 800
    win_distance_multiplier: int = 4.5

@dataclass(frozen=True)
class CarConfig:
    angle_change: int = 2
    max_speed: int = 6
    acceleration: float = 0.05
    sensors_angle: tuple[int, ...] = (0, 20, 45, 90, 270, 315, 340)
    dest_point_rect: tuple[int, int]= (40, 40)

    sensor: SensorConfig = field(default_factory=SensorConfig)
    ml_input_norm: MlInputNormConfig = field(default_factory=MlInputNormConfig)
    score: CarScoreConfig = field(default_factory=CarScoreConfig)
    @property
    def num_of_sensors(self) -> int:
        return len(self.sensors_angle)


@dataclass(frozen=True)
class SimulationConfig:
    window_width: int = 1700
    window_height: int = 1000
    num_of_cars: int = 15
    background_color: tuple[int, int, int] = (30, 30, 30)
    clock_tick: int = 40
    car: CarConfig = field(default_factory=CarConfig)

    @property
    def cars_position(self) -> list[tuple[int, int]]:
        return [
            (0 + 70, self.window_height / 2 + (i - self.num_of_cars/2) * 60) for i in range(self.num_of_cars) 
        ]

    @property
    def obsticles_pos(self) -> list[tuple[int, int, int, int]]:
        return [
            (0, 0, self.window_width, 10),
            (0, self.window_height - 10, self.window_width, 10),
            (0, 0, 10, self.window_height),
            (self.window_width - 10, 0, 10, self.window_height),
            
            (300, 150, 100, 170),   # Blok pionowy (lewa góra)
            (250, 550, 170, 80),    # Blok poziomy (lewy środek)
            (550, 750, 100, 120),   # Kwadratowy blok (lewy dół)
            (700, 150, 220, 100),   # Szeroka belka (środek góra)
            (750, 500, 80, 80),     # Mała kostka (centrum)
            (800, 750, 100, 100),   # Mniejszy blok (środek dół)
            # w(500, 350, 170, 60),    # Pozioma belka (środek lewy)
            (1150, 150, 60, 120),   # Wąski wpust (prawa góra)
            (1050, 420, 160, 200),   # Wysoki słupek (środek dół)
            (1150, 800, 120, 60),   # Niska belka (prawa dół)
            (1400, 150, 120, 120),  # Masywny blok (skrajna prawa góra)
            (1450, 750, 170, 100),  # Pozioma przeszkoda (skrajna prawa dół)
        ]
    @property
    def cars_destination_points_and_color(self) -> list[tuple[tuple[int, int], tuple[int, int, int]]]:
        return [
            # Górna strefa
            ((950, 100), (255, 0, 0)),        # Czerwony
            ((1300, 100), (0, 255, 0)),       # Zielony
            ((1600, 100), (0, 150, 255)),     # Jasnoniebieski
            
            # Środkowa strefa (wyżej)
            ((1000, 300), (255, 255, 0)),     # Żółty
            ((1300, 350), (0, 255, 255)),     # Cyjan (Jasnobłękitny)
            ((1600, 350), (255, 0, 255)),     # Magenta (Fuksja)
            
            # Środkowa strefa (niżej)
            ((950, 600), (255, 165, 0)),      # Pomarańczowy
            ((1300, 550), (255, 105, 180)),   # Różowy (Hot Pink)
            ((1600, 550), (50, 205, 50)),     # Limonkowy
            
            # Dolna strefa
            ((950, 900), (255, 215, 0)),      # Złoty
            ((1350, 920), (255, 99, 71)),     # Pomidorowy
            ((1650, 950), (64, 224, 208)),    # Turkusowy
            
            # Dodatkowe zakamarki
            ((1250, 700), (238, 130, 238)),   # Fioletowy
            ((1550, 200), (255, 127, 80)),    # Koralowy
            ((1100, 750), (100, 149, 237)),   # Chabrowy
        ]


SIMULATION_CONFIG = SimulationConfig()
CAR_CONFIG = CarConfig()
ML_INPUT_NORM_CONFIG = MlInputNormConfig()
SENSOR_CONFIG = SensorConfig()
