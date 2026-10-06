"""
Balloon: falls from the top of the screen. The player must pop it
before it reaches the bottom. Balloons vary in size - this matters for
how click detection should work.
"""

import pygame

# kind -> (points awarded on pop, color, spawn weight)
BALLOON_TYPES = {
    "normal":  {"points": 10,  "color": (220, 90, 120), "weight": 70},
    "bonus":   {"points": 30,  "color": (240, 190, 40), "weight": 15},
    "penalty": {"points": -20, "color": (70, 70, 80),   "weight": 15},
}


class Balloon:
    def __init__(self, x, y, radius, speed, kind="normal"):
        if kind not in BALLOON_TYPES:
            raise ValueError(f"Unknown balloon kind: {kind}")
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.kind = kind
        self.points = BALLOON_TYPES[kind]["points"]
        self.color = BALLOON_TYPES[kind]["color"]

    def update(self):
        self.y += self.speed

    def is_past_bottom(self, height):
        return self.y - self.radius > height

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.radius), int(self.y - self.radius),
            self.radius * 2, self.radius * 2,
        )
