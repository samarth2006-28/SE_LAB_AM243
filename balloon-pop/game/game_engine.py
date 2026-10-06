"""
GameEngine: owns all balloons, spawns new ones, and handles clicks.

Balloon types: normal (+10), bonus (+30), penalty (-20), each with its
own color, spawned by weighted random choice.

Lives: the player starts with 3. A balloon falling past the bottom costs
one life (except penalty balloons - dodging those is the right play).
Popping never costs a life.

Round: 30 seconds. The round ends when time runs out or lives hit 0,
whichever comes first. Then spawning and clicks stop, the final score is
shown, and reset() starts a fresh round.
"""

import random

import pygame

from game.balloon import Balloon, BALLOON_TYPES
from game.click_detection import check_pop
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 45
STARTING_LIVES = 3
ROUND_SECONDS = 30
# Set True to make missed penalty balloons also cost a life.
PENALTY_MISS_COSTS_LIFE = False


class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        """Start a new round: clears balloons, resets score, lives and timer."""
        self.balloons = []
        self.frames_until_spawn = 0
        self.score = 0
        self.lives = STARTING_LIVES
        self.game_over = False
        self.end_reason = ""
        # Wall-clock timer, so the round is 30 real seconds even if FPS dips.
        self.round_start_ms = pygame.time.get_ticks()
        self.time_left = float(ROUND_SECONDS)

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

    def _end_round(self, reason):
        self.game_over = True
        self.end_reason = reason

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

        elapsed = (pygame.time.get_ticks() - self.round_start_ms) / 1000.0
        self.time_left = max(0.0, ROUND_SECONDS - elapsed)
        if self.time_left <= 0:
            self._end_round("Time's up!")
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
            self._end_round("Out of lives!")

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.balloons)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Lives: {self.lives}", (10, 36))
        timer_text = f"Time: {int(self.time_left + 0.999)}s"  # ceil: 30 -> 1, then 0
        timer_surf = font.render(timer_text, True, renderer.COLOR_TEXT)
        surface.blit(timer_surf, (surface.get_width() - timer_surf.get_width() - 10, 10))
        renderer.draw_legend(surface, font)
        if self.game_over:
            renderer.draw_game_over(surface, font, self.end_reason, self.score)
