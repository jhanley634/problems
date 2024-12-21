#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/281398/solar-system-simulation

import math
import sys

from pygame.font import SysFont
from pygame.locals import (
    K_DOWN,
    K_ESCAPE,
    K_UP,
    KEYDOWN,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    MOUSEMOTION,
    QUIT,
    RESIZABLE,
    VIDEORESIZE,
)
from pygame.math import Vector2
import pygame

pygame.display.init()
pygame.font.init()

win = pygame.display.set_mode((750, 500), RESIZABLE)
pygame.display.set_caption("Solar System 2.0")
clock = pygame.time.Clock()

WIDTH, HEIGHT = pygame.display.get_surface().get_size()
FONT = SysFont("Tahoma", 16)
LARGE_FONT = SysFont("Tahoma", 26)

AU = 1.496e8 * 1000  # km to m
G = 6.67428e-11
SCALE = 225 / AU
TIME_STEP = 3600 * 24  # 1 day
WIN_CENTER = Vector2(WIDTH // 2, HEIGHT // 2)

BLACK = "#000000"
DARK_GREY = "#5A5A5A"
WHITE = "#FFFFFF"
PEARL_WHITE = "#E2DFD2"
YELLOW = "#FFFF00"
BLUE = "#0000FF"
RED = "#FF0000"
ORANGE = "#FFA500"
BROWN = "#964B00"
YELLOWISH_BROWN = "#9B7A01"
CYAN = "#00FFFF"


def convert_to_win_pos(pos):
    """Converts a position in the real universe to window coordinates."""
    # X increases towards right in pygame window
    # -pos[1] because Y increases downards in pygame window
    return WIN_CENTER + (pos[0] * SCALE, -pos[1] * SCALE)


def convert_to_real_pos(pos):
    """Converts a position on the window to real universe coordinates."""
    real_pos = Vector2(pos) - WIN_CENTER
    real_pos.x /= SCALE
    real_pos.y /= -SCALE  # -SCALE because Y increases downards in pygame window
    return real_pos


class Planet:
    def __init__(self, name, pos, color, mass, radius, orbital_period, y_vel) -> None:
        self.name = name
        self.pos = pos
        self.color = color
        self.mass = mass
        self.radius = radius
        self.x_vel = 0
        self.y_vel = y_vel
        self.orbital_period = orbital_period
        self.orbit_counter = 0
        self.orbit = []

    def render(self, win) -> None:
        """Render the planet and orbit on the window."""
        # Rendering orbit...
        if len(self.orbit) > 2:
            scaled_points = []
            for x, y in self.orbit:
                scaled_points.append(convert_to_win_pos((x, y)))
            pygame.draw.lines(win, self.color, False, scaled_points, 2)

        # Rendering planet...
        pygame.draw.circle(win, self.color, convert_to_win_pos(self.pos), self.radius)

    def render_info(self, win, sun) -> None:
        """Renders information about the planet."""
        # Information text labels...
        distance_from_sun = self.pos.distance_to(sun.pos)
        name_text = FONT.render(f"Name: {self.name}", 1, self.color)
        mass_text = FONT.render(f"Mass: {self.mass}", 1, self.color)
        orbital_period_text = FONT.render(
            f"Orbital period: {self.orbital_period} days", 1, self.color
        )
        distance_text = FONT.render(
            f"Distance from sun: {round(distance_from_sun):,}km", 1, self.color
        )
        vel_text = FONT.render(
            f"Velocity: {round(self.y_vel / 1000, 2):,} km/s", 1, self.color
        )

        # Rendering the labels...
        alignment = (
            max(
                name_text.get_width(),
                mass_text.get_width(),
                orbital_period_text.get_width(),
                distance_text.get_width(),
                vel_text.get_width(),
            )
            + 15
        )
        win.blit(name_text, (WIDTH - alignment, 15))
        win.blit(mass_text, (WIDTH - alignment, 35))
        win.blit(orbital_period_text, (WIDTH - alignment, 55))
        win.blit(distance_text, (WIDTH - alignment, 75))
        win.blit(vel_text, (WIDTH - alignment, 95))

        # Rendering line joining planet and sun
        planet_pos = convert_to_win_pos(self.pos)
        sun_pos = convert_to_win_pos(sun.pos)
        pygame.draw.line(win, self.color, planet_pos, sun_pos, 2)

    def update_position(self, planets) -> None:
        """Updates the position considering gravity of other planets."""
        total_force_x = total_force_y = 0
        for planet in planets:
            if planet == self:
                continue
            force_x, force_y = self.gravity(planet)
            total_force_x += force_x
            total_force_y += force_y

        # F = ma, a = F / m
        self.x_vel += total_force_x / self.mass * TIME_STEP
        self.y_vel += total_force_y / self.mass * TIME_STEP
        self.pos.x += self.x_vel * TIME_STEP
        self.pos.y += self.y_vel * TIME_STEP

        if self.name == "Sun":  # Do not render orbit for sun
            return

        point_dist = self.orbital_period // 25
        self.orbit_counter += 1
        if self.orbit_counter >= point_dist:
            self.orbit_counter = 0
            self.orbit.append([*self.pos])
            if len(self.orbit) > (self.orbital_period / point_dist) + 1:
                del self.orbit[0]

    def gravity(self, other):
        distance_x = other.pos.x - self.pos.x
        distance_y = other.pos.y - self.pos.y
        distance = math.sqrt(distance_x**2 + distance_y**2)
        # F = GMm/d^2
        force = G * self.mass * other.mass / distance**2
        force_angle = math.atan2(distance_y, distance_x)
        force_x = force * math.cos(force_angle)
        force_y = force * math.sin(force_angle)

        return force_x, force_y


sun = Planet("Sun", Vector2(0, 0), YELLOW, 1.9891e30, 20, 0, 0)
mercury = Planet("Merucry", Vector2(5.79e10, 0), DARK_GREY, 3.30e23, 7.5, 88, 47.87e3)
venus = Planet(
    "Venus", Vector2(1.082e11, 0), PEARL_WHITE, 4.87e24, 8.5, 224.7, -35.02e3
)
earth = Planet("Earth", Vector2(1.496e11, 0), BLUE, 5.97e24, 9, 365.2, 29.783e3)
mars = Planet("Mars", Vector2(2.28e11, 0), RED, 6.42e23, 8.75, 687, 24.077e3)
jupiter = Planet("Jupiter", Vector2(7.785e11, 0), BROWN, 1.898e27, 12, 4331, 13.07e3)
saturn = Planet(
    "Saturn", Vector2(1.432e12, 0), YELLOWISH_BROWN, 5.68e26, 10, 10747, 9.69e3
)
uranus = Planet("Uranus", Vector2(2.867e12, 0), CYAN, 8.68e25, 9, 30589, -6.81e3)
neptune = Planet("Neptune", Vector2(4.515e12, 0), BLUE, 1.02e26, 9.75, 59800, 5.43e3)
pluto = Planet("Pluto", Vector2(5.9064e12, 0), BROWN, 1.30e22, 3.5, 90560, 4.7e3)

moon = Planet("Moon", Vector2(1.5e11, 0), WHITE, 7.3e22, 5, 0, 1.022e3)

planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, pluto]
selected_planet = earth

run = True
drag = False
drag_start = None


def render_win_info() -> None:
    """Renders window related info such as x-pos, y-pos, scale, fps and timestep..."""
    x, y = convert_to_real_pos(pygame.mouse.get_pos())
    x_text = FONT.render(f"Position - x: {round(x):,}km", 1, WHITE)
    y_text = FONT.render(f"Position - y: {round(y):,}km", 1, WHITE)
    scale_text = FONT.render(f"Scale: 1-(x, y): {round(1 / SCALE):,}km", 1, WHITE)
    timestep_text = FONT.render(f"Timestep: {TIME_STEP / (3600 * 24)} days", 1, WHITE)
    fps_text = FONT.render(f"FPS: {int(clock.get_fps())}", 1, WHITE)
    win.blit(fps_text, (15, 15))
    win.blit(x_text, (15, 35))
    win.blit(y_text, (15, 55))
    win.blit(scale_text, (15, 75))
    win.blit(timestep_text, (15, 95))


while run:
    clock.tick(60)
    win.fill(BLACK)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                drag = True
                drag_start = pygame.mouse.get_pos()
                for planet in planets:
                    planet_pos = convert_to_win_pos(planet.pos)
                    if (
                        planet_pos.distance_to(pygame.mouse.get_pos())
                        < planet.radius * 2
                    ):
                        selected_planet = planet
                        break
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                drag = False
                drag_start = None
        elif event.type == MOUSEMOTION:
            if drag:
                WIN_CENTER += Vector2(pygame.mouse.get_pos()) - drag_start
                drag_start = pygame.mouse.get_pos()
        elif event.type == VIDEORESIZE:
            WIDTH, HEIGHT = pygame.display.get_surface().get_size()

    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[K_UP]:
        SCALE += 1 / AU  # Zoom in
    if keys_pressed[K_DOWN]:
        SCALE -= 1 / AU  # Zoom out

    for planet in planets:
        planet.update_position(planets)
        planet.render(win)

    selected_planet.render_info(win, sun)
    render_win_info()
    pygame.display.update()
