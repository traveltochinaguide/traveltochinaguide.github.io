#!/usr/bin/env python3
"""Generate placeholder hero images for new city pages."""
import struct, zlib, os, base64

OUT = '/home/ubuntu/traveltochinaguide.github.io/images'

def create_png(width, height, r, g, b, filename):
    """Create a solid-color PNG using pure Python (struct + zlib)."""
    def png_chunk(chunk_type, data):
        c = chunk_type + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

    # Raw pixel data: filter byte (0=None) + RGB triplets
    raw = b''
    for y in range(height):
        raw += b'\x00' + bytes([r, g, b] * width)

    compressed = zlib.compress(raw, 6)

    with open(filename, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        f.write(png_chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)))
        f.write(png_chunk(b'IDAT', compressed))
        f.write(png_chunk(b'IEND', b''))

# City colors (RGB) - each city gets a distinct color
cities = [
    ('chongqing', 220, 80, 30),   # fiery red-orange (火锅之都)
    ('guangzhou', 200, 40, 60),   # canton red
    ('shenzhen',  30,  100, 180), # blue (经济特区)
    ('kunming',   40,  160, 80),  # green (春城)
    ('dali',      80,  140, 190), # sky blue (苍山洱海)
    ('lijiang',  210,  160, 50),  # golden (纳西文化)
]

w, h = 1600, 900
for city, r, g, b in cities:
    path = f'{OUT}/hero-{city}.webp'
    # Create PNG first, then we'll convert
    png_path = f'{OUT}/hero-{city}.png'
    create_png(w, h, r, g, b, png_path)
    print(f'Created {png_path}')

print('Done creating PNG placeholders')