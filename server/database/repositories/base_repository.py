from typing import Type, AsyncIterator

from cassandra.query import BatchStatement, ConsistencyLevel, SimpleStatement

from database.types import ModelQueries, Model as m
from database import Cassandra

# Repositories
# т.е. коллекции объектов,
# в отличие от моделей уже определяют методы
# взаимодействия с коллекциями


class CassandraRepository[Model: m]:
    """Same CRUD methods for all repositories"""
    def __init__(self, queries: ModelQueries, model: Type[Model]):
        self.queries: ModelQueries = queries
        self.model: Type[Model] = model

    def validate_starts_with(self, name: str) -> None:
        if not name.startswith('@'):
            raise ValueError(self.model.__starts_with__)

    async def find(self, *args) -> Model:
        """Searching only for one thing"""
        lookup = Cassandra.session.prepare(self.queries.FIND)
        future = Cassandra.session.execute_async(lookup, args)
        data = future.result().one()
        if data is None:
            raise Exception(self.model.__unknown__)
        return self.model(**data)

    async def get(self, *args) -> AsyncIterator[Model]:
        """Return all rows which match arg"""
        lookup = Cassandra.session.prepare(self.queries.GET)
        future = Cassandra.session.execute_async(lookup, args)
        data = future.result()
        if data is None:
            raise Exception(self.model.__unknown__)
        for row in data:
            yield self.model(**row)

    async def save(self, kwargs) -> bool:
        f = Cassandra.session.execute_async(self.queries.SAVE, kwargs)
        if not f.result().was_applied:
            raise Exception(self.model.__already_exist__)
        return True

    @staticmethod
    async def save_batch(queries: list[str], models: list[Model]) -> None:
        batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
        for i, model in enumerate(models):
            batch.add(SimpleStatement(queries[i]), model.__dict__)
        Cassandra.session.execute(batch)

    async def update(self, **kwargs) -> bool:
        feature = Cassandra.session.execute_async(
            Cassandra.session.prepare(self.queries.UPDATE), kwargs)
        if feature.result().rowcount == 0:
            raise Exception(self.model.__update_error__)
        return True

    async def delete(self, **kwargs) -> bool:
        future = Cassandra.session.execute_async(
            Cassandra.session.prepare(self.queries.DELETE), kwargs)
        if future.result().rowcount == 0:
            raise Exception(self.model.__delete_error__)
        return True
