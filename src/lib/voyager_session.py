from pathlib import Path
from types import TracebackType

from voyager import Index, Space


class VoyagerSession:
    def __init__(self, index: Index, path: Path) -> None:
        self.index = index
        self.path = path

    @classmethod
    def create(cls, path: Path, dim: int, space: Space = Space.Cosine) -> "VoyagerSession":
        return cls(Index(space, dim), path)

    @classmethod
    def load(cls, path: Path) -> "VoyagerSession":
        return cls(Index.load(str(path)), path)

    def __enter__(self) -> Index:
        return self.index

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.index.save(str(self.path))
