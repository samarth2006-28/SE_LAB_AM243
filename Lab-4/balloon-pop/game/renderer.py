"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

from game.balloon import BALLOON_TYPES

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (200, 230, 245)
COLOR_TEXT = (30, 30, 30)


def draw_scene(surface, balloons):
    surface.fill(COLOR_BG)
    for b in balloons:
        pygame.draw.circle(surface, b.color, (int(b.x), int(b.y)), b.radius)
        pygame.draw.line(surface, (120, 120, 120), (b.x, b.y + b.radius), (b.x, b.y + b.radius + 12), 2)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text):
    surf = font.render(text, True, (180, 40, 40))
    rect = surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
    surface.blit(surf, rect)


def draw_legend(surface, font):
    """Small key at the bottom-left: colored dot + points per balloon type."""
    x, y = 10, surface.get_height() - 30
    for kind, info in BALLOON_TYPES.items():
        pygame.draw.circle(surface, info["color"], (x + 8, y + 11), 8)
        label = f"{kind} {info['points']:+d}"
        surf = font.render(label, True, COLOR_TEXT)
        surface.blit(surf, (x + 22, y))
        x += 22 + surf.get_width() + 20


def draw_game_over(surface, font, reason, score):
    """Dim the playfield and show why the round ended, the score, and how to restart."""
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    surface.blit(overlay, (0, 0))
    cx, cy = surface.get_width() // 2, surface.get_height() // 2
    big = pygame.font.SysFont("consolas", 40, bold=True)
    lines = [
        (big, reason, (255, 255, 255)),
        (big, f"Final score: {score}", (255, 215, 80)),
        (font, "Press R to play again", (230, 230, 230)),
    ]
    y = cy - 70
    for f, text, color in lines:
        surf = f.render(text, True, color)
        surface.blit(surf, surf.get_rect(center=(cx, y)))
        y += 55
