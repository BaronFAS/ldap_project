from enum import Enum


class SizeUnit(Enum):
    BYTES = "bytes"
    KB = "kb"
    MB = "mb"
    GB = "gb"


def get_file_size(
    file_in_memory: bytes,
    unit=SizeUnit.BYTES.value,
) -> float:
    units_map = {
        SizeUnit.BYTES.value: 0,
        SizeUnit.KB.value: 1,
        SizeUnit.MB.value: 2,
        SizeUnit.GB.value: 3,
    }

    if unit not in units_map:
        raise ValueError("Must select from [%s]", ", ".join([item.value for item in SizeUnit]))

    size = len(file_in_memory) / 1024 ** units_map[unit]
    return round(size, 2)
