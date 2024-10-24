import torch
from voyager import Index


class RetrieveSimilarVectorsQueryService:
    def __init__(self, index: Index, num: int) -> None:
        self.index = index
        self.num = num

    def __call__(self, vector: torch.Tensor) -> tuple[list[int], list[float]]:
        ids, distances = self.index.query(vector.cpu().numpy(), self.num)
        return ids.tolist(), distances.tolist()
