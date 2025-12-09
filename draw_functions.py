# -*- coding: utf-8 -*-
"""
Draw utilities for TSP visualizer.
Uses FigureCanvasAgg.tostring_argb() and converts ARGB -> RGB for Pygame.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import pygame
from typing import List, Tuple, Optional
import numpy as np


def draw_plot(screen: pygame.Surface, x: list, y: list, x_label: str = 'Generation', y_label: str = 'Fitness') -> None:
    """
    Draw a matplotlib plot into a pygame surface and blit it to `screen` at (0,0).
    Uses FigureCanvasAgg.tostring_argb(), converts ARGB -> RGB (3 bytes/pixel) and creates
    a pygame surface with format "RGB".
    """
    fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
    ax.plot(x, y)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    plt.tight_layout()

    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    # Use tostring_argb() (available on FigureCanvasAgg) and convert to RGB bytes
    raw_argb = canvas.tostring_argb()
    w, h = canvas.get_width_height()

    # Convert ARGB (A,R,G,B bytes) -> RGB (R,G,B)
    # raw_argb is bytes length w*h*4
    arr = np.frombuffer(raw_argb, dtype=np.uint8)
    try:
        arr = arr.reshape((h, w, 4))
    except ValueError:
        # fallback: try (w,h,4) reshape if needed
        arr = arr.reshape((w, h, 4)).swapaxes(0, 1)

    rgb_arr = arr[:, :, 1:4]  # drop alpha channel (keep R,G,B)
    rgb_bytes = rgb_arr.tobytes()

    try:
        surf = pygame.image.fromstring(rgb_bytes, (w, h), "RGB")
        # Matplotlib's image origin is top-left; pygame expects top-left as well,
        # but sometimes the image appears flipped — flip vertically if needed.
        # surf = pygame.transform.flip(surf, False, True)
        screen.blit(surf, (0, 0))
    finally:
        plt.close(fig)


def draw_cities(screen: pygame.Surface, cities_locations: List[Tuple[int, int]], rgb_color: Tuple[int, int, int], node_radius: int) -> None:
    """
    Draws circles representing cities on the given Pygame screen.
    """
    for city_location in cities_locations:
        pygame.draw.circle(screen, rgb_color, city_location, node_radius)


def draw_paths(screen: pygame.Surface, path: List[Tuple[int, int]], rgb_color: Tuple[int, int, int], width: int = 1) -> None:
    """
    Draw a path on a Pygame screen as a closed polyline.
    """
    if not path:
        return
    pygame.draw.lines(screen, rgb_color, True, path, width=width)


def draw_text(screen: pygame.Surface, text: str, color: Tuple[int, int, int], position: Optional[Tuple[int, int]] = None, font_size: int = 15) -> None:
    """
    Draw text on a Pygame screen.

    Parameters:
    - screen: pygame.Surface
    - text: string to render
    - color: (R,G,B) tuple
    - position: (x,y) tuple for blit position. If None, uses (10,10).
    - font_size: font size in px
    """
    pygame.font.init()
    my_font = pygame.font.SysFont('Arial', font_size)
    text_surface = my_font.render(text, False, color)
    if position is None:
        position = (10, 10)
    screen.blit(text_surface, position)
