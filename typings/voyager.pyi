from enum import Enum

import numpy as np

class Index:
    def __init__(self, space: Space, num_dimensions: int) -> None: ...
    def add_items(
        self,
        vectors: np.ndarray,
        ids: list[int] | None = None,
        num_threads: int = -1,
    ) -> None: ...
    def query(self, vector: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]: ...
    def save(self, path: str) -> None: ...
    @staticmethod
    def load(path: str) -> Index: ...

class Space(Enum):
    Cosine = 2
