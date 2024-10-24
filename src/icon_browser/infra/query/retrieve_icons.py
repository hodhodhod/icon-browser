import csv
from collections.abc import Iterable
from pathlib import Path


class RetrieveIconsQueryService:
    def __init__(self, csv_path: Path) -> None:
        with csv_path.open("r") as f:
            self.mapping = {int(row["id"]): row["name"] for row in csv.DictReader(f)}

    def __call__(self, ids: Iterable[int]) -> list[str]:
        return [self.mapping[id_] for id_ in ids]
