from dataclasses import dataclass

g = 9.81

N_STEPS = 12000
SIMULATION_TIME = 24

@dataclass
class ModelParams:
    r: float = 1
    R: float = 2
    m: float = 1
    b: float = 0.8
