from typing import Union


class HttpBaseException(Exception):
    def __init__(
        self,
        http_status: int,
        code: Union[str, int],
        detail: str,
    ) -> None:
        self.http_status = http_status
        self.code = code
        self.detail = detail


class EntryAlreadyExists(HttpBaseException):
    pass


class VehicleNotFound(HttpBaseException):
    pass


class StopNotFound(HttpBaseException):
    pass
