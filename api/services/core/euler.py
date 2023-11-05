import matplotlib.pyplot as plt
from schemas.euler import EulerSchema

# Core algorithm for Euler method


# def euler_method(euler: EulerSchema) -> EulerSchema:
class Model:
    def __init__(
        self,
        t: float = 10,
        t0: float = 0,
        x0: float = 2,
        a: float = 0.35,
        N: int = 100
    ):
        self.t: float = t
        self.t0: float = t0
        self.x0: float = x0
        self.a: float = a
        self.N: int = N

        self.T: list[float] = []
        self.X: list[float] = []

    def solve(self):
        pass

