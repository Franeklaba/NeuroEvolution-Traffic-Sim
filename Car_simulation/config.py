from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CarConfig:
    angle_change: int = 2
    max_speed: int = 6
    acceleration: float = 0.05
    sensors_angle: tuple[int, ...] = (0, 20, 45, 90, 270, 315, 340)

    dest_point_rect = (40, 40)
    @property
    def num_of_sensors(self) -> int:
        return len(self.sensors_angle)


@dataclass(frozen=True)
class SimulationConfig:
    window_width: int = 1700
    window_height: int = 1000
    num_of_cars: int = 10
    background_color: tuple[int, int, int] = (30, 30, 30)
    clock_tick: int = 20
    simulation_time: int = 1000
    car: CarConfig = field(default_factory=CarConfig)

    @property
    def cars_position(self) -> list[tuple[int, int]]:
        return [
            (0 + 70, self.window_height / 2 + (i - self.num_of_cars/2) * 50) for i in range(self.num_of_cars) 
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
