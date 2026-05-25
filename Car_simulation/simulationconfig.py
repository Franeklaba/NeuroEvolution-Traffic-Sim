from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(frozen=True)
class MlInputNormConfig:
    max_nav_distance: float = 2000.0       # Maximum distance for normalization
    nav_distance_exponent: float = 0.5     # Exponent to emphasize close targets
    
@dataclass(frozen=True)
class SensorConfig: 
    base_range: int = 250  
    angle_range_multiplier: float = 0.7

@dataclass(frozen=True)
class CarScoreConfig:
    min_score: float = 1.0
    progress_distance_multiplier: float = 10.0
    win_distance_multiplier: float = 5.0
    time_efficiency_exponent: float = 2.0
    collision_multiplier: float = 0.5
    timeout_multiplier: float = 0.8
    
@dataclass(frozen=True)
class CarConfig:
    angle_change: int = 2
    max_speed: int = 8
    acceleration: float = 0.2
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
    simulation_time: int = 1600

    window_width: int = 1900
    window_height: int = 1000
    num_of_cars: int = 15
    background_color: tuple[int, int, int] = (30, 30, 30)
    clock_tick: int = 30
    car: CarConfig = field(default_factory=CarConfig)
    
    _city_positions_and_angles: list[tuple[tuple[int, int], int]] = field(default_factory=lambda: [
        # Przesunięto punkty idealnie na środek 120-pikselowych dróg (np. Y = 60 zamiast Y = 100)
        ((60, 60), 342),      # 1. Lewy górny róg
        ((370, 60), 344),     # 2. Górna ulica (środek lewy)
        ((680, 60), 233),     # 3. Skrzyżowanie górne
        ((1020, 60), 233),    # 4. Górna ulica (środek prawy)
        ((1300, 60), 233),    # 5. Przed prawym murem (góra)
        ((1840, 60), 225),    # 6. Za prawym murem (góra)
        ((60, 500), 347),     # 7. Lewe skrzyżowanie poziome
        ((680, 500), 146),    # 8. Środek mapy (skrzyżowanie)
        ((1300, 500), 156),   # 9. Środek mapy, przed murem
        ((1840, 500), 160),   # 10. Zaułek za prawym murem
        ((60, 940), 42),      # 11. Lewy dolny róg
        ((370, 940), 42),     # 12. Dolna ulica (środek lewy)
        ((680, 940), 36),     # 13. Dolne skrzyżowanie
        ((1020, 940), 156),   # 14. Dolna ulica (środek prawy)
        ((1840, 940), 160),   # 15. Skrajnie prawy dolny róg
    ], repr=False, hash=False, compare=False)

    _city_destination_points: list[tuple[int, int]] = field(default_factory=lambda: [
        # Losowo przypisane, zaktualizowane pozycje docelowe
        (1300, 500), (1840, 940), (60, 940), (680, 940), (1300, 940),
        (1020, 940), (60, 60), (370, 940), (1840, 60), (370, 60),
        (680, 60), (1020, 60), (60, 500), (680, 500), (1300, 60)
    ], repr=False, hash=False, compare=False)

    def cars_position_and_angle(self, map_type="slalom") -> list[tuple[tuple[int, int], int]]:
        if map_type == "slalom":
            return [((self.window_width - 80 - (i % 3) * 60, 100 + (i // 3) * 40), 180) for i in range(self.num_of_cars)]
        elif map_type == "city":
            return self._city_positions_and_angles[:self.num_of_cars]
        elif map_type == "bottleneck":
            return [((self.window_width / 2 + ((i % 5) - 2) * 200, 80 + (i // 5) * 80), 270) for i in range(self.num_of_cars)]
        elif map_type == "track":
            return [((100, self.window_height / 2 + (i - self.num_of_cars // 2)* 70), 0) for i in range(self.num_of_cars)]
        else:
            return [(((70, self.window_height / 2)), 0) for _ in range(self.num_of_cars)]
    @property 
    def map_types(self) -> list[str]:
        return ["slalom", "city", "bottleneck", "track"]
    
    def obsticles_pos(self, map_type="slalom") -> list[tuple[int, int, int, int]]:
        borders = [
            (0, 0, self.window_width, 10),
            (0, self.window_height - 10, self.window_width, 10),
            (0, 0, 10, self.window_height),
            (self.window_width - 10, 0, 10, self.window_height),
        ]
        if map_type == "slalom":
            inner_obstacles = [
                (1500, 350, 80, 650),
                (1150, 0, 80, 650),
                (800, 450, 80, 550),
                (450, 350, 80, 300),
                (200, 0, 20, 250),  
                (200, 400, 20, 200),   # Blokada środkowa
                (200, 750, 20, 250),   # Blokada dolna
            ]
        elif map_type == "city":
            inner_obstacles = [
                (120, 120, 500, 320),    # Lewy górny kwartał
                (120, 560, 500, 320),    # Lewy dolny kwartał
                (740, 120, 500, 320),    # Środkowy górny kwartał
                (740, 560, 500, 320),    # Środkowy dolny kwartał
                (1360, 120, 420, 760),   # Prawy masywny blok (odcina środek, tworzy ślepy zaułek z prawej)
            ]
        elif map_type == "bottleneck":
            inner_obstacles = [
                (0, 300, 600, 50),       # Lewa góra
                (1300, 300, 600, 50),    # Prawa góra                
                # 2. WŁAŚCIWE WĄSKIE GARDŁO (Zostawia tylko 300px przerwy)
                (0, 550, 800, 100),      # Lewa główna zapora
                (1100, 550, 800, 100),   # Prawa główna zapora
                # 3. ROZDZIELACZ (Splitter) - wymusza nagły manewr po wyjeździe z gardła
                (900, 750, 100, 150),    # Centralny słup na dole
                # 4. ŚCIANKI DZIAŁOWE (Tworzą wydzielone boksy dla celów)
                (400, 750, 50, 250),     # Oddziela lewą strefę
                (1450, 750, 50, 250),    # Oddziela prawą strefę
            ]
        elif map_type == "track":
            inner_obstacles = [
                (250, 250, 50, 500),   
                (450, 0, 60, 350),      
                (450, 650, 60, 350),    
                (700, 300, 60, 400),    
                (900, 150, 300, 80),    
                (900, 770, 300, 80),    
                (1100, 400, 80, 200),   
                (1350, 200, 40, 600),   
                (1550, 300, 150, 50),   # Górna pułapka pozioma
                (1550, 650, 150, 50),   # Dolna pułapka pozioma
                (1700, 450, 100, 100),  # Kloc na samym końcu dla aut lecących z nadmierną prędkością
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
            points = [
                (1350, 150), (1350, 250), (1400, 100),
                (1000, 750), (1000, 850), (1050, 950),
                (650, 100), (650, 250), (650, 400),
                (100, 300), (100, 350), (50, 325),
                (100, 650), (100, 700), (50, 675)
            ]
        elif map_type == "city":
            points = self._city_destination_points[:self.num_of_cars]
        elif map_type == "bottleneck":
            points = [
                (850, 680), (950, 680), (1050, 680),
                (750, 850), (1150, 850), (850, 920), (1050, 920),
                (550, 850), (650, 950),     
                (1250, 850), (1350, 950),  
                (150, 800), (300, 900),    
                (1600, 900), (1750, 800)   
            ]
        elif map_type == "track":
            points = [
                # --- POZIOM 1: Łatwy (Przed centrum) ---
                # Wymaga jedynie ominięcia pierwszej i drugiej ściany
                (580, 150),       # Czerwony - Górny przesmyk
                (580, 850),       # Zielony - Dolny przesmyk
                (800, 500),       # Jasnoniebieski - Dokładnie pośrodku przed zadaszeniami
                
                # --- POZIOM 2: Średni (Centrum Labiryntu) ---
                # Wymaga precyzyjnego manewrowania między słupami a poziomymi belkami
                (1000, 80),       # Żółty - Przy samej górnej krawędzi (nad belką)
                (1000, 920),      # Cyjan - Przy samej dolnej krawędzi (pod belką)
                (1250, 500),      # Magenta - Środek, zaraz za wielkim centralnym słupem
                
                # --- POZIOM 3: Trudny (Przekroczenie Wielkiego Muru) ---
                # Wymaga odnalezienia wąskich luk na samej górze (y < 200) lub dole (y > 800)
                (1450, 100),      # Pomarańczowy - Zaraz za górną luką Wielkiego Muru
                (1450, 900),      # Różowy - Zaraz za dolną luką Wielkiego Muru
                (1600, 200),      # Limonkowy - Nad górną pułapką 
                (1600, 800),      # Złoty - Pod dolną pułapką
                
                # --- POZIOM 4: Ekstremalny (Pułapki i Zakamarki) ---
                # Wymagają nawrotów, zawracania i omijania kloców na końcu mapy
                (1450, 500),      # Pomidorowy - GŁĘBOKA PUŁAPKA: schowana zaraz za murem, trzeba zawrócić po przejechaniu luki!
                (1800, 350),      # Turkusowy - Pomiędzy górną pułapką a klocem na mecie
                (1800, 600),      # Fioletowy - Pomiędzy dolną pułapką a klocem na mecie
                (1800, 100),      # Koralowy - Skrajny prawy górny róg
                (1800, 900),      # Chabrowy - Skrajny prawy dolny róg
            ]
                

        else:
            points = [(100 + i*50, 100) for i in range(15)] 

        return list(zip(points, colors))


SIMULATION_CONFIG = SimulationConfig()
CAR_CONFIG = CarConfig()
ML_INPUT_NORM_CONFIG = MlInputNormConfig()
SENSOR_CONFIG = SensorConfig()
