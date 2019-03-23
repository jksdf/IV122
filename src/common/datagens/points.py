import random


def gen_points_normal(n, xy_range):
    points = []
    for _ in range(n):
        points.append((random.uniform(*xy_range), random.uniform(*xy_range)))
    return points


def gen_points_grid(n, start, step, fuzz=0, remove=0.):
    points = []
    for x in range(n):
        for y in range(n):
            if random.random() < remove:
                continue
            points.append((start + x * step + random.uniform(-fuzz, fuzz),
                           start + y * step + random.uniform(-fuzz, fuzz)))
    return points