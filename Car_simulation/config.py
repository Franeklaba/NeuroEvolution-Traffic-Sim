from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CarConfig:
    angle_change: int = 2
    max_speed: int = 6
    acceleration: float = 0.05
    sensors_angle: tuple[int, ...] = (0, 20, 45, 90, 155, 180, 205, 270, 315, 340)

    @property
    def num_of_sensors(self) -> int:
        return len(self.sensors_angle)


@dataclass(frozen=True)
class SimulationConfig:
    window_width: int = 1700
    window_height: int = 1000
    num_of_cars: int = 1
    background_color: tuple[int, int, int] = (30, 30, 30)
    clock_tick: int = 20
    simulation_time: int = 1000
    car: CarConfig = field(default_factory=CarConfig)

    @property
    def cars_position(self) -> list[tuple[int, int]]:
        return [
            (0 + 70, self.window_height - 80 - i * 80)
            for i in range(self.num_of_cars)
        ]

    @property
    def obsticles_pos(self) -> list[tuple[int, int, int, int]]:
        return [
            (0, 0, self.window_width, 20),
            (0, self.window_height - 20, self.window_width, 20),
            (0, 0, 20, self.window_height),
            (self.window_width - 20, 0, 20, self.window_height),
            (400, 300, 200, 50),
            (1000, 500, 50, 300),
            (750, 700, 100, 100),
        ]


SIMULATION_CONFIG = SimulationConfig()
CAR_CONFIG = CarConfig()
