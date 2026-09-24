"""Generate the simple PWA play-button icons with Python's standard library."""

import math
import struct
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def icon(size):
    rows = []
    for y in range(size):
        row = bytearray([0])
        for x in range(size):
            # Rounded navy square with a soft mint play button.
            corner_x = max(0, abs(x - size / 2) - size * .39)
            corner_y = max(0, abs(y - size / 2) - size * .39)
            inside = math.hypot(corner_x, corner_y) < size * .10
            color = (20, 42, 59, 255) if inside else (0, 0, 0, 0)
            circle = math.hypot(x - size / 2, y - size / 2) < size * .295
            if circle:
                color = (142, 208, 183, 255)
            # Triangle with a blunt enough profile to remain clear at small sizes.
            left = size * .445
            right = size * .645
            half_height = size * .16
            if left <= x <= right and abs(y - size / 2) <= half_height * (right - x) / (right - left):
                color = (20, 42, 59, 255)
            row.extend(color)
        rows.append(bytes(row))
    raw = b''.join(rows)

    def chunk(kind, data):
        return struct.pack('!I', len(data)) + kind + data + struct.pack('!I', zlib.crc32(kind + data) & 0xffffffff)

    return (
        b'\x89PNG\r\n\x1a\n'
        + chunk(b'IHDR', struct.pack('!2I5B', size, size, 8, 6, 0, 0, 0))
        + chunk(b'IDAT', zlib.compress(raw, 9))
        + chunk(b'IEND', b'')
    )


for dimension in (192, 512):
    (ROOT / 'assets' / f'icon-{dimension}.png').write_bytes(icon(dimension))
