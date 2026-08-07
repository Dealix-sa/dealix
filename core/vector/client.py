from __future__ import annotations

from abc import ABC, abstractmethod

from .schemas import SearchResult, VectorPoint


class VectorClient(ABC):
    @abstractmethod
    async def upsert(self, collection: str, points: list[VectorPoint]) -> None:
        ...

    @abstractmethod
    async def search(
        self,
        collection: str,
        query: list[float],
        top_k: int = 10,
    ) -> list[SearchResult]:
        ...

    @abstractmethod
    async def delete(self, collection: str, point_ids: list[str]) -> None:
        ...

    @abstractmethod
    async def create_collection(
        self,
        name: str,
        dims: int = 1536,
    ) -> None:
        ...

    async def health_check(self) -> bool:
        try:
            await self.search("_health", [0.0] * 1536, top_k=1)
            return True
        except Exception:
            return False

    # Abstract, like its four siblings above: the body is `...`, not a usable
    # default. Without the decorator a subclass that forgot to implement it
    # inherited a silent no-op — `delete_collection` would report success and
    # delete nothing. `list_collections` and `collection_info` below are
    # deliberately different: they return real, safe defaults.
    @abstractmethod
    async def delete_collection(self, name: str) -> None:
        ...

    async def list_collections(self) -> list[str]:
        return []

    async def collection_info(self, name: str) -> dict:
        return {}
