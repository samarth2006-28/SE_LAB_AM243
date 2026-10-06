"""
GameEngine: owns all balloons, spawns new ones, and handles clicks.

Balloon types: normal (+10), bonus (+30), penalty (-20), each with its
own color, spawned by weighted random choice.

Lives: the player starts with 3. A balloon falling past the bottom costs
one life (except penalty balloons - dodging those is the right play).
Popping never costs a life. At 0 lives the game is over.
"""

import random

from game.balloon import Balloon, BALLOON_TYPES
from game.click_detection import check_pop
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 45
STARTING_LIVES = 3
# Set True to make missed penalty balloons also cost a life.
PENALTY_MISS_COSTS_LIFE = False


class GameEngine:
    def __init__(self):
        self.balloons = []
        self.frames_until_spawn = 0
        self.score = 0
        self.lives = STARTING_LIVES
        self.game_over = False

    def _spawn_balloon(self):
        radius = random.randint(16, 44)
        x = random.randint(radius + 10, WIDTH - radius - 10)
        speed = random.uniform(1.5, 3.0)
        kinds = list(BALLOON_TYPES)
        weights = [BALLOON_TYPES[k]["weight"] for k in kinds]
        kind = random.choices(kinds, weights=weights, k=1)[0]
        self.balloons.append(
            Balloon(x=x, y=-radius, radius=radius, speed=speed, kind=kind)
        )

    def handle_click(self, pos):
        if self.game_over:
            return
        popped = check_pop(self.balloons, pos)
        if popped is not None:
            self.balloons.remove(popped)
            self.score += popped.points

    def update(self):
        if self.game_over:
            return

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_balloon()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for b in self.balloons:
            b.update()

        remaining = []
        for b in self.balloons:
            if not b.is_past_bottom(HEIGHT):
                remaining.append(b)
            elif b.kind != "penalty" or PENALTY_MISS_COSTS_LIFE:
                self.lives -= 1
        self.balloons = remaining

        if self.lives <= 0:
            self.lives = 0
            self.game_over = True

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.balloons)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Lives: {self.lives}", (10, 36))
        renderer.draw_legend(surface, font)
        if self.game_over:
            renderer.draw_banner(surface, font, f"GAME OVER - Final score: {self.score}")
