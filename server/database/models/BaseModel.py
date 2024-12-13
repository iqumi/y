from dataclasses import dataclass

# database models


@dataclass
class Model:
    __starts_with__ = ""
    __update_error__ = ""
    __delete_error__ = ""
    __already_exist__ = ""
    __unknown__ = ""
