from typing import Protocol


class ModelQueries(Protocol):
    GET: str
    FIND: str
    SAVE: str
    UPDATE: str
    DELETE: str


class Model(Protocol):
    __update_error__: str
    __delete_error__: str
    __already_exist__: str
    __unknown__: str
