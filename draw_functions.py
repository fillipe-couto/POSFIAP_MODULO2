# -*- coding: utf-8 -*-
"""
Draw utilities for TSP visualizer.
Uses FigureCanvasAgg.tostring_argb() and converts ARGB -> RGB for Pygame.
"""
import matplotlib
from parametros import COR_AZUL, COR_CINZA, COR_PRETO, COR_VERDE, COR_VERMELHA, ESPESSURA_AVIAO, ESPESSURA_CAMINHAO, ESPESSURA_CARRO_ELETRICO, ESPESSURA_TREM, RAIO
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


def draw_cities(
        screen: pygame.Surface,
        cities_locations: List[Tuple[int, int]],
        labels: Optional[List[str]] = None,
        font_size: int = 18,
        font_color: Tuple[int, int, int] = (0, 0, 0),
        label_offset: Tuple[int, int] = (-5, 7)) -> None:
        """
        Desenha cidades (círculos) e opcionalmente um label para cada cidade.
        - labels: lista de strings com mesmo comprimento que cities_locations.
        - label_offset: deslocamento (x,y) em pixels aplicado à posição do label.
        """
        for city_location in cities_locations:
            pygame.draw.circle(screen, COR_VERMELHA, city_location, RAIO)
            if labels is not None:
                pygame.font.init()
                my_font = pygame.font.SysFont('Arial', font_size, True)
                text_surface = my_font.render(labels[cities_locations.index(city_location)], False, font_color)
                screen.blit(text_surface, (city_location[0] + label_offset[0], city_location[1] + label_offset[1]))


def draw_paths(screen: pygame.Surface, path: Tuple[List[str], float, List[int]], cidades: dict[str, Tuple[int, int]]) -> None:
    """
    Draw a path on a Pygame screen as a closed polyline.
    """
    if not path:
        return
    for i in range(len(path[0])):
        ponto_atual = cidades[path[0][i]]
        ponto_proximo = cidades[path[0][(i + 1) % len(path[0])]]
        match path[2][i]:
            case 1:  # Avião
                pygame.draw.line(screen, COR_VERMELHA, ponto_atual, ponto_proximo, ESPESSURA_AVIAO)
            case 2:  # Trem
                pygame.draw.line(screen, COR_AZUL, ponto_atual, ponto_proximo, ESPESSURA_TREM)
            case 3:  # Carro Elétrico
                pygame.draw.line(screen, COR_VERDE, ponto_atual, ponto_proximo, ESPESSURA_CARRO_ELETRICO)
            case 4:  # Caminhão
                pygame.draw.line(screen, COR_CINZA, ponto_atual, ponto_proximo, ESPESSURA_CAMINHAO)
            case _:  # Desconhecido
                print(f"{path[2][i]}  -> Transporte desconhecido: desenhando linha preta espessura 1")


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
