from perlin_noise import PerlinNoise
from random import randint
from sys import maxsize

_seed = randint(-1 - maxsize, maxsize)
noise = PerlinNoise(3, _seed)

def get_block(x: int, y: int, z: int):
    height = noise.noise(x + z)
    if y >= height:
        return 0
    
    ground_block = Blocks.GRASS[0]
    if height - y > 1:
        if height - y <= 4 + randint(0, 3): # TODO: replace randint(0, 3) to random with seed
            ground_block = Blocks.DIRT[0]
        else:
            ground_block = Blocks.STONE[0]

    return ground_block