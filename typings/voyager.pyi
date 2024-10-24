from collections.abc import Iterator
from enum import Enum

import numpy as np

class Index:
    def __init__(self, space: Space, num_dimensions: int) -> None: ...
    def add_item(self, vector: np.ndarray, id: int) -> None: ...  # noqa: A002
    def add_items(self, vectors: np.ndarray, ids: list[int]) -> None: ...
    def query(self, vector: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]: ...
    def save(self, path: str) -> None: ...
    def get_vector(self, id: int) -> np.ndarray: ...  # noqa: A002
    def get_vectors(self, ids: list[int]) -> np.ndarray: ...
    def __contains__(self, id: int) -> bool: ...  # noqa: A002
    def __len__(self) -> int: ...
    @staticmethod
    def load(path: str) -> Index: ...
    @property
    def num_dimensions(self) -> int: ...
    @property
    def ids(self) -> LabelSetView: ...

class Space(Enum):
    Euclidean = 0
    InnerProduct = 1
    Cosine = 2

class LabelSetView:
    def __iter__(self) -> Iterator[int]: ...
    def __contains__(self, item: int) -> bool: ...
