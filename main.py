import time
from Car_simulation import CarSimulationMenager
train_menager = CarSimulationMenager(is_trainig_mode=True)

start_time = time.time()
for _ in range(10):
    train_menager.run()
    train_menager.reset()
end_time = time.time()
train_menager.quit()
# print(f"Czas wykonywania symulacji: {end_time - start_time:.2f} sekund")
simulation_menager = CarSimulationMenager(is_trainig_mode=False)
simulation_menager.run()
simulation_menager.quit()

