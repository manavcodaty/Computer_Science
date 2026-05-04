import math
import random
import sys
import time

import pygame


# Single-file, asset-free "Pokemon Go" style raycaster.
# Controls:
#   W/S or Up/Down    move
#   A/D or Left/Right rotate
#   Q/E               strafe
#   Space             throw a PokeBall down the crosshair
#   Esc               quit

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
HALF_HEIGHT = SCREEN_HEIGHT // 2
FPS = 60

FOV = math.radians(60)
HALF_FOV = FOV / 2
NUM_RAYS = SCREEN_WIDTH
MAX_DEPTH = 24.0

MOVE_SPEED = 3.0
ROT_SPEED = 2.2
PLAYER_RADIUS = 0.18

MINIMAP_SCALE = 8
NOTIFICATION_TIME = 4.0

SKY_COLOR = (88, 157, 214)
FLOOR_COLOR = (59, 69, 55)
CROSSHAIR_COLOR = (245, 245, 245)

WORLD_MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 1, 1, 0, 0, 0, 2, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 2, 0, 1],
    [1, 2, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 2, 0, 1, 1, 1, 0, 2, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 0, 2, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

MAP_HEIGHT = len(WORLD_MAP)
MAP_WIDTH = len(WORLD_MAP[0])

WALL_COLORS = {
    1: (126, 112, 96),
    2: (95, 134, 151),
}


def clamp(value, low, high):
    return max(low, min(high, value))


def shade_color(color, distance, side):
    # Simple depth shading: far walls fade darker, and north/south wall hits
    # are slightly dimmed so corners read as 3D.
    shade = clamp(1.0 - distance / MAX_DEPTH, 0.16, 1.0)
    if side == 1:
        shade *= 0.78
    return (
        int(color[0] * shade),
        int(color[1] * shade),
        int(color[2] * shade),
    )


def is_wall(x, y):
    mx = int(x)
    my = int(y)
    if mx < 0 or my < 0 or mx >= MAP_WIDTH or my >= MAP_HEIGHT:
        return True
    return WORLD_MAP[my][mx] != 0


def empty_tiles():
    tiles = []
    for y, row in enumerate(WORLD_MAP):
        for x, cell in enumerate(row):
            if cell == 0:
                tiles.append((x + 0.5, y + 0.5))
    return tiles


class Player:
    def __init__(self):
        self.x = 2.5
        self.y = 2.5
        self.angle = 0.0
        self.caught = 0

    @property
    def dir_x(self):
        return math.cos(self.angle)

    @property
    def dir_y(self):
        return math.sin(self.angle)

    def try_move(self, dx, dy):
        # Circle-ish collision against grid walls. X and Y are resolved
        # separately so sliding along walls feels natural.
        next_x = self.x + dx
        if not (
            is_wall(next_x + PLAYER_RADIUS, self.y)
            or is_wall(next_x - PLAYER_RADIUS, self.y)
            or is_wall(next_x, self.y + PLAYER_RADIUS)
            or is_wall(next_x, self.y - PLAYER_RADIUS)
        ):
            self.x = next_x

        next_y = self.y + dy
        if not (
            is_wall(self.x + PLAYER_RADIUS, next_y)
            or is_wall(self.x - PLAYER_RADIUS, next_y)
            or is_wall(self.x, next_y + PLAYER_RADIUS)
            or is_wall(self.x, next_y - PLAYER_RADIUS)
        ):
            self.y = next_y

    def update(self, keys, dt):
        move = MOVE_SPEED * dt
        rot = ROT_SPEED * dt

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle -= rot
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle += rot

        forward = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            forward += 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            forward -= 1

        strafe = 0
        if keys[pygame.K_e]:
            strafe += 1
        if keys[pygame.K_q]:
            strafe -= 1

        dx = self.dir_x * forward * move + math.cos(self.angle + math.pi / 2) * strafe * move
        dy = self.dir_y * forward * move + math.sin(self.angle + math.pi / 2) * strafe * move
        self.try_move(dx, dy)
        self.angle %= math.tau


class Entity:
    def __init__(self, name, x, y, body_color, accent_color, shape):
        self.name = name
        self.x = x
        self.y = y
        self.body_color = body_color
        self.accent_color = accent_color
        self.shape = shape
        self.target_x = x
        self.target_y = y
        self.speed = random.uniform(0.32, 0.58)
        self.next_target_time = 0.0
        self.bob_time = random.random() * math.tau

    def choose_target(self, now):
        options = []
        tile_x = int(self.x)
        tile_y = int(self.y)
        for oy in (-1, 0, 1):
            for ox in (-1, 0, 1):
                nx = tile_x + ox
                ny = tile_y + oy
                if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT and WORLD_MAP[ny][nx] == 0:
                    options.append((nx + 0.5, ny + 0.5))
        if options:
            self.target_x, self.target_y = random.choice(options)
        self.next_target_time = now + random.uniform(1.0, 2.8)

    def update(self, dt, now):
        self.bob_time += dt * 4.0
        if now >= self.next_target_time:
            self.choose_target(now)

        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.hypot(dx, dy)
        if dist < 0.05:
            self.next_target_time = now
            return

        step = min(self.speed * dt, dist)
        next_x = self.x + dx / dist * step
        next_y = self.y + dy / dist * step
        if not is_wall(next_x, self.y):
            self.x = next_x
        if not is_wall(self.x, next_y):
            self.y = next_y


class NotificationFeed:
    def __init__(self):
        self.items = []

    def add(self, message):
        self.items.append((message, time.time()))
        self.items = self.items[-5:]

    def draw(self, surface, font):
        now = time.time()
        self.items = [(msg, t) for msg, t in self.items if now - t < NOTIFICATION_TIME]
        y = SCREEN_HEIGHT - 30 - len(self.items) * 22
        for msg, created in self.items:
            age = now - created
            alpha = int(clamp(255 - max(0.0, age - 2.8) * 210, 40, 255))
            text = font.render(msg, True, (255, 255, 255))
            bg = pygame.Surface((text.get_width() + 18, text.get_height() + 8), pygame.SRCALPHA)
            bg.fill((0, 0, 0, min(alpha, 155)))
            bg.blit(text, (9, 4))
            bg.set_alpha(alpha)
            surface.blit(bg, (18, y))
            y += 22


class PokeBall:
    def __init__(self):
        self.active = False
        self.start_time = 0.0
        self.duration = 0.32

    def throw(self):
        self.active = True
        self.start_time = time.time()

    def draw(self, surface):
        if not self.active:
            return
        progress = (time.time() - self.start_time) / self.duration
        if progress >= 1.0:
            self.active = False
            return

        # Screen-space throw animation: the gameplay uses hitscan, while this
        # gives the player immediate visual feedback at the crosshair.
        radius = int(12 + progress * 18)
        y = int(SCREEN_HEIGHT * 0.73 - progress * SCREEN_HEIGHT * 0.22)
        x = SCREEN_WIDTH // 2
        pygame.draw.circle(surface, (235, 236, 238), (x, y), radius)
        pygame.draw.arc(surface, (220, 35, 35), (x - radius, y - radius, radius * 2, radius * 2), math.pi, math.tau, radius)
        pygame.draw.line(surface, (32, 32, 32), (x - radius, y), (x + radius, y), 3)
        pygame.draw.circle(surface, (32, 32, 32), (x, y), max(3, radius // 4))
        pygame.draw.circle(surface, (245, 245, 245), (x, y), max(2, radius // 7))


class RaycasterGame:
    def __init__(self, self_test=False):
        self.self_test = self_test
        self.screen = None
        self.clock = None
        self.font = None
        self.small_font = None
        self.player = Player()
        self.z_buffer = [MAX_DEPTH] * SCREEN_WIDTH
        self.entities = []
        self.notifications = NotificationFeed()
        self.ball = PokeBall()
        self.running = True
        self.empty_spawn_tiles = empty_tiles()
        self.init_pygame()
        self.spawn_entities()

    def init_pygame(self):
        try:
            pygame.init()
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("ShapeMon Go Raycaster")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.SysFont("arial", 20)
            self.small_font = pygame.font.SysFont("arial", 14)
        except pygame.error as exc:
            raise RuntimeError("Pygame failed to initialize: " + str(exc))

    def spawn_entities(self):
        random.shuffle(self.empty_spawn_tiles)
        definitions = [
            ("Charmander", (236, 83, 45), (250, 214, 72), "charmander"),
            ("Squirtle", (69, 143, 220), (209, 232, 244), "squirtle"),
            ("Bulbasaur", (70, 181, 117), (79, 98, 194), "bulbasaur"),
            ("Pikachu", (245, 211, 58), (209, 48, 44), "pikachu"),
            ("Gastly", (132, 83, 178), (218, 214, 235), "gastly"),
        ]

        safe_tiles = [
            pos for pos in self.empty_spawn_tiles
            if math.hypot(pos[0] - self.player.x, pos[1] - self.player.y) > 3.0
        ]
        count = random.randint(3, 5)
        for i in range(count):
            x, y = safe_tiles[i % len(safe_tiles)]
            name, body, accent, shape = definitions[i]
            self.entities.append(Entity(name, x, y, body, accent, shape))
            self.notifications.add("A wild " + name + " appeared!")

    def cast_single_ray(self, ray_angle):
        # DDA grid traversal. The ray advances from one vertical/horizontal
        # grid boundary to the next instead of stepping in tiny increments.
        ray_dir_x = math.cos(ray_angle)
        ray_dir_y = math.sin(ray_angle)
        map_x = int(self.player.x)
        map_y = int(self.player.y)

        delta_dist_x = abs(1.0 / ray_dir_x) if ray_dir_x != 0 else 1e30
        delta_dist_y = abs(1.0 / ray_dir_y) if ray_dir_y != 0 else 1e30

        if ray_dir_x < 0:
            step_x = -1
            side_dist_x = (self.player.x - map_x) * delta_dist_x
        else:
            step_x = 1
            side_dist_x = (map_x + 1.0 - self.player.x) * delta_dist_x

        if ray_dir_y < 0:
            step_y = -1
            side_dist_y = (self.player.y - map_y) * delta_dist_y
        else:
            step_y = 1
            side_dist_y = (map_y + 1.0 - self.player.y) * delta_dist_y

        side = 0
        wall_type = 1
        raw_distance = 0.0
        hit = False

        while not hit and raw_distance < MAX_DEPTH:
            if side_dist_x < side_dist_y:
                raw_distance = side_dist_x
                side_dist_x += delta_dist_x
                map_x += step_x
                side = 0
            else:
                raw_distance = side_dist_y
                side_dist_y += delta_dist_y
                map_y += step_y
                side = 1

            if map_x < 0 or map_y < 0 or map_x >= MAP_WIDTH or map_y >= MAP_HEIGHT:
                hit = True
                wall_type = 1
            elif WORLD_MAP[map_y][map_x] != 0:
                hit = True
                wall_type = WORLD_MAP[map_y][map_x]

        # This explicit cosine correction removes fish-eye distortion by
        # converting the ray length into distance perpendicular to the camera.
        corrected_distance = raw_distance * math.cos(ray_angle - self.player.angle)
        return max(corrected_distance, 0.0001), side, wall_type

    def render_world(self):
        self.screen.fill(SKY_COLOR)
        pygame.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, SCREEN_WIDTH, HALF_HEIGHT))

        for column in range(NUM_RAYS):
            camera_x = column / NUM_RAYS
            ray_angle = self.player.angle - HALF_FOV + camera_x * FOV
            distance, side, wall_type = self.cast_single_ray(ray_angle)
            self.z_buffer[column] = distance

            wall_height = int(SCREEN_HEIGHT / distance)
            draw_start = max(0, HALF_HEIGHT - wall_height // 2)
            draw_end = min(SCREEN_HEIGHT, HALF_HEIGHT + wall_height // 2)

            base_color = WALL_COLORS.get(wall_type, WALL_COLORS[1])
            color = shade_color(base_color, distance, side)
            pygame.draw.line(self.screen, color, (column, draw_start), (column, draw_end))

            # A faint floor gradient sells depth without textures.
            if column % 3 == 0:
                floor_shade = int(clamp(100 - distance * 4, 30, 100))
                pygame.draw.line(
                    self.screen,
                    (floor_shade // 2, floor_shade, floor_shade // 2),
                    (column, draw_end),
                    (column, SCREEN_HEIGHT),
                )

    def make_sprite_surface(self, entity, size):
        size = max(8, int(size))
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        cx = size // 2
        cy = size // 2 + int(math.sin(entity.bob_time) * size * 0.04)
        r = max(3, size // 3)

        if entity.shape == "charmander":
            pygame.draw.rect(surf, entity.body_color, (cx - r, cy - r, r * 2, r * 2), border_radius=max(2, size // 12))
            pygame.draw.circle(surf, entity.accent_color, (cx, cy), max(3, r // 2))
            pygame.draw.polygon(surf, (255, 160, 40), [(cx + r, cy - r), (cx + r + r // 2, cy), (cx + r, cy + r)])
        elif entity.shape == "squirtle":
            pygame.draw.polygon(surf, entity.body_color, [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)])
            pygame.draw.circle(surf, entity.accent_color, (cx, cy), max(3, r // 2))
            pygame.draw.circle(surf, (35, 56, 96), (cx - r // 3, cy - r // 5), max(2, r // 8))
        elif entity.shape == "bulbasaur":
            pygame.draw.circle(surf, entity.body_color, (cx, cy + r // 5), r)
            pygame.draw.polygon(surf, entity.accent_color, [(cx, cy - r), (cx + r, cy), (cx - r, cy)])
            pygame.draw.circle(surf, (32, 88, 59), (cx - r // 3, cy), max(2, r // 8))
        elif entity.shape == "pikachu":
            pygame.draw.circle(surf, entity.body_color, (cx, cy), r)
            pygame.draw.polygon(surf, entity.body_color, [(cx - r // 2, cy - r), (cx - r, cy - r * 2), (cx, cy - r)])
            pygame.draw.polygon(surf, entity.body_color, [(cx + r // 2, cy - r), (cx + r, cy - r * 2), (cx, cy - r)])
            pygame.draw.circle(surf, entity.accent_color, (cx - r // 2, cy + r // 5), max(2, r // 5))
            pygame.draw.circle(surf, entity.accent_color, (cx + r // 2, cy + r // 5), max(2, r // 5))
        else:
            pygame.draw.circle(surf, entity.body_color, (cx, cy), r)
            pygame.draw.circle(surf, entity.accent_color, (cx - r // 3, cy - r // 6), max(2, r // 6))
            pygame.draw.circle(surf, entity.accent_color, (cx + r // 3, cy - r // 6), max(2, r // 6))
            pygame.draw.arc(surf, (35, 25, 45), (cx - r // 2, cy - r // 4, r, r), 0, math.pi, max(1, r // 8))

        return surf

    def render_entities(self):
        plane_len = math.tan(HALF_FOV)
        dir_x = self.player.dir_x
        dir_y = self.player.dir_y
        plane_x = -dir_y * plane_len
        plane_y = dir_x * plane_len
        inv_det = 1.0 / (plane_x * dir_y - dir_x * plane_y)

        sorted_entities = sorted(
            self.entities,
            key=lambda e: (e.x - self.player.x) ** 2 + (e.y - self.player.y) ** 2,
            reverse=True,
        )

        for entity in sorted_entities:
            sprite_x = entity.x - self.player.x
            sprite_y = entity.y - self.player.y

            # Transform world coordinates into camera space. transform_y is
            # forward depth; transform_x is horizontal offset from the view axis.
            transform_x = inv_det * (dir_y * sprite_x - dir_x * sprite_y)
            transform_y = inv_det * (-plane_y * sprite_x + plane_x * sprite_y)

            if transform_y <= 0.05:
                continue

            sprite_screen_x = int((SCREEN_WIDTH / 2) * (1 + transform_x / transform_y))
            sprite_size = abs(int(SCREEN_HEIGHT / transform_y))
            draw_start_y = max(0, HALF_HEIGHT - sprite_size // 2)
            draw_end_y = min(SCREEN_HEIGHT, HALF_HEIGHT + sprite_size // 2)
            draw_start_x = max(0, sprite_screen_x - sprite_size // 2)
            draw_end_x = min(SCREEN_WIDTH, sprite_screen_x + sprite_size // 2)

            if draw_start_x >= draw_end_x or draw_start_y >= draw_end_y:
                continue

            sprite_surface = self.make_sprite_surface(entity, sprite_size)

            # Z-buffered billboarding: draw only the vertical sprite stripes
            # whose projected depth is closer than the wall depth for that
            # exact screen column.
            for stripe in range(draw_start_x, draw_end_x):
                if 0 <= stripe < SCREEN_WIDTH and transform_y < self.z_buffer[stripe]:
                    source_x = int((stripe - (sprite_screen_x - sprite_size // 2)) * sprite_surface.get_width() / sprite_size)
                    if 0 <= source_x < sprite_surface.get_width():
                        source = pygame.Rect(source_x, 0, 1, sprite_surface.get_height())
                        target = pygame.Rect(stripe, draw_start_y, 1, draw_end_y - draw_start_y)
                        self.screen.blit(sprite_surface, target, source)

    def catch_attempt(self):
        best_entity = None
        best_angle = 999.0
        best_dist = 999.0

        for entity in self.entities:
            dx = entity.x - self.player.x
            dy = entity.y - self.player.y
            dist = math.hypot(dx, dy)
            if dist > 8.0:
                continue

            angle_to_entity = math.atan2(dy, dx)
            angle_diff = abs((angle_to_entity - self.player.angle + math.pi) % math.tau - math.pi)
            hit_radius = max(math.radians(2.2), math.atan(0.32 / max(dist, 0.1)))

            center_column = SCREEN_WIDTH // 2
            visible = dist < self.z_buffer[center_column] + 0.25
            if angle_diff < hit_radius and visible and angle_diff < best_angle:
                best_entity = entity
                best_angle = angle_diff
                best_dist = dist

        self.ball.throw()

        if best_entity is None:
            self.notifications.add("The PokeBall missed.")
            return

        chance = clamp(0.78 - best_dist * 0.045, 0.28, 0.82)
        if random.random() < chance:
            self.entities = [e for e in self.entities if e is not best_entity]
            self.player.caught += 1
            self.notifications.add("Caught " + best_entity.name + "!")
        else:
            self.notifications.add(best_entity.name + " broke free!")

    def draw_crosshair(self):
        x = SCREEN_WIDTH // 2
        y = SCREEN_HEIGHT // 2
        pygame.draw.line(self.screen, CROSSHAIR_COLOR, (x - 12, y), (x - 4, y), 2)
        pygame.draw.line(self.screen, CROSSHAIR_COLOR, (x + 4, y), (x + 12, y), 2)
        pygame.draw.line(self.screen, CROSSHAIR_COLOR, (x, y - 12), (x, y - 4), 2)
        pygame.draw.line(self.screen, CROSSHAIR_COLOR, (x, y + 4), (x, y + 12), 2)
        pygame.draw.circle(self.screen, CROSSHAIR_COLOR, (x, y), 3, 1)

    def draw_minimap(self):
        width = MAP_WIDTH * MINIMAP_SCALE
        height = MAP_HEIGHT * MINIMAP_SCALE
        ox = SCREEN_WIDTH - width - 16
        oy = 16
        bg = pygame.Surface((width, height), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 135))
        self.screen.blit(bg, (ox, oy))

        for y, row in enumerate(WORLD_MAP):
            for x, cell in enumerate(row):
                rect = (ox + x * MINIMAP_SCALE, oy + y * MINIMAP_SCALE, MINIMAP_SCALE, MINIMAP_SCALE)
                if cell:
                    pygame.draw.rect(self.screen, (178, 180, 172), rect)
                else:
                    pygame.draw.rect(self.screen, (35, 43, 38), rect)

        px = ox + int(self.player.x * MINIMAP_SCALE)
        py = oy + int(self.player.y * MINIMAP_SCALE)
        left = self.player.angle - HALF_FOV
        right = self.player.angle + HALF_FOV
        p1 = (px, py)
        p2 = (px + int(math.cos(left) * 28), py + int(math.sin(left) * 28))
        p3 = (px + int(math.cos(right) * 28), py + int(math.sin(right) * 28))
        pygame.draw.polygon(self.screen, (255, 255, 255, 55), [p1, p2, p3])
        pygame.draw.circle(self.screen, (255, 255, 255), (px, py), 3)

        for entity in self.entities:
            ex = ox + int(entity.x * MINIMAP_SCALE)
            ey = oy + int(entity.y * MINIMAP_SCALE)
            pygame.draw.circle(self.screen, entity.body_color, (ex, ey), 3)

        pygame.draw.rect(self.screen, (225, 225, 225), (ox, oy, width, height), 1)

    def draw_hud(self):
        caught = self.font.render("Caught: " + str(self.player.caught), True, (255, 255, 255))
        active = self.font.render("Wild: " + str(len(self.entities)), True, (255, 255, 255))
        hint = self.small_font.render("WASD/Arrows move + turn | Q/E strafe | Space throw", True, (230, 230, 230))

        panel = pygame.Surface((210, 76), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 120))
        self.screen.blit(panel, (16, 16))
        self.screen.blit(caught, (28, 25))
        self.screen.blit(active, (28, 50))
        self.screen.blit(hint, (18, SCREEN_HEIGHT - 24))

        self.draw_crosshair()
        self.draw_minimap()
        self.notifications.draw(self.screen, self.font)
        self.ball.draw(self.screen)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.player.update(keys, dt)
        now = time.time()
        for entity in self.entities:
            entity.update(dt, now)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.catch_attempt()

    def draw(self):
        self.render_world()
        self.render_entities()
        self.draw_hud()
        pygame.display.flip()

    def run(self):
        try:
            frame_limit = 12 if self.self_test else None
            frames = 0
            while self.running:
                dt = self.clock.tick(FPS) / 1000.0
                self.handle_events()
                self.update(dt)
                self.draw()
                frames += 1
                if frame_limit is not None and frames >= frame_limit:
                    self.running = False
            return 0
        except Exception as exc:
            print("Runtime error:", exc, file=sys.stderr)
            return 1
        finally:
            pygame.quit()


def main():
    self_test = "--self-test" in sys.argv
    try:
        game = RaycasterGame(self_test=self_test)
        return game.run()
    except Exception as exc:
        print("Startup error:", exc, file=sys.stderr)
        try:
            pygame.quit()
        except Exception:
            pass
        return 1


if __name__ == "__main__":
    sys.exit(main())
