import math
import pygame
from .config import CAR_CONFIG, CarConfig
from .raycastsensor import RaycastSensor


class Car(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int], car_config: CarConfig = CAR_CONFIG):
        super().__init__()
        self.car_config = car_config

        self._base_sprite = pygame.Surface((25, 20), pygame.SRCALPHA)
        self._base_sprite.fill("Red")
        self.image = self._base_sprite

        self.current_observation = list()

        self.pos_x, self.pos_y = position  # kod do zmiany wprzyszłosci nalezy urzyć Vector2
        self.pos = pygame.math.Vector2(position)
        self.direction_vector = pygame.math.Vector2((1, 0))

        self.rect = self.image.get_rect(center=position)
        self.mask = pygame.mask.from_surface(self.image)

        self.speed = 0.0
        self.angle = 0.0

        self.sensors = [RaycastSensor(angle) for angle in self.car_config.sensors_angle]

    def _update_pos(self):  # kod do pozniejszego usunięcia
        keys = pygame.key.get_pressed()  # kod do pozniejszego usunięcia
        cfg = self.car_config
        if keys[pygame.K_w] and self.speed < cfg.max_speed:  # kod do pozniejszego usunięcia
            self.speed += cfg.acceleration  # kod do pozniejszego usunięcia
        else:  # kod do pozniejszego usunięcia
            if self.speed > 0:  # kod do pozniejszego usunięcia
                self.speed -= cfg.acceleration  # kod do pozniejszego usunięcia
            else:
                self.speed = 0
        if keys[pygame.K_d]:  # kod do pozniejszego usunięcia
            self.angle -= cfg.angle_change  # kod do pozniejszego usunięcia
        elif keys[pygame.K_a]:  # kod do pozniejszego usunięcia
            self.angle += cfg.angle_change  # kod do pozniejszego usunięcia


        self.direction_vector.from_polar((1, 0 - self.angle))
        self.pos += self.direction_vector * self.speed
        self.rect.center = self.pos
        
        self.pos_y += self.speed * math.sin(math.radians(self.angle))  # kod do pozniejszego usunięcia
        self.pos_x -= self.speed * math.cos(math.radians(self.angle))  # kod do pozniejszego usunięcia
        # self.rect.centery = self.pos_y  # kod do pozniejszego usunięcia
        # self.rect.centerx = self.pos_x  # kod do pozniejszego usunięcia

    def _update_sprite(self):
        self.image = pygame.transform.rotate(self._base_sprite, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
    def _draw_sensors(self, distacnce_to_obsticle, obsticle_col_point, car_col_point, screen, is_car):
        if distacnce_to_obsticle == 0:
            current_color = 'DarkGray' # Pusty laser, brak jakiejkolwiek przeszkody
        elif distacnce_to_obsticle < 0.2:
            current_color = 'Green'    # Przeszkoda bardzo daleko (strefa komfortu)
        elif distacnce_to_obsticle < 0.5:
            current_color = 'Yellow'   # Umiarkowane zagrożenie (AI zaczyna zwracać uwagę)
        elif distacnce_to_obsticle < 0.8:
            current_color = 'Orange'   # Duże niebezpieczeństwo (AI powinno mocno korygować tor jazdy)
        else:
            current_color = 'Red'      # Krytycznie blisko - kolizja jest niemal pewna
        
        if distacnce_to_obsticle > 0:
            pygame.draw.circle(screen, current_color, obsticle_col_point, 3)

        
        if is_car:
            pygame.draw.line(screen, "White", self.pos, car_col_point, 4)
        pygame.draw.line(screen, current_color, self.pos, obsticle_col_point, 1)
        

        
        if distacnce_to_obsticle > 0:
            pygame.draw.circle(screen, current_color, obsticle_col_point, 3)


    def _get_ml_input(self, measur): # aktualnie funckcja ta przetwarza jedynie wejście z czujnika ścian zakładamy ze na planszy jest tylko jeden samochod 
        ml_input = list()
        for distance_to_obsticle, distance_to_another_car, sensor_range, car_obj in measur:
            dead_zone = 15 + (abs(self.speed) * 2.0) + (sensor_range * 0.1)

            if dead_zone >= sensor_range:
                dead_zone = sensor_range - 1.0

            standardized_data = (sensor_range - distance_to_obsticle) / (sensor_range - dead_zone)
            standardized_data = max(0.0, min(1.0, standardized_data))
            standardized_data = standardized_data ** 1.5
            ml_input.append(standardized_data)
        return standardized_data


    def _sensors_managment(self, obsticles_group: pygame.sprite.Group, cars_group: pygame.sprite.Group, screen = None):
        measurement = list()
        for i in range(self.car_config.num_of_sensors):
            distance_to_obsticle, distance_to_another_car, sensor_range, car_obj, obsticle_col_point, car_col_point = \
            self.sensors[i].get_sensor_data(self.pos, self.direction_vector, obsticles_group, cars_group, self.speed, self)

            if screen: 
                self._draw_sensors(distance_to_obsticle, obsticle_col_point, car_col_point, screen, not(car_obj == None))

            measurement.append((distance_to_obsticle, distance_to_another_car, sensor_range, car_obj))
        
        self.current_observation = self._get_ml_input(measurement)
                
        
                
        

    def update(self, obsticles_group: pygame.sprite.Group, cars_group: pygame.sprite.Group, screen):
        self._update_pos()
        self._update_sprite()
        self._sensors_managment(obsticles_group, cars_group, screen)
