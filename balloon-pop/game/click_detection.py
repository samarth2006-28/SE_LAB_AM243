"""
click_detection: figures out whether a click landed on a balloon.
"""


def check_pop(balloons, click_pos):
    """
    Returns the balloon that was clicked, or None if the click missed
    every balloon.

    A click hits a balloon when its distance from the balloon's center
    is at most the balloon's radius. Both sides are squared so we can
    skip the sqrt: dist <= r  <=>  dist^2 <= r^2 (both non-negative).

    Balloons are iterated newest-first because newer balloons are drawn
    on top; if two overlap, the one the player can see gets popped.
    """
    for balloon in reversed(balloons):
        dx = click_pos[0] - balloon.x
        dy = click_pos[1] - balloon.y
        distance_squared = dx * dx + dy * dy
        if distance_squared <= balloon.radius * balloon.radius:
            return balloon
    return None
